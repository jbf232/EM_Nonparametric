import xlwt
import numpy as np
import matplotlib.pyplot as plt


def GetOfferDict():
	
	file = open('search_options_sc.txt', 'r')	
	modeOptions=['rideshare', 'walking', 'transit','biking', 'scoot']
	offerDict={}
	t=0
	flag=0
	offeredTimes = []
	offeredPrices = []
	offeredDistances=[]
	prodNum=0
	for line in file:
		info=line.split(',')
		searchID=info[0]
		
		if searchID.strip('\n') in modeOptions:

			#Make sure correct mode was chosen + chosen option had price + there were offered items
			if searchID.strip('\n') not in ["biking", "scoot"] and flag == 0 and len(offeredTimes)>3 and min(offeredTimes)>=5:
				offerDict[t]={}
				minTime = min(offeredTimes) 
				maxTime = max(offeredTimes)
				maxPrice = max(offeredPrices)
				avgDistance = np.mean(offeredDistances)
				offerDict[t]["times"] = offeredTimes
				offerDict[t]["prices"]  = offeredPrices
				offerDict[t]["purchased"] = purchased
				offerDict[t]["maxTime"] = maxTime
				offerDict[t]["minTime"] = minTime
				offerDict[t]["maxPrice"] = maxPrice
				offerDict[t]["avgDistance"] = avgDistance
				t+=1				

			prodNum=0
			flag=0
			offeredTimes = []
			offeredPrices = []
			offeredDistances=[]

		else:
			
			#Will need surge later
			chosen, product, distance, time, price,surge =info[2], info[3], float(info[4]), float(info[5]),float(info[6]), float(info[7])
			time =int(round(time/60.0))
			price = int(round(price))
			if price>=0 and "scoot" not in product and "biking" not in product:

				if chosen == "True":
					purchased = prodNum

				offeredTimes +=[time]
				offeredPrices +=[price]
				offeredDistances+=[distance]
				prodNum+=1

			else:
				if chosen == "True":
					flag=1
	print t
	return offerDict


def WriteSalesData(offerDict, minAllowableTime , maxAllowableTime, maxAllowablePrice):

	f1 = open('../Real_Data/SalesData_Long.csv','w')
	F=open('../Other_Models/SalesData_Long.txt','w')
	G=open('../Other_Models/Purchases_Long.txt','w') 

	for t in offerDict.keys():
		

		
		offeredTimes  = offerDict[t]["times"]
		numOffered =len(offeredTimes)
		offeredPrices = offerDict[t]["prices"]  
		purchasedIndex = offerDict[t]["purchased"] 
		purchased = offeredTimes[purchasedIndex]
		minTime = offerDict[t]["minTime"]
		maxTime = offerDict[t]["maxTime"] 
		maxPrice = offerDict[t]["maxPrice"]
		avgDistance = offerDict[t]["avgDistance"]
		pricePurchased = offeredPrices[purchasedIndex]

		if minTime>=minAllowableTime and maxTime <= maxAllowableTime and pricePurchased <= maxAllowablePrice and avgDistance<(1600*20) and avgDistance>(1600*5):

			#Wite sales data for EM Algorithm
			f1.write(str(numOffered) + "\n")

			for time in offeredTimes:
				f1.write(str(time) + ",")
			f1.write("\n")

			for price in offeredPrices:
				f1.write(str(price) + ",")
			f1.write("\n")

			f1.write(str(purchased) + "\n")


			#Write the Sales data for the other models
			F.write('%d\t' %1)
			for j in range(1,maxAllowableTime+1):
 
				if j in offeredTimes:
				 
					F.write('%d\t' %1)
				else:
				
					F.write('%d\t' %0)

			F.write('\n')


			for j in range(maxAllowableTime+1):
 
				if j == purchased:
				
					G.write('%d\t' %1)
				else:
				
					G.write('%d\t' %0)

			G.write('\n')

def WriteCustomerData(offerDict, priceThresholdList, minAllowableTime , maxAllowableTime, maxAllowablePrice,step):

	f1 = open('../Real_Data/CustomerData%d_Long.csv' %step,'w') 

	tCount=0
	for t in offerDict.keys():

		offeredPrices = offerDict[t]["prices"] 
		purchasedIndex = offerDict[t]["purchased"] 
		minTime = offerDict[t]["minTime"]
		maxTime = offerDict[t]["maxTime"] 
		maxPrice = offerDict[t]["maxPrice"]
		avgDistance = offerDict[t]["avgDistance"]
		pricePurchased = offeredPrices[purchasedIndex]

		if minTime>=minAllowableTime and maxTime <= maxAllowableTime and pricePurchased <= maxAllowablePrice  and avgDistance<(1600*20) and avgDistance>(1600*5) :

			tCount+=1
	print tCount
	f1.write(str(tCount) + "\n")
	f1.write(str(minAllowableTime) + "\n")
	f1.write(str(maxAllowableTime) + "\n")
	f1.write(str(len(priceThresholdList)) + "\n")
	for price in priceThresholdList:
		f1.write(str(price) + ",")
	

def GetPricingInfo(offerDict,minAllowableTime , maxAllowableTime):

	listPrices = []

	for t in offerDict.keys():
		offeredPrices = offerDict[t]["prices"]  
		minTime = offerDict[t]["minTime"]
		maxTime = offerDict[t]["maxTime"] 
		if minTime>=minAllowableTime and maxTime <= maxAllowableTime:
			listPrices+=offeredPrices
	plt.hist(listPrices, 1000)
	plt.show()


def TestVertical(offerDict,minAllowableTime , maxAllowableTime):

	total=0.0
	count=0.0
	for t in offerDict.keys():


		offeredTimes  = offerDict[t]["times"]
		offeredPrices = offerDict[t]["prices"]  
		purchasedIndex = offerDict[t]["purchased"] 
		purchased = offeredTimes[purchasedIndex]
		minTime = offerDict[t]["minTime"]
		maxTime = offerDict[t]["maxTime"] 
		minPrice = min(offeredPrices)
	

		if minTime>=minAllowableTime and maxTime <= maxAllowableTime:

			minPriceList=[]
			for j in range(len(offeredTimes)):
				if offeredPrices[j]<= minPrice:
					minPriceList = [offeredTimes[j]]

			if min(minPriceList)<=minTime:
				total+=1
				if offeredTimes[purchasedIndex]<=minTime and offeredPrices[purchasedIndex] <= minPrice:
					count+=1


	return count/total

if __name__ == '__main__':
	minAllowableTime = 5
	maxAllowableTime = 60
	priceSteps=[5,2,1]
	for step in priceSteps:
		priceThresholdList=[step*i for i in range(int(40/step)+1)]
		maxAllowablePrice = max(priceThresholdList) 
		offerDict = GetOfferDict()
		WriteSalesData(offerDict, minAllowableTime , maxAllowableTime, maxAllowablePrice)
		WriteCustomerData(offerDict, priceThresholdList, minAllowableTime , maxAllowableTime, maxAllowablePrice, step)

