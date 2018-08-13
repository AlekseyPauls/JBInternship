import pandas as pd

"""
Templates:
In which ... were ...
"""

"""
args: {"interval": "", "feature": "", "value"}
"""

def calc(current_template, dataset, args1, connectors1, args2, connectors2):
    df = pd.read_csv("datasets/" + dataset)
    s = ""
    for arg in args2:
        s += arg["feature"]
        if arg["interval"] == "":
            s += "=="
        elif arg["interval"] == "less":
            s += "<"
        elif arg["interval"] == "more":
            s += ">"
        s += arg["value"] + " "
        if connectors2[args2.index(arg)] is not None:
            if connectors2[args2.index(arg)] == "and":
                s += "& "
            elif connectors2[args2.index(arg)] == "or":
                s += "| "
    print(s)
    tmp = [df.query(s)[args1[0]["feature"]]]
    for con in connectors1:
        if con is not None:
            tmp.append(df.query(s)[args1[connectors1.index(con) + 1]["feature"]])

    for t in tmp:
        print(str(t))

    res = "ok"
    return str(res)