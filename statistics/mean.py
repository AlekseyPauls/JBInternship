import pandas as pd

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def calc(dataset, columns, values):
    df = pd.read_csv("datasets/" + dataset)
    if (values[1] in months):
        values[1] = months.index(values[1]) + 1
    mean = df.query(str(columns[1]) + " == " + str(values[1]))[columns[0]].mean()
    return "The mean number of " + columns[0] + " in " + columns[1] + " " + str(values[1]) + " is " + str(mean)
