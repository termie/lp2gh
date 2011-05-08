import os

import gflags
from launchpadlib import launchpad


FLAGS = gflags.FLAGS
gflags.DEFINE_string('project', None, 'which project to export')
gflags.DEFINE_string('username', None, 'github username')
gflags.DEFINE_string('password', None, 'github password')
gflags.DEFINE_string('repo_user', None, 'github repo user')
gflags.DEFINE_string('repo_name', None, 'github repo name')


class Client():
  def __init__(self):
    self.__conn = None

  @property
  def conn(self):
    if not self.__conn:
      cachedir = os.path.abspath('./cachedir')
      if not os.path.exists(cachedir):
        os.mkdir(cachedir)
      lp = launchpad.Launchpad.login_anonymously(
          'lp2gh', 'production', cachedir, version='devel')
      self.__conn = lp
    return self.__conn

  def project(self, name):
    return self.conn.projects[name]
