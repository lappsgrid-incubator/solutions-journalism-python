import json
import tempfile
from lif.discriminators import Uri
from lif.lif import *


class Converter:

    def __init__(self):
        self.metadata = generate_metadata()

    def generate_metadata():
        metadata = {}
        metadata['name'] = 'Converter'
        metadata['description'] = "A converter creating temporary fasttext files from json files."
        ## TODO: version
        metadata['version'] = '0.0.1'
        metadata['vendor'] = 'http://www.lappsgrid.org'
        metadata['license'] = Uri.APACHE2

        requires = {}
        requires['format'] = Uri.JSON
        requires['encoding'] = "UTF-8"

        produces = {}
        produces['format'] = Uri.TEXT
        produces['encoding'] = "UTF-8"

        metadata['requires'] = requires
        metadata['produces'] = produces

        data = Data(Uri.META, metadata)
        return data.as_pretty_json()

    def getMetadata(self):
        return self.metadata


    def filter_blanks(dataset):
        return [val for val in dataset if val is not None and val != '']

    def getfield(dataset, field):
        if isinstance(dataset, dict):
            index = dataset['fields'].index(field)
            return filter_blanks([row[index] for row in dataset['values']])
        else:
            return filter_blanks([row[field] for row in dataset])


    def execute(self, input):
        Data data = Serializer.parse(input, Data)

        ## Return ERRORS back
        if data.discriminator == Uri.ERROR:
            return input
            

        ## If the input discriminator is wrong, return an error
        elif data.discriminator != Uri.JSON
            return Data(Uri.ERROR, "Invalid input").as_json()

        jsonData = json.load(data.payload)

        lab = data.get_parameter('labels')

        if lab == None:
            return Data(Uri.ERROR, "A valid list of labels must be given, in order to create appropriate temporary files for fasttext").as_json()

        labels = lab.split(',')

        allLabels = []

        for each in labels:
            labelData = getfield(jsonData, each)
            allLabels.append(('__label__%s %s' % ex) for ex in labelData)

        tmp, filename = tempfile.mkstemp()

        with open(tmp, 'w') as f:
            f.write('\n'.join(allLabels))

        return Data(Uri.TEXT, filename)