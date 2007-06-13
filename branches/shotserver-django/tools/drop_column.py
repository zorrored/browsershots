import sys

headline = sys.stdin.readline()
headline = headline.replace(', request_id', '')
sys.stdout.write(headline)

while True:
    line = sys.stdin.readline()
    if not line:
        break
    if line.strip() == r'\.':
        sys.stdout.write(line)
        break
    values = line.rstrip('\n').split('\t')
    values.pop(2)
    sys.stdout.write('\t'.join(values) + '\n')
