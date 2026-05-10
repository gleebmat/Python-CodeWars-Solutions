​
def duplicate_count(text):
    
    text=text.lower()
    uniqueText=set(text)
    amount=0
    for char in uniqueText:
        if text.count(char)>1:
            amount+=1
            
    return amount