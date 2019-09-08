import numpy as np
import cmath as cm

#A State object represents the state of a given input
class State:
    vector = None
    qubits = 0

    #given a character representing a bit, returns the vector
    def constructBits(self, char):
        bitv = list()
        if(char == '0'):
            bitv.append(1)
            bitv.append(0)
        if(char == '1'):
            bitv.append(0)
            bitv.append(1)
        if(char == '+'):
            bitv.append(1/np.sqrt(2))
            bitv.append(1/np.sqrt(2))
        if(char == '-'):
            bitv.append(1/np.sqrt(2))
            bitv.append(-(1/np.sqrt(2)))
        return np.array(bitv)

    def tensor(self, v1, v2):
        return np.kron(v1, v2)

    def constructVector(self, string, qubits):
        self.qubits = qubits

        #get our bits
        bits = list()
        for i in range(0, qubits):
            bit = self.constructBits(string[i])
            bits.append(bit)
        
        #tensor our bits
        v = bits[0]
        for i in range(1, len(bits)):
            v = self.tensor(v, bits[i])

        #the final v is returned
        return v

    #given a string representation of qubits, will construct a state object
    def __init__(self, string, qubits):
        self.vector = self.constructVector(string, qubits)

    def transform(self, mat):
        self.vector = self.vector.dot(mat)

    def getVector(self):
        return self.vector
   