import numpy as np 



def Generate_Classes(lowEnd, highEnd):
	#Assume that the intervals are spaced by minute. Returns all n^2 classes of interval model

	listClasses = []
	for i in range(lowEnd,highEnd+1):
		for j in range(i +1, highEnd+1):
			listClasses+=[[i,j]]

	return listClasses

def Generate_ArrivalProbs(numClasses):

	
	arrivalProbsUnNormalized=[np.random.uniform() for i in range(numClasses)]
	sumProbs=sum(arrivalProbsUnNormalized)
	arrivalProbs=[arrivalProbsUnNormalized[i]/sumProbs for i in range(numClasses)]

	return arrivalProbs

def Generate_Budgets(lowEnd,highEnd,numClasses):

	listBudgets=[round(np.random.uniform(lowEnd,highEnd)) for i in range(numClasses)]

	return listBudgets






if __name__ == '__main__':
	print Generate_Budgets(5,10,5)