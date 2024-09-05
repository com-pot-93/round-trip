import os

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def check_metric(func, arg1, arg2, method=""):
    try:
        if method == "":
            val = func(arg1, arg2)
        else:
            val = func(arg1, arg2, method)
    except:
        val = [0,0]
    return val

