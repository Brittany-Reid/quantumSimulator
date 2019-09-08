import numpy
import sys
import Input

#get command line argument, the file name
file = sys.argv[1]

#read this file and store the information in an input object
input = Input.Input()
input.readFile(file)

circuit = input.getCircuit()
states = input.getStates()

stateList = circuit.run(states)

for i in range(0, len(stateList)):
    inputStates = stateList[i]
    for j in range(0, len(inputStates)):
        print(inputStates[j])