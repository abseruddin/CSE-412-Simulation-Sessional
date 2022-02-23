import random
import  pandas as pd
import numpy as np

class MsSimulaion:
    def __init__(self):
        # self.df = pd.DataFrame(columns=['Simulation Number','Number of customers serviced','Average Delivery Time',
        #         'Maximum Delivery Time','Average time in elevator','Maximum time in elevator','Average Customers in a queue',
        #         'Number of customers in longest queue','Average Time in a queue','Longest Time in a queue',
        #         'Total Number of stops for each elevator','Number of times max load occur in each elevator',
        #         ' Percentage of total timeeach elevator is in transport','Percentage of available time each elevator is in transport'])
        
        ##step1
        self. DELTIME = 0
        self. ELEVTIME = 0
        self. MAXDEL = 0
        self. MAXELEV = 0
        self. QUELEN = 0
        self. QUETIME  = 0
        self. MAXQUE = 0
        self. quetotal = 0
        self. remain = 0

        self.terminationTime = 4800
        self.totalFloor = 12
        self.totalElevator = 4
        self.totalCustomer = 24000
        
        self.capacity = 12
        self.batchSize = 6
        self.doorHoldingTime = 15
        self.interFloorTravellingTime = 12
        self.openingTime = 3
        self.closingTime = 3
        self.embarkingTime = 3
        self.disembarkingTime = 3
        self.meanInterArrivalTime = 1.5

        self.first = [0 for k in range(self.totalElevator)]
        self.occup = [0 for k in range(self.totalElevator)]
        self.selvec = [[0]*self.totalFloor for k in range(self.totalElevator)]
        self.flrvec = [[0]*self.totalFloor for k in range(self.totalElevator)]
        self.elevator = [0 for k in range(self.totalCustomer)]
        self.queue = 0
        self.arrive = [0 for k in range(self.totalCustomer)]
        self.floor = [0 for k in range(self.totalCustomer)]
        self.between = [0 for k in range(self.totalCustomer)]
        self.delivery = [0 for k in range(self.totalCustomer)]
        self.fullLoadedElevator = [0 for k in range(self.totalElevator)]
        self.TIME = 0
        self.currentBatch = 0
        self.i = 0
        
        self.returnTime = [self.TIME for k in range(self.totalElevator)]
        self.stopTime = [0 for k in range(self.totalElevator)]
        self.operateTime = [0 for k in range(self.totalElevator)]
        self.wait = [0 for i in range(self.totalCustomer)]
        pass

    def findMax(self,s):
        m = max(s)
        idx = 0
        for j in range(self.totalFloor):
            if s[j] == m:
                idx = j
        return idx

    def setParameters(self):
        parameters = open('./input.txt','r')
        values = []
	
        for i in range(5):
            values.append([float(x) for x in parameters.readline().split()])
        self.terminationTime = values[0][0]

        self.totalFloor = int(values[1][0])
        self.totalElevator = int(values[1][1])
        self.capacity = int(values[1][2])
        self.batchSize = int(values[1][3])

        self.doorHoldingTime = values[2][0]
        self.interFloorTravellingTime = values[2][1]
        self.openingTime = values[2][2]
        self.closingTime = values[2][3]

        self.embarkingTime = values[3][0]
        self.disembarkingTime = values[3][1]

        self.meanInterArrivalTime = 60*values[4][0]
        parameters.close()
        pass

    def generateOutput(self,df):
        N = self.i - self.queue
        ELEVTIME = 0
        for m in range(self.limit):
            ELEVTIME += self.elevator[m]/self.limit
        operation = []
        for k in range(self.totalElevator):
            operation.append(self.operateTime[k]/self.terminationTime)

        # self.df.append(0,N,self.DELTIME/N,self.MAXDEL,ELEVTIME,self.MAXELEV,self.QUELEN,
        #   self.QUETIME/max(self.quetotal,1),self.MAXQUE,self.stopTime[:],operation[:])
        
        a=[(N,self.DELTIME/N,self.MAXDEL,ELEVTIME,self.MAXELEV,self.QUELEN/N,self.QUELEN,
          self.QUETIME/max(self.quetotal,1),self.MAXQUE,self.stopTime[:],
          self.fullLoadedElevator[:],operation[:],tuple(np.ones(self.totalElevator)-operation[:]))]
        df=df.append(a,ignore_index=True)
        return df
        # print(self.df)
        # self.df.to_excel('results.xlsx') 

    def arrival(self):
        self.i = self.i + 1
        if self.currentBatch ==0:
            self.between[self.i] = self.getExpon()
            self.currentBatch = self.getBinom() - 1
        else:
            self.between[self.i] = 0
            self.currentBatch -=1
        self.floor[self.i] = random.randint(2,self.totalFloor)
        pass

    def selectElevator(self):
        for k in range(self.totalElevator):
            if self.returnTime[k] <= self.TIME:
                return k
        return -1
        pass

    def getExpon(self):
        rand = random.random()
        m = - (self.meanInterArrivalTime * np.log(rand))
        return m
        # return random.randint(0,30)

    def getBinom(self):
        c = 0
        for i in range(self.batchSize-1):
            m = random.random()
            if m >= 0.5:
                c = c+1
        return c+1
        # return 1

    def startElevator(self,first,last,j):
        for k in range(first,last+1):
            N = self.floor[k] - 1
            self.elevator[k] = self.interFloorTravellingTime*N + self.disembarkingTime + self.openingTime 
            for m in range(N):
                self.elevator[k] += self.disembarkingTime*self.flrvec[j][m]
                self.elevator[k] += (self.openingTime + self.closingTime)*self.selvec[j][m] 
            self.delivery[k] += self.elevator[k]
            self.DELTIME += self.delivery[k] 

            if self.delivery[k] > self.MAXDEL:
                self.MAXDEL = self.delivery[k]
            if self.elevator[k] > self.MAXELEV:
                self.MAXELEV = self.elevator[k]

        if last+1-first == self.capacity:
            self.fullLoadedElevator[j] += 1

        self.stopTime[j] += sum(self.selvec[j])
        
        m = self.findMax(self.selvec[j])
        eldel = 2* self.interFloorTravellingTime * (m-1) + self.disembarkingTime*sum(self.flrvec[j]) + (self.openingTime + self.closingTime)*sum(self.selvec[j])
        self.returnTime[j] = self.TIME + eldel
        self.operateTime[j] += eldel

    def simulate(self):
        self.arrival()
        self.delivery[self.i] = self.doorHoldingTime
        self.TIME = self.between[self.i]
        isFromQueue = False
        while self.TIME <= self.terminationTime:
            j = self.selectElevator()
            if  j!=-1:
                if isFromQueue == False:
                    self.occup[j] = 0
                    self.selvec[j] = [0 for k in range(self.totalFloor)]
                    self.flrvec[j] = [0 for k in range(self.totalFloor)]
                    self.first[j] = self.i
                isElevatorQuit = False
                while isElevatorQuit == False:
                    ## assign current customer to an elevator
                    # if isFromQueue == False and firstPassenger == True:
                    #     self.first[j] = self.i
                    if isFromQueue == False:
                        self.selvec[j][self.floor[self.i]-1] = 1
                        self.flrvec[j][self.floor[self.i]-1] = self.flrvec[j][self.floor[self.i]-1] + 1
                        self.occup[j] = self.occup[j] + 1

                    # arrival of new customer
                    isFromQueue = False
                    self.arrival()
                    self.TIME = self.TIME + self.between[self.i]
                    self.delivery[self.i] = self.doorHoldingTime

                    for k in range(self.totalElevator):
                        if self.TIME >= self.returnTime[k]:
                            self.returnTime[k] = self.TIME

                    if self.between[self.i] <= self.doorHoldingTime and self.occup[j] < self.capacity:
                        for k in range(self.first[j], self.i):
                            self.delivery[k] = self.delivery[k] + self.between[self.i]
                    else:
                        self.limit = self.i - 1
                        '''for k in range(self.first[j],self.limit+1):
                            N = self.floor[k] - 1
                            self.elevator[k] = self.interFloorTravellingTime*N + self.disembarkingTime + self.openingTime 
                            for m in range(N):
                                self.elevator[k] += self.disembarkingTime*self.flrvec[j][m]
                                self.elevator[k] += (self.openingTime + self.closingTime)*self.selvec[j][m] 
                            self.delivery[k] += self.elevator[k]
                            self.DELTIME += self.delivery[k] 

                            if self.delivery[k] > self.MAXDEL:
                                self.MAXDEL = self.delivery[k]
                            if self.elevator[k] > self.MAXELEV:
                                self.MAXELEV = self.elevator[k]
                        
                        self.stopTime[j] += sum(self.selvec[j])'''

                        self.startElevator(self.first[j],self.limit+1,j)
                        '''m = self.findMax(self.selvec[j])
                        eldel = 2* self.interFloorTravellingTime * (m-1) + self.disembarkingTime*sum(self.flrvec[j]) + (self.openingTime + self.closingTime)*sum(self.selvec[j])
                        self.returnTime[j] = self.TIME + eldel
                        self.operateTime[j] += eldel'''
                        isElevatorQuit = True
            else:
                quecust = self.i
                startque = self.TIME
                self.queue = 1
                self.arrive[self.i] = self.TIME
                continueInQueue = True
                while continueInQueue:
                    self.arrival()
                    self.TIME = self.TIME + self.between[self.i]
                    self.arrive[self.i] = self.TIME
                    self.queue += 1

                    j = self.selectElevator()
                    while j == -1:
                        self.arrival()
                        self.TIME = self.TIME + self.between[self.i]
                        self.arrive[self.i] = self.TIME
                        self.queue += 1

                        j = self.selectElevator()

                    self.selvec[j] = [0 for k in range(self.totalFloor)]
                    self.flrvec[j] = [0 for k in range(self.totalFloor)]
                    self.remain = self.queue - self.capacity
                    R = 0
                    if self.remain <= 0:
                        R = self.i
                        self.occup[j] = self.queue
                    else:
                        R = quecust + self.capacity - 1
                        self.occup[j] = self.capacity
                    for k in range(quecust,R+1):
                        self.selvec[j][self.floor[k]-1] = 1
                        self.flrvec[j][self.floor[k]-1] = self.flrvec[j][self.floor[k]-1] + 1
                    if self.queue > self.QUELEN:
                        self.QUELEN = self.queue
                    self.quetotal += self.occup[j]

                    for m in range(quecust,R+1):
                        self.QUETIME += self.TIME - self.arrive[m]
                    
                    if (self.TIME - startque) >= self.MAXQUE:
                        self.MAXQUE = self.TIME - startque

                    self.first[j] = quecust

                    for k in range(self.first[j],R+1):
                        self.delivery[k] = self.doorHoldingTime + self.TIME - self.arrive[k] + self.embarkingTime
                        self.wait[k] = self.TIME - self.arrive[k]

                    if self.remain<=0:
                        self.queue = 0
                        continueInQueue = False
                        isFromQueue = True
                    
                    else:
                        self.limit = R
                        '''for k in range(self.first[j],self.limit+1):
                            N = self.floor[k] - 1
                            self.elevator[k] = self.interFloorTravellingTime*N + self.disembarkingTime + self.openingTime
                            for m in range(N):
                                self.elevator[k] += self.disembarkingTime*self.flrvec[j][m]
                                self.elevator[k] += (self.openingTime + self.closingTime)*self.selvec[j][m] 
                            self.delivery[k] += self.elevator[k]
                            self.DELTIME += self.delivery[k] 

                            if self.delivery[k] > self.MAXDEL:
                                self.MAXDEL = self.delivery[k]
                            if self.elevator[k] > self.MAXELEV:
                                self.MAXELEV = self.elevator[k]
                            
                        self.stopTime[j] += sum(self.selvec[j])'''

                        self.startElevator(self.first[j],self.limit+1,j)

                        '''m = self.findMax(self.selvec[j])
                        eldel = 2* self.interFloorTravellingTime * (m-1) + self.disembarkingTime*sum(self.flrvec[j]) + (self.openingTime+self.closingTime)*sum(self.selvec[j])
                        self.returnTime[j] = self.TIME + eldel
                        self.operateTime[j] += eldel'''
                        self.queue = self.remain
                        quecust = R + 1
                        startque = self.arrive[R+1]


df = pd.DataFrame()
for itr in range(10):
    s = MsSimulaion()
    s.setParameters()
    s.simulate()
    df = s.generateOutput(df)
print(df)
df.to_csv("Output.csv")
