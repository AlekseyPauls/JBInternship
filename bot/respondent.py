import importlib, collections, re, csv, traceback
from dateutil import parser
import bot.service as serv
from bot import log

intervals = ["more ", "less ", "before ", "after "]
connectors = ["and", "or"]


""" Types: string, datetime, integer, float, money  """


def make_answer(question, dataset):
    try:
        input_question = question

        if question == "":
            log.info("answer", extra={"question": input_question,
                                      "dataset": dataset,
                                      "answerType": "error",
                                      "answer": "Void question"
                                      })
            return "Void question"

        statistics = serv.get_statistics()

        if "-d=" in question:
            dataset = question[question.find("-d=") + 3:]
            question = question[0:question.find("-d=")]

        question = prepare_question(question)

        if dataset == "":
            ds = serv.find_dataset(question)
            if ds["type"] == "one":
                dataset = ds["dataset"]
            elif ds["type"] == "none":
                log.info("answer", extra={"question": input_question,
                                          "dataset": dataset,
                                          "answerType": "error",
                                          "answer": "No suitable dataset"
                                          })
                return "No suitable dataset. Please, remake your question by the rules (use \"/rules\" command)"
            else:
                s = "There are several suitable datasets: "
                for name in ds["dataset"]:
                    dst = serv.get_dataset(name)
                    s += dst["name"] + " (" + dst["description"] + "), "
                s = s[:-2]
                s += ". \nSpecify the one you need with the \"-d\" key at the end of the question (for example: \"What kind of animal is a cat? -d=Animals\")."
                log.info("answer", extra={"question": input_question,
                                          "dataset": dataset,
                                          "answerType": "error",
                                          "answer": "Several suitable datasets"
                                          })
                return s

        ds = serv.get_dataset(dataset)
        if not ds:
            log.info("answer", extra={"question": input_question,
                                      "dataset": dataset,
                                      "answerType": "error",
                                      "answer": "No dataset in database"
                                      })
            return "Wrong dataset. There is no dataset with this name."
        features, file = ds['features'], ds['file']

        current_statistic, current_template, current_delimiter = find_template(statistics, question)

        if current_template == {}:
            log.info("answer", extra={"question": input_question,
                                      "dataset": dataset,
                                      "answerType": "error",
                                      "answer": "No suitable dataset"
                                      })
            return "Have no suitable template (can't understand your question)"
        question = question.replace(current_template["question"].lower(), "")

        if (current_delimiter == ""):  # Single-argument template
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

        stat = importlib.import_module("statistics." + current_statistic["file"][:-3])
        calc = getattr(stat, "calc")
        res = calc(current_template, file, args1, connectors1, args2, connectors2)

        log.info("answer", extra={"question": input_question,
                                  "dataset": dataset,
                                  "answerType": "correct",
                                  "answer": res,
                                  "statistic": current_statistic,
                                  "delimiter": current_delimiter,
                                  "template": current_template,
                                  "args1": args1,
                                  "args2": args2,
                                  "connectors1": connectors1,
                                  "connectors2": connectors2
                                  })
        return res
    except Exception as e:
        log.info("answer", extra={"question": question,
                                  "dataset": dataset,
                                  "answerType": "exception",
                                  "answer": traceback.format_exc(),
                                  })


def prepare_question(question):
    question = question.lower()
    if question[-1] == "?":
        question = question[:-1] + " "
    return question


def find_template(statistics, question):
    for statistic in statistics:
        print(statistic["name"])
        for template in statistic["templates"]:
            for q in serv.variants(template["question"]):
                for delimiter in template["delimiters"]:
                    for d in serv.variants(delimiter):
                        if q.lower() in question and d.lower() in question:
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


def get_arg_by_type(arg, type):
    if serv.clean(arg) == "":
        return None
    elif type == "datetime":
        return get_datetime(serv.clean(arg))
    elif type == "currency":
        return get_currency(arg)
    elif type == "percent":
        return get_percent(arg)
    elif type == "float":
        return get_float(arg)
    elif type == "integer":
        return get_integer(arg)
    elif type == "string":
        return "\"" + serv.clean(arg) + "\""
    else:
        return None


def get_type(s):
    if get_datetime(s):
        return "datetime"
    elif get_currency(s):
        return "currency"
    elif get_percent(s):
        return "percent"
    elif get_float(s):
        return "float"
    elif get_integer(s):
        return "integer"
    else:
        return "string"


# TO DO: make it better
def get_datetime(s):
    try:
        t = parser.parse(s)
        return t
    except ValueError:
        return None


def get_currency(s):
    return re.search(r'([$¢£¤¥₠₣₤₪€₯₰₱₸₹₽﹩＄￠￥￡￦]\s*[0-9])|([0-9]\s*[$¢£¤¥₠₣₤₪€₯₰₱₸₹₽﹩＄￠￥￡￦])', s)


def get_percent(s):
    return re.search(r'[0-9]+\s*%', s)


def get_float(s):
    return re.search(r'([0-9]*[.,][0-9]+)|([0-9]+[.,][0-9]*)', s)


def get_integer(s):
    return re.search(r'[0-9]+', s)
