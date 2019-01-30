try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx

class Stack:
    def __init__(self):
    	self.seenSoFar = []
    	self.stack = []

    def add(self, ASN):
        if ASN not in self.seenSoFar:
        	self.seenSoFar.append(ASN)
        	self.stack.append(ASN)
        	return True
        else:
            return False

    def remove(self):
        if len(self.stack) <= 0:
            return None
        else:
            return self.stack.pop()

class Graph:
	def __init__(self):
		self.graph = nx.Graph()
		self.asnStack = Stack()
		self.nodeToASNDict = {}
		self.labels = {}

		self.nodes = []
		self.edges = []
		self.weights = []

	def getASNFromNodeNo(self,nodeNo):
		for key,val in self.nodeToASNDict.items():
			if val == nodeNo:
				return int(key)
		return None

	def fixStringKeysLabels(self):
		newLabels = {}

		for key,val in self.labels.items():
			newLabels[int(key)] = val

		self.labels = newLabels

	def fixStringNodes(self):
		fixedNodes = []

		for node in self.nodes:
			fixedNodes.append(int(node))

		self.nodes = fixedNodes

		try:
			self.graph = nx.Graph()
			self.graph.add_nodes_from(fixedNodes)
		except Exception as e:
			print(e)

	def fixStringKeysDict(self):
		newDict = {}

		for key,val in self.nodeToASNDict.items():
			newDict[int(key)] = val

		self.nodeToASNDict = newDict

	def updateGraph(self,newNodes,newEdges):
		self.fixStringKeysDict()
		self.fixStringNodes()
		self.fixStringKeysLabels()


		nodesSoFar = [self.getASNFromNodeNo(x) for x in self.nodes]
		noOfNodesSoFar = len(nodesSoFar)

		#remove nodes from newNodes that are already in nodesSoFar
		cleanedNewNodes = []
		for node in newNodes:
			if node not in nodesSoFar:
				cleanedNewNodes.append(node)

		#print("Nodes so far: ",nodesSoFar)
		#print("Cleaned new nodes: ",cleanedNewNodes)

		print("")
		print("")
		print("")
		print("")
		print("Nodes so far: ",nodesSoFar)
		print("New nodes: ",newNodes)
		print("Cleaned nodes: ",cleanedNewNodes)
		print("New edges: ", newEdges)
		#print("Positions: ", self.graph.pos)
		print("")
		print("")
		print("")
		print("")

		try:
			#Add the new nodes
			for i,node in enumerate(cleanedNewNodes):
				nodeIdentifier = noOfNodesSoFar + i
				self.graph.add_node(nodeIdentifier)
				self.nodeToASNDict[node] = nodeIdentifier
				self.labels[nodeIdentifier] = node
				self.nodes.append(nodeIdentifier)

			#Add the new edges
			for i,edgeKey in enumerate(newEdges.keys()):
				node1 = self.nodeToASNDict[edgeKey[0]]
				node2 = self.nodeToASNDict[edgeKey[1]]

				self.graph.add_edge(node1,node2)

				#only save edge if it is really new
				if(node2,node1) not in self.edges:
					self.edges.append((node1,node2))
					self.weights.append(newEdges[edgeKey])
		except Exception as e:
			print("Error: ",e)


		#Get the position layout
		self.pos=nx.spring_layout(self.graph)

		#plt.clf()

		#Draw the graph so far
		#nx.draw(self.graph,self.pos,nodelist=self.nodes,node_size=2000,node_color='#52ADDA',edgelist=self.edges,edge_color=self.weights,width=10.0,edge_cmap=plt.cm.Blues,labels=self.labels)

		#And Save it!
		#plt.savefig(fileName)
