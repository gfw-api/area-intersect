import re

def getlist(k, args):
    # find multiple keys with same name in MultiDict and return their values as list
    # replaces the request.args.getlist function
    # which is somehow not working for me

    l = list()
    for key in args.keys():
        a = re.search('{}(?=\[[0-9]\])'.format(k), key)

        if k == key or (a is not None and a.group() == k):
            l.append(args[key])
    return l
