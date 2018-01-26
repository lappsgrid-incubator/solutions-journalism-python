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

    all_labels = list()

    for each in labels:
        pos_data = getfield(json_pos, each)
        pos_labels = [('__label__pos %s' % ex) for ex in pos_data]
        neg_data = getfield(json_neg, each)
        neg_labels = [('__label__neg %s' % ex) for ex in neg_data]
        all_labels += pos_labels + neg_labels

    return '\n'.join(all_labels)

if __name__ == '__main__':
    app.run(debug=True)

execute()