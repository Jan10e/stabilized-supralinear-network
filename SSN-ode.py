"""
Simulate a E-I 2D model with supra-linear stabilization

Created by Nirag Kadakia at 16:51 01-29-2018
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon

import matplotlib 
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

#from PyQt5 import QtCore 
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
#import matplotlib.pyplot as plt




##############################
######     Parameters    #####
##############################


# Parameters
Kk = 0.3 
Nn = 2
V_rest = -70.
 
# Connectivity Matrix W
w_EE = 1.25
w_EI = -0.65
w_IE = 1.2
w_II = -0.5
Ww = sp.array([[w_EE, w_EI], [w_IE, w_II]])

# Membrane time constants
tau_E = 0.02 
tau_I = 0.01 
tau = sp.array([tau_E, tau_I])

# external forcing
h = sp.ones(2)*0

# initial and time vector
u_0 = sp.array([-60, -80])
T_init = 0
T_final = 100
dt = 1e-3

# noise process is Ornstein-Uhlenbeck
tau_noise = 0.05
sigma = sp.array([0.2, 0.1])
sigma_scaled = sigma*(1. + tau/tau_noise)**0.5
eta_init = sp.array([1, -1])
seed = 1

##############################
######     Functions     #####
##############################



def ReLU(x, alpha=0):
    return sp.maximum(x, x*alpha*sp.ones(x.shape))

def df(u, t):
    du = ((-u + V_rest) + sp.dot(Ww, (Kk*ReLU(u - V_rest)**Nn)) + h)/tau
    return du 

def euler(u, t, dt, df):
    return u + df(u, t)*dt

    

##############################
######  Data structures  #####
##############################

    
    
Tt = sp.arange(T_init, T_final, dt)
Uu = sp.zeros((len(Tt), 2))
eta = sp.zeros((len(Tt), 2))
    
    
    
##############################
######    Integration    #####
##############################

# Generate a graph of fluctuations versus input
stds = []
mean = []
trace = []
h_range = sp.arange(0, 20, 0.5)
for h_factor in h_range:
    
    # update input
    print(h_factor)
    h = sp.ones(2)*h_factor

    # First generate noise vector
    eta[0, :] = eta_init
    sp.random.seed(seed)
    for iT, t in enumerate(Tt[:-1]):
        dt = Tt[iT + 1] - Tt[iT]
        eta[iT + 1, :] = eta[iT, :]  - eta[iT, :]*dt/tau_noise +\
                            sp.random.normal(0, sigma_scaled)*\
                            (2.*dt/tau_noise)**0.5

    # Next, integrate neural system with noise forcing
    Uu[0, :] = u_0
    for iT, t in enumerate(Tt[:-1]):
        dt = Tt[iT + 1] - Tt[iT]
        Uu[iT + 1, :] = euler(Uu[iT, :], t, dt, df) + eta[iT, :]*dt/tau
    
    # Get std and mean Vm
    stds.append(sp.std(Uu, axis=0))
    mean.append(sp.mean(Uu, axis=0))
    
    # Get the rates
    R = Kk*ReLU(Uu - V_rest)**Nn    
    trace.append(sp.mean(R, axis=0))
    


plt.subplot(1,3,1)
plt.plot(h_range, mean)
plt.ylabel('mean V_E/V_I [mV]')
plt.xlabel('h')

plt.subplot(1,3,2)
plt.plot(h_range, stds)
plt.ylabel('std. dev. V_E/V_I')
plt.xlabel('h')

plt.subplot(1,3,3)
plt.plot(h_range, trace)
plt.ylabel('mean rate')
plt.xlabel('h')

plt.show()
        