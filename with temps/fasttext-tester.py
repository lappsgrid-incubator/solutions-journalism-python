import fasttext
import tempfile
from flask import Flask
import sys

args = sys.argv
app = Flask(__name__)

@app.route('/tester/')
def execute(self, input):
    if "-t" not in args:
        return "ERROR: No input test file was given"

    test_file = args[args.index("-t")+1]

    if "-m" not in args:
        return "ERROR: No model was given"

    model_file = args[args.index("-m")+1]
    
    classifier = fasttext.load_model(model_file)
    result = classifier.test(test_file)
    return vars(result)

if __name__ == '__main__':
    app.run(debug=True)

execute()