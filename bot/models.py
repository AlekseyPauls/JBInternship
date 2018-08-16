from bot import db
import ast


class Datasets(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.String(200))
    features = db.Column(db.JSON)
    file = db.Column(db.String(100))

    def __init__(self, name, description, features, file):
        self.name = name
        self.description = description
        self.features = features
        self.file = file

    def __repr__(self):
        return self.name + " ; " + self.description + " ; " + self.features + " ; " + self.file

    def get_name(self):
        return self.name

    def get_info(self):
        features = ast.literal_eval(self.features)
        s = ""
        for feature in features:
            s += "" + feature["name"] + " (" + feature["type"] + "), "
        s = s[:-2]
        return [self.name, self.description, s]

    def get_values(self):
        return {"name": self.name, "description": self.description, "features": ast.literal_eval(self.features), "file": self.file}


class Statistics(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.String(200))
    templates = db.Column(db.JSON)
    file = db.Column(db.String(100))

    def __init__(self, name, description, templates, file):
        self.name = name
        self.description = description
        self.templates = templates
        self.file = file

    def __repr__(self):
        return self.name + " ; " + self.description + " ; " + self.templates + " ; " + self.file

    def get_name(self):
        return self.name

    def get_info(self):
        templates = ast.literal_eval(self.templates)
        s = ""
        for template in templates:
            s += template["question"] + "..."
            dels = ""
            for delimiter in template["delimiters"]:
                dels += delimiter + ", "
            dels = dels[:-2]
            if template["delimiters"] is not None:
                s += " [" + dels + "] ..."
            s += "?  "
        return [self.name, self.description, s]

    def get_values(self):
        return {"name": self.name, "description": self.description, "templates": ast.literal_eval(self.templates), "file": self.file}
