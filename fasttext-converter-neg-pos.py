import datetime
import json
from flask import Flask
from flask import request

app = Flask(__name__)

def filter_blanks(dataset):
    return [val for val in dataset if val is not None and val != '']

def getfield(dataset, field):
    if isinstance(dataset, dict):
        index = dataset['fields'].index(field)
        return filter_blanks([row[index] for row in dataset['values']])
    else:
        return filter_blanks([row[field] for row in dataset])

## Print the comma-seperated log portion as a table
def input_log_table(info):
    header = "{:10}{:20}{}".format("InputID","Date","FilePath")
    table = [header]
    for (inID,date,path) in info[1:].split(','):
        table.append("{:10}{:20}{}".format(inID,date,path))
    return '\n'.join(table)


@app.route('/convert/pos-neg', methods=['POST','GET'])
def execute():
    pos = request.form['pos']
    if pos is None:
        return "ERROR: No positive examples file was given\n"
    
    json_pos = json.loads(pos)

    neg = request.form['neg']
    if neg is None:
        return "ERROR: No negative examples file was given\n"

    json_neg = json.loads(neg)

    lab_text = request.args.get("lab", default=None)
    if lab_text is None:
        return "ERROR: A valid list of labels must be given, in order to create appropriate temporary files for fasttext\n"

    lab = lab_text.split(",")

    all_labels = list()

    for each in lab:
        pos_data = getfield(json_pos, each)
        pos_labels = [('__label__pos %s' % ex) for ex in pos_data]
        neg_data = getfield(json_neg, each)
        neg_labels = [('__label__neg %s' % ex) for ex in neg_data]
        all_labels += pos_labels + neg_labels


    current_id = 1
    log_info = []

    input_id = request.args.get("id", default=None)

    name = request.args.get("name", default=None)
    
    if input_id == None:
        try:
            with open('data/cache/inputs/log.txt', 'r') as log:
                log_info = log.readlines()
                current_id = int(log_info[0].strip()) + 1
                log_info[0] = str(current_id) + "\n"

        except IOError:
            log_info.append("1\n")

        if name is None:
            name = 'input' + current_id + '.ftxt'
        current_file = 'data/cache/inputs/' + name

        with open(current_file, 'w') as f:
            f.write('\n'.join(all_labels))

        log_info.append(str(current_id) + "," + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "," + current_file + '\n')

        with open('data/cache/inputs/log.txt', 'w') as log:
            f.write(''.join(log_info))

    else:
        current_id = int(input_id)

        try:
            with open('data/cache/inputs/log.txt', 'r') as log:
                log_info = log.readlines()
                if current_id < len(log_info):
                    line = log_info[current_id].split(",")
                    if name is None:
                        name = line[2]
                    current_file = 'data/cache/inputs/' + name
                    line[2] = current_file
                    line[1] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    log_info[current_id] = ",".join(line)

                ## If the given ID is higher than the current highest, use the next available ID
                else:
                    current_id = len(log_info)
                    log_info[0] = str(current_id) + "\n"
                    if name is None:
                        name = 'input' + current_id + '.ftxt'
                    current_file = 'data/cache/inputs/' + name
                    log_info.append(str(current_id) + "," + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "," + current_file + '\n')


        except IOError:
            current_id = 1
            log_info.append("1\n")
            if name is None:
                current_file = 'data/cache/inputs/input1.fstx'
            else:
                current_file = 'data/cache/inputs/' + name
            log_info.append("1," + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "," + current_file + '\n')

        with open(current_file, 'w') as f:
            f.write('\n'.join(all_labels))

        with open('data/cache/inputs/log.txt', 'w') as log:
            f.write(''.join(log_info))  

    instr = "Use InputID {} for the trainer tool.\n\n".format(current_id)
    
    return instr + input_log_table(log_info[1:])

if __name__ == '__main__':
    app.run(debug=True)

execute()