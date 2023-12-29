class Point:
    x=0
    y=0
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def toString(self):
        return '('+str(int(self.x))+","+str(int(self.y))+")"