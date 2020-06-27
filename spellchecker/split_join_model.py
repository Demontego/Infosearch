class SplitJoin:
    
    def __init__(self, language_model):
        self.words=language_model.weights.keys()
        
    def split(self, tokens):
        split = False
        words_positions = []
        split_tokens = []
        for i, token in enumerate(tokens):
            if token.isalpha():
                words_positions.append(i)
        for i in words_positions:
            token = tokens[i]
            if len(token) > 2:
                for pos in range(1, len(token)):
                    left = token[:pos]
                    right = token[pos:]
                    if (left in self.words and right in self.words) and (token not in self.words):
                        split_tokens = list(tokens)
                        split_tokens[i] = right
                        split_tokens.insert(i, ' ')
                        split_tokens.insert(i, left)
                        split = True
                        break
            if (split == True):
                break
        return split_tokens, split

    def join(self, tokens):
        joined = False
        words_positions = []

        for i, token in enumerate(tokens):
            if token.isalpha():
                words_positions.append(i)

        for i in range(len(words_positions) - 1):
            left = tokens[words_positions[i]]
            right = tokens[words_positions[i + 1]]
            if (left not in self.words or right not in self.words) and left + right in self.words:
                tokens[words_positions[i]] = left + right
                for pos in sorted(range(words_positions[i] + 1, words_positions[i + 1] + 1), reverse=True):
                    del tokens[pos]
                joined = True
                break

        return tokens, joined
