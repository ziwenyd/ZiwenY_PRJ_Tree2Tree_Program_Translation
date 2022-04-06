"""
Extended and Commented by Ziwen Yuan.
original authors: Xinyun Chen and Chang Liu and Dawn Song
paper: Tree-to-tree Neural Networks for Program Translation
url: http://arxiv.org/abs/1802.03691
"""
import csv
import math
import os
import random
import sys
import time
import logging
import argparse

import numpy as np
from six.moves import xrange
import json

import torch
import torch.nn as nn
import torch.optim as optim
from torch import cuda
from torch.autograd import Variable
from torch.nn.utils import clip_grad_norm

import data_utils
import network
import pickle


def create_model(source_vocab_size, target_vocab_size, source_vocab_list, target_vocab_list, dropout_rate, max_source_len, max_target_len):
    if args.network == 'seq2seq':
        model = network.Seq2SeqModel(
            source_vocab_size,
            target_vocab_size,
            source_vocab_list,
            target_vocab_list,
            max_source_len,
            max_target_len,
            args.max_depth,
            args.embedding_size,
            args.hidden_size,
            args.num_layers,
            args.max_gradient_norm,
            args.batch_size,
            args.learning_rate,
            dropout_rate)
    elif args.network == 'seq2tree':
        model = network.Seq2TreeModel(
            source_vocab_size,
            target_vocab_size,
            source_vocab_list,
            target_vocab_list,
            max_source_len,
            max_target_len,
            args.max_depth,
            args.embedding_size,
            args.hidden_size,
            args.num_layers,
            args.max_gradient_norm,
            args.batch_size,
            args.learning_rate,
            dropout_rate)
    elif args.network == 'tree2seq':
        model = network.Tree2SeqModel(
            source_vocab_size,
            target_vocab_size,
            source_vocab_list,
            target_vocab_list,
            max_target_len,
            args.max_depth,
            args.embedding_size,
            args.hidden_size,
            args.num_layers,
            args.max_gradient_norm,
            args.batch_size,
            args.learning_rate,
            dropout_rate)
    else:
        model = network.Tree2TreeModel(
            source_vocab_size,
            target_vocab_size,
            source_vocab_list,
            target_vocab_list,
            args.max_depth,
            args.embedding_size,
            args.hidden_size,
            args.num_layers,
            args.max_gradient_norm,
            args.batch_size,
            args.learning_rate,
            dropout_rate,
            args.no_pf,
            args.no_attention)

    if cuda.is_available():
        model.cuda()

    if args.load_model:
        print("Reading model parameters from %s" % args.load_model)
        pretrained_model = torch.load(args.load_model)
        model.load_state_dict(pretrained_model)
    else:
        print("Created model with fresh parameters.")
        model.init_weights(args.param_init)
    return model


def step_seq2seq(model, encoder_inputs, decoder_inputs, source_serialize=True, feed_previous=False):
    if feed_previous == False:
        model.dropout_rate = args.dropout_rate
    else:
        model.dropout_rate = 0.0

    if source_serialize:
        encoder_inputs = Variable(torch.LongTensor(encoder_inputs))
        if cuda.is_available():
            encoder_inputs = encoder_inputs.cuda()

    decoder_inputs = Variable(torch.LongTensor(decoder_inputs))
    if cuda.is_available():
        decoder_inputs = decoder_inputs.cuda()

    predictions = model(encoder_inputs, decoder_inputs,
                        feed_previous=feed_previous)

    if feed_previous:
        output_predictions = []

    total_loss = None
    for time_step in xrange(model.max_target_len - 1):
        prediction = predictions[time_step]
        if feed_previous:
            output_prediction = prediction.max(1)[1]
            output_prediction = output_prediction.squeeze()
            output_predictions.append(output_prediction.data)

        target = decoder_inputs[:, time_step + 1]
        loss = model.loss_function(prediction, target)
        if total_loss is None:
            total_loss = loss
        else:
            total_loss += loss
    total_loss /= len(encoder_inputs)
    if feed_previous == False:
        model.optimizer.zero_grad()
        total_loss.backward()
        if args.max_gradient_norm > 0:
            clip_grad_norm(model.parameters(), args.max_gradient_norm)
        model.optimizer.step()

    if feed_previous:
        return total_loss.data[0], output_predictions
    else:
        return total_loss.data[0]


def step_seq2tree(model, encoder_inputs, init_decoder_inputs, feed_previous=False):
    if feed_previous == False:
        model.dropout_rate = args.dropout_rate
    else:
        model.dropout_rate = 0.0
    encoder_inputs = Variable(torch.LongTensor(encoder_inputs))
    if cuda.is_available():
        encoder_inputs = encoder_inputs.cuda()
    for idx in xrange(len(init_decoder_inputs)):
        init_decoder_inputs[idx] = model.convert_node_to_tensor(
            init_decoder_inputs[idx])
    predictions_per_batch, prediction_nodes, raw_predictions = model(
        encoder_inputs, init_decoder_inputs, feed_previous=feed_previous)

    total_loss = None
    for (predictions, decoder_inputs) in predictions_per_batch:
        for time_step in xrange(model.max_target_len - 1):
            prediction = predictions[time_step]
            target = decoder_inputs[:, time_step + 1]
            loss = model.loss_function(prediction, target)
            if total_loss is None:
                total_loss = loss
            else:
                total_loss += loss
    total_loss /= len(encoder_inputs)

    if feed_previous:
        output_predictions = []

        for node_idx in raw_predictions:
            output_predictions.append(
                model.tree2seq(prediction_nodes, node_idx))

    if feed_previous == False:
        model.optimizer.zero_grad()
        total_loss.backward()
        if args.max_gradient_norm > 0:
            clip_grad_norm(model.parameters(), args.max_gradient_norm)
        model.optimizer.step()

    if feed_previous:
        return total_loss.data[0], output_predictions
    else:
        return total_loss.data[0]


def step_tree2tree(model, encoder_inputs, init_decoder_inputs, feed_previous=False):
    if feed_previous == False:
        model.dropout_rate = args.dropout_rate
    else:
        model.dropout_rate = 0.0

    predictions_per_batch, prediction_managers = model(
        encoder_inputs, init_decoder_inputs, feed_previous=feed_previous)
    # print('prediction managers[0]', prediction_managers[0].num_trees)

    total_loss = None
    for (predictions, target) in predictions_per_batch:
        loss = model.loss_function(predictions, target)
        if total_loss is None:
            total_loss = loss
        else:
            total_loss += loss

    total_loss /= len(encoder_inputs)

    if feed_previous:
        output_predictions = []
        # print('prediction managers', prediction_managers)
        for prediction_manager in prediction_managers:
            output_predictions.append(model.tree2seq(prediction_manager, 1))

    if feed_previous == False:
        model.optimizer.zero_grad()
        total_loss.backward()
        if args.max_gradient_norm > 0:
            clip_grad_norm(model.parameters(), args.max_gradient_norm)
        model.optimizer.step()

    for idx in range(len(encoder_inputs)):
        encoder_inputs[idx].clear_states()

    if feed_previous:
        # print('step output predictions', output_predictions)
        return total_loss.item(), output_predictions
    else:
        return total_loss.item()


