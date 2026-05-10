def exactNumber(word):
    for char in word:
        if char.isdigit():
            return int(char)
    return 0
​
def order(sentence):
    if not sentence:
        return ""
    
    words = sentence.split()
    resortedSentence = sorted(words, key=exactNumber)
    
    return " ".join(resortedSentence)