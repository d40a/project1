import sys
import json
import os
from models import Task, Test
import tempfile
import collections
import subprocess

class SwarmingInteractionController(object):
  TEMP_DIR = tempfile.mkdtemp(prefix=u'dimaa_tmp')

  SWARMING_PY_DIR = r'/usr/local/google/home/dimaa/dev/luci-py/client/swarming.py'
  # From example/common.py:

  @staticmethod
  def run(cmd, verbose):
    """Prints the command it runs then run it."""
    cmd = cmd[:]
    cmd.extend(['--verbose'] * verbose)
    cmd = [sys.executable, os.path.join(cmd[0])] + cmd[1:]
    if sys.platform != 'win32' and verbose:
      cmd = ['time', '-p'] + cmd
    devnull = open(os.devnull, 'w') if not verbose else None
    subprocess.check_call(cmd, stdout=devnull)


  @staticmethod
  def _getListOfTasks(test_name, limit):
    list_file = os.path.join(SwarmingInteractionController.TEMP_DIR, 'list.json')
    SwarmingInteractionController.run([
        SwarmingInteractionController.SWARMING_PY_DIR, 'query',
        '--limit', limit,
        '-S', 'https://chromium-swarm.appspot.com',
        'tasks/list?state=COMPLETED&tags=name:%s' % (test_name),
        '--json', list_file
    ], verbose=False)
    tasks = []
    with open(list_file, 'rb') as f:
      jsonf = json.load(f)
      for task in jsonf['items']:
        task_id = task['task_id']
        tasks.append(Task(task_id))

    if len(tasks) == 0:
      sys.stderr.write('No matching task found.')
      sys.exit(1)
    return tasks


  @staticmethod
  def _processResultsForAllOfTheTasks(tasks):
    taskdir = os.path.join(SwarmingInteractionController.TEMP_DIR, 'results')

    SwarmingInteractionController.run([
        SwarmingInteractionController.SWARMING_PY_DIR, 'collect',
        '-S', 'https://chromium-swarm.appspot.com',
        # '--no-log',
        '--task-output-dir', taskdir
    ] + [ task.id for task in tasks ], verbose=False)

    os.system("ls %s" % taskdir)

    for i in range(len(tasks)):
      resultname = os.path.join(taskdir, str(i), 'output.json')
      tasks[i].process(resultname)

  @staticmethod
  def _buildResponse(tasks):
    # TODO: make user able to adjust number of intervals
    intervals = [
      (0., 1.),
      (1., 10.),
      (10., 50.),
      (50., 100.),
      (100., 500.),
      (500., 1000.),
      (1000., 10000.),
      (10000., 100000000.),
    ]

    def fill_buckets(tasks, buckets, intervals):
      for task in tasks:
        for test in task.all_tests:
          rn = test.getRuntime(task.id)
          if rn == -1: continue

          def belongs_to_interval(rn, intervals):
            for interval in intervals:
              if interval[0] <= rn and interval[1] >= rn:
                return interval
            return (10000., 100000000.)

          interval = belongs_to_interval(rn, intervals)
          buckets[interval].append(test)

    cnt_of_ran_tests = 0
    for t in tasks:
      cnt_of_ran_tests += len(t.all_tests)

    def build_interval_cnt_dict(buckets, intervals):
      dict = collections.OrderedDict()
      for key in intervals:
        dict['< %s ms' % key[1]] = len(buckets[key])
      return dict

    runtime_buckets = {x: [] for x in intervals}
    fill_buckets(tasks, runtime_buckets, intervals)

    dict_response = {
      'cnt_of_tasks': len(tasks),
      'cnt_of_ran_tests': cnt_of_ran_tests,
      'buckets': build_interval_cnt_dict(runtime_buckets, intervals),
    }
    return dict_response

  @staticmethod
  def callCollectCommand(test_suit, limit):
    tasks = SwarmingInteractionController._getListOfTasks(test_suit, limit)
    SwarmingInteractionController._processResultsForAllOfTheTasks(tasks)
    return SwarmingInteractionController._buildResponse(tasks)
