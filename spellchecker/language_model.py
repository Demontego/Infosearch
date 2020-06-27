import dill 
import numpy as np 
from collections import defaultdict
import json

class LanguageModel:

    def __init__(self):
        self.statistics = defaultdict(int)
        self.size=0
        
    def load_json(self, json_path):
        (size, stat) = json.loads(open(json_path, "r").read())
        self.size, self.statistics= size, stat
        self.calculate_weights()

    def store_json(self, json_path):
        file = open(json_path, "w")
        file.write(json.dumps((self.size, self.statistics)))
        file.close()
        
    def update_statistics(self, token):
        self.statistics[token]+=1
        self.size+=1

    def calculate_weights(self):
        self.weights=defaultdict(lambda: 0.5/self.size)
        for item,stat in self.statistics.items():
            self.weights[item]=stat/self.size