def evaluate(model, test_set, source_vocab, target_vocab, source_vocab_list, target_vocab_list):

    test_loss = 0
    acc_tokens = 0
    tot_tokens = 0
    tot_output_tokens = 0
    acc_programs = 0
    tot_programs = len(test_set)
    res = []
    average_EDR = 0

    for idx in xrange(0, len(test_set), args.batch_size):
        # here so-called "decoder_inputs" is not actually the input of the decoder
        # it is the ground truth TreeManagers.
        # The data it represents will be called 'target_tree' in the model.forward()
        # and in the model.forward(),
        # decoder_input is the prediction_tree.root, which is t_t, the prediction result - a token id
        encoder_inputs, decoder_inputs = model.get_batch(
            test_set, start_idx=idx)
        # print('decoder_inputs[0]', decoder_inputs[0].num_trees)
        if args.network == 'seq2seq' or args.network == 'tree2seq':
            if args.network == 'seq2seq':
                source_serialize = True
            else:
                source_serialize = False
            eval_loss, raw_outputs = step_seq2seq(
                model, encoder_inputs, decoder_inputs, source_serialize=source_serialize, feed_previous=True)
        elif args.network == 'seq2tree':
            eval_loss, raw_outputs = step_seq2tree(
                model, encoder_inputs, decoder_inputs, feed_previous=True)
        else:
            eval_loss, raw_outputs = step_tree2tree(
                model, encoder_inputs, decoder_inputs, feed_previous=True)
        test_loss += len(encoder_inputs) * eval_loss
        for i in xrange(len(encoder_inputs)):
            if idx + i >= len(test_set):
                break
            current_output = []
            if args.network == 'seq2seq' or args.network == 'tree2seq':
                for j in xrange(model.max_target_len - 1):
                    current_output.append(raw_outputs[j][i])
                    if raw_outputs[j][i] == data_utils.EOS_ID:
                        break
            else:
                for j in xrange(len(raw_outputs[i])):
                    current_output.append(raw_outputs[i][j])
            if args.network == 'tree2tree' or args.network == 'tree2seq':
                current_source, current_target, current_source_manager, current_target_manager = test_set[
                    idx + i]
            else:
                current_source, current_target = test_set[idx + i]
            if args.network != 'seq2seq' and args.network != 'tree2seq':
                current_target = data_utils.serialize_tree(current_target)
            if args.network == 'tree2tree':
                current_source = data_utils.serialize_tree(current_source)
            res.append((current_source, current_target, current_output))

            tot_tokens += len(current_target)
            tot_output_tokens += len(current_output)
            all_correct = 1
            wrong_tokens = 0
            # Save Translation Result
            save_translation_result(
                idx, current_output, source_vocab, target_vocab, source_vocab_list, target_vocab_list)

            if len(current_output) == 0:
                all_correct = 0
            # Calculate: Token Accuracy & Program Accuracy
            for j in xrange(len(current_output)):
                if j >= len(current_target):
                    break
                # print('c token', current_output[j],
                #       '- t token', current_target[j])
                if current_output[j] == current_target[j]:
                    acc_tokens += 1
                else:
                    # print('not all correct')
                    all_correct = 0
                    wrong_tokens += 1
            acc_programs += all_correct
            # Calculate: Edit Distance Rate
            EDR = edit_distance(current_output, current_target)
            average_EDR += EDR

    test_loss /= tot_programs
    average_EDR /= tot_output_tokens
    print("  eval: loss %.2f" % test_loss)
    print("  eval: total number of programs: " + str(tot_programs))
    print("  eval: total number of matched(correct) token: " + str(acc_tokens))
    print("  eval: total number of output(translated) token: " +
          str(tot_output_tokens))
    print("  eval: total number of target(ground truth) token: " + str(tot_tokens))
    print("  eval: accuracy of tokens %.2f" % (acc_tokens * 1.0 / tot_tokens))
    print("  eval: accuracy of programs %.2f" %
          (acc_programs * 1.0 / tot_programs))
    print("  eval: average EDR of programs %.2f" %
          average_EDR)


def edit_distance(output, target):
    output_len = len(output)
    target_len = len(target)
    OPT = [[0 for i in range(target_len+1)]
           for j in range(output_len + 1)]  # DP table

    # OPT[i][0] = i, assign values to first column
    for i in range(1, output_len+1):
        OPT[i][0] = i
    # OPT[0][j] = j, assign values to first row
    for j in range(1, target_len+1):
        OPT[0][j] = j
    single_insert_cost = 1
    single_delete_cost = 1
    single_align_cost = 1
    for i in range(1, output_len+1):  # row
        for j in range(1, target_len+1):  # column
            delta = single_align_cost if output[i-1] != target[j-1] else 0
            alignment_cost = OPT[i-1][j-1] + delta
            delete_cost = OPT[i-1][j] + single_delete_cost
            insertion_cost = OPT[i][j-1] + single_insert_cost
            OPT[i][j] = min(alignment_cost, delete_cost, insertion_cost)
    return OPT[output_len][target_len]


def save_translation_result(count, current_output_token_id_list, source_vocab, target_vocab, source_vocab_list, target_vocab_list):
    if not os.path.isdir(args.result_dir):
        os.makedirs(args.result_dir)
    output_str = ""
    target_vocab_id_to_token = {value: key for (
        key, value) in target_vocab.items()}

    for token_id in current_output_token_id_list:
        if token_id in target_vocab_id_to_token:
            output_token = target_vocab_id_to_token[token_id]
            if isinstance(output_token, bytes):
                output_token = output_token.decode('utf-8')
            output_str = output_str + output_token
        else:
            output_str = output_str + "OOV "
    if 'eval_loss' in args.load_model:
        f_dir = args.result_dir + 'best_eval_loss/'
    elif 'loss' in args.load_model:
        f_dir = args.result_dir + 'best_loss/'
    if not os.path.isdir(f_dir):
        os.makedirs(f_dir)
    f_name = os.path.join(f_dir + args.target_lang +
                          '_atom_test_'+str(count+1)+'.txt')
    f = open(f_name, 'w')
    f.write(output_str)
    f.close()
    print('File wrote:', f_name)


def get_tree_depth(one_TreeManager):
    current_tree = None
    depth = 0
    for i in range(one_TreeManager.num_trees):
        current_tree = one_TreeManager.trees[i]
        current_tree_depth = current_tree.depth
        if current_tree_depth >= depth:
            depth = current_tree_depth
    return depth


def calculate_tree_depth_statistics(data_set):
    """
    data_set: a list of 
    (source JSON in token id, 
     target JSON in token id, 
     source TreeManager in token id, 
     target TreeManager in token id)
    """
    source_TreeMangers = []
    target_TreeMangers = []
    for _, _, sourceTreeManager, targetTreeManager in data_set:
        source_TreeMangers.append(sourceTreeManager)
        target_TreeMangers.append(targetTreeManager)
    print(source_TreeMangers)
    source_tree_depth = []
    target_tree_depth = []
    for i in range(len(source_TreeMangers)):
        sourceTreeManager = source_TreeMangers[i]
        targetTreeManager = target_TreeMangers[i]
        source_depth = get_tree_depth(sourceTreeManager)
        target_depth = get_tree_depth(targetTreeManager)
        source_tree_depth.append(source_depth)
        target_tree_depth.append(target_depth)
    source_average_depth = sum(source_tree_depth) / len(source_tree_depth)
    target_average_depth = sum(target_tree_depth) / len(target_tree_depth)
    print('Source Tree average depth ', source_average_depth)
    print('Target Tree average depth ', target_average_depth)
    print('Source Tree min depth ', min(source_tree_depth))
    print('Source Tree max depth ', max(source_tree_depth))
    print('Target Tree min depth ', min(target_tree_depth))
    print('Target Tree max depth ', max(target_tree_depth))


