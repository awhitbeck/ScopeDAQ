import numpy as np
#import ROOT as r 
import random as rand
import math
import matplotlib.pyplot as plt

plt.ion()

debug = False

# box size: 2*alpha x 2*beta
alpha=1.0 # x half width
beta=1.0  # y half width
pi=3.1415

def y_of_x(x,x0,theta):
    return (x-x0)*math.tan(theta)

thetas=[]
xs=[]
lengths=[]
ys_pass=[]
ys_fail=[]
thetas_fail=[]
for i in range(100000):
    
    ## generate theta according to CRY simulation
    #fin=r.TFile('../cry_v1.7/test/test.root','READ')
    #shape = fin.Get('h')
    #theta=shape.GetRandom()
    #if rand.uniform(0.,1.) > 0.5 : 
    #    theta = -theta
    # - - - - - - - - - - - - - - - - - - - - - - - - 

    ## generate theta according to cos^2(x) distributions
    #theta = rand.uniform(-pi/2.,pi/2.)
    #y=rand.uniform(0.,1.)
    #if y > (math.cos(theta))**2. : 
    #    thetas_fail.append(theta)
    #    ys_fail.append(y)
    #    continue
    #ys_pass.append(y)
    #thetas.append(theta)
    # - - - - - - - - - - - - - - - - - - - - - - - - 
    
    ## generate theta isotropically
    theta = math.acos(rand.uniform(-1,1))
    # - - - - - - - - - - - - - - - - - - - - - - - - 

    x0 = rand.uniform(-10,10)

    t_hat_p = beta/math.tan(theta)+x0
    t_hat_m = -beta/math.tan(theta)+x0

    # at least one of the t_hats must be between +/- alpha for line to cross box
    if not ((t_hat_p > -alpha and t_hat_p < alpha) or (t_hat_m > -alpha and t_hat_m < alpha)):
        continue

    xs.append(x0)

    ## find all t differences
    ts = [alpha,-alpha,beta/math.tan(theta)+x0,-beta/math.tan(theta)+x0]
    # get all pairs of ts
    ts.sort()
    length=abs(ts[1]-ts[2])/abs(math.cos(theta))
    lengths.append(length)
    
    if debug :
        print 't_hat_p',t_hat_p
        print 't_hat_m',t_hat_m
        print 'theta',theta
        print 'x0',x0
        print 'length',length

        ## compute end points and draw
        x_points = [alpha,-alpha,beta/math.tan(theta)+x0,-beta/math.tan(theta)+x0]
        y_points = [y_of_x(alpha,x0,theta),y_of_x(-alpha,x0,theta),beta,-beta]

        plt.plot(x_points,y_points)
        plt.plot([alpha,alpha,-alpha,-alpha,alpha],[beta,-beta,-beta,beta,beta])
        plt.show()
        raw_input('hit any key to continue')
        plt.cla()
        plt.clf()

plt.hist(lengths,histtype='step',bins=np.arange(0,math.sqrt(4*alpha*alpha+4*beta*beta),0.1))
#plt.hist(thetas,histtype='step')
#plt.scatter(thetas,ys_pass,alpha=0.1)
#plt.scatter(thetas_fail,ys_fail,alpha=0.1)
plt.show()
