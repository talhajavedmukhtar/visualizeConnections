from .getComponents import getGraphComponents
from .graph import Graph
import networkx as nx
import os

import plotly
import plotly.plotly as py
import plotly.graph_objs as go


def getOtherASN(origin,edge):
	if edge[0] == origin:
		return edge[1]
	else:
		return edge[0]

def getNewVictor(origin,nodes,edges,asnStackSoFar):
	#depth first get next victor

	for node in nodes:
		if node != origin:
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

	try:
		pos = getPosWithIntKeys(pos)
		graph.pos = pos

		labels = getLabelsWithIntKeys(graph.labels)
		graph.labels = labels
	except Exception as e:
		print("Error in getPlotlyGraph(1): ",e)

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
		print("Error in getPlotlyGraph(2): ",e)

	edge_trace = []
	for k,e in enumerate(graph.edges):
		#print("doing for edge: ",e)
		edge_trace.append(dict(type='scatter',
	             		x=[pos[e[0]][0], pos[e[1]][0]],
	             		y=[pos[e[0]][1], pos[e[1]][1]],
	              		mode='lines',
	              		line=dict(width=10, color=getColor(graph.weights[k]))))


	"""node_trace = go.Scatter(
	    x=[],
	    y=[],
	    text=[],
	    mode='markers+text',
	    hoverinfo='text',
	    marker=dict(
	        color="#52ADDA",
	        size=60,
	        line=dict(width=2)))"""

	node_trace = []


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
				

	try:
		for node in graph.nodes:
			x, y = graph.pos[node]


			node_info = graph.labels[node]
			if graph.nodeExpanded(node_info) or node_info == asn:
				color = "#39a2a6"
			else:
				color = "#B8DCE7"

			node_trace.append(dict(type='scatter',
				x=[x],
				y=[y],
				text=[node_info],
				mode='markers+text',
		    	hoverinfo='text',
		    	marker=dict(
		        	color=color,
		        	size=60,
		        	line=dict(width=2))))


			#node_trace['x'] += tuple([x])
			#node_trace['y'] += tuple([y])
	except Exception as e:
		print("This error occurred: ",e)

	"""
	try:
		for node, adjacencies in enumerate(graph.graph.adjacency()):
			node_info = graph.labels[node]
			node_trace['text']+=tuple([node_info])

			if graph.nodeExpanded(node_info):
				node_trace[]

			print("\n\n\n\n\n\n\n\n")
			print(node_info)
			print("\n\n\n\n\n\n\n\n")
	except Exception as e:
		print("Error in getPlotlyGraph(3): ",e)"""


	try:
		fig = go.Figure(data=edge_trace+node_trace+[node_trace2],
	             layout=go.Layout(
	                title='<br>Expanded from ASN#'+str(asn),
	                titlefont=dict(size=16),
	                showlegend=False,
	                hovermode='closest',
	                margin=dict(b=20,l=5,r=5,t=40),
	                annotations=[ dict(
	                    text="Added the strong links between AS'es near ASN#"+str(asn),
	                    showarrow=False,
	                    xref="paper", yref="paper",
	                    x=0.005, y=-0.002 ) ],
	                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
	                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

	except Exception as e:
		print("This the error: ",e)

	return plotly.offline.plot(fig, auto_open=False, output_type='div')

def getGraph(asn,G=None):
	if G is None:
		G = Graph(asn)

	try:
		try:
			newNodes,newEdges = getGraphComponents(asn)
		except:
			newNodes = []
			newEdges = {}
		G.updateGraph(newNodes,newEdges)

		try:
			newVictor = getNewVictor(asn,newNodes,newEdges,G.asnStack)
			if newVictor is None:
				newVictor = "noVictor"
		except Exception as e:
			print("exception was raised: ",e)
			newVictor = "noVictor"

		divContent = getPlotlyGraph(asn,G)
	except Exception as e:
		divContent = "<p>Could not grab data from server for "+str(asn)+"</p>"
		newVictor = "noVictor"

	return G, divContent, newVictor


