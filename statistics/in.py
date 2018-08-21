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

    answ = ""
    tmp = {}
    tmp[args1[0]["feature"]] = df.query(s)[args1[0]["feature"]]
    for con in connectors1:
        if con == "and":
            tmp[args1[connectors1.index(con) + 1]["feature"]] = df.query(s)[args1[connectors1.index(con) + 1]["feature"]]
        if con == "or":
            if len(tmp) != 0:
                d = pd.DataFrame(tmp)
                for i in range(len(d.index)):
                    for e in d.iloc[i]:
                        answ += str(e) + " "
                    answ = answ[:-1] + ", "
                answ = answ[:-2] + " or "
                tmp = {}
                tmp[args1[connectors1.index(con) + 1]["feature"]] = df.query(s)[args1[connectors1.index(con) + 1]["feature"]]
    if len(tmp) != 0:
        d = pd.DataFrame(tmp)
        for i in range(len(d.index)):
            for e in d.iloc[i]:
                answ += str(e) + " "
            answ = answ[:-1] + ", "
        answ = answ[:-2] + "."
    else:
        answ += "."

    res = current_template["answer"].replace("<>", answ)
    return str(res)


# Can add function for all actions, with params like a "только один повтор"
