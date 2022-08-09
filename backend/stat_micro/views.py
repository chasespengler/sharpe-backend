from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *

@api_view(['GET', 'POST'])
def apiOverview(request):
    api_urls = {
        'Get security info':'/get-stats/<str:pk>/',
        'Add security info':'/post-stats/',
        'Edit security info':'/update-stats/<str:pk>/',
        'Delete security info':'/delete-stats/<str:pk>/',
        'Does security exist':'/exists/<str:pk>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def getStats(request, pk):
    sec = SecurityStats.objects.get(pk=pk)
    serializer = SecStatsSerializer(sec, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def postStats(request):
    serializer = SecStatsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def updateStats(request, pk):
    sec = SecurityStats.objects.get(pk=pk)
    serializer = SecStatsSerializer(instance=sec, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def deleteStats(request, pk):
    SecurityStats.objects.get(pk=pk).delete()
    return Response('Item successfully deleted.')

@api_view(['GET'])
def existStats(request, pk):
    return Response(SecurityStats.objects.filter(pk=pk).exists())