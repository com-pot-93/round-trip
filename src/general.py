import os

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def check_metric(func, arg1, arg2, method="", similarity_threshold=""):
    try:
        if method == "" and similarity_threshold == "":
            val = func(arg1, arg2)
        elif method != "" and similarity_threshold == "":
            val = func(arg1, arg2, method)
        elif method == "" and similarity_threshold != "":
            val = func(arg1, arg2, similarity_threshold = similarity_threshold)
        else:
            val = func(arg1, arg2, method, similarity_threshold)
    except:
        val = [0,0]
    return val

