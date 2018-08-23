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
    # Open dataset from folder 'datasets' as Dataframe
    df = pd.read_csv("datasets/" + dataset)

    # Single-argument (only main arguments) case
    if args2 is None:
        answ = ""
        answ += str(df[args1[0]["feature"]].var()) + ", "
        for con in connectors1:
            if con == "and":
                answ += str(df[args1[connectors1.index(con) + 1]["feature"]].var()) + ", "
            if con == "or":
                answ = answ[:-2] + " or " + str(
                    df[args1[connectors1.index(con) + 1]["feature"]].var()) + ", "
        answ = answ[:-2] + "."

        # Return answer like a string
        res = current_template["answer"].replace("<>", answ)
        return str(res)

    # Check arguments
    none_counter = 0
    for arg in args2:
        if arg is None:
            none_counter += 1
    if none_counter != 0:
        return "Bad question: can`t find value for some dependent feature"

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
    answ += str(df.query(s)[args1[0]["feature"]].var()) + ", "
    for con in connectors1:
        if con == "and":
            answ += str(df.query(s)[args1[connectors1.index(con) + 1]["feature"]].var()) + ", "
        if con == "or":
            answ = answ[:-2] + " or " + str(df.query(s)[args1[connectors1.index(con) + 1]["feature"]].var()) + ", "
    answ = answ[:-2] + "."

    # Return answer like a string
    res = current_template["answer"].replace("<>", answ)
    return str(res)
