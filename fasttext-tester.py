import fasttext
import tempfile
from flask import Flask
from flask import request


app = Flask(__name__)

@app.route('/tester/')
def execute():
    test_id = request.args.get("test", default=None)
    if test_id is None:
        return "ERROR: No InputID was given for the test file."

    else:
        try:
            with open('data/cache/inputs/log.txt', 'r') as log:
                log_info = log.readlines()
                ## If the given ID is higher than the current highest, use the next available ID
                if test_id < len(log_info):
                    test_file = log_info[test_id].split(",")[2]

                else:
                    instr = "ERROR: The given InputID ({}) does not correspond to any input file. The table below shows the current input files.\n\n".format(current_id)
                    return instr + log_as_table(log_info[1:])

        except IOError:
            return "There is no log file for inputs. You can use the converter to create fasttext input files."


    model_id = request.args.get("model", default=None)
    if model_id is None:
        return "ERROR: No ModelID was given for the model file."

    else:
        try:
            with open('data/cache/models/log.txt', 'r') as log:
                log_info = log.readlines()
                ## If the given ID is higher than the current highest, use the next available ID
                if model_id < len(log_info):
                    model_file = log_info[model_id].split(",")[3]

                else:
                    instr = "ERROR: The given ModelID ({}) does not correspond to any model. The table below shows the existing models.\n\n".format(current_id)
                    return instr + log_as_table(log_info[1:])

        except IOError:
            return "There is no log file for models. You can use the trainer to create fasttext models."

    classifier = fasttext.load_model(model_file)
    result = classifier.test(test_file)
    return str(vars(result))

if __name__ == '__main__':
    app.run(debug=True)

execute()