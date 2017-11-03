import random
from random import randint
import math
import numpy as np
from scipy.spatial import distance



dim = 1000
clusterCenters = np.zeros((2, dim))
clusters = {}
data = []
ratio = [3,5,10]

# center is the actual center of the hypersphere
def circle(center,circleNumber,N):
    global data,clusterCenters
    norm = np.random.normal
    normal_deviates = norm(size=(dim, N))
    radius = np.sqrt((normal_deviates**2).sum(axis=0))
    points = normal_deviates/radius
    for i in xrange(0,N):
        rand = random.uniform(0,1)
        for j in xrange(0,dim):
            points[j][i] = points[j][i] * rand
    for i in xrange(0,dim):
        arr = points[i]
        xmax = arr.flat[abs(arr).argmax()]
        for j in xrange(0,N):
            points[i][j] = points[i][j]/abs(xmax)
    for j in xrange(0,N):
        points[0][j]+=center
    clusterCenter = np.full((dim),0)
    clusterCenter[0] = center+1
    if(circleNumber==0):
        data = points
        clusterCenters[0] = clusterCenter
    else:
        data = np.concatenate((data, points), axis=1)
        clusterCenters[1] = clusterCenter


def printClusters():
    for i in xrange(0,dim):
        print clusterCenters[0][i],"  :::::::::   ",clusterCenters[1][i]
    print "---------------------------------------"

def kmean(center1,center2,clusterCenters,iteration,N1,N2):
    global data
    for i in xrange(0,2):
        clusters["cluster" + str(i)] = []
    err = error(center1,center2,clusterCenters)
    print "err ",err
    print "iteration ",iteration
    while err > .675:
        no_of_correct_points = 0
        for j in xrange(0,N1+N2):
            min = 100000;
            minIndex = 0;
            for k in xrange(0,2):
                currentPoint = data[:,j]
                currentCenter = clusterCenters[k]
                dist = distance.euclidean(currentPoint,currentCenter);
                if(dist<min):
                    min = dist
                    minIndex = k
            if (j<N1):
                if minIndex==0:
                    no_of_correct_points+=1
            else:
                if minIndex==1:
                    no_of_correct_points+=1
            clusters["cluster" + str(minIndex)].append(data[:,j])
        for j in xrange(0,2):
            clusterCenters[j] = np.mean(clusters["cluster" + str(j)],axis=0)
        err = error(center1,center2,clusterCenters)
        iteration = iteration+1
        print "err ",err
        print "iteration ",iteration
        print "correct points", no_of_correct_points
    return err,iteration,no_of_correct_points

def error(center1,center2,clusterCenters):
    c1 = np.full((dim),0)
    c2 = np.full((dim),0)
    c1[0] = center1
    c2[0] = center2
    dist1 = distance.euclidean(c1,clusterCenters[0])
    dist2 = distance.euclidean(c2,clusterCenters[1])
    return dist2+dist1

for i in xrange(0,len(ratio)):
        number_of_points_circle1 = int(round((1000.0/(ratio[i]+1))*1))
        number_of_points_circle2 = int(round((1000.0/(ratio[i]+1))*ratio[i]))
        print "******************************************"
        print "Current Ratio is 1 :",ratio[i]
        print "******************************************"
        for i in xrange(0,20):
            circle(0,0,number_of_points_circle1)
            circle(2+i/10.0,1,number_of_points_circle2)
            err,iteration,no_of_correct_points = kmean(0,2+i/10.0,clusterCenters,0,number_of_points_circle1,number_of_points_circle2)
            print "-------------------------------------------------------------------------------------->"
            print "Initial Center1 ------->  ",0
            print "Initial Center2 ------->  ",2+i/10.0
            print "err ",err
            print "iteration ",iteration
            print "percentage of correct points ",no_of_correct_points
            print "-------------------------------------------------------------------------------------->"

        for i in xrange(3,6):
            circle(0,0,number_of_points_circle1)
            circle(2**i,1,number_of_points_circle2)
            err,iteration,no_of_correct_points = kmean(0,2**i,clusterCenters,0,number_of_points_circle1,number_of_points_circle2)
            print "-------------------------------------------------------------------------------------->"
            print "Initial Center1 ------->  ",0
            print "Initial Center2 ------->  ",2**i
            print "err ",err
            print "iteration ",iteration
            print "percentage of correct points ",no_of_correct_points/((number_of_points_circle1+number_of_points_circle2)*1.0)
            print "-----------------------------"
