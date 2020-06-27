import dill 
import numpy as np 
from collections import defaultdict
import json

def flatten_dictionary(dictionary):
    values = []
    for d in dictionary.values():
        for v in d.values():
            values.append(v)
    return values

class ErrorModel:

    def __init__(self):
        self.statistics = defaultdict(lambda: defaultdict(int))
    
    def update_statistics(self, given, fixed):
        n, m = len(given), len(fixed)
        MAX_DISTANCE = (n + 1) * (m + 1)

        matrix=_get_levenshtein_matrix(given,fixed)

        position = [n, m, matrix[m, n]] 
        while position[2] != 0: 
            x, y = position[0], position[1]

            possible_actions = [matrix[y - 1][x - 1] if (x > 0) and (y > 0) else MAX_DISTANCE,  # change
                                matrix[y - 1][x] if y > 0 else MAX_DISTANCE,  # add
                                matrix[y][x - 1] if x > 0 else MAX_DISTANCE]  # delete
            action = np.argmin(possible_actions)

            if action == 0:  # change
                if position[2] != possible_actions[action.item()]:
                    position[2] -= 1
                    self.statistics[given[x-1]][fixed[y-1]] += 1
                position[0] -= 1
                position[1] -= 1
            elif action == 1:  # add
                if position[2] != possible_actions[action.item()]:
                    position[2] -= 1
                    self.statistics[''][fixed[y - 1]] += 1
                position[1] -= 1
            else:  # delete
                if position[2] != possible_actions[action.item()]:
                    position[2] -= 1
                    self.statistics[given[x - 1]][''] += 1
                position[0] -= 1

                    
    def load_json(self, json_path):
        stat = json.loads(open(json_path, "r").read())
        self.statistics =  stat
        self.calculate_weights()

    def store_json(self, json_path):
        file = open(json_path, "w")
        file.write(json.dumps((self.statistics)))
        file.close()
  
    def calculate_weights(self):
        frequencies_to_weights, default_weight = ErrorModel.prepare_weights(
            (flatten_dictionary(self.statistics)))

        self.weights = defaultdict(
            lambda: defaultdict(lambda: default_weight))
        for k1, v in self.statistics.items():
            for k2 in v.keys():
                self.weights[k1][ k2] =\
                    frequencies_to_weights[self.statistics[k1][k2]]
    
    @staticmethod
    def prepare_weights(values):
        list_frequencies = np.sort(np.array(values))[::-1]
        list_weights = np.log1p(list_frequencies).astype(float)[::-1]
        list_frequencies_to_weights = {}
        for i in range(len(list_frequencies)):
            list_frequencies_to_weights[list_frequencies[i]] = list_weights[i]
        default_weight = np.max(list_weights)
        return list_frequencies_to_weights, default_weight
def _get_levenshtein_matrix(a, b):
    n, m = len(a), len(b)
    inverse = False
    if n > m:
        a, b = b, a
        n, m = m, n
        inverse = True

    current_row = list(range(n + 1))  
    matrix = np.array([current_row])
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, \
                                  current_row[j - 1] + 1, \
                                  previous_row[j - 1] + int(a[j - 1] != b[i - 1])
            current_row[j] = min(add, delete, change)
        matrix = np.vstack((matrix, [current_row]))
    return matrix if not inverse else matrix.T