def train(train_data, val_data, source_vocab, target_vocab,
          source_vocab_list, target_vocab_list, source_serialize, target_serialize):
    print("Reading training and val data :")
    train_set = data_utils.prepare_data(train_data, source_vocab, target_vocab,
                                        args.input_format, args.output_format, source_serialize, target_serialize)
    val_set = data_utils.prepare_data(val_data, source_vocab, target_vocab,
                                      args.input_format, args.output_format, source_serialize, target_serialize)

    calculate_tree_depth_statistics(train_set)
    if not os.path.isdir(args.train_dir):
        os.makedirs(args.train_dir)
    print("Creating %d layers of %d units." %
          (args.num_layers, args.hidden_size))
    model = create_model(len(source_vocab), len(target_vocab), source_vocab_list,
                         target_vocab_list, args.dropout_rate, args.max_source_len, args.max_target_len)

    step_time, loss = 0.0, 0.0
    current_step = 0
    previous_losses = []

    train_data_size = len(train_set)

    # Record training process data
    best_eval_loss_model = None
    best_eval_loss_ckpt_path = ""
    best_eval_loss = float("inf")
    best_loss_model = None
    best_loss_ckpt_path = ""
    best_loss = float("inf")
    f = open('train_process_data.csv', 'w', encoding='UTF8')
    # create the csv writer
    header = ['step(checkpoint)', 'step_time',
              'loss', 'is_best_loss', 'eval_loss', 'is_best_eval_loss']
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    for epoch in range(args.num_epochs):
        random.shuffle(train_set)
        for batch_idx in range(0, train_data_size, args.batch_size):
            start_time = time.time()
            encoder_inputs, decoder_inputs = model.get_batch(
                train_set, start_idx=batch_idx)

            if args.network == 'seq2seq' or args.network == 'tree2seq':
                step_loss = step_seq2seq(
                    model, encoder_inputs, decoder_inputs, source_serialize=source_serialize, feed_previous=False)
            elif args.network == 'seq2tree':
                step_loss = step_seq2tree(
                    model, encoder_inputs, decoder_inputs, feed_previous=False)
            else:
                step_loss = step_tree2tree(
                    model, encoder_inputs, decoder_inputs, feed_previous=False)

            step_time += (time.time() - start_time) / args.steps_per_checkpoint
            loss += step_loss / args.steps_per_checkpoint
            current_step += 1

            print("step " + str(current_step) + " ", end="")
            if current_step % args.learning_rate_decay_steps == 0 and model.learning_rate > 0.0001:
                model.decay_learning_rate(args.learning_rate_decay_factor)

            if current_step % args.steps_per_checkpoint == 0:
                previous_losses.append(loss)
                # Save the Model with Best loss score
                csv_row = [current_step, step_time, loss]
                csv_row.append('')
                if loss <= best_loss:
                    best_loss = loss
                    best_loss_ckpt_path = os.path.join(
                        args.train_dir, "best_loss_" + "translate_" + str(current_step) + ".ckpt")
                    csv_row[-1] = 'T'
                    best_loss_model = model.state_dict()
                step_time, loss = 0.0, 0.0

                encoder_inputs, decoder_inputs = model.get_batch(
                    val_set, start_idx=0)
                if args.network == 'seq2seq' or args.network == 'tree2seq':
                    eval_loss, decoder_outputs = step_seq2seq(
                        model, encoder_inputs, decoder_inputs, source_serialize=source_serialize, feed_previous=True)
                elif args.network == 'seq2tree':
                    eval_loss, decoder_outputs = step_seq2tree(
                        model, encoder_inputs, decoder_inputs, feed_previous=True)
                else:
                    eval_loss, decoder_outputs = step_tree2tree(
                        model, encoder_inputs, decoder_inputs, feed_previous=True)

                print("learning rate %.4f step-time %.2f loss "
                      "%.2f" % (model.learning_rate, step_time, loss), end="")
                print("  eval: loss %.2f" % eval_loss)
                csv_row.append(eval_loss)
                csv_row.append('')
                # Save the Model with best evaluate loss Score.
                if eval_loss <= best_eval_loss:
                    best_eval_loss = eval_loss
                    best_eval_loss_ckpt_path = os.path.join(
                        args.train_dir, "best_eval_loss_" + "translate_" + str(current_step) + ".ckpt")
                    csv_row[-1] = 'T'
                    best_eval_loss_model = model.state_dict()
                csv_writer.writerow(csv_row)
                sys.stdout.flush()

    print('best eval path', best_eval_loss_ckpt_path)
    print('best loss path', best_loss_ckpt_path)
    torch.save(best_eval_loss_model, best_eval_loss_ckpt_path)
    print("Best Model saved with eval_loss = " +
          str(best_eval_loss), best_eval_loss_ckpt_path)
    torch.save(best_loss_model, best_loss_ckpt_path)
    print("Best Model saved with loss = " +
          str(best_loss), best_loss_ckpt_path)


def test(train_data, test_data, source_vocab, target_vocab, source_vocab_list, target_vocab_list, source_serialize, target_serialize):
    model = create_model(len(source_vocab), len(target_vocab), source_vocab_list,
                         target_vocab_list, 0.0, args.max_source_len, args.max_target_len)
    test_set = data_utils.prepare_data(test_data, source_vocab, target_vocab,
                                       args.input_format, args.output_format, source_serialize, target_serialize)
    # train_set is only built here to calculate the statistics.
    # it is not used anywhere else while testing a trained Tree2Tree model.
    train_set = data_utils.prepare_data(train_data, source_vocab, target_vocab,
                                        args.input_format, args.output_format, source_serialize, target_serialize)
    print('train data statistics:')
    calculate_tree_depth_statistics(train_set)
    print('test data statistics:')
    calculate_tree_depth_statistics(test_data)
    evaluate(model, test_set, source_vocab, target_vocab,
             source_vocab_list, target_vocab_list)


parser = argparse.ArgumentParser()
parser.add_argument('--network', type=str, default='tree2tree',
                    choices=['seq2seq', 'seq2tree', 'tree2seq', 'tree2tree'])
parser.add_argument('--param_init', type=float, default=0.1,
                    help='Parameters are initialized over uniform distribution in (-param_init, param_init)')
parser.add_argument('--num_epochs', type=int, default=1,
                    help='number of training epochs')
parser.add_argument('--learning_rate', type=float, default=0.005,
                    help='learning rate')
parser.add_argument('--learning_rate_decay_factor', type=float, default=0.8,
                    help='learning rate decays by this much')
parser.add_argument('--learning_rate_decay_steps', type=int, default=2000,
                    help='decay the learning rate after certain steps')
