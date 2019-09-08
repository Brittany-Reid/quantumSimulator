import State
import Wire
import Circuit

#A class to process input
class Input:
    qubits = 0
    inputs = 0
    circuit = Circuit.Circuit()
    states = list()

    def __init__(self):
        self.qubits = 0
        self.inputs = 0

    #this function reads a file and stores the information within an input object
    def readFile(self, filename):
        i = 0

        with open(filename) as fp:
            for line in fp:
                #trim line
                line = line.strip()

                #first line, how many qubits
                if(i == 0):
                    self.qubits = int(line)
                #for the number of bits, there will be a wire
                elif(i <= self.qubits):
                    wire = Wire.Wire(line)
                    self.circuit.append(wire)
                #the line after specifies number of inputs
                elif(i == self.qubits+1):
                    self.inputs = int(line)
                #for the number of inputs
                elif(i <= self.qubits+1+self.inputs):
                    state = State.State(line, self.qubits)
                    self.states.append(state)
                i+=1

    #returns the list of initial states
    def getStates(self):
        return self.states

    def getCircuit(self):
        return self.circuit