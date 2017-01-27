from django.shortcuts import render
from django.http import HttpResponse
import json
from controllers import SwarmingInteractionController
from django.template import Context, Template
import collections

def index(request):
  oss_dict = collections.OrderedDict()
  oss_dict['all'] = {
    'name': 'all',
    'checked': 'checked',
    'disabled': '',
    'innerHtml': 'All',
  }
  oss_dict['ubuntu'] = {
    'name': 'ubuntu',
    'checked': '',
    'disabled': '',
    'innerHtml': 'Ubuntu',
  }
  oss_dict['win'] = {
    'name': 'windows',
    'checked': '',
    'disabled': '',
    'innerHtml': 'Windows',
  }
  oss_dict['android'] = {
    'name': 'android',
    'checked': '',
    'disabled': '',
    'innerHtml': 'Android',
  }
  oss_dict['mac'] = {
    'name': 'mac',
    'checked': '',
    'disabled': '',
    'innerHtml': 'Mac os',
  }

  context = Context({
    'oss': oss_dict,
  })

  return render(request, 'dashboards/index.html', context)

def get_data(request):
  dict_response = SwarmingInteractionController.callCollectCommand(
    request.GET['test_suit'],
    request.GET['tasks_limit'],
    request.GET['oss'],
  )
  json_obj = json.dumps(dict_response)
  return HttpResponse(json_obj, content_type='application/json')
