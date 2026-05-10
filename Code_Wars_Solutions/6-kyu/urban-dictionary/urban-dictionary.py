import re
class WordDictionary:
    def __init__(self):
        self.allWords=[]
        pass
​
    def add_word(self, word):
        self.allWords.append(word)
        pass
​
    def search(self, word):
        pattern=f"^{word}$"
        for eachword in self.allWords:
            if re.match(pattern, eachword):
                return True
        
        return False