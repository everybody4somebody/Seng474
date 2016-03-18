import sqlite3
import numpy
import pickle

myConnection = sqlite3.connect('../Data/database.sqlite')
myCursor = myConnection.cursor()

myCursor.execute('SELECT DISTINCT author FROM May2015 LIMIT 100')
listAuthors = myCursor.fetchall()

myCursor.execute('SELECT DISTINCT subreddit FROM May2015')
listSubreddits = myCursor.fetchall()

dictAuthorsToIndex = {}
dictIndexToAuthors = {}

dictSubredditsToIndex = {}
dictIndexToSubreddits = {}

numAuthors = len(listAuthors)
numSubreddits = len(listSubreddits)

for index in range(numAuthors):
    dictIndexToAuthors[index] = listAuthors[index]
    dictAuthorsToIndex[listAuthors[index]] = index

for index in range(numSubreddits):
    dictIndexToSubreddits[index] = listSubreddits[index][0]
    dictSubredditsToIndex[listSubreddits[index][0]] = index

f = open('../Data/table', 'w')

for outerIndex in range(numAuthors):
    innerReturnList = [0] * numSubreddits
    for row in myCursor.execute('SELECT DISTINCT subreddit FROM May2015 where author=(?) LIMIT 1000', dictIndexToAuthors[outerIndex]):
        for subreddit in row:
            if subreddit in dictSubredditsToIndex:
                innerReturnList[dictSubredditsToIndex[subreddit]] = 1
    for x in innerReturnList:
        f.write(str(x))
    f.write('\n')

f.close()

f = open('../Data/subredditDict', 'w')
pickle.dump(dictIndexToSubreddits, f)
f.close()
