import numpy as np

def Generate_Offer_Sets(numProds, T):

	offerSet=[]
	for t in range(T):
		day=[]
		for j in range(1,numProds+1):
			randNum = np.random.uniform()
			if randNum > 0.5:
				day+=[j]
		offerSet+=[day]

	return offerSet

def Generate_Offer_Prices(offerSet, T, lowEnd, highEnd):

	prices=[]
	for t in range(T):
		day=[round(np.random.uniform(lowEnd, highEnd)) for i in range(len(offerSet[t]))]
		prices+=[day]

	return prices
	

if __name__ == '__main__':
 	print Generate_OfferPrices([[1,2,3],[5,6],[4]],3,5,10) 