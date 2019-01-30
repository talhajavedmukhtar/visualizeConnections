from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from . import graphHandler

import jsonpickle

# Create your views here.

def index(request):
	data = request.POST

	if "asn" in data.keys():
		newASN = data["asn"]

	return render(request,"visualize/index.html")

def getGraphForASN(request):
	asn = request.GET["asn"]

	asn = int(asn)

	passedOnGraph = request.GET["graphSoFar"]

	if(passedOnGraph):
		passedOnGraph = jsonpickle.decode(passedOnGraph)
		graphSoFar, graphAsDiv, newVictor = graphHandler.getGraphSingle(asn,G=passedOnGraph)
		print("New victor: ",newVictor)
	else:
		graphSoFar, graphAsDiv, newVictor = graphHandler.getGraphSingle(asn)
		print("New victor: ",newVictor)

	data = {"graphSoFar": jsonpickle.encode(graphSoFar), "graphAsDiv": graphAsDiv, "nextASN": newVictor}

	return JsonResponse(data,safe=False)
