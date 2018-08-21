import pandas as pd

"""
Input:

current_template - Dict with keys 'question', 'answer' and 'delimiters'
dataset - name of csv file with dataset
args1 - list of dicts with keys 'feature', 'interval' and 'value'. This is a main part of question
connectors1 - list of string. Strings may be 'and' or 'or'. Last value always should be a 'None'
args1 - list of dicts with keys 'feature', 'interval' and 'value'. This is a main part of question
connectors1 - list of string. Strings may be 'and' or 'or'. Last value always should be a 'None'

Output:

String of the form in current_template['answer']. Values from dataset should replace '<>' in answer template. Connectors
also should be processed and take part in answer
"""


def calc(current_template, dataset, args1, connectors1, args2, connectors2):
    try:
        # Open dataset from folder 'datasets' as Dataframe
        df = pd.read_csv("datasets/" + dataset)

        # Make query request for Dataframe
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

        # Generate answer in dependence on connectors
        answ = ""
        tmp = {}
        tmp[args1[0]["feature"]] = df.query(s)[args1[0]["feature"]]
        for con in connectors1:
            if con == "and":
                tmp[args1[connectors1.index(con) + 1]["feature"]] = df.query(s)[
                    args1[connectors1.index(con) + 1]["feature"]]
            if con == "or":
                if len(tmp) != 0:
                    d = pd.DataFrame(tmp)
                    for i in range(len(d.index)):
                        for e in d.iloc[i]:
                            answ += str(e) + " "
                        answ = answ[:-1] + ", "
                    answ = answ[:-2] + " or "
                    tmp = {}
                    tmp[args1[connectors1.index(con) + 1]["feature"]] = df.query(s)[
                        args1[connectors1.index(con) + 1]["feature"]]
        if len(tmp) != 0:
            d = pd.DataFrame(tmp)
            for i in range(len(d.index)):
                for e in d.iloc[i]:
                    answ += str(e) + " "
                answ = answ[:-1] + ", "
            answ = answ[:-2] + "."
        else:
            answ += "."

        # Return answer like a string
        res = current_template["answer"].replace("<>", answ)
        return str(res)
    except Exception as e:
        return "Something wrong at question processing. \n" + "Template: " + str(current_template) + \
               "\nArgs1: " + str(args1) + "\nConnectors1: " + str(connectors1) + \
               "\nArgs2: " + str(args2) + "\nConnectors2: " + str(connectors2)
