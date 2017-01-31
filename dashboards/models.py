from __future__ import unicode_literals

from django.db import models
import json
import sys

# Create your models here.

class Test:
  __all = {}

  @staticmethod
  def Get(name):
    return Test.__all[name] if name in Test.__all else Test(name)

  @staticmethod
  def ForEach(fn):
    for name in Test.__all:
      fn(Test.__all[name])

  @staticmethod
  def delAll():
    Test.__all.clear()

  def __init__(self, name):
    self.name = name
    self.fail = []
    self.success = []
    self.crash = []
    self.timeout = []
    self.exit_failure = []
    self.disabled = False
    self.dict_task_id_to_runtime = {} # right now we suppose that test ran once for each task
    Test.__all[name] = self

  def AddRun(self, task_id, runtime):
    self.dict_task_id_to_runtime[task_id] = runtime

  # def AddSuccess(self, task_id): self.success.append(task_id)
  # def AddFail(self, task_id): self.fail.append(task_id)
  # def AddCrash(self, task_id): self.crash.append(task_id)
  # def AddTimeout(self, task_id): self.timeout.append(task_id)
  # def AddExitFilure(self, task_id): self.exit_failure.append(task_id)
  # def HasFailure(self):
  #   return len(self.fail) > 0 or len(self.crash) > 0 or len(self.timeout) > 0 \
  #          or len(self.exit_failure) >0

  def getRuntime(self, task_id):
    if task_id in self.dict_task_id_to_runtime:
      return self.dict_task_id_to_runtime[task_id]
    return -1

class Task:
  __all = {}

  @staticmethod
  def Get(name):
    return Task.__all[name] if name in Task.__all else None

  @staticmethod
  def delAll():
    Task.__all.clear()

  def __init__(self, task_id):
    self.id = task_id
    self.os = 'unknown'
    self.mode = 'unknown'
    self.cpu = '0 bit'
    Task.__all[task_id] = self
    self.all_tests = []

  def process(self, filename):
    """Reads json data from |filename|.

    """
    # e.g. /tmp/bisect-content_unittestshMDyOp/results/0/output.json

    with open(filename, 'rb') as f:
      jsonf = json.load(f)
      # self.all_tests = jsonf["all_tests"]
      if 'global_tags' not in jsonf:
        sys.stderr.write('Unable to read info for %s' % self.id)
      else:
        global_tags = jsonf['global_tags']
        self.mode = 'Release' if 'MODE_RELEASE' in global_tags else 'Debug'
        self.cpu = '64bit' if 'CPU_64_BITS' in global_tags else '32bit'
        if self.os == 'unknown':
          if 'OS_MAC' in global_tags:
            self.os = 'mac'
          elif 'OS_WIN' in global_tags:
            self.os = 'win'
          elif 'OS_LINUX' in global_tags:
            self.os = 'linux'


      assert len(jsonf['per_iteration_data']) == 1, "Oops. Check again"
      all_results = jsonf['per_iteration_data'][0]
      for test_name in all_results:
        test_results = all_results[test_name]
        test = Test.Get(test_name)
        self.all_tests.append(test)
        for res in test_results:
          # if res['status'] == 'SUCCESS':
          #   test.AddSuccess(self.id)
          # elif res['status'] == 'FAILURE':
          #   test.AddFail(self.id)
          # elif res['status'] == 'CRASH':
          #   test.AddCrash(self.id)
          # elif res['status'] == 'TIMEOUT':
          #   test.AddTimeout(self.id)
          # elif res['status'] == 'FAILURE_ON_EXIT':
          #   test.AddExitFilure(self.id)
          # else:
          #   sys.stderr.write('Unknown status: %s\n' % res['status'])
          # # suppose that test_results contains only one element, in other case we need take a look more deeply
          runtime = res['elapsed_time_ms']
          test.AddRun(self.id, runtime)
