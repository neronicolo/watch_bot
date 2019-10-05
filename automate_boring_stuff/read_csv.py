import csv
from pathlib import Path

example_file = open(Path.cwd()/'automate_boring_stuff'/'files'/'example.csv')
example_reader = csv.reader(example_file)
#example_data = list(example_reader)
#print(example_data)
#print(example_data[0][1])

for row in example_reader:
    print(f'Row: {example_reader.line_num} {row}')

