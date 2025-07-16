def multiply(a,b):
    if not isinstance(a,(int,float)) or not isinstance(b,(int,float)):
        raise TypeError("Inputs must be int or float")
    return a * b

