def diamond(n):
    if n%2==0 or n<0:
        return None
    total=""
    stars=list(range(1,n+1,2))+list(range(n-2,0,-2))
    for each in stars:
        space=(n-each)//2
        total+=" "*space+"*"*each+"\n"
    return total