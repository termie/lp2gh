import logging
import re
import os
import subprocess
import sys

from launchpadlib import launchpad


from os import mkdir
from os import chdir as cd


def die(message, *args):
  logging.error(message, *args)
  raise Exception(message)
  #sys.exit(1)


def run_command(cmd, error_ok=False, error_message=None, exit_code=False,
               redirect_stdout=True, return_proc=False, stdout=None,
               stdin=None):
  # Useful for debugging:
  logging.debug(' '.join(cmd))
  if redirect_stdout and stdout is None:
    stdout = subprocess.PIPE

  proc = subprocess.Popen(cmd, stdout=stdout, stdin=stdin)

  if return_proc:
    return proc

  if stdout == subprocess.PIPE:
    output = proc.communicate()[0]
  else:
    output = ''
    proc.wait()

  if exit_code:
    return proc.returncode
  if not error_ok and proc.returncode != 0:
    die('Command "%s" failed.\n' % (' '.join(cmd)) +
                 (error_message or output))
  return output


def branch_exists(branch):
  branches = run_command(['git','branch', '-a'])
  branches = branches.split('\n')
  matcher = re.compile(r'\s%s$' % branch)
  for x in branches:
    if matcher.search(x):
      return True
  return False


def main(proj):
  cachedir = os.path.abspath('./cachedir')
  try:
    mkdir(cachedir)
  except Exception:
    pass
  lp = launchpad.Launchpad.login_anonymously(
      'lp2gh', 'production', cachedir)
  project = lp.projects[proj]

  # do initial clone
  if not os.path.exists(proj):
    run_command(['git', 'bzr', 'clone', 'lp:%s' % proj])

  cd(proj)

  branches = [x for x in project.getBranches()]
  failures = []

  for branch in branches:
    print 'importing', branch
    parts = str(branch).split('/')

    name = parts[-1]
    owner = parts[-3]

    import_name = '%s_%s' % (owner[1:], name)
    import_name = import_name.replace('~', '-')

    try:
      if branch_exists(import_name):
        run_command(['git', 'checkout', import_name])
        run_command(['git', 'bzr', 'pull'])
      else:
        lp_name = 'lp:%s/%s/%s' % (owner, proj,name)
        run_command(['git', 'bzr', 'import', '--strip_tags', lp_name, import_name])
    except Exception as e:
      failures.append([str(branch), e])

  print failures

if __name__ == '__main__':
  main(sys.argv[1])

