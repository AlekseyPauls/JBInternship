import csv, importlib, collections, ast
from dateutil import parser


def make_answer(question, dataset):
        current_statistic = {}
        current_template = {}
        intervals = ["more ", "less ", "before ", "after "]
        connectors = [" and ", " or "]
        statistics = get_statistics()
        features, dataset = get_features(dataset)

        question = prepare_question(question)
        for statistic in statistics:
            for template in statistic["templates"]:
                if template["question"] in question and template["delimiter"] in question:
                    current_statistic = statistic
                    current_template = template
        if current_template == {}:
            print("Have no templates")
            exit()
        question = question.replace(current_template["question"], "")
        args = question.split(current_template["delimiter"])

        args1, connectors1 = find_connectors(args[0], connectors)
        args2, connectors2 = find_connectors(args[1], connectors)
        args1 = find_features(args1, features, intervals)
        args2 = find_features(args2, features, intervals)

        print("Template: " + str(current_template) + "\nArgs1: " + str(args1) + "\nConnectors1: " + str(
            connectors1) + "\nArgs2: " + str(args2) + "\nConnectors2: " + str(connectors2))

        stat = importlib.import_module("statistics." + current_statistic["file"])
        calc = getattr(stat, "calc")
        res = calc(current_template, dataset, args1, connectors1, args2, connectors2)

        return res


def get_statistics():
    res = []
    with open('statistics/statistics.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            if row[3] == "file":
                continue
            res.append({"name": row[0], "templates": ast.literal_eval(row[2]), "file": row[3]})
    return res


def get_features(dataset):
    with open('datasets/datasets.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            if row[0] == dataset:
                return ast.literal_eval(row[2]), row[3]


def prepare_question(question):
    question = question.lower()
    if question[-1] == "?":
        question = question[:-1]

    return question


def find_connectors(s, cons):
    for con in cons:
        if con in s:
            t1, t2 = find_connectors(s.split(con)[1], cons)
            return [s.split(con)[0]] + t1, [clean(con)] + t2
    return [s], [None]


def find_features(args, features, intervals):
    a = []
    for arg in args:
        x = {}
        flag = True
        for interval in intervals:
            if interval in arg:
                x["interval"] = clean(interval)
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
                elif get_type(clean(arg)) == feature["type"]:
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
        if clean(arg) == "":
            x["value"] = None
        else:
            x["value"] = clean(arg)
        a.append(x)

    return a


def clean(s):
    if s == "":
        return s
    if s[0] == " ":
        s = s[1:]
    if s[-1] == " ":
        s = s[:-1]
    return s


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

