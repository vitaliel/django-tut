from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import Snippet
from .serializers import SnippetSerializer

@csrf_exempt
def snippet_list(req):
  """
  List all code snippets, or create a new snippet
  """
  if req.method == 'GET':
    snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    return JsonResponse(serializer.data, safe=False)
  elif req.method == 'POST':
    data = JSONParser().parse(req)
    serializer = SnippetSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=201)

    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(req, pk):
  """
  Retrieve, update, or delete a code snippet
  """
  try:
    snippet = Snippet.objects.get(pk=pk)
  except Snippet.DoesNotExist:
    return HttpResponse(status=404)

  if req.method == 'GET':
    serializer = SnippetSerializer(snippet)
    return JsonResponse(serializer.data)
  elif req.method == 'PUT':
    data = JSONParser().parse(req)
    serializer = SnippetSerializer(snippet, data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)
  elif req.method == 'DELETE':
    snippet.delete()
    return HttpResponse(status=204)
