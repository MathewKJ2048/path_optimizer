class Path:
    start = None
    end = None
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, p): # check if p lies in path
        if (p.x-self.start.x)*(self.end.x-p.x) >= 0:
            return True
        return False
    
    def toString(self):
        return self.start.toString()+" - "+self.end.toString()