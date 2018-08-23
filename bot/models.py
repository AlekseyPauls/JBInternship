from bot import db
import ast


class Datasets(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.String(300))
    features = db.Column(db.JSON)
    file = db.Column(db.String(100))

    def __init__(self, name, description, features, file):
        self.name = name
        self.description = description
        self.features = features
        self.file = file

    def __repr__(self):
        return self.name + ", " + self.description + ", " + self.features + ", " + self.file

    def set_description(self, description):
        self.description = description

    def set_features(self, features):
        self.features = features

    def set_file(self, file):
        self.file = file

    def get_name(self):
        return self.name

    def get_features(self):
        return self.features

    def get_description(self):
        return self.description

    def get_info(self):
        features = self.features
        s = ""
        for feature in features:
            syns = "("
            for syn in feature["synonyms"]:
                if syn != "":
                    syns += syn + ", "
            if syns != "(":
                syns = syns[:-2] + ") "
            else:
                syns = ""
            s += "" + feature["name"] + " " + syns + "- " + feature["type"] + ", "
        s = s[:-2]
        print(s)
        return [self.name, self.description, s]

    def get_values(self):
        return {"name": self.name, "description": self.description, "features": self.features, "file": self.file}


class Statistics(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.String(300))
    templates = db.Column(db.JSON)
    file = db.Column(db.String(100))

    def __init__(self, name, description, templates, file):
        self.name = name
        self.description = description
        self.templates = templates
        self.file = file

    def __repr__(self):
        return self.name + ", " + self.description + ", " + self.templates + ", " + self.file

    def set_description(self, description):
        self.description = description

    def set_templates(self, templates):
        self.templates = templates

    def set_file(self, file):
        self.file = file

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_info(self):
        templates = self.templates
        s = ""
        for template in templates:
            s += template["question"] + "..."
            dels = ""
            for delimiter in template["delimiters"]:
                dels += delimiter + ", "
            dels = dels[:-2]
            if template["delimiters"] != ['']:
                s += " [" + dels + "] ..."
            s += "?, "
        s = s[:-2]
        return [self.name, self.description, s]

    def get_values(self):
        return {"name": self.name, "description": self.description, "templates": self.templates, "file": self.file}


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500))
    datetime = db.Column(db.DateTime)

    def __init__(self, message, datetime):
        self.message = message
        self.datetime = datetime

    def __repr__(self):
        return self.id + ", " + self.message + ", " + self.datetime
