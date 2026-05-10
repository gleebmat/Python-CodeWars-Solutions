from collections import deque
def get_number_of_reachable_fields(grid, rows, columns, start_row, start_column):
    visited={(start_row,start_column)}
    queue=deque([(start_row,start_column)])
    reachable_cols=set()
    
    while queue:
        row, column=queue.popleft()
        if row==rows-1:
            reachable_cols.add(column)
        for dr,dc in [(1,0),(0,1),(0,-1)]:
            newRow=row+dr
            newColumn=column+dc
            if 0<=newRow<=rows-1 and 0<=newColumn<=columns-1:
                if grid[newRow][newColumn]!=0:
                    if (newRow,newColumn) not in visited:
                        visited.add((newRow,newColumn))
                        queue.append((newRow,newColumn))
    return len(reachable_cols)
        