import numpy as np

def Generate_Offer_Sets(numProds, T):

	offerSet=[]
	for t in range(T):
		day=[0]
		for j in range(1,numProds+1):
			randNum = np.random.uniform()
			if randNum > 0.5:
				day+=[j]
		offerSet+=[day]

	return offerSet

def Generate_Offer_Prices(offerSets, T,  lowPrice,highPrice):

	prices=[]
	for t in range(T):
		day=[0] + [round(np.random.uniform(lowPrice, highPrice)) for i in range(len(offerSets[t])-1)]
		prices+=[day]

	return prices
	

if __name__ == '__main__':
 	print Generate_OfferPrices([[1,2,3],[5,6],[4]],3,5,10) 