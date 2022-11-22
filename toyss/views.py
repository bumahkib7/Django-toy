from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from toyss.models import Toy
from toyss.serializers import ToySerializer


# Create your views here.
class JSONResponse(HttpResponse):
  """
  An HttpResponse that renders its content into JSON.
  """

  def __init__(self, data, **kwargs):
    content = JSONRenderer().render(data)
    kwargs['content_type'] = 'application/json'
    super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
@api_view(['GET', 'POST'])
def toy_list(request):
  """
  If the request is a GET, we return a list of all the toys in the database. If the request is a POST, we create a
  new toy in the database

  :param request: The request object is an HttpRequest object. It contains metadata about the request, including the
  HTTP method.
  :return: The HttpResponse object is an object that contains the content that will be returned to the
  browser
  """

  if request.method == 'GET':
    toys = Toy.objects.all()
    serializer = ToySerializer(toys, many=True)
    return JSONResponse(serializer.data)

  elif request.method == 'POST':
    toy_data = JSONParser().parse(request)
    toy_serializer = ToySerializer(data=request.data)
    if toy_serializer.is_valid():
      toy_serializer.save()
      return JSONResponse(toy_serializer.data, status=201)
    return JSONResponse(toy_serializer.errors, status=400)

  return HttpResponse(status=405)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def toy_detail(request, pk):
  """
  Retrieve, update or delete a toy.

  :param request: The request object is an HttpRequest object. It contains metadata about the request, including the HTTP
  method:
  :param pk: The primary key of the toy that we want to retrieve, update or delete
  :return: The HttpResponse object is an object that contains the content that will be returned to the browser
  """

  try:
    toy = Toy.objects.get(pk=pk)
  except Toy.DoesNotExist:
    return HttpResponse(status=404)

  if request.method == 'GET':
    serializer = ToySerializer(toy)
    return JSONResponse(serializer.data)

  elif request.method == 'PUT':
    data = JSONParser().parse(request)
    serializer = ToySerializer(toy, data=data)
    if serializer.is_valid():
      serializer.save()
      return JSONResponse(serializer.data)
    return JSONResponse(serializer.errors, status=400)

  elif request.method == 'DELETE':
    toy.delete()
    return HttpResponse(status=204)

  return HttpResponse(status=405)
