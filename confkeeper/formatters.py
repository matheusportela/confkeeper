import json
import pickle


class BaseFormatter:
    def convert_to_format(self, data):
        raise NotImplementedError(f'{self.__class__.__name__} must implement "convert_to_format"')

    def convert_from_format(self, data):
        raise NotImplementedError(f'{self.__class__.__name__} must implement "convert_from_format"')


class JSONFormatter:
    def convert_to_format(self, data):
        return json.dumps(data)

    def convert_from_format(self, data):
        return json.loads(data)


class PickleFormatter:
    def convert_to_format(self, data):
        return str(pickle.dumps(data), encoding='latin1')

    def convert_from_format(self, data):
        return pickle.loads(bytes(data, encoding='latin1'))

formatters = {
    'json': JSONFormatter(),
    'pickle': PickleFormatter(),
}
