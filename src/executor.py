import argparse
import os
import yaml

from concurrent.futures import ThreadPoolExecutor
from src.store import Store
from src.textprocessor import TextProcessor


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class ConfigLoader:
    @classmethod
    def load(cls, path):
        with open(path, 'r') as f:
            return yaml.load(f)


def benchmark(func):
    import time

    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print(func.__name__, time.clock() - t)
        return res

    return wrapper


class Executor:
    def __init__(self, confpath):
        self.conf = ConfigLoader.load(confpath)
        self.store = Store(self.conf['store'])
        self.dirfiles = self.conf.get('dirfiles', os.path.join(CURRENT_DIR, os.pardir, 'text_files'))
        self.max_workers = self.conf.get('max_workers')

    def __enter__(self):
        self.prepare()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def shutdown(self):
        self.store.close()

    def prepare(self):
        self.store.connect()

    @staticmethod
    def create_arg_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('--confpath',
                            help="path to config file",
                            type=str,
                            default=os.path.abspath(os.path.join(CURRENT_DIR, os.path.pardir, 'conf.yaml')))
        return parser

    def _exec(self, filename):
        """
        Процессит файл, инсерит в бд
        """
        with open(os.path.join(self.dirfiles, filename)) as f:
            txt = f.read()
            text_processor = TextProcessor(txt)
            sick, hack = text_processor.academic_sickness()
            self.store.collection.insert({
                'file': filename,
                'sickness': sick,
                'hack': hack
            })

    @benchmark
    def run(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self._exec, os.listdir(self.dirfiles))
