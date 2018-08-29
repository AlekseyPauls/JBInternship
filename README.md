# JBInternship

## About project

This project is a web-application and Slack bot. 
The purpose of this app is a providing a convenient interface for working with data - 
users ask a question in natural language and receive a response in the form of data from the database. 
Question - it is a traditional question or command. Possible questions can be viewed either with the help of a 
special bot command, or on the appropriate tab in the application. 
Similarly, you can find out about available datasets. Also app provided interface to add new datasets and 
questions (call them 'statistics'). 

## Usage example

We suggest that we have a dataset with information on the number of users per month in several years. 
Now we ask a question: 

"How many users were in the april?" (or simply "Users in april") 

And get the answer: "24352, 53241, 24234"

What did you learn? The number of users in the month of April in different years. 
To clarify the information, add one more condition: 

"How many users were in the april and 2017?" 

It looks strange, does not it? The reason is that in our dataset the month and year are different entities 
and we must use the connector "and".

Now the answer is: "53424"

Done! But we want to know the average attendance for 2017. Let's do it:

"What is mean of users in 2017?"

The answer is: "24564,4354352"

Well, but it would be great to know in which months of 2016 there were more than 50000 users. Let's do:

"In which months were 2017 year and more then 50000 users?"

The answer is: "In april, december, november, may, june."

There are other questions (we call them 'statistics' - because we perform some sort of data actions) 
and they are constantly added. If you do not receive an answer to your question, 
then put a feedback and this will be fixed.

## Web-application

The latest version is available under the link: https://apaulstest.herokuapp.com/

Warning! The answer to the question may be delayed for a few seconds due to waiting to connect to the server. 
Also, it is strongly recommended not to load large datasets - server capacity is limited.

### Pages and functionality

#### Start page (/)

On this page you can ask, get answer and leave a feedback. 
To ask the question, you first have to select the 'dataset' - data base from which the information will be provided.
Feedback is what you want to tell the developer. 
It might be a suggestion to add new statistics, datasets, or fix any errors. 
Work with feedback is available to authorized users in the "Development" page.

#### Info (/info)

This page does not require you to do anything - just look at the information provided.
The information about the datasets is presented in the form of a name, description and features of the dataset - 
columns in the database (the feature is described by a name of feature, 
list of synonyms in brackets and a type through dashes).
The information about the statistics is presented in the form of a name, description and templates of the statistic - 
variants of questions and answers (the template is described by a question and 
list of delimiters of arguments in square brackets, '...' show the place to argument).

#### Development (/development)

(login/password to "Develop" tab - admin/admin)

This page is for adding, editing and deleting datasets and statistics and working with feedback, 
for a specific action, go to the tab. To add a dataset, you must fill in the field name, description, 
select the database file (in '.csv' format) and fill in the feature list (or import it automatically from the 
database file and edit it manually). Adding new statistics is similar, but you need to select a file 
in the '.py' format, and the import of the templates is made from a separate file in '.csv' format containing 
three columns: a question, a list of delimiters and the answer.

## Bot

"This will be link to a bot-app page"

You can ask the bot about anything. He will try to recognize the data and give you an answer. If in the process 
of recognition the bot finds several suitable datasets, it will ask you to clarify the question with the help of 
the key "-d =".

Now look at the available commands:

#### /info

You will get a message with lists of the datasets and statistics with names and descriptions. 

#### /info_dataset dataset_name

You will get a message with information about dataset features

#### /info_statistic statistic_name

You will get a message with information about statistic templates

#### /rules

You will get a message with information about question creating for better recognition of your intentions.

#### /fb your text

With this command you can leave feedback.

## Rules

Bot tries to recognize the questions in natural language, but we can help him in this by formulating clear questions. 
Here are a few simple rules:

1. Formulate simple questions consisting of a question, the main argument (what information is being searched for), 
a delimiter (often a preposition), and a dependent argument (a condition, usually a specific value or an 
interval of a feature)
2. To enter multiple arguments of the first or second type, separate them explicitly with the words "and" and "or" 
(don`t use commas)
3. Don`t use hard dependencies when one feature depends on another in one argument 
(for example, "Mean of users after 2017 year"). You can achieve the same effect by slightly changing the question 
("Mean of users in year after 2017") - now dependence of the features is explicit.
3. If you want to add an interval ("more", "less") for a group of arguments, make it for each individual entity
4. Do not use unnecessary words, like adjectives. If you did not receive an answer, try to delete the unnecessary 
words and articles
5. If the bot replied that it did not find a suitable template, examine the list of statistics and their templates 
and try asking a question again
6. If there was a problem with the recognition of the dataset, specify your arguments in the name of the feature 
("4535 users", "montn april")
7. If nothing helped, then leave a feedback and the problem will be solved

## Development

### Dataset

To edit the dataset, select it, change it, and click the save button. To create new ones, select the 
green dataset 'New' and enter the information.

#### Add the feature

Example:

Name: year; Synonyms: "Year", "YEAR"; Type: integer; Values: "2017", "2016", "2018"

'Name' is a name of column in data base, 'Synonyms' is a variants of writings this name in questions 
(it is important to put different synonyms in quotes and separate from a comma), 'Type' is a kind of data in column, 
'Values' is a values of this feature in data base (also in quotes and comma separated) - if the values are special, 
or they are few and they do not coincide with the values of other features, you can write them out to improve 
the search.

#### Import features

When you select a file with a database, you can automatically extract features, their types and values, 
and then edit them manually. To do this, click the import button in the new feature row.

#### Prepare data

To download data, it need to be prepared. It is enough to take into account several recommendations:

1. Give the date in the form "DD.MM.YYYY" or "DD/MM/YYYY"
2. If in your data, for example, month and year are different features then they are different entities and can`t be recognized as 
one entity (date)

### Statistic

#### Add the template

Question: "What is variance of"; Delimiters: "in", "at"; Answer: "The variance is <>"

'Question' is a trigger-string to choose this statistic (may be void only in "In" statistic, quotes and commas 
are required), 'delimiters' is a list of strings which separate the arguments in the question (may be void if 
statistic supports single-argument semantic), 'Answer' is a string of answer in which will be inserted data 
instead of "<>" symbols (answer must contain "<>" symbols).

#### Import templates

Example of content in the file with templates:

Question,Delimiters,Answer<br/>
What,"['were', 'was']",The <><br/>
How many,"['were', 'was']",<><br/>
Mean of,"['']",Mean is <><br/>

#### Statistic script

The statistics script is invoked by the application to find and process data from the database file. 
This is a script in Python, which contains one function - "calc", which takes several arguments 
(current_template, dataset, args1, connectors1, args2, connectors2) to the input and returns a string.
The function should not handle exceptions and should do several things:
1. Check the presence and number of arguments
2. Implement behavior with single (main) argument, if necessary
3. Find and use data in a file whose name is received at the input
4. Process the intervals and connectors that come with the arguments
5. If the necessary data were not found, then report it. If found, then substitute them for "<>" in response from the 
template

### Feedback

Feedback - in progress