import csv, importlib, collections, ast, re
from dateutil import parser
import bot.service as serv

intervals = ["more ", "less ", "before ", "after "]
connectors = ["and", "or"]


def make_answer(question, dataset):
    statistics = serv.get_statistics()

    if "-d=" in question:
        dataset = question[question.find("-d=") + 3:]
        question = question[0:question.find("-d=")]

    question = prepare_question(question)

    print(dataset + ", " + question)

    if dataset == "":
        ds = serv.find_dataset(question)
        if ds["type"] == "one":
            dataset = ds["dataset"]
        elif ds["type"] == "none":
            return "No suitable dataset. Please, remake your question by the rules (use \"/rules\" command)"
        else:
            s = "There are several suitable datasets: "
            for name in ds["dataset"]:
                dst = serv.get_dataset(name)
                s += dst["name"] + " (" + dst["description"] + "), "
            s = s[:-2]
            s += ". \nSpecify the one you need with the \"-d\" key at the end of the question (for example: \"What kind of animal is a cat? -d=Animals\")."
            return s

    ds = serv.get_dataset(dataset)
    if not ds:
        return "Wrong dataset. There is no dataset with this name."
    features, file = ds['features'], ds['file']

    current_statistic, current_template, current_delimiter = find_template(statistics, question)

    if current_template == {}:
        return "Have no suitable template (can't understand your question)"
    question = question.replace(current_template["question"].lower(), "")

    if (current_delimiter == ""): # Single-argument template
        args1, connectors1 = find_connectors(question)
        args1 = find_features(args1, features)
        args2 = None
        connectors2 = None
    else:
        args = question.split(current_delimiter)
        args1, connectors1 = find_connectors(args[0])
        args2, connectors2 = find_connectors(args[1])
        args1 = find_features(args1, features)
        args2 = find_features(args2, features)
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
                    if template["question"].lower() in question and variant.lower() in question:
                        return statistic, template, delimiter
    return {}, {}, ""


def find_connectors(s):
    args = []
    cons = []

    flag = True

    while flag:
        flag = False
        indices = {}
        for con in connectors:
            for var in serv.variants(con):
                if var in s:
                    indices[var] = s.find(var)
                    break
        if len(indices) != 0:
            sorted_indices = collections.OrderedDict(reversed(sorted(indices.items(), key=lambda t: t[1])))
            l = list(sorted_indices.keys())
            for con in connectors:
                if con in l[0]:
                    cons.append(con)
                    break
            args.append(s[:s.find(l[0])])
            s = s[s.find(l[0]) + len(l[0]):]
            flag = True
    args.append(s)
    cons.append(None)

    return args, cons


def find_features(args, features):
    a = []
    for arg in args:
        x = {}
        x["interval"] = ""
        for interval in intervals:
            if interval in arg:
                x["interval"] = serv.clean(interval)
                arg = arg.replace(interval, "")
                break
        ft, val = get_feature_by_name(arg, features)
        if ft is None:
            ft, val = get_feature_by_values(arg, features)
        if ft is None:
            ft, val = get_feature_by_type(arg, features)
        x["feature"], x["value"] = ft, val
        a.append(x)

    return a


def get_feature_by_name(arg, features):
    for feature in features:
        if feature["name"] in arg:
            val = get_arg_by_values(arg.replace(feature["name"], ""), feature["values"])
            val = get_arg_by_type(val, feature["type"])
            return feature["name"], val
        for syn in feature["synonyms"]:
            if syn != "" and syn in arg:
                val = get_arg_by_values(arg.replace(syn, ""), feature["values"])
                val = get_arg_by_type(val, feature["type"])
                return feature["name"], val
    return None, None


def get_feature_by_values(arg, features):
    for feature in features:
        for val in feature["values"]:
            if val != "" and val in arg:
                val = get_arg_by_type(val, feature["type"])
                return feature["name"], val
    return None, None


def get_feature_by_type(arg, features):
    f = {}
    counter = 0
    for feature in features:
        if get_type(serv.clean(arg)) == feature["type"]:
            f = feature
            counter += 1
    if counter > 1:
        return "More then one match"
    if counter == 1:
        return f["name"], get_arg_by_type(arg, f["type"])
    return None, None


def get_arg_by_values(arg, values):
    for value in values:
        if value in arg:
            return value
    return arg


# To do: MAKE IT
def get_arg_by_type(arg, type):
    if serv.clean(arg) == "":
        return None
    if type == "number":
        r = re.search(r'\d+', arg)
        if r is not None:
            return int(re.search(r'\d+', arg).group())
    if type == "special":
        return "\"" + serv.clean(arg) + "\""
    else:
        return None


# Type 'special' doesn`t participate in the type definition, because it can be something unexpected
def get_type(s):
    if is_number(s):
        return "number"
    if is_date(s):
        return "date"


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

