import csv

with open('pre-procesados/pokes_test_binariz.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    with open('pre-procesados/pokes_test_binariz.txt', 'w') as txtfile:
       for row in reader:
            txtfile.write('\t'.join(row[:]) + '\n')

with open('pre-procesados/pokes_train_binariz.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    with open('pre-procesados/pokes_train_binariz.txt', 'w') as txtfile:
       for row in reader:
            txtfile.write('\t'.join(row[:]) + '\n')

