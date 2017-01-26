from django.shortcuts import render
from django.http import HttpResponse
import json
from controllers import SwarmingInteractionController

def index(request):
  return render(request, 'dashboards/index.html')

def get_data(request):
  dict_response = SwarmingInteractionController.callCollectCommand(
    request.GET['test_suit'],
    request.GET['tasks_limit']
  )
  json_obj = json.dumps(dict_response)
  return HttpResponse(json_obj, content_type='application/json')
