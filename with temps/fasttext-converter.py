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


@app.route('/convert/')
def execute():
    if "-i" not in args:
    	return "ERROR: No input file was given"

	input_path = args[args.index("-i")+1]
	with open(input_path, 'r') as f:
		json_data = json.load(f)


    if "-l" not in args:
        return "ERROR: A valid list of labels must be given, in order to create appropriate temporary files for fasttext"

	labels = args[args.index("-l")+1].split(',')

    all_labels = []

    for each in labels:
        label_data = getfield(json_data, each)
        all_labels.append(('__label__%s %s' % ex) for ex in label_data)

    tmp, filename = tempfile.mkstemp()

    with open(tmp, 'w') as f:
        f.write('\n'.join(all_labels))

    return filename


if __name__ == '__main__':
    app.run(debug=True)

execute()