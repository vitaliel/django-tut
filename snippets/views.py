from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Snippet
from .serializers import SnippetSerializer

@api_view(['GET', 'POST'])
def snippet_list(req, format=None):
  """
  List all code snippets, or create a new snippet
  """
  if req.method == 'GET':
    snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    return Response(serializer.data)
  elif req.method == 'POST':
    serializer = SnippetSerializer(data=req.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(req, id=None, format=None):
  """
  Retrieve, update, or delete a code snippet
  """
  try:
    snippet = Snippet.objects.get(pk=id)
  except Snippet.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if req.method == 'GET':
    serializer = SnippetSerializer(snippet)
    return Response(serializer.data)

  elif req.method == 'PUT':
    serializer = SnippetSerializer(snippet, data=req.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  elif req.method == 'DELETE':
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
