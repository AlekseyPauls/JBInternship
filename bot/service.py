import os, json, csv, ast
from bot.models import Datasets, Statistics
from bot import db


db.create_all()
# db.session.add(Statistics("Mean", "Mean", "[{'question': 'what is mean ', 'delimiters': [' in ']}]", "mean.py"))
# db.session.add(Statistics("In", "In", "[{'question': 'in which ', 'delimiters': [' were ', ' was '], 'answer': 'In <>.'}]", "in.py"))
# db.session.commit()


def save_dataset(name, descriprion, features, file):
    dataset = Datasets.query.filter_by(name=name).first()
    if dataset:
        dataset.set_description(descriprion)
        dataset.set_features(features)
        dataset.set_file(file[0:-4])
        db.session.commit()
    else:
        db.session.add(Datasets(name, descriprion, features, file))
        db.session.commit()


def save_statistic(name, descriprion, templates, file):
    statistic = Statistics.query.filter_by(name=name).first()
    if statistic:
        statistic.set_description(descriprion)
        statistic.set_templates(templates)
        statistic.set_file(file[0:-3])
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
