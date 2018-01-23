import fasttext
import tempfile
from lif.discriminators import Uri
from lif.lif import *


class Trainer:

    def __init__(self):
        self.metadata = generate_metadata()

    def generate_metadata():
        metadata = {}
        metadata['name'] = 'Trainer'
        metadata['description'] = "The classifier trainer function from the FastText python package."
        ## TODO: version
        metadata['version'] = '0.0.1'
        metadata['vendor'] = 'http://www.lappsgrid.org'
        metadata['license'] = Uri.APACHE2

        requires = {}
        requires['format'] = Uri.TEXT
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

    def execute(self, input):
        Data data = Serializer.parse(input, Data)

        ## Return ERRORS back
        if data.discriminator == Uri.ERROR:
            return input

        ## If the input discriminator is wrong, return an error
        elif data.discriminator != Uri.TEXT
            return Data(Uri.ERROR, "Invalid input").as_json();

        trainFileName = data.payload

        epoch = data.get_parameter('epoch')

        if epoch == None:
            epoch = 5

        ngrams = data.get_parameter('ngrams')

        if ngrams = None:
            ngrams = 1

        label_prefix = data.get_parameter('label_prefix')

        if label_prefix == None:
            label_prefix = '__label__'

        tmp, modelname = tempfile.mkstemp()

        classifier = fasttext.supervised(trainFileName, modelname, epoch=epoch, word_ngrams=ngrams, label_prefix=label_prefix)

        return Data(Uri.TEXT, modelname)