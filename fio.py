import random

with open('FIO.txt', encoding='utf-8') as f:
    fio = [x.split(' ') for x in f]

random.shuffle(fio)

with open('FIO_re.txt', 'w+') as f:
    f.writelines([('%s %s.%s.\n' % (x[0], x[1][0], x[2][0])) for x in fio])
