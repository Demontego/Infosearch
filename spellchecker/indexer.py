from re import escape
from string import punctuation
import pandas as pd
from read_queries import read, flatten_list, flatten_dictionary
from error_model import ErrorModel
from language_model import LanguageModel
from bor_tree import BorTree




queries_file = open('queries_all.txt', 'r', encoding='utf-8')
queries = queries_file.read()
queries = [q.split('\t') for q in queries]
original_queries = []
fixed_queries = []
for q in queries:
    if len(q) == 2:
        original_queries.append(q[0])
        fixed_queries.append(q[1])
    else:
        original_queries.append(q[0])
        fixed_queries.append(q[0])

punctuation = escape(punctuation)

fixed_queries_to_words = pd.Series(fixed_queries).replace('[' + punctuation + ']', '', regex=True).str.split()
fixed_words = flatten_list(fixed_queries_to_words)


original_queries_to_words = pd.Series(original_queries).replace('[' + punctuation + ']', '', regex=True).str.split()
original_words = flatten_list(original_queries_to_words)





error_model = ErrorModel()

for original, fixed in zip(original_queries_to_words, fixed_queries_to_words):
    number_of_words = min(len(original), len(fixed))
    for i in range(number_of_words):
        error_model.update_statistics(original[i], fixed[i])

error_model.calculate_weights()





language_model= LanguageModel()

for fixed in fixed_queries_to_words:
    for word in fixed:
        language_model.update_statistics(word)

language_model.calculate_weights()





error_model.store_json('error.json')
language_model.store_json('language.json')


# In[ ]:




