import tempfile
import json
from flask import Flask
import sys

args = sys.argv
app = Flask(__name__)

def filter_blanks(dataset):
    return [val for val in dataset if val is not None and val != '']

def getfield(dataset, field):
    if isinstance(dataset, dict):
        index = dataset['fields'].index(field)
        return filter_blanks([row[index] for row in dataset['values']])
    else:
        return filter_blanks([row[field] for row in dataset])


@app.route('/convert/pos-neg/')
def execute():
    if "-p" not in args:
        return "ERROR: No positive examples file was given"

    input_pos = args[args.index("-p")+1]
    with open(input_pos, 'r') as f:
        json_pos = json.load(f)

    if "-n" not in args:
        return "ERROR: No negative examples file was given"

    input_neg = args[args.index("-n")+1]
    with open(input_neg, 'r') as f:
        json_neg = json.load(f)

    if "-l" not in args:
        return "ERROR: A valid list of labels must be given, in order to create appropriate temporary files for fasttext"

    labels = args[args.index("-l")+1].split(',')

    all_labels = []

    for each in labels:
        label_data = getfield(json_pos, each)
        all_labels.append(('__label__pos %s' % ex) for ex in label_data)
        label_data = getfield(json_neg, each)
        all_labels.append(('__label__neg %s' % ex) for ex in label_data)


    tmp, filename = tempfile.mkstemp()

    with open(tmp, 'w') as f:
        f.write('\n'.join(all_labels))

    return filename


if __name__ == '__main__':
    app.run(debug=True)

execute()