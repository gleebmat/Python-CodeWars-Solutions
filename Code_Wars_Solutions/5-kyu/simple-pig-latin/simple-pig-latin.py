def pig_it(text):
    text=text.split()
    newText=[]
    for word in text:
            if word.isalpha():
                firstLetter=word[0]
                newText.append(word[1:]+word[0]+"ay") 
            else:
                newText.append(""+word)
    return " ".join(newText)