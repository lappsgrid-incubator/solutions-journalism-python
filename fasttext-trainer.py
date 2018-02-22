import fasttext
from flask import Flask
from flask import request


app = Flask(__name__)


def input_log_table(info):
    header = "{:10}{:20}{}".format("InputID","Date","FilePath")
    table = [header]
    for (inID,date,path) in info.split(','):
        table.append("{:10}{:20}{}".format(inID,date,path))
    return '\n'.join(table)

def model_log_table(info):
    header = "{:10}{:20}{:11}{}".format("ModelID","Date","Type","FilePath")
    table = [header]
    for (inID,date,modtype,path) in info.split(','):
        table.append("{:10}{:20}{:11}{}".format(inID,date,modtype,path))
    return '\n'.join(table)

@app.route('/trainer/')
def execute():
    train_id = request.args.get("train", default=None)
    if train_id is None:
        return "ERROR: No InputID was given for the train file."

    else:
        try:
            with open('data/cache/inputs/log.txt', 'r') as log:
                log_info = log.readlines()
                ## If the given ID is higher than the current highest, use the next available ID
                if train_id < len(log_info):
                    train_file = log_info[train_id].split(",")[2]

                else:
                    instr = "ERROR: The given InputID ({}) does not correspond to any input file. The table below shows the existing input files.\n\n".format(current_id)
                    return instr + log_as_table(log_info[1:])

        except IOError:
            return "There is no log file for inputs. You can use the converter to create fasttext input files."

    model_type = request.args.get("type", default=None)

    if model_type is None:
        return "ERROR: No model type was given"

    valid_types = ["supervised","skipgram","cbow"]

    if model_type not in valid_types:
        return "ERROR: Only three types are allowed: supervised, skipgram, or cbow."

    
    epoch = request.args.get("epoch", default=5)
    ngrams = request.args.get("ngrams", default=1)
    label_prefix = request.args.get("label", default='__label__')

    current_id = 1
    log_info = []

    model_id = request.args.get("id", default=None)
    name = request.args.get("name", default=None)
    
    if model_id == None:
        try:
            with open('data/cache/models/log.txt', 'r') as log:
                log_info = log.readlines()
                current_id = int(log_info[0].strip()) + 1
                log_info[0] = str(current_id) + "\n"

        except IOError:
            log_info.append("1\n")

        if name is None:
            name = 'model' + current_id + '.ftxt'

        model_file = 'data/cache/models/' + name

        if model_type == "supervised":
            classifier = fasttext.supervised(train_file, model_file, epoch=epoch, word_ngrams=ngrams, label_prefix=label_prefix)

        elif model_type == "skipgram":
            classifier = fasttext.skipgram(train_file, model_file, epoch=epoch, word_ngrams=ngrams, label_prefix=label_prefix)

        elif model_type == "cbow":
            classifier = fasttext.cbow(train_file, model_file, epoch=epoch, word_ngrams=ngrams, label_prefix=label_prefix)

        log_info.append(str(current_id) + "," + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "," + model_type + "," + model_file + '\n')

        with open('data/cache/models/log.txt', 'w') as log:
            f.write(''.join(log_info))


    else:
        current_id = int(model_id)

        try:
            with open('data/cache/models/log.txt', 'r') as log:
                log_info = log.readlines()
                if current_id < len(log_info):
                    line = log_info[current_id].split(",")
                    if name is None:
                        name = line[3]
                    model_file = 'data/cache/models/' + name
                    line[3] = model_file
                    line[2] = model_type
                    line[1] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    log_info[current_id] = ",".join(line)

                ## If the given ID is higher than the current highest, use the next available ID
                else:
                    current_id = len(log_info)
                    log_info[0] = str(current_id) + "\n"
                    if name is None:
                        name = 'model' + current_id + '.ftxt'
                    model_file = 'data/cache/models/' + name
                    log_info.append(str(current_id) + "," + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "," + model_type + "," + model_file + '\n')

        except IOError:
            current_id = 1
            log_info.append("1\n")
            if name is None:
                model_file = 'data/cache/models/model1.fstx'
            else:
                model_file = 'data/cache/models/' + name
            log_info.append("1," + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "," + model_type + "," + model_file + '\n')

        if model_type == "supervised":
            classifier = fasttext.supervised(train_file, model_file, epoch=epoch, word_ngrams=ngrams, label_prefix=label_prefix)

        elif model_type == "skipgram":
            classifier = fasttext.skipgram(train_file, model_file, epoch=epoch, word_ngrams=ngrams, label_prefix=label_prefix)

        elif model_type == "cbow":
            classifier = fasttext.cbow(train_file, model_file, epoch=epoch, word_ngrams=ngrams, label_prefix=label_prefix)

        with open('data/cache/models/log.txt', 'w') as log:
            f.write(''.join(log_info))  

    instr = "Use modelID {} for the tester tool.\n\n".format(current_id)

    return instr + model_log_table(log_info)


if __name__ == '__main__':
    app.run(debug=True)

execute()