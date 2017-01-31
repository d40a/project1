from django.shortcuts import render
from django.http import HttpResponse
import json
from controllers import InteractionWithSwarmingController
from django.template import Context, Template
import collections

def index(request):
  oss_dict = collections.OrderedDict()
  oss_dict['all'] = {
    'name': 'mixed',
    'checked': 'checked',
    'disabled': '',
    'innerHtml': 'Mixed',
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
  runtimes_of_tests = InteractionWithSwarmingController.run_test_suit_and_get_runtimes(
    request.GET['test_suit'],
    request.GET['tasks_limit'],
    request.GET['os'],
  )
  dict_response = {
    'tests': runtimes_of_tests,
  }
  json_obj = json.dumps(dict_response, default=lambda o: o.__dict__)
  return HttpResponse(json_obj, content_type='application/json')
