def absolute_value_extra_return(x):
    if x < 0:
        return -x
    else:
        return x
    
    return 'This is dead code.'
# dead code" 是指那些永遠不會被執行的程式碼。這通常是由於邏輯錯誤或多餘的程式碼所導致的。
# 一般來說，dead code 應該被移除，因為它會使程式碼變得混亂且難以維護。
print(absolute_value_extra_return(-5))