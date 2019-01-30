from ihr.hegemony import Hegemony

def getGraphComponents(originASN):
	hege = Hegemony(originasns=[originASN], start="2018-02-09 00:00", end="2018-02-09 00:00")

	nodes = [originASN]
	edgesWithWeights = {}


	for r in hege.get_results():
		for chunk in r:
			asnName = chunk["asn"]
			if asnName not in nodes:
				nodes.append(asnName)

				hegemonyVal = chunk["hege"]

				edgeF = (originASN,asnName)
				edgeR = (asnName,originASN)

				if (edgeF not in edgesWithWeights.keys()) and (edgeR not in edgesWithWeights.keys()):
					edgesWithWeights[(edgeF)] = hegemonyVal

	return (nodes,edgesWithWeights)



