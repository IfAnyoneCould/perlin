import math

class Perlin:

    permutation = [151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,
    190, 6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,
    88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,
    77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,
    102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,
    135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,
    5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,
    223,183,170,213,119,248,152, 2,44,154,163, 70,221,153,101,155,167, 43,172,9,
    129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,
    251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,
    49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,
    138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]

    def __init__(self,*coords):

        self.p = []

        for i in range(512):
            self.p.append(self.permutation[i%256])

        self.dim = len(coords)
        self.point = list(i for i in coords)
        self.corners = self.GetCorners()
        self.gradientVectors = self.GenGradientVectors()
        self.distanceVectors = self.GetDistanceVectors()
        
    def GetCorners(self):
        corners = []
        for i in range(2 ** self.dim):
            next = list(int(d) for d in f"{i:0{self.dim}b}")
            for o in range(self.dim):
                if next[o] == 0: next[o] = -1
            corners.append(next) 
        return corners

    def GenGradientVectors(self):
        #gen pairs
        pairs = []
        corners = self.corners[:]
        for c in corners:
            other = c[:]
            for d in range(self.dim):
                other[d] = -other[d]
                pairs.append([c,other])
                if other in corners: corners.remove(other)
                other = c[:]

        #gen edges
        edges = []
        for p in pairs:
            edge = []
            for i in range(self.dim):
                edge.append(int((p[0][i] + p[1][i])/2))
            edges.append(edge)
            
        return edges

    def GetDistanceVectors(self):
        dist = []
        for c in self.corners:
            this = [i for i in range(self.dim)]
            for d in this:
                this[d] = (self.point[d] % 1) - c[d]
            dist.append(this)
        return dist

    def Perlin(self):

        #get bound coord values
        bound = []
        for d in range(self.dim):
            bound.append(int(math.floor(self.point[d])) & 255)

        #get corner hashes and use them to get gradient values
        gradient = []
        for c in range(len(self.corners)):
            addVal = f"{c:0{self.dim}b}"[::-1]
            hash = 0
            for i in range(self.dim):
                hash = self.p[hash + bound[i] + int(addVal[i])]
            gradient.append(self.gradientVectors[hash % (self.dim * 2 ** (self.dim-1))])

        #calculate final influence values
        influence = []
        for c in range(len(self.corners)):
            dimInfluence = 0
            addVal = f"{c:0{self.dim}b}"[::-1]
            for d in range(self.dim):
                dimInfluence += gradient[c][d] * (self.distanceVectors[c][d] - int(addVal[d]))
            influence.append(dimInfluence)

        def Fade(val):
            return val * val * val * (val * (val * 6 - 15) + 10)

        def Lerp(a,b,c):
            return a + (b - a) * c

        ranDimVals = []
        for d in range(self.dim):
            ranDimVals.append(Fade(self.point[d]%1))
       
        #putting everything together, idk why this is the way it is lmao
        self.count = 0
        def RecursiveAvg(d,c):
            if d == 0:
                self.count += 1
                return influence[c]
            val = Lerp(RecursiveAvg(d-1,self.count),RecursiveAvg(d-1,self.count),ranDimVals[d-1])
            return val

        final = RecursiveAvg(self.dim,self.count)
        print(final)
        return final




