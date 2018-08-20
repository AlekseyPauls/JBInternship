import os, json, csv, ast, collections
from bot.models import Datasets, Statistics
from bot import db


# db.session.add(Statistics("Mean", "Mean", "[{'question': 'what is mean ', 'delimiters': [' in ']}]", "mean.py"))
# db.session.add(Statistics("In", "In", "[{'question': 'in which ', 'delimiters': [' were ', ' was '], 'answer': 'In <>.'}]", "in.py"))
# db.session.commit()


def find_dataset(question):
    ds = {}
    for dataset in Datasets.query.all():
        ds_name = dataset.get_name()
        ds[ds_name] = 0
        for feature in dataset.get_features():
            for name in variants(feature["name"]):
                if name in question:
                    ds[ds_name] += 1
                    break
        if ds[ds_name] == 0:
            del ds[ds_name]
    sorted_ds = collections.OrderedDict(reversed(sorted(ds.items(), key=lambda t: t[1])))
    print(sorted_ds)
    l = list(sorted_ds.keys())
    if len(l) >= 3:
        if (ds[l[0]] - (ds[l[0]] + ds[l[1]] + ds[l[2]]) / 3) <= 1:
            return {"type": "choose", "dataset": [l[0], l[1], l[2]]}
        if (ds[l[0]] - ds[l[1]]) <= 1:
            return {"type": "choose", "dataset": [l[0], l[1]]}
        else:
            return {"type": "one", "dataset": l[0]}
    elif len(l) == 2:
        if (ds[l[0]] - ds[l[1]]) <= 1:
            return {"type": "choose", "dataset": [l[0], l[1]]}
        else:
            return {"type": "one", "dataset": l[0]}
    elif len(l) == 1:
        return {"type": "one", "dataset": l[0]}
    else:
        return {"type": "none"}


def save_dataset(name, descriprion, features, file):
    dataset = Datasets.query.filter_by(name=name).first()
    if dataset:
        dataset.set_description(descriprion)
        dataset.set_features(features)
        dataset.set_file(file)
        db.session.commit()
    else:
        db.session.add(Datasets(name, descriprion, features, file))
        db.session.commit()


def save_statistic(name, descriprion, templates, file):
    statistic = Statistics.query.filter_by(name=name).first()
    if statistic:
        statistic.set_description(descriprion)
        statistic.set_templates(templates)
        statistic.set_file(file)
        db.session.commit()
    else:
        db.session.add(Statistics(name, descriprion, templates, file))
        db.session.commit()


def delete_dataset(name):
    dataset = Datasets.query.filter_by(name=name).first()
    if dataset:
        db.session.delete(dataset)
        db.session.commit()


def delete_statistic(name):
    statistic = Statistics.query.filter_by(name=name).first()
    if statistic:
        db.session.delete(statistic)
        db.session.commit()


def get_datasets_info():
    res = []
    for dataset in Datasets.query.all():
        res.append(dataset.get_info())
    return res


def get_dataset(name):
    dataset = Datasets.query.filter_by(name=name).first()
    if dataset:
        return dataset.get_values()
    return None


def get_dataset_names():
    res = []
    for dataset in Datasets.query.all():
        res.append(dataset.get_name())
    return res


def get_statistics_info():
    res = []
    for statistic in Statistics.query.all():
        res.append(statistic.get_info())
    return res


def get_statistic(name):
    statistic = Statistics.query.filter_by(name=name).first()
    if statistic:
        return statistic.get_values()
    return None


def get_statistics():
    res = []
    for statistic in Statistics.query.all():
        res.append(statistic.get_values())
    return res


def get_statistic_names():
    res = []
    for statistic in Statistics.query.all():
        res.append(statistic.get_name())
    return res


def variants(word):
    res = []
    res.append(" " + word + " ")
    res.append(" " + word + ",")
    res.append("(" + word + " ")
    res.append(" " + word + ")")
    res.append("(" + word + ")")
    return res


def clean(s):
    if s == "":
        return s
    if s[0] == " ":
        s = s[1:]
    if s[-1] == " ":
        s = s[:-1]
    return s
