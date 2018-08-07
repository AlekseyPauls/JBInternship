import csv, importlib, collections, ast

class Respondent:

    def answer(self, question):
        with open("datasets/datasets.csv") as datasets_csv, \
            open("statistics/statistics.csv") as statistics_csv, \
            open("feedback/feedback.csv") as feedback_csv:

            p1, delta1 = self.probability(self, datasets_csv, question)
            p2, delta2 = self.probability(self, statistics_csv, question)
            print(p1, delta1, p2, delta2)

            if delta1 < 0.2 or delta2 < 0.2:
                return "Cant understand"

            columns, values = self.find_column_names(self, datasets_csv, question, ast.literal_eval(list(p1.keys())[0]))

            stat = importlib.import_module("statistics." + ast.literal_eval(list(p2.keys())[0])[3])
            calc = getattr(stat, "calc")
            res = calc(ast.literal_eval(list(p1.keys())[0])[3], columns, values)

            return res


    def probability(self, csv_file, question):
        ds = csv.reader(csv_file, delimiter=',', quotechar='"')
        prob = {i: 0 for i in range(3)}
        for row in ds:
            counter = 0
            for word in question.split(' '):
                if word in row[2]:
                    counter += 1
            prob = self.replacement_insert(self, prob, str(row), counter)
        n = sum(prob[i] for i in prob)
        if (n != 0):
            for i in prob:
                prob[i] /= n
        prob = collections.OrderedDict(sorted(prob.items(), key=lambda t: t[1], reverse=True))
        delta = prob[list(prob.keys())[0]] - prob[list(prob.keys())[1]]
        return prob, delta


    def find_column_names(self, csv_file, question, dataset):
        cols = []
        vals = []

        synonyms = ast.literal_eval(dataset[4])
        for word in question.split(" "):
            for key in synonyms.keys():
                if word in synonyms[key]:
                    cols.append(key)
                    vals.append(word)
        return cols, vals


    def replacement_insert(self, dict, key, value):
        dict[key] = value
        min = key
        for i in dict:
            if (dict[i] < dict[min]):
                min = i
        del dict[min]
        return dict
