import fasttext
import tempfile
from lif.discriminators import Uri
from lif.lif import *


class Tester:

    def __init__(self):
        self.metadata = generate_metadata()

    def generate_metadata():
        metadata = {}
        metadata['name'] = 'Tester'
        metadata['description'] = "The classifier test function from the FastText python package."
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
            return Data(Uri.ERROR, "Invalid input").as_json()

        testFileName = data.payload

        modelname = data.get_parameter('model')

        if modelname == None:
            return Data(Uri.ERROR, "You must specify the model to be used on this test set").as_json()

        classifier = fasttext.load_model(modelname)
        result = classifier.test(testFileName)
        return Data(Uri.TEXT, vars(result))