#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import operator
import re
import numpy as np
from string import punctuation
from bor_tree import Candidate, Node, BorTree
from error_model import ErrorModel
from language_model import LanguageModel
from split_join_model import SplitJoin
from layout import switch_layout
punctuation = re.escape(punctuation)



error_model=ErrorModel()
error_model.load_json('error.json')
language_model=LanguageModel()
language_model.load_json('language.json')
tree=BorTree(error_model,language_model)
tree.fit()
split_join=SplitJoin(language_model)


def fix_query(query):
    
    tokens = re.split('([' + punctuation + ' ' + '])', query)
    candidate = fix_tokens(tokens)

    layout,switch= switch_layout(query)
    if switch:
        return layout
    joined_tokens, join = split_join.join(tokens)
    if join:
        joined_candidate = fix_tokens(joined_tokens)
        if joined_candidate.error_weight < candidate.error_weight:
            return joined_candidate.word
    split_tokens, split = split_join.split(tokens)
    if split:
        split_candidate = fix_tokens(split_tokens)
        return split_candidate.word
    return candidate.word



def fix_tokens(tokens):
    result = ''
    language_weight = 0
    error_weight = 0
    for t in tokens:
        is_word = not re.match('[' + punctuation + ' ' + ']*$', t)
        if is_word:
            fixed = fix_word(t)
            t = fixed.word
            language_weight += fixed.language_weight
            error_weight += fixed.error_weight
        result += t

    return Candidate(word=result, language_weight=language_weight, error_weight=error_weight)



def fix_word(word):
    global tree
    candidates = tree.generate(
        word, max_number_of_candidates=60, max_sum_of_weights=10, part=0.7)
    if len(candidates) < 1:
        return Candidate(word=word, language_weight=0, error_weight=0)
    else:
        candidates.sort(key=operator.attrgetter('language_weight'))
        candidates.sort(key=operator.attrgetter('error_weight'))
        part = max(1, len(candidates) // 8)
        candidates = candidates[:part]
        return sorted(candidates, key=operator.attrgetter('language_weight'))[-1]



def iterations(query):
    max_counter = 2
    iterations_counter = 0


    while (iterations_counter < max_counter):

        new_query = fix_query(query)
        if (new_query == query):
            break
        query = new_query
        iterations_counter += 1

    return new_query



while (True):
    try:
        query =raw_input().decode('utf-8')
    except (EOFError):
        break

    print (iterations(query).strip()).encode('utf-8')





