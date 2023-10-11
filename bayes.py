import math
import pandas
from functools import cache
column_labels = ["animal_name","hair","feathers","eggs","milk","airborne","aquatic","predator","toothed","backbone","breathes","venomous","fins","legs","tail","domestic","catsize","class_type","predicted","probability","correct?"]
class AnswerRow:
    def __init__(self,percentage,classValue):
        self.percentage = percentage
        self.classValue = classValue
def generalProbability(classType,classValue,frame):
    return_value = len(frame[(frame[classType] == classValue)])/len(frame)
    return return_value
def generalNotProbability(classType,classValue,frame):
    return_value = len(frame[(frame[classType] != classValue)])/len(frame)
    return return_value
def conditionalProbability(classType,classValue,feature,value,frame):
    a = len(frame[((frame[feature] == value) & (frame[classType] == classValue))])
    b = len(frame[(frame[classType] == classValue)])+0.01
    return a/b
def conditionalNotProbability(classType,classValue,feature,value,frame):
    a = len(frame[((frame[feature] != value) & (frame[classType] == classValue))])
    b = len(frame[(frame[classType] == classValue)])+0.01
    return a/b
def PredictClass(classType,classValue,row):
    a = 1
    b = 1
    c = 0
    d = 1
    e = 1
    a = generalProbability(classType,classValue,train) + 0.1
    d = generalNotProbability(classType,classValue,train) + 0.1
    for column in row:
        v = 0
        if column == 0:
            v = 1
        if c != 0 and c != len(row)-1 and column_labels[c] != "legs":
            a = a * (conditionalProbability(classType,classValue,column_labels[c],column,train) + 0.1)
            b = b * (generalProbability(column_labels[c],column,train) + (0.1 * 16))
            d = d * (conditionalProbability(classType,classValue,column_labels[c],v,train) + 0.1)
            e = e * (generalProbability(column_labels[c],v,train) + (0.1 * 16))
        elif c != 0 and c != len(row)-1 and column_labels[c] == "legs":
            a = a * (conditionalProbability(classType,classValue,column_labels[c],column,train) + 0.1)
            b = b * (generalProbability(column_labels[c],column,train) + (0.1 * 16))
            d = d * (conditionalNotProbability(classType,classValue,column_labels[c],column,train) + 0.1)
            e = e * (generalNotProbability(column_labels[c],column,train) + (0.1 * 16))
        c = c+1
    f = a/b
    g = d/e
    h = f/(f+g)
    j = g/(g+f)
    if(f > h):
        return h
    else:
        return h
def findClass(rows):
    max_val = 0
    class_val = 0
    total = 0
    for i in range(7):
        #print(i)
        prediction = PredictClass("class_type",i+1,rows)
        if(prediction > max_val):
            max_val = prediction
            class_val = i+1
        total = total+prediction
    max_val = max_val/total
    return AnswerRow(max_val,class_val)
data = pandas.read_csv('zoo.csv')
train = data.sample(frac = 0.7)
test = data.drop(train.index)
k = 0
total = 0
correct = 0
top = ""
count = 0
for items in column_labels:
    if(count != len(column_labels)-1):
        top = top + items + ","
        count = count+1
    else:
        top = top + items
print(top)
for index,rows in test.iterrows():
    string_print = ""
    for column in rows:
        string_print = string_print + str(column) + ","
    
    rowObject = findClass(rows)
    string_print = string_print+str(rowObject.classValue) + ","+str(rowObject.percentage) + ","
    isCorrect = False
    if(rowObject.classValue) == rows["class_type"]:
        correct = correct+1
        isCorrect = True
    if(isCorrect == True):
        string_print = string_print + "CORRECT"
    else:
        string_print = string_print + "wrong"
    print(string_print)
    total = total+1
#debug statement below        
#print(correct/total)
