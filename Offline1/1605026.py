import numpy as np
from queue import Queue 
import random
import statistics
import math
import matplotlib.pyplot as plt

class Scheduler:
    def __init__(self):
        self.meanInterArrivalTime = 0
        self.meanServiceTime = 0
        self.totalCustomer = 0

        self.totalDelay = 0
        self.customerServed = 0
        self.totalSimTime = 0
        self.currentTime = 0
        self.lastEventTime = 0
        self.nextEvent = 0
        self.timeForNextEvent = 0
        self.q = Queue()
        self.timeEvent = [ 0 , 0 ]
        self.areaNumInQueue = 0
        self.areaServerStatus = 0
        self.serverStatus = "IDLE"

        self.arrivalUniform = []
        self.arrivalExpon = []
        self.serviceUniform = []
        self.serviceExpon = []

    def setParameter(self):

        #global meanInterArrivalTime
        #global meanServiceTime
        #global totalCustomer

        inputFile = open("input.txt","r",encoding='utf-8')
        self.meanInterArrivalTime = float(inputFile.readline())
        self.meanServiceTime = float(inputFile.readline())
        self.totalCustomer = int(inputFile.readline())
        inputFile.close()
        pass

    def printToFile(self):
        '''global meanInterArrivalTime
        global meanServiceTime
        global totalCustomer
        global totalDelay
        global customerServed
        global areaNumInQueue
        global currentTime
        global areaServerStatus'''

        outputFile = open("outputA.txt","w")
        outputFile.write("Single-server queuing system\n")
        outputFile.write("\nMean interarrival time\t"+str(self.meanInterArrivalTime)+" minutes")
        outputFile.write("\nMean service time\t"+str(self.meanServiceTime)+" minutes")
        outputFile.write("\nNumber of customers\t"+str(self.totalCustomer)+"\n")

        '''print(totalDelay)
        print(customerServed)'''
        avgDelay = self.totalDelay/self.customerServed
        avgNumberInQueue = self.areaNumInQueue/self.currentTime
        serverUtilize = self.areaServerStatus/self.currentTime
        outputFile.write("\n\nAverage delay in queue\t"+str(avgDelay))
        outputFile.write("\nAverage number in queue\t"+str(avgNumberInQueue))
        outputFile.write("\nServer utilization\t"+str(serverUtilize)+" minutes")
        outputFile.write("\nTime simulation ended\t"+str(self.currentTime)+" minutes")
        outputFile.close()
        pass

    def getExpon(self,r):
        rand = random.random()
        m = - r * np.log(rand)
        if self.meanInterArrivalTime == r :
            self.arrivalUniform.append(rand)
            self.arrivalExpon.append(m)
        elif self.meanServiceTime == r :
            self.serviceUniform.append(rand)
            self.serviceExpon.append(m)
        return m

    def initialize(self):
        '''global meanServiceTime
        global currentTime
        global timeEvent'''

        t = self.getExpon(self.meanInterArrivalTime) ##################
        self.timeEvent[0] = self.currentTime + t
        self.timeEvent[1] = 99999999999999999
        pass

    def timing(self):
        '''global nextEvent
        global timeEvent
        global currentTime'''

        minNextEventTime = 99999999999999999
        self.nextEvent = -1
        for i in range(2):
            if self.timeEvent[i] < minNextEventTime :
                minNextEventTime = self.timeEvent[i]
                self.nextEvent = i
        if self.nextEvent == -1 :
            return
        self.currentTime = minNextEventTime
        pass

    def arrive(self):
        '''global meanInterArrivalTime
        global timeEvent
        global currentTime
        global serverStatus
        global meanServiceTime
        global customerServed
        global q'''

        delay = 0
        self.timeEvent[0] = self.currentTime + self.getExpon(self.meanInterArrivalTime) ##################
        if self.serverStatus == "BUSY" :
            self.q.put(self.currentTime)
        else:
            self.customerServed = self.customerServed +1 
            self.serverStatus = "BUSY"
            self.timeEvent[1] = self.currentTime + self.getExpon(self.meanServiceTime)
        pass

    def depart(self):
        '''global timeEvent
        global currentTime
        global serverStatus
        global q
        global customerServed
        global meanServiceTime
        global totalDelay'''

        if self.q.empty():
            self.timeEvent[1] = 99999999999999999
            self.serverStatus = "IDLE"
        else:
            self.totalDelay = self.totalDelay + self.currentTime - self.q.get()
            self.customerServed = self.customerServed +1
            self.timeEvent[1] = self.currentTime + self.getExpon(self.meanServiceTime) 

    def updateStat(self):
        '''global currentTime
        global lastEventTime
        global serverStatus
        global areaServerStatus
        global areaNumInQueue
        global totalDelay
        global q'''

        time = self.currentTime - self.lastEventTime
        # totalDelay = totalDelay + time
        self.lastEventTime = self.currentTime
        self.areaNumInQueue = self.areaNumInQueue + time * self.q.qsize()
        if self.serverStatus == "BUSY":
            self.areaServerStatus = self.areaServerStatus + time
        pass
    
    def clearValue(self):

        self.meanServiceTime = 0

        self.totalDelay = 0
        self.customerServed = 0
        self.totalSimTime = 0
        self.currentTime = 0
        self.lastEventTime = 0
        self.nextEvent = 0
        self.timeForNextEvent = 0
        self.q = Queue()
        self.timeEvent = [ 0 , 0 ]
        self.areaNumInQueue = 0
        self.areaServerStatus = 0
        self.serverStatus = "IDLE"
        pass

    def generateUniformStatistics(self,outputFile,List,beta):

        outputFile.write("Mean : "+str(min(List))+"\n")
        outputFile.write("Median : "+"{:.5f}".format(statistics.median(List))+"\n")
        outputFile.write("Max : "+"{:.5f}".format(max(List))+"\n")

        probability = []
        for i in range(10):
            probability.append(0)

        for i in List:
            if i < 0.1:
                probability[0] = probability[0] + 1
            elif i < 0.2:
                probability[1] = probability[1] + 1
            elif i < 0.3:
                probability[2] = probability[2] + 1
            elif i < 0.4:
                probability[3] = probability[3] + 1
            elif i < 0.5:
                probability[4] = probability[4] + 1
            elif i < 0.6:
                probability[5] = probability[5] + 1
            elif i < 0.7:
                probability[6] = probability[6] + 1
            elif i < 0.8:
                probability[7] = probability[7] + 1
            elif i < 0.9:
                probability[8] = probability[8] + 1
            elif i < 1:
                probability[9] = probability[9] + 1
        for i in range(10):
            probability[i] = probability[i]/len(List)
        outputFile.write("\n   Range  |  p(x) | F(x)\n")
        sum = 0
        for i in range(10):
            sum = sum + probability[i]
            outputFile.write(str(i/10.0) + " - " +str((i+1)/10.0)+" | "+"{:.3f}".format(probability[i])+" | "+"{:.3f}".format(sum)+"\n")
        pass
        x = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
        plt.plot(x,probability)
        if beta == self.meanInterArrivalTime:
            plt.ylabel('p(x)')
            plt.title('Inter Arrival Time (Uniform )')
        else:
            plt.ylabel('p(x)')
            plt.title('Service Time (Uniform )')
        plt.show()

    def generateExponStatistics(self,outputFile,List,beta):

        outputFile.write("Mean : "+str(min(List))+"\n")
        outputFile.write("Median : "+"{:.5f}".format(statistics.median(List))+"\n")
        outputFile.write("Max : "+"{:.5f}".format(max(List))+"\n")

        probability = []
        for i in range(5):
            probability.append(0)

        for i in List:
            if i < beta/2:
                probability[0] = probability[0] + 1
            elif i < beta:
                probability[1] = probability[1] + 1
            elif i < 2*beta:
                probability[2] = probability[2] + 1
            elif i < 3*beta:
                probability[3] = probability[3] + 1
            else:
                probability[4] = probability[4] + 1
            
        for i in range(5):
            probability[i] = probability[i]/len(List)
        outputFile.write("\n  Range  | p(x)  | F(x)\n")
        sum = 0
        sum = sum + probability[0]
        outputFile.write("  0 - Beta/2   | "+"{:.3f}".format(probability[0])+" | "+"{:.3f}".format(sum)+"\n")
        sum = sum + probability[1]
        outputFile.write(" Beta/2 - Beta | "+"{:.3f}".format(probability[1])+" | "+"{:.3f}".format(sum)+"\n")
        sum = sum + probability[2]
        outputFile.write(" Beta - 2Beta  | "+"{:.3f}".format(probability[2])+" | "+"{:.3f}".format(sum)+"\n")
        sum = sum + probability[3]
        outputFile.write(" 2Beta - 3Beta | "+"{:.3f}".format(probability[3])+" | "+"{:.3f}".format(sum)+"\n")
        sum = sum + probability[4]
        outputFile.write("    >3Beta     | "+"{:.3f}".format(probability[4])+" | "+"{:.3f}".format(sum)+"\n")
        
        x = [beta/2,beta,2*beta,3*beta,4*beta]
        plt.plot(x,probability)
        if beta == self.meanInterArrivalTime:
            plt.ylabel('p(x)')
            plt.title('Inter Arrival Time ( Exponential )')
        else:
            plt.ylabel('p(x)')
            plt.title('Service Time ( Exponential )')
        plt.show()
        pass

    def mainForA(self):
        '''global customerServed
        global totalCustomer
        global nextEvent'''
        self.setParameter()
        self.initialize()
        while self.customerServed < self.totalCustomer:
            self.timing()
            self.updateStat()
            if self.nextEvent == 0:
                self.arrive()
            elif self.nextEvent == 1:
                self.depart()
            
        self.printToFile()
        pass

    def mainForB(self):
        outputFile = open("outputB.txt","w")
        values = [0.5,0.6,0.7,0.8,0.9] 
        delay = []
        avgInQueue = []
        utilize = []
        total = []
        for value in values :
            self.clearValue()
            self.meanServiceTime = value
            self.initialize()
            while self.customerServed < self.totalCustomer:
                self.timing()
                self.updateStat()
                if self.nextEvent == 0:
                    self.arrive()
                elif self.nextEvent == 1:
                    self.depart()
                
            avgDelay = self.totalDelay/self.customerServed
            avgNumberInQueue = self.areaNumInQueue/self.currentTime
            serverUtilize = self.areaServerStatus/self.currentTime
            delay.append(avgDelay)
            avgInQueue.append(avgNumberInQueue)
            utilize.append(serverUtilize)
            total.append(self.currentTime)
            outputFile.write("k = " + str(value))
            outputFile.write("\n"+str(avgDelay))
            outputFile.write("\n"+str(avgNumberInQueue))
            outputFile.write("\n"+str(serverUtilize)+" minutes")
            outputFile.write("\n"+str(self.currentTime)+" minutes\n\n")

        plt.plot(values,delay)
        plt.title("Average delay(minutes)")
        plt.show()

        plt.plot(values,avgInQueue)
        plt.title("Average Number In Queue")
        plt.show()

        plt.plot(values,utilize)
        plt.title("Server Utilization")
        plt.show()

        plt.plot(values,total)
        plt.title("Total Simulation Time(minutes)")
        plt.show()
        pass
    
    def mainForC(self):
        outputFile = open("outputC.txt","w")
        self.clearValue()
        self.meanServiceTime = 0.5
        self.initialize()
        while self.customerServed < self.totalCustomer:
            self.timing()
            self.updateStat()
            if self.nextEvent == 0:
                self.arrive()
            elif self.nextEvent == 1:
                self.depart()

        outputFile.write("Inter-arrival time statistics ( Uniform )\n\n")
        self.generateUniformStatistics(outputFile,self.arrivalUniform,self.meanInterArrivalTime)

        outputFile.write("\n\nService time statistics ( Uniform )\n\n")
        self.generateUniformStatistics(outputFile,self.serviceUniform,self.meanServiceTime)
        outputFile.write("\n\nInter-arrival time statistics ( Exponential )\n\n")
        self.generateExponStatistics(outputFile,self.arrivalExpon,self.meanInterArrivalTime)
        outputFile.write("\n\nService time statistics ( Exponential )\n\n")
        self.generateExponStatistics(outputFile,self.serviceUniform,self.meanServiceTime)
    
if __name__ == "__main__" :
    s = Scheduler()
    s.mainForA()
    s.mainForB()
    s.mainForC()