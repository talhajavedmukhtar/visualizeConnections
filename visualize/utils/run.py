from .getComponents import getGraphComponents
from .graph import Graph
import networkx as nx
import os

import plotly
import plotly.plotly as py
import plotly.graph_objs as go


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

#ASNsList = Stack()

def getOtherASN(origin,edge):
	if edge[0] == origin:
		return edge[1]
	else:
		return edge[0]

def getNewVictor(origin,nodes,edges,asnStackSoFar):
	#depth first get next victor

	for node in nodes:
		asnStackSoFar.add(node)

	return asnStackSoFar.remove()


def getColor(hegemonyVal):
	"""
	colorRange = ["#e6f9ff","#ccf2ff","#b3ecff","#99e6ff","#80dfff",
	"#66d9ff","#4dd2ff","#33ccff","#1ac6ff","#00bfff","#00ace6","#0099cc"
	,"#0086b3","#007399","#006080","#004d66","#00394d","#002633"] """#18 shades of blue

	colorRange = ["#fdffd0","#f1fbd0","#daf1c1","#c1e8aa","#95d5a8","#6ac1ae",
	"#44b0b5","#2e9ab5","#1d80b2","#1d60a4","#1d4394","#1d2b87","#151d6f",
	"#0b144c"] #14 shades

	#hegemony value is going to be in the range 0 to 1
	index = int(hegemonyVal*13)
	return colorRange[index]

def getPosWithIntKeys(posWithStringKeys):
	pos = {}

	for key in posWithStringKeys:
		pos[int(key)] = posWithStringKeys[key]

	return pos

def getLabelsWithIntKeys(labelsWithStringKeys):
	labels = {}

	for key in labelsWithStringKeys:
		labels[int(key)] = labelsWithStringKeys[key]

	return labels


def getPlotlyGraph(asn,graph):
	pos = graph.pos

	#print("Pos before: ",pos)
	try:
		pos = getPosWithIntKeys(pos)
		graph.pos = pos

		labels = getLabelsWithIntKeys(graph.labels)
		graph.labels = labels
	except Exception as e:
		print("This occurred: ",e)
	#print("Pos after: ",pos)

	dmin = 1
	ncenter = 0
	for n in pos:
	    x,y = pos[n]
	    d = (x-0.5)**2+(y-0.5)**2
	    if d < dmin:
	        ncenter = n
	        dmin = d

	try:
		p = nx.single_source_shortest_path_length(graph.graph,ncenter)
	except Exception as e:
		print("This thooo: ",e)
		print(graph.graph.nodes)
	"""
	try:
		print("About to do the deed with: ")
		print("Pos: ",graph.pos)
		print("Edges: ",graph.edges)
		print("Weights: ",graph.weights)
		print("**********")
		edge_trace = [ dict(type='scatter',
	             		x=[pos[e[0]][0], pos[e[1]][0]],
	             		y=[pos[e[0]][1], pos[e[1]][1]],
	              		mode='lines',
	              		line=dict(width=2, color=getColor(graph.weights[k])))  for k, e in enumerate(graph.edges)]
	except Exception as e:
		print("2)This is the error: ",e)"""

	"""
	print("About to do the deed with: ")
	print("Pos: ",graph.pos)
	print("Edges: ",graph.edges)
	print("Weights: ",graph.weights)
	print("**********")"""

	edge_trace = []
	for k,e in enumerate(graph.edges):
		#print("doing for edge: ",e)
		edge_trace.append(dict(type='scatter',
	             		x=[pos[e[0]][0], pos[e[1]][0]],
	             		y=[pos[e[0]][1], pos[e[1]][1]],
	              		mode='lines',
	              		line=dict(width=10, color=getColor(graph.weights[k]))))



	print("Here2")

	node_trace = go.Scatter(
	    x=[],
	    y=[],
	    text=[],
	    mode='markers+text',
	    hoverinfo='text',
	    marker=dict(
	        color="#52ADDA",
	        size=60,
	        line=dict(width=2)))

	print("Here3")

	node_trace2 = go.Scatter(
		x=[1,1],
		y=[1,1],
		marker=dict(
	        showscale=True,
	        # colorscale options
	        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
	        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
	        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
	        colorscale='YlGnBu',
	        reversescale=True,
	        color=[0,1],
	        size=0.2,
	        colorbar=dict(
	            thickness=15,
	            title='Hegemony Value for the edges',
	            xanchor='left',
	            titleside='right'
	        ),
	        line=dict(width=2)))
				
	#print("Here4")

	for node in graph.nodes:
		x, y = graph.pos[node]
		node_trace['x'] += tuple([x])
		node_trace['y'] += tuple([y])

	#print("Here5")

	try:
		for node, adjacencies in enumerate(graph.graph.adjacency()):
			#node_trace['marker']['color']+=tuple([len(adjacencies[1])])
			node_info = graph.labels[node]
			node_trace['text']+=tuple([node_info])
	except Exception as e:
		print("This for setting texts: ",e)

	print("about to make figure")

	try:
		fig = go.Figure(data=edge_trace+[node_trace]+[node_trace2],
	             layout=go.Layout(
	                title='<br>Graph originating from ASN#'+str(asn),
	                titlefont=dict(size=16),
	                showlegend=False,
	                hovermode='closest',
	                margin=dict(b=20,l=5,r=5,t=40),
	                annotations=[ dict(
	                    text="Visualizing the strong links between AS'es near ASN#"+str(asn),
	                    showarrow=False,
	                    xref="paper", yref="paper",
	                    x=0.005, y=-0.002 ) ],
	                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
	                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

	except Exception as e:
		print("This the error: ",e)
	print("figure made")

	return plotly.offline.plot(fig, auto_open=False, output_type='div')

def getGraph(asn,G=None):
	if G is None:
		G = Graph()
	else:
		print("Graph with following nodes: ",G.nodes)

	try:
		newNodes,newEdges = getGraphComponents(asn)
		print("nodes and edges snatched from the server")
		G.updateGraph(newNodes,newEdges)

		print("graph updated")

		try:
			newVictor = getNewVictor(asn,newNodes,newEdges,G.asnStack)
			if newVictor is None:
				newVictor = "noVictor"
		except:
			newVictor = "noVictor"

		print("Only plotly graph func left")

		divContent = getPlotlyGraph(asn,G)
	except Exception as e:
		divContent = "<p>Could not grab data from server for "+str(asn)+"</p>"
		newVictor = "noVictor"

	return G, divContent, newVictor

"""
originASN = 174

G = Graph()

centralASN = originASN
for i in range(1,100):
	#print("Iteration# "+str(i))
	try:
		newNodes,newEdges = getGraphComponents(centralASN)
	except Exception as e:
		print("Could not grab results from server")
		break

	if not os.path.exists("convergence/"+str(originASN)):
		os.mkdir("convergence/"+str(originASN))

	newFileName = "convergence/"+str(originASN)+"/"+str(originASN)+"--ASNGraph"+str(i)+".png"
	G.updateGraph(newNodes,newEdges,newFileName)

	getPlotlyGraph(G)

	centralASN = getNewVictor(centralASN,newNodes,newEdges)

	if centralASN is None:
		print("Converged")
		break
	else:
		print("New Victor: ",centralASN)"""



