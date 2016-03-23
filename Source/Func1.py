import sqlite3
import numpy
import pickle

myConnection = sqlite3.connect('../Data/database.sqlite')
myCursor = myConnection.cursor()


myCursor.execute('SELECT author FROM may2015 GROUP BY author HAVING COUNT(author) > 10')
listAuthors = myCursor.fetchall()

myCursor.execute('SELECT subreddit FROM may2015 GROUP BY subreddit HAVING COUNT(subreddit) > 500')
listSubreddits = myCursor.fetchall()

dictAuthorsToIndex = {}
dictIndexToAuthors = {}

dictSubredditsToIndex = {}
dictIndexToSubreddits = {}

numAuthors = len(listAuthors)
numSubreddits = len(listSubreddits)

for index in range(numAuthors):
    dictIndexToAuthors[index] = listAuthors[index][0]
    dictAuthorsToIndex[listAuthors[index][0]] = index

for index in range(numSubreddits):
    dictIndexToSubreddits[index] = listSubreddits[index][0]
    dictSubredditsToIndex[listSubreddits[index][0]] = index

f = open('../Data/table', 'w')

f.write(str(numAuthors) + ',' + str(numSubreddits) + '\n')

for outerIndex in range(numSubreddits):
    flag = False
    for row in myCursor.execute('SELECT DISTINCT author FROM May2015 where subreddit=(?)', (dictIndexToSubreddits[outerIndex],)):
        for author in row:
            if author in dictAuthorsToIndex:
                if(flag):
                    f.write(',' + str(dictAuthorsToIndex[author]))
                else:
                    f.write(str(dictAuthorsToIndex[author]))
                    flag = True
    f.write('\n')
f.close()

f = open('../Data/subredditDict', 'w')
pickle.dump(dictIndexToSubreddits, f)
f.close()


##myCursor.execute('SELECT avg(count) FROM(SELECT COUNT(author) AS count FROM may2015 GROUP BY author)')
##print(myCursor.fetchall())

##myCursor.execute('SELECT avg(count) FROM(SELECT COUNT(subreddit) AS count FROM may2015 GROUP BY subreddit)')
##print(myCursor.fetchall())

##myCursor.execute('SELECT subreddit, author FROM may2015 GROUP BY author LIMIT 50')
##print(myCursor.fetchall())

##myCursor.execute('SELECT DISTINCT author FROM May2015 LIMIT 100')
##listAuthors = myCursor.fetchall()

##myCursor.execute('SELECT DISTINCT subreddit FROM May2015')
##listSubreddits = myCursor.fetchall()
