# BSc Final Year Project
GitHub Repository link: https://github.com/ziwenyd/ZiwenY_PRJ_Tree2Tree_Program_Translation

This repository includes the code implementation of Ziwen Yuan's BSc Final Year Project at King's College London, supervised by Dr.Kevin Lano. This repo is the supplymentary material of Ziwen Yuan's project of the final report.

The code implementation includes three parts:

1. parser/ : Prepare data for the Tree2Tree Neural Network model.
2. tree2tree/ : The implementation of the Tree2Tree Neural Network, where training and testing performs.
3. evaluation/ : Two commertial Python-JavaScript Translator, with an emphasize on JavaScripthon. This folder includes scripts to perform translation via JavaScripthon, analyze statistics(with JavaScript and Python raw program tokenizers), and evaluate the result (based on several evaluation metrics used in previous research on Program Translation task).

Each folder contains its own README.md file that includes detailed information of that folder, including useful commands to copy-paste and use straight-away.

Code in this repository are directly executable and expected to perform in the same way as described in the final report. Environment set up instructions(utilizing Python Virtual Environment and Anaconda) are provided clearly inside each folder where needed. All dependencies included.

# Reference

1. The Tree2Tree model was proposed and intialllay built by Chen et al. for their paper[[arXiv](https://arxiv.org/abs/1802.03691)][[NeurIPS](https://papers.nips.cc/paper/7521-tree-to-tree-neural-networks-for-program-translation)].

```bash
@inproceedings{chen2018tree,
  title={Tree-to-tree Neural Networks for Program Translation},
  author={Chen, Xinyun and Liu, Chang and Song, Dawn},
  booktitle={Proceedings of the 31st Advances in Neural Information Processing Systems},
  year={2018}
}
```

2. ANTLR4 is used to build TreeParser for Python3 and JavaScript. TreeParser is used to convert raw Python3 or JavaScript programs into string-formatted parse trees.
   ANTLR4 official website: https://www.antlr.org/

3. JavaScripthon is an open-sourced Python to JavaScript single-directional translator.
   Its official GitHub repo: https://github.com/metapensiero/metapensiero.pj#introduction
   An online platform built on top of JavaScripthon that allow instant interaction to translate simple funcitons: https://extendsclass.com/python-to-javascript.html

4. js-tokens is an open-sourced JavaScript tokenizer. It is used during evaluation, to analyze the statistics of raw JavaScript programs.
   js-tokens GitHub repo: https://github.com/lydell/js-tokens
