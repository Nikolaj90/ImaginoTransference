def left_lower(left,right):
    # If all checks go through, the check is set to True
    check = True
    
    # For some reason, an empty list counts as an item, that you can run out of, so this needs to be incorporated
    if len(left) == 0:
        return check
    if len(right) == 0:
        check = False
        return check
    
    # Iterate over the smallest amount of values of the list (here the list will not run out of values, for some reason)
    for i in range(min(len(left),len(right))):
        # Only compare the values, if both are integer
        if type(left[i]) == type(right[i]) == int:
            if left[i] > right[i]:
                check = False
                return check
        # If both aren't integers, one will be a list. Both are converted to list and passed back into the function 
        # recursively
        else:
            new_left = left[i]
            new_right = right[i]
            if type(new_left) != list:
                new_left = [new_left]
            if type(new_right) != list:
                new_right = [new_right]
            check = left_lower(new_left,new_right)
    return check 

sum_ = 0
for i, pair in enumerate(list_pairs):
    left = pair[0]
    right = pair[1]
    if left_lower(left,right)&(len(left)<=len(right)) :
        sum_ += i+1