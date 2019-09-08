import numpy as np

#contains gates

IDENTITY = np.array([[1, 0],[0, 1]])
NOT = np.array([[0, 1],[1, 0]])
PAULIY = np.array([[0, 1],[-1, 0]])
PHASESHIFT= np.array([[1, 0],[0, -1]])
HADAMARD = np.array([[(1/np.sqrt(2)), (1/np.sqrt(2))],[(1/np.sqrt(2)), -(1/np.sqrt(2))]])
CNOT = np.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 0, 1],[0, 0, 1, 0]])
CY = np.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 0, 1],[0, 0, -1, 0]])
CZ = np.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, -1]])
CH = np.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, (1/np.sqrt(2)), (1/np.sqrt(2))],[0, 0, (1/np.sqrt(2)), -(1/np.sqrt(2))]])
SWAP = np.array([[1, 0, 0, 0],[0, 0, 1, 0],[0, 1, 0, 0],[0, 0, 0, 1]])

def getCGate(op):
    if op == 'X':
        return CNOT
    if op == 'Y':
        return CY
    if op == 'Z':
        return CZ
    if op == 'H':
        return CH

def getGate(op):
    if(op == 'X'):
        return NOT
    #no op adds an idenity
    elif(op == '-'):
        return IDENTITY
    #for testing we can also just specify identity
    elif(op == 'I'):
        return IDENTITY
    elif(op == 'Y'):
        return PAULIY
    elif(op == 'Z'):
        return PHASESHIFT
    elif(op == 'H'):
        return HADAMARD
    #just in case, default no doing nothing
    else:
        return IDENTITY