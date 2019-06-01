import ast
import json
import os


class IOutput(object):
    def output(self, message, lock):
        raise NotImplementedError()


class FileOutputManager(IOutput):

    def __init__(self, file_name=None):

        if file_name:
            self._file = file_name
        else:
            self._file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output.txt')

    def output(self, message, lock):
        if isinstance(message, dict):
            message = ast.literal_eval(json.dumps(message))

        try:
            lock.acquire(timeout=20)

            with open(self._file, 'a') as f:
                f.writelines("{}\n".format(message))

        finally:
            lock.release()
