import sys


def copy_table(line, echo=True):
    if echo:
        sys.stdout.write(line)
    while line.strip() != r'\.':
        line = sys.stdin.readline()
        if echo:
            sys.stdout.write(line)


while True:
    line = sys.stdin.readline()
    if not line:
        break
    if line.startswith('COPY '):
        table = line.split()[1]
        copy_table(line, table in sys.argv[1:])
