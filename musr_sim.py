# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 13:30:38 2020

@author: Shayan
"""

import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import cauchy
import scipy.stats as stats
from scipy.special import jv
##################

def musr(nevent):
#initialization of the arrays and parameters we will use later on, will be explained later
  plt.close('all')
  n_event=nevent#
  alp=1
  fig = plt.figure() 
  B=np.zeros(n_event) #back detector array
  F=np.zeros(n_event) #forward detector array
  time=np.zeros(n_event) #time of decay array
  energy=np.zeros(n_event) #energy of emitted positron
  a=np.zeros(n_event) #"a" parameter 
  mu=np.zeros(n_event) #The relative angle of the muon spin before decaying
  std=np.zeros(n_event) #standard deviation of the angular distribution, depends on positron energy, or "a" parameter
  field=np.zeros(n_event) #field experienced by nth muon
  theta=np.zeros(n_event) #The actual decay angle following the \mu angle

  angles=np.linspace(0,2*np.pi,100)
  lower, upper = -2*np.pi, 2*np.pi

  #run the simulation here
  for i in range (n_event):
      #the time it takes for the nth muon to decay
      time[i]=np.random.exponential(((2.2)))
      #The magnetic field sensed by the muons
      field[i]=.016#np.random.normal(loc=40,scale=50)/10000 #
      #The energy of the emitted positron (approximates the real distribution)
      energy[i]=51*(stats.genhalflogistic.rvs(c=1,loc=1)-1)#np.random.normal(25,5)
      #"a" parameter of the nth muon decay event (see notes)
      a[i]= ((2*energy[i]/52)-1)/(3-2*(energy[i]/52)) 
      std[i]=np.true_divide(2.6,(a[i]+0.34))
      #mu is the angle the muon spin has before decaying
      mu[i]=0.8*np.pi*np.cos(field[i]*135.5*time[i])#*np.exp(-0.3*time[i])
      #The actual angle of decay based on an approximation of the cardiod decay distribution.
      theta[i]=stats.truncnorm.rvs((lower - mu[i]) / std[i], (upper - mu[i]) / std[i], loc=mu[i], scale=std[i])
      #Here the events are "binned" and theta's are scaled into the [-pi,pi] domain
      if theta[i]>np.pi:
          theta[i]=theta[i]-1*np.pi
      if theta[i]<-np.pi:
          theta[i]=theta[i]+1*np.pi
      #if pointing toward B detector, assume it will be detected by the B detector
      if theta[i]>0:
          B[i]=time[i]
      #otherwise, it's a F event. ideal experiment = no background detectors are large
      else:
          F[i]=time[i]

  #now we produce the histograms
  #k is the number of bins the 10 \mu s are divided into
  k=100#int((n_event)/(10000))
  fo=np.histogram(F,bins=(np.linspace(0,10,k)))
  ba=np.histogram(B,bins=(np.linspace(0,10,k)))
  asy=np.zeros(len(fo[0]))
  # for i in range (len(ba[0])):
  #     ba[0][i]=ba[0][i]#+.00002*max(ba[0])*np.random.exponential(((2.2)))
  #     fo[0][i]=fo[0][i]#+.00002*max(fo[0])*np.random.exponential(((2.2)))

  #compute the asymmetry
  def asy(f,b):
      return np.true_divide((f-alp*b),(f+alp*b))

  #calculate the errors assuming poisson statistics
  erb=np.zeros(len(ba[0]))
  erf=np.zeros(len(fo[0]))
  erasy=np.zeros(len(fo[0]))
  for o in range (len(ba[0])):
      erb[o]=(np.sqrt(ba[0][o]))
      erf[o]=(np.sqrt(fo[0][o]))
      erasy[o]=2*np.sqrt((((ba[0][o])**2*erf[o]**2)+((fo[0][o])**2*erb[o]**2))/(ba[0][o]+fo[0][o])**4)
  calc=asy(ba[0],fo[0])   
  #filter the bad "edge" points to plot it properly
  for i in range (len(calc)):
      if calc[i]==1 or calc[i]==-1:
          calc[i]=None
  plt.errorbar(fo[1][0:k-1],fo[0][0:k-1],yerr=erf[0:k-1],fmt='o',capsize=2,markersize=3,color='black')
  plt.errorbar(fo[1][0:k-1],ba[0][0:k-1],yerr=erb[0:k-1],fmt='o',capsize=2,markersize=3,color='red')
  plt.ylim(0,2*fo[0][2])
  plt.xlim(0,10)
  plt.ylabel('Number of counts')
  plt.xlabel('Time ($\mu$s)')
  x=plt.figure(tight_layout=True,figsize=(8, 6))
  #plt.ylim(0,0.5)
  plt.clf()
  plt.errorbar(fo[1][1:k-1],calc[1:k-1],yerr=erasy[1:k-1],fmt='o',capsize=2,markersize=3,color='blue',label=str(n_event)+' events')
  plt.xlabel('Time ($\mu$s)',fontsize=24)

  plt.ylabel('Asymmetry',fontsize=24)
  plt.xticks(fontsize=16.5)
  plt.yticks(fontsize=16.5)
  plt.ylim(-1,1)#(-1,1)
  plt.xlim(0,10)
  plt.legend(loc=4,frameon=True,facecolor='white',edgecolor='white',framealpha=1,fontsize=15)
  ttheory=np.linspace(0,10,100)
  plt.text(8.5,0.9,'$shayang$',fontsize=15,)
  #plt.savefig(str(nevent))


#the rest is plotting
