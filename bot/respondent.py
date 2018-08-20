import csv, importlib, collections, ast
from dateutil import parser
import bot.service as serv

intervals = ["more ", "less ", "before ", "after "]
connectors = [" and ", " or "]


def make_answer(question, dataset):
    statistics = serv.get_statistics()

    dataset = ""

    if "-d=" in question:
        dataset = question[question.find("-d=") + 3:]
        question = question[0:question.find("-d=")]

    question = prepare_question(question)

    print(dataset + "," + question)

    if dataset == "":
        ds = serv.find_dataset(question)
        if ds["type"] == "one":
            dataset = ds["dataset"]
        elif ds["type"] == "none":
            return "No suitable dataset"
        else:
            s = "There were several suitable datasets: "
            for name in ds["dataset"]:
                dst = serv.get_dataset(name)
                s += dst["name"] + " (" + dst["description"] + "), "
            s = s[:-2]
            s += ". \nSpecify the one you need with the \"-d\" key at the end of the question (for example: \"What kind of animal is a cat? -d=Animals\")."
            return s
    print(dataset)
    ds = serv.get_dataset(dataset)
    if not ds:
        return "Wrong dataset"
    features, file = ds['features'], ds['file']

    current_statistic, current_template, current_delimiter = find_template(statistics, question)

    if current_template == {}:
        return "Have no suitable template (can't understand your question)"
    question = question.replace(current_template["question"], "")
    args = question.split(current_delimiter)

    args1, connectors1 = find_connectors(args[0], connectors)
    args2, connectors2 = find_connectors(args[1], connectors)
    args1 = find_features(args1, features, intervals)
    args2 = find_features(args2, features, intervals)

    print("Template: " + str(current_template) + "\nArgs1: " + str(args1) + "\nConnectors1: " + str(
        connectors1) + "\nArgs2: " + str(args2) + "\nConnectors2: " + str(connectors2))

    stat = importlib.import_module("statistics." + current_statistic["file"][:-3])
    calc = getattr(stat, "calc")
    res = calc(current_template, file, args1, connectors1, args2, connectors2)

    return res


def prepare_question(question):
    question = question.lower()
    if question[-1] == "?":
        question = question[:-1] + " "
    return question


def find_template(statistics, question):
    for statistic in statistics:
        for template in statistic["templates"]:
            for delimiter in template["delimiters"]:
                for variant in serv.variants(delimiter):
                    if template["question"] in question and variant in question:
                        return statistic, template, delimiter
    return {}, {}, ""


def find_connectors(s, cons):
    for con in cons:
        if con in s:
            t1, t2 = find_connectors(s.split(con)[1], cons)
            return [s.split(con)[0]] + t1, [serv.clean(con)] + t2
    return [s], [None]


def find_features(args, features, intervals):
    a = []
    for arg in args:
        x = {}
        flag = True
        for interval in intervals:
            if interval in arg:
                x["interval"] = serv.clean(interval)
                arg = arg.replace(interval, "")
                flag = False
                break
        if flag:
            x['interval'] = ""
        f = []
        counter = 0
        flag = True
        for feature in features:
            if flag:
                if feature["name"] in arg:
                    x["feature"] = feature["name"]
                    arg = arg.replace(feature["name"], "")
                    break
                elif feature["type"] == "special":
                    for val in feature["values"]:
                        if val in arg:
                            x["feature"] = feature["name"]
                            x["value"] = val
                            flag = False
                            break
                elif get_type(serv.clean(arg)) == feature["type"]:
                    counter += 1
                    f.append(feature)
            else:
                break
        if not flag:
            a.append(x)
            continue
        if counter == 1 and "feature" not in x.keys():
            x["feature"] = f[0]["name"]
        elif counter > 1:
            print("Too many choices")
        elif counter == 0 and "feature" not in x.keys():
            print("Can not find suitable feature")
        if serv.clean(arg) == "":
            x["value"] = None
        else:
            x["value"] = serv.clean(arg)
        a.append(x)

    return a


def get_type(s):
    if is_number(s):
        return "number"
    if is_date(s):
        return "date"
    else:
        return "special"


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_date(s):
    try:
        parser.parse(s)
        return True
    except ValueError:
        return False