parser.add_argument('--max_gradient_norm', type=float, default=5.0,
                    help='clip gradients to this norm')
parser.add_argument('--batch_size', type=int, default=1,
                    help='batch size')
parser.add_argument('--max_depth', type=int, default=100,
                    help='max depth for tree models')
parser.add_argument('--hidden_size', type=int, default=256,
                    help='size of each model layer')
parser.add_argument('--embedding_size', type=int, default=256,
                    help='size of the embedding')
parser.add_argument('--dropout_rate', type=float, default=0.5,
                    help='dropout rate')
parser.add_argument('--num_layers', type=int, default=1,
                    help='number of layers in the model')
parser.add_argument('--source_vocab_size', type=int, default=0,
                    help='source vocabulary size (0: no limit)')
parser.add_argument('--target_vocab_size', type=int, default=0,
                    help='target vocabulary size (0: no limit)')
parser.add_argument('--train_dir', type=str, default='../model_ckpts/tree2tree/',
                    help='training directory')
parser.add_argument('--load_model', type=str, default=None,
                    help='path to the pretrained model')
parser.add_argument('--vocab_filename', type=str, default=None,
                    help='filename for the vocabularies')
parser.add_argument('--steps_per_checkpoint', type=int, default=1,
                    help='number of training steps per checkpoint')
parser.add_argument('--max_source_len', type=int, default=115,
                    help='max length for input')
parser.add_argument('--max_target_len', type=int, default=315,
                    help='max length for output')
parser.add_argument('--test', action='store_true',
                    help='set to true for testing')
parser.add_argument('--input_format', type=str,
                    default='tree', choices=['seq', 'tree'])
parser.add_argument('--output_format', type=str,
                    default='tree', choices=['seq', 'tree'])
parser.add_argument('--no_attention', action='store_true',
                    help='set to true to disable attention')
parser.add_argument('--no_pf', action='store_true',
                    help='set to true to disable parent attention feeding')

# Python-JavaScript Dataset
parser.add_argument('--train_data', type=str, default='../../parser/data/source_py_target_js_train.json',
                    help='training data')
parser.add_argument('--val_data', type=str, default='../../parser/data/source_py_target_js_valid.json',
                    help='training data')
parser.add_argument('--test_data', type=str, default='../../parser/data/source_py_target_js_atom_test.json',
                    help='test data')

# Additional Arguments
parser.add_argument('--result_dir', default='../result/',
                    help='director to save the translation result.')
parser.add_argument('--train_process_data_dir', type=str, default='train_process_data.csv',
                    help='directory to save data during training process')
parser.add_argument('--source_lang', type=str, default='py',
                    help='the source language of the translator')
parser.add_argument('--target_lang', type=str, default='js',
                    help='the target language of the translator')

args = parser.parse_args()


def save_vocabulary_in_csv(source_vocab, target_vocab):
    header = ['vocab', 'token_id']
    with open('source_vocab.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)  # csv writer
        writer.writerow(header)
        for vocab in source_vocab.keys():
            writer.writerow([vocab, source_vocab[vocab]])
    with open('target_vocab.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)  # csv writer
        writer.writerow(header)
        for vocab in target_vocab.keys():
            writer.writerow([vocab, target_vocab[vocab]])
    print('File Wrote: Vocabulary Files.')


def main():
    if args.network == 'seq2seq' or args.network == 'seq2tree':
        source_serialize = True
    else:
        source_serialize = False
    if args.network == 'seq2seq' or args.network == 'tree2seq':
        target_serialize = True
    else:
        target_serialize = False
    if args.no_attention:
        args.no_pf = True
    train_data = json.load(open(args.train_data, 'r'))
    source_vocab, target_vocab, source_vocab_list, target_vocab_list = data_utils.build_vocab(
        train_data, args.vocab_filename, args.input_format, args.output_format)
    save_vocabulary_in_csv(source_vocab, target_vocab)
    if args.test:
        test_data = json.load(open(args.test_data, 'r'))
        test(train_data, test_data, source_vocab, target_vocab, source_vocab_list,
             target_vocab_list, source_serialize, target_serialize)
    else:
        val_data = json.load(open(args.val_data, 'r'))
        train(train_data, val_data, source_vocab, target_vocab, source_vocab_list,
              target_vocab_list, source_serialize, target_serialize)


main()
