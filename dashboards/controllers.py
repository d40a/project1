import sys
import json
import os
from models import Task, Test
import tempfile
import collections
import subprocess
import shutil

class InteractionWithSwarmingController(object):
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

    InteractionWithSwarmingController.run([
        InteractionWithSwarmingController.SWARMING_PY_DIR, 'query',
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
  def _collect(tasks, temp_dir):
    taskdir = os.path.join(temp_dir, 'results')

    InteractionWithSwarmingController.run([
        InteractionWithSwarmingController.SWARMING_PY_DIR, 'collect',
        '-S', 'https://chromium-swarm.appspot.com',
        '--no-log',
        '--task-output-dir', taskdir
    ] + [ task.id for task in tasks ], verbose=False)

    for i in range(len(tasks)):
      resultname = os.path.join(taskdir, str(i), 'output.json')
      tasks[i].process(resultname)


  @staticmethod
  def run_test_suit_and_get_runtimes(test_suit, limit, bot_os='all'):
    temp_dir = tempfile.mkdtemp(prefix=u'dimaa_tmp')

    try:
      tasks = InteractionWithSwarmingController._getListOfTasks(test_suit, limit, temp_dir, bot_os)
      InteractionWithSwarmingController._collect(tasks, temp_dir)
    finally:
      shutil.rmtree(temp_dir)

    result = []
    for task in tasks:
      result.extend(task.all_tests)
    del tasks
    return result
