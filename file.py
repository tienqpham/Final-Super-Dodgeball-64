import os
import json
import sys

sys.path.append('..')

class File:
    class __File:
        def __init__(self):
            self.config = json.load(open('data.json'))


        def get_objects(self):
            return list(self.config.keys())


        def load(self, key):
            if key in self.config:
                return self.config[key]['path']

            return ValueError('object not found')


        def get_data(self, key):
            path = self.get_path(key)
            
            if os.path.exists(path):
                return open(path).read()
            
            return ValueError('media not found')

        def reopen(self):
            self.config = json.load(open('data.json'))

        

    instance = None
    def __init__(self):
        if not File.instance:
            File.instance = File.__File()

    def __getattr__(self, name):
        return getattr(self.instance, name)
