def snail(snail_map):
    res=[]
    top=0
    left=0
    right=len(snail_map[0])-1
    bottom=len(snail_map)-1
    while top<=bottom and left<=right:
        for each in range(left,right+1):
            res.append(snail_map[top][each])
            
        top+=1
        for each in range(top,bottom+1):
            res.append(snail_map[each][right])
        if not (top<=bottom and left<=right):
            break
        right-=1
        for each in range(right,left-1,-1):
            res.append(snail_map[bottom][each])
        bottom-=1
        for each in range(bottom,top-1,-1):
            res.append(snail_map[each][left])
        left+=1
        
    return res
        