from graphviz import Graph
 
def convexComb (k, u, v):
    if not len(u) == len(v):
        raise ValueError("vectors need to have same length")
    ans = []
    for i in range(len(u)):
        ans.append((1 - k) * u[i] + k * v[i])
    return ans
 
class Animator:
    def __init__ (self, path, fname, xl, xr, yl, yr):
        self.vertices = {}
        self.edges = {}
        self.frameID = 0
        self.path = path
        self.fname = fname
        self.xlMargin = xl
        self.xrMargin = xr
        self.ylMargin = yl
        self.yrMargin = yr
 
    def addVertex (self, name, **attrs):
        self.vertices[name] = attrs
 
    def setVertexAttr (self, name, attr, val):
        self.vertices[name][attr] = val
 
    def setVertexPos (self, name, x, y):
        self.vertices[name]["pos"] = str(x) + "," + str(y) + "!"
 
    def addEdge (self, u, v, fillRate, **attrs):
        self.edges[(u, v)] = [0, fillRate, attrs]
 
    def setFillRate (self, u, v, fillRate):
        self.edges[(u, v)][1] = fillRate
 
    def setFillDir (self, u, v, fillDir):
        self.edges[(u, v)][0] = fillDir
 
    def draw (self):
        G = Graph(format="png", engine="neato", directory = self.path)
        G.attr("node", shape="circle", width="0.75", height="0.75", fixedsize="true", fontsize="22")
        G.attr(splines="true", overlap="false", sep="2")
 
        G.node("dlMargin", pos = str(self.xlMargin) + "," + str(self.ylMargin) + "!",
               color = "white", fontcolor = "white")
        G.node("drMargin", pos = str(self.xrMargin) + "," + str(self.ylMargin) + "!",
               color = "white", fontcolor = "white")
        G.node("ulMargin", pos = str(self.xlMargin) + "," + str(self.yrMargin) + "!",
               color = "white", fontcolor = "white")
        G.node("urMargin", pos = str(self.xrMargin) + "," + str(self.yrMargin) + "!",
               color = "white", fontcolor = "white")
 
        for (name, attrs) in self.vertices.items():
            G.node(name, **attrs)
            
        for (u, v), (fillDir, fillRate, attrs) in self.edges.items():
            if fillRate > 0.005:
                if fillDir == 0:
                    G.edge(u, v, **attrs, penwidth = "4", color = "red;" + str(fillRate) + ":blue")
                else:
                    G.edge(v, u, **attrs, penwidth = "4", color = "red;" + str(fillRate) + ":blue")
            else:
                if fillDir == 0:
                    G.edge(u, v, **attrs, penwidth = "1", color = "blue")
                else:
                    G.edge(v, u, **attrs, penwidth = "1", color = "blue")

        G.render(self.fname + str(self.frameID).zfill(4))
        self.frameID += 1
 
    def sleep (self, frames):
        for i in range(frames):
            self.draw()
 
    def moveVertices (self, targets, steps = 40):
        for vertex in targets:
            if not "pos" in self.vertices[vertex]:
                raise ValueError("vertex does not have set position")
 
        currents = {}
        for vertex in targets:
            currents[vertex] = list(map(int, self.vertices[vertex]["pos"].replace("!", "").split(",")))
 
        for k in range(1, steps + 1):
            for vertex in targets:
                cc = convexComb(k / steps, currents[vertex], targets[vertex])
                self.setVertexPos(vertex, cc[0], cc[1])
            self.draw()         
 
    def fillEdge (self, u, v, step = 0.05):
        (p, q) = (u, v)
        if (u, v) in self.edges:
            self.setFillDir(u, v, 0)
            (p, q) = (u, v)
        elif (v, u) in self.edges:
            self.setFillDir(v, u, 1)
            (p, q) = (v, u)
        else:
            raise ValueError("no such edge exists!")
 
        fillRate = 0
        while fillRate < 0.999:
            fillRate += step
            self.setFillRate(p, q, fillRate)
            self.draw()

def toAnimLabel (num):
    return "v" + str(num + 1)
            
class DFSAnimator:    
    def __init__ (self, inFileName, outDir, outFileName):
        fi = open(inFileName, "rt")
        (vertexc, edgec) = map(int, fi.readline().split())
        self.vertexc = vertexc
        self.edgec = edgec
 
        self.initCoords = [(0, 0) for i in range(vertexc)]
        self.finalCoords = [(0, 0) for i in range(vertexc)]
        for i in range(vertexc):
            (ix, iy, tx, ty) = map(int, fi.readline().split())
            self.initCoords[i] = [ix, iy]
            self.finalCoords[i] = [tx, ty]
        xlMargin = min(min(i[0] for i in self.initCoords),
                       min(t[0] for t in self.finalCoords)) - 1
        xrMargin = max(max(i[0] for i in self.initCoords),
                       max(t[0] for t in self.finalCoords)) + 1
        ylMargin = min(min(i[1] for i in self.initCoords),
                       min(t[1] for t in self.finalCoords)) - 1
        yrMargin = max(max(i[1] for i in self.initCoords),
                       max(t[1] for t in self.finalCoords)) + 1
 
        self.animator = Animator(outDir, outFileName, xlMargin, xrMargin, ylMargin, yrMargin)
            
        for i in range(vertexc):
            self.animator.addVertex(toAnimLabel(i), label = str(i + 1))
            self.animator.setVertexPos(toAnimLabel(i), self.initCoords[i][0], self.initCoords[i][1])
            self.animator.setVertexAttr(toAnimLabel(i), "style", "filled")
            self.animator.setVertexAttr(toAnimLabel(i), "fillcolor", "white")
 
        self.adj = [[] for i in range(vertexc)]
        for i in range(edgec):
            (u, v) = map(int, fi.readline().split())
            u = u - 1
            v = v - 1
            self.adj[u].append(v)
            self.adj[v].append(u)
            self.animator.addEdge(toAnimLabel(u), toAnimLabel(v), 0)
 
        fi.close()
 
    def drawBuildDFS (self, vertex, visited):
        visited[vertex] = True
        self.animator.setVertexAttr(toAnimLabel(vertex), "fillcolor", "green")
        self.animator.sleep(8) # TO ADJUST
        for nxt in self.adj[vertex]:
            if not visited[nxt]:
                self.animator.setVertexAttr(toAnimLabel(vertex), "fillcolor", "red")
                self.animator.fillEdge(toAnimLabel(vertex), toAnimLabel(nxt), 0.07) # TO ADJUST
                self.drawBuildDFS(nxt, visited)
                self.animator.setVertexAttr(toAnimLabel(vertex), "fillcolor", "green")
                self.animator.sleep(8) # TO ADJUST
        self.animator.setVertexAttr(toAnimLabel(vertex), "fillcolor", "red")
            
    def drawBuild (self, root):
        visited = [False for i in range(self.vertexc)]
        self.drawBuildDFS(root, visited)
 
        targets = {}
        for i in range(self.vertexc):
            targets[toAnimLabel(i)] = self.finalCoords[i]
 
        self.animator.moveVertices(targets, 60) # TO ADJUST
        self.animator.sleep(50) # TO ADJUST
    
dfsanim = DFSAnimator("graph.txt", "frames", "frame")
dfsanim.drawBuild(0)