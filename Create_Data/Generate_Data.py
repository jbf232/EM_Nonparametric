import numpy as np
from scipy.stats import rv_discrete
from Generate_NP_Model import *
from Generate_Offer import *

def findPurchase(S, P , prefList, B ):

	for j in range(len(prefList)):
		prod = prefList[j]
		if prod in S:
			prodIndex = S.index(prod)
			price = P[prodIndex]
			if price <= B:
				return prod


def WriteSalesData(salesDataDict,T):

	f = open('SalesData.csv', 'w')

	
	for t in range(T):
		S = salesDataDict[t][0]
		P = salesDataDict[t][1]
		purchase = salesDataDict[t][2]
		f.write(str(len(S)) + '\n')
		for prod in S[:-1]:
			f.write(str(prod) + ',')
		f.write(str(S[-1]))
		f.write('\n')
		for price in P[:-1]:
			f.write(str(price) + ',')
		f.write(str(P[-1]))
		f.write('\n')
		f.write(str(purchase) +  '\n')

def WriteCustomerData(numProds, lowPrice, highPrice,T):

	f= open('CustomerData.csv', 'w')
	f.write(str(T))
	f.write('\n')
	f.write(str(1) + '\n')
	f.write(str(numProds) + '\n')
	f.write(str(highPrice - lowPrice + 1) + '\n')
	for price in range(lowPrice,highPrice):
		f.write(str(price) + ',')
	f.write(str(highPrice))


def Generate_Data(numProds, lowPrice,highPrice,T):

	customerClasses = Generate_Classes(numProds)
	numClasses = len(customerClasses)
	arrivalProbs = Generate_ArrivalProbs(numClasses)
	customerBudgets = Generate_Budgets(lowPrice,highPrice,numClasses)

	salesDataDict={}
	offerSets = Generate_Offer_Sets(numProds, T)
	offerPrices = Generate_Offer_Prices(offerSets, T,  lowPrice,highPrice)
	for t in range(T):
		distrib = rv_discrete(values=([i for i in range(numClasses)], arrivalProbs))
		customerArrival = distrib.rvs(size=1)[0]
		purchase = findPurchase(offerSets[t], offerPrices[t], customerClasses[customerArrival], customerBudgets[customerArrival])
		salesDataDict[t] = [offerSets[t], offerPrices[t], purchase]

	WriteSalesData(salesDataDict,T)
	WriteCustomerData(numProds, lowPrice, highPrice,T)
if __name__ == '__main__':
	
	Generate_Data(5, 5,10,5)

