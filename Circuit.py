import Wire
import State
import Gates
import numpy as np

#An object representing a circuit. Can run states through itself.
class Circuit:
    wires = list()

    def __init__(self):
        self.wires = list()
    
    #Adds a wire to the circuit
    def append(self, wire):
        self.wires.append(wire)

    #This funcion swaps bits upwards for the given distance
    def moveUp(self, state, distance, bit):
        for i in range(0, distance):
            #the positions to swap
            a = bit-i
            b = a-1

            #get and apply matrix
            mat = self.getCMatrix(a, b, Gates.SWAP)
            state.transform(mat)

        return state

        #This funcion swaps bits upwards for the given distance
    def moveDown(self, state, distance, bit):
        for i in range(0, distance):
            #the positions to swap
            a = bit+i
            b = a+1

            #get and apply matrix
            mat = self.getCMatrix(a, b, Gates.SWAP)
            state.transform(mat)

        return state


    def getCMatrix(self, cpos, bpos, gate):
        operations = list()

        #get list of operations
        for j in range(0, len(self.wires)):

            #for non operating values            
            if j != cpos and j != bpos :
                operations.append(Gates.IDENTITY)

            #for operating value            
            if j == cpos :
                operations.append(gate)

        #then construct the matrix
        mat = np.array([])
        for j in range(0, len(operations)):

            #construct our matrix
            if len(mat) == 0:
                mat = operations[j]
            else:
                mat = np.kron(mat, operations[j])

        return mat

    #constructs the operation matrix
    def getMatrix(self, step):
        operations = list()

        #go through wires and collect gates
        for i in range(0, len(self.wires)):
            #get operation
            op = self.wires[i].opAt(step)
            operations.append(Gates.getGate(op))

        mat = np.array([])
        for i in range(0, len(operations)):
                #construct our matrix
                if len(mat) == 0:
                    mat = operations[i]
                else:
                    mat = np.kron(mat, operations[i])
        
        return mat
                

    #handles control bits, its a bit messy but it just chains some operations
    def control(self, state, pos, step):
        swap = False
        bPos = 0
        newb = 0
        newc = 0
        distance = 0

        #how many non-control operations?
        num=0
        for i in range(0, len(self.wires)):
            op = self.wires[i].opAt(step)
            if op != 'o' and op != '-':
                num+=1
            
        #there must be an op, cancel
        if num == 0:
            return state
            
        #if there is only 1 and we have 2 qubits, we only need to deal with binary swaps
        if num == 1 and state.qubits == 2:
            #get the operation
            for i in range(0, len(self.wires)):
                op = self.wires[i].opAt(step)
                if op != 'o':
                    if i != 1:
                        swap = True
                    break
                    
            #if we need to swap
            if swap == True:
                mat = Gates.SWAP
                state.transform(mat)

            #get the c gate
            mat = Gates.getCGate(op)

            #transform
            state.transform(mat)

            #make sure we swap back
            if swap == True:
                mat = Gates.SWAP
                state.transform(mat)

        else:
            #go through all wires
            for i in range(0, len(self.wires)):
                op = self.wires[i].opAt(step)

                #process each c op at a time
                if op != 'o' and op != '-':
                    #get the position of the bit to change
                    bPos = i

                    #simple case, the two bits are adjacent and in order
                    if(bPos == pos + 1):
                        swap == False  
                    
                    #adjacent but out of order
                    elif(bPos == pos-1):
                        mat = self.getCMatrix(pos, bPos, Gates.SWAP)
                        state.transform(mat)
                    
                    #op is below control
                    elif(bPos > pos):
                        #get the distance, this will be the number of swaps
                        distance = bPos-(pos+1)
                        state = self.moveUp(state, distance, bPos)

                    #op is above control
                    elif(bPos < pos):
                        #move op down
                        distance = pos - (bPos+1)
                        state = self.moveDown(state, distance, bPos)
                        #then flip op and control
                        mat = self.getCMatrix(pos, bPos+distance, Gates.SWAP)
                        state.transform(mat)

                    #any other case just return, not yet implemented
                    else:
                        return state

                    #preform control op
                    mat = self.getCMatrix(pos, bPos, Gates.getCGate(op))
                    state.transform(mat)

                    #if we did any swapping
                    if(bPos == pos-1):
                        mat = self.getCMatrix(pos, bPos, Gates.SWAP)
                        state.transform(mat)
                    elif(bPos > pos):
                        #do the reverse, move down
                        state = self.moveDown(state, distance, bPos-distance)
                    elif(bPos < pos):
                        #flip op and control
                        mat = self.getCMatrix(pos, bPos+distance, Gates.SWAP)
                        #then move op back up
                        state = self.moveUp(state, distance, bPos+distance)
                        state.transform(mat)

        return state

    #Processes a step
    def processStep(self, step, state):
        operations = list()
        control = False
        conp = 0

        #first, check over all wires for a control
        for i in range(0, len(self.wires)):
            op = self.wires[i].opAt(step)
            if op == 'o':
                #if we have multiple controls, cancel
                if control == True:
                    return state

                control = True
                conp = i

        if control == True:
            state = self.control(state, conp, step)

        #if no control, process this step as normal
        if control == False:

            mat = self.getMatrix(step)

            #apply matrix to our state vector
            state.transform(mat)

        #return the changed state    
        return state
    
    #Runs a single state through the circuit
    def runSingle(self, state):
        states = list()
        steps = self.wires[0].steps()

        #for each step in the wire
        for i in range(0, steps):

            #first, check that there is a valid op
            noOp = True
            for j in range(0, len(self.wires)):
                if self.wires[j].isOpAt(i) == True:
                    noOp = False
                    break
            
            #if there isn't skip this step
            if(noOp == True): continue

            state = self.processStep(i, state)
            states.append(state.getVector())

        #return the list of states at each step    
        return states

    #Runs a list of inputs through the ciruit
    def run(self, states):
        stateList = list()
        #pass to a function that runs an individual input
        for i in range(0, len(states)):
            stateList.append(self.runSingle(states[i]))
        
        #return our list of intermediate states
        return stateList
        