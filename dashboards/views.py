from django.shortcuts import render
from django.http import HttpResponse
import json

def index(request):
  return render(request, 'dashboards/index.html')

def get_data(request):
  json_obj = json.dumps(request.GET)
  return HttpResponse(json_obj, content_type='application/json')
# Create your views here.
