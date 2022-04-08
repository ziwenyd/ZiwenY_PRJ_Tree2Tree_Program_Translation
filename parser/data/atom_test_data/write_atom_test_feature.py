import csv

def main():
    features = ["For loop", "Map(Dict)","String","If-elif-else","Array(List)","Equality(===)","Infinity","undefined","JS !''"]
    file_counts = []
    file_counts.append(" ".join([ str(i) for i in range(1,11)]))
    file_counts.append(" ".join([ str(i) for i in range(11,21)]))
    file_counts.append(" ".join([ str(i) for i in range(21,26)]))
    file_counts.append(" ".join([ str(i) for i in range(26,31)]))
    file_counts.append(" ".join([ str(i) for i in range(31,36)]))
    file_counts.append(" ".join([ str(i) for i in range(36,38)]))
    file_counts.append("38")
    file_counts.append("39")
    file_counts.append("40")

    header = ['feature', 'file_numbers']
    csv_result = []
    for i in range(len(features)):
        csv_result.append([features[i],file_counts[i]])

    rdir = 'atom_test_feature.csv'
    f = open(rdir, 'w',encoding='UTF8')
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    csv_writer.writerows(csv_result)
    print('finished')

main()