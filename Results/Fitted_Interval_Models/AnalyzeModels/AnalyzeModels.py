import pandas as pd
import matplotlib.pyplot as plt

def AnalyzeModelProds(dfModel, minTime, maxTime):


	resultsDict={}	
	for time in range(minTime, maxTime+1):
		resultsDict[time]=0

	for i in range(len(dfModel)):
		first = dfModel.ix[i,0]
		last = dfModel.ix[i,1]
		lam = dfModel.ix[i,3]
		for time in range(first, last +1):
			resultsDict[time] += lam

	return resultsDict

def AnalyzeModelBudget(dfModel, minTime, maxTime):


	resultsDict={}	
	for time in range(minTime, maxTime+1):
		resultsDict[time]=[[],[]]

	for i in range(len(dfModel)):
		first = dfModel.ix[i,0]
		last = dfModel.ix[i,1]
		budget = dfModel.ix[i,2]
		lam = dfModel.ix[i,3]
	
		for time in range(first, last +1):
			resultsDict[time][0] += [budget]
			resultsDict[time][1] += [lam]

	print "Done"
	for time in range(minTime, maxTime+1):
		print time
		resultsDict[time][1] = [resultsDict[time][1][i]/sum(resultsDict[time][1]) for i in range(len(resultsDict[time][1]))]

	finalResults={}
	for time in range(minTime, maxTime+1):
		finalResults[time] = sum([resultsDict[time][0][i]*resultsDict[time][1][i] for i in range(len(resultsDict[time][1]))])

	return finalResults

def linePlot(resultsDict):

	x=[]
	y=[]
	for time in resultsDict.keys():
		x+=[time]
		y+=[resultsDict[time]]
	plt.plot(x,y)
	plt.show()

if __name__ == '__main__':
	maxTime = 60
	minTime =15
	dfModel = pd.read_csv("../IntervalModel5.csv", header=None)
	resultsDict = AnalyzeModelBudget(dfModel, minTime, maxTime)
	linePlot(resultsDict)