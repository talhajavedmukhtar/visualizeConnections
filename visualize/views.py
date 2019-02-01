from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from . import graphHandler

import jsonpickle

import json

# Create your views here.

def index(request):
	data = request.POST

	if "asn" in data.keys():
		newASN = data["asn"]

	return render(request,"visualize/index.html")

def getComponentsFromPOST(request):
	data = json.loads(request.body)
	asn = data["asn"]
	graphSoFar = data["graphSoFar"]

	return int(asn), graphSoFar

def getGraphForASN(request):

	try:
		asn, passedOnGraph = getComponentsFromPOST(request)
		#print("ASN: ",asn)
		#print("Graph: ",passedOnGraph)
	except Exception as e:
		print("Error: ",e)

	if(passedOnGraph):
		passedOnGraph = jsonpickle.decode(passedOnGraph)
		graphSoFar, graphAsDiv, newVictor = graphHandler.getGraphSingle(asn,G=passedOnGraph)
		#print("New victor: ",newVictor)
	else:
		graphSoFar, graphAsDiv, newVictor = graphHandler.getGraphSingle(asn)
		#print("New victor: ",newVictor)

	data = {"graphSoFar": jsonpickle.encode(graphSoFar), "graphAsDiv": graphAsDiv, "nextASN": newVictor}

	return JsonResponse(data,safe=False)
