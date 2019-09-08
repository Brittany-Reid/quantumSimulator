 #An object representing a wire. For now this is just a wrapper for a String.
class Wire:
    wire = None

    def __init__(self, wire):
        self.wire = wire
    
    def getWire(self):
        return self.wire

    def steps(self):
        return len(self.wire)

    def opAt(self, pos):
        return self.wire[pos]
    
    def isOpAt(self, pos):
        if self.opAt(pos) == '-':
            return False
        else:
            return True