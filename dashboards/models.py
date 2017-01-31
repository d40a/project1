from __future__ import unicode_literals

from django.db import models
import json
import sys


class Test:

  def __init__(self, name, task_id, runtime):
    self.name = name
    self.task_id = task_id
    self.runtime = runtime


class Task:

  def __init__(self, task_id):
    self.id = task_id
    self.all_tests = []


  def process(self, filename):
    """Reads json data from |filename|.

    """
    # e.g. /tmp/bisect-content_unittestshMDyOp/results/0/output.json

    with open(filename, 'rb') as f:
      jsonf = json.load(f)

      assert len(jsonf['per_iteration_data']) == 1, "Oops. Check again"
      all_results = jsonf['per_iteration_data'][0]
      for test_name in all_results:
        test_results = all_results[test_name]
        for res in test_results:
          runtime = res['elapsed_time_ms']
          test = Test(test_name, self.id, runtime)
          self.all_tests.append(test)
