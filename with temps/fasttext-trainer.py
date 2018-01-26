import fasttext
import tempfile
from flask import Flask
import sys

args = sys.argv
app = Flask(__name__)

def get_optional_param(param, default):
    if param not in args:
        return default

    else:
        return args[args.index(param)+1]


@app.route('/trainer/')
def execute():
    if "-i" not in args:
        return "ERROR: No input file was given"

    train_file = args[args.index("-i")+1]

    if "-t" not in args:
        return "ERROR: No model type was given"

    model_type = args[args.index("-t")+1]
    
    epoch = get_optional_param('--epoch',5)

    ngrams = get_optional_param('--ngrams',1)

    label_prefix = get_optional_param('--label','__label__')

    tmp, modelname = tempfile.mkstemp()

    tmp.close()

    if model_type == "supervised":
        classifier = fasttext.supervised(train_file, modelname, epoch=epoch, word_ngrams=ngrams, label_prefix=label_prefix)

    elif model_type == "skipgram":
        classifier = fasttext.skipgram(train_file, modelname, epoch=epoch, word_ngrams=ngrams, label_prefix=label_prefix)

    elif model_type == "cbow":
        classifier = fasttext.cbow(train_file, modelname, epoch=epoch, word_ngrams=ngrams, label_prefix=label_prefix)

    return modelname

if __name__ == '__main__':
    app.run(debug=True)

execute()