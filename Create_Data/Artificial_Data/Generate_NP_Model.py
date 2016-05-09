import numpy as np 



def Generate_Classes(numProds):
	#Assume that the intervals are spaced by minute. Returns all n^2 classes of interval model

	listClasses = []
	for i in range(1,numProds+1):
		for j in range(i, numProds+1):
			listClasses+=[[k for k in range(i,j+1)]+[0]]

	return listClasses

def Generate_ArrivalProbs(numClasses):

	
	arrivalProbsUnNormalized=[np.random.exponential(1)**2 for i in range(numClasses)]
	sumProbs=sum(arrivalProbsUnNormalized)
	arrivalProbs=[arrivalProbsUnNormalized[i]/sumProbs for i in range(numClasses)]

	return arrivalProbs

def Generate_Budgets(lowPrice,highPrice,numClasses):

	listBudgets=[round(np.random.uniform(lowPrice,highPrice)) for i in range(numClasses)]

	return listBudgets






if __name__ == '__main__':
	print Generate_Classes(4)