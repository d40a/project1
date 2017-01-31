import sys
import json
import os
from models import Task, Test
import tempfile
import collections
import subprocess
import shutil

class SwarmingInteractionController(object):
  # TEMP_DIR = tempfile.mkdtemp(prefix=u'dimaa_tmp')

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
    print(' '.join(cmd))
    devnull = open(os.devnull, 'w') if not verbose else None
    subprocess.check_call(cmd, stdout=devnull)


  @staticmethod
  def _getListOfTasks(test_name, limit, temp_dir, bot_os):
    list_file = os.path.join(temp_dir, 'list.json')

    supported_os = {
      'mac': 'Mac-10.9',
      'win': 'Windows-7-SP1',
      'ubuntu': 'Ubuntu-12.04',
      'android': 'Android'
    }
    bot_os_tag = ''
    if bot_os in supported_os:
      bot_os_tag = '&tags=os:' + supported_os[bot_os]

    SwarmingInteractionController.run([
        SwarmingInteractionController.SWARMING_PY_DIR, 'query',
        '--limit', limit,
        '-S', 'https://chromium-swarm.appspot.com',
        'tasks/list?state=COMPLETED&tags=name:%s%s' % (test_name, bot_os_tag),
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
  def _processResultsForAllOfTheTasks(tasks, temp_dir):
    taskdir = os.path.join(temp_dir, 'results')

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

    def build_dict_cnt_on_intervals(buckets, intervals):
      dict = collections.OrderedDict()
      for key in intervals:
        dict['< %s ms' % key[1]] = len(buckets[key])
      return dict

    runtime_buckets = {x: [] for x in intervals}
    fill_buckets(tasks, runtime_buckets, intervals)

    def convert_objects_to_serializable_in_dict(dict):
      # result is not sorted by intervals!!!!!
      result_dict = collections.OrderedDict()
      for key in dict:
        result_dict[str(key)] = []
        for val in dict[key]:
          if len(val.dict_task_id_to_runtime) == 0:
            print(val.name)
          result_dict[str(key)].append(val)

      return result_dict

    dict_response = {
      'cnt_of_tasks': len(tasks),
      'cnt_of_ran_tests': cnt_of_ran_tests,
      'buckets': convert_objects_to_serializable_in_dict(runtime_buckets),
    }

    return dict_response

  @staticmethod
  def callCollectCommand(test_suit, limit, bot_os='all'):
    temp_dir = tempfile.mkdtemp(prefix=u'dimaa_tmp')
    print(temp_dir)
    tasks = SwarmingInteractionController._getListOfTasks(test_suit, limit, temp_dir, bot_os)
    SwarmingInteractionController._processResultsForAllOfTheTasks(tasks, temp_dir)
    shutil.rmtree(temp_dir)

    response = SwarmingInteractionController._buildResponse(tasks)
    del tasks
    Test.delAll()
    Task.delAll()
    return response
