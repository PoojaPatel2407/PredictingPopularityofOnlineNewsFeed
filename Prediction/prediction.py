
import os,sys,math,json
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation, metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from time import time
import xlsxwriter
import plotly.plotly as py
import plotly.graph_objs as go
from collections import OrderedDict
import matplotlib.pyplot as plt; plt.rcdefaults()

def percentile(data, percentile):
    """
    This function calcaute given percentile for given data.
    :return:
    """
    size = len(data)
    return sorted(data)[int(math.ceil((size * percentile) / 100)) - 1]

def prediction(train_file,test_file):

	# Load dataset to padas dataframe
	train_data = pd.read_csv(train_file)
	test_data = pd.read_csv(test_file)

	perc = percentile(train_data['shares'], 50)
	popular = train_data.shares >= perc
	unpopular = train_data.shares < perc

	train_data.loc[popular,'shares'] = 1
	train_data.loc[unpopular,'shares'] = 0

	features = list(train_data.columns[2:60])
	label = {0:'Unpopular',1:'Popular'}

	// implemnted by Pooja Patel
	# Calculation for Logistic Regression
	print "Logistic Regression"
	clf = LogisticRegression()
	clf_lr = clf.fit(train_data[features] , train_data['shares'])
	result_lr = clf.predict(test_data[features])

	# Calculation for Random Forest
	print "RandomForest"
	rf = RandomForestClassifier(n_estimators=100,n_jobs=-1)
	clf_rf = rf.fit(train_data[features], train_data['shares'])
	result_rndmfrst = rf.predict(test_data[features ] )

	# Calculation for Decision Tree
	print "DecisionTree"
	dt = DecisionTreeClassifier(min_samples_split=20,random_state=99)
	clf_dt = dt.fit(train_data[features], train_data['shares'])
	result_dt = rf.predict(test_data[features])

	# Calculation for KNN
	print "KNN"
	knn = KNeighborsClassifier()
	clf_knn=knn.fit(train_data[features], train_data['shares'])
	result_knn = rf.predict(test_data[features])

	// implemnted by Pooja Patel
	# Calculation for NaiveBayes
	print "NaiveBayes"
	nb = BernoulliNB()
	clf_nb=nb.fit(train_data[features], train_data['shares'])
	result_nb = rf.predict(test_data[features])


	prediction_file = open('Predictions.txt', 'w')
	prediction_file.write("URL\t\t\t\t\t\t[Logistic Regression, RandomForest,DecisionTree,KNN,NaiveBayes]"+'\n')
	for lr,rndm,dt,knn,nb,url in zip(result_lr,result_rndmfrst,result_dt,result_knn,result_nb,test_data['url']):
		prediction_file.write(str([label[lr],label[rndm],label[dt],label[knn],label[nb]])+'\n')
	prediction_file.close()


if __name__ == '__main__':
	prediction(sys.argv[1],sys.argv[2])