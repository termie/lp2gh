import os

import gflags
from launchpadlib import launchpad


FLAGS = gflags.FLAGS
gflags.DEFINE_string('project', None, 'which project to export')


class Client():
  def __init__(self):
    self.__conn = None

  @property
  def conn(self):
    if not self.__conn:
      cachedir = './cachedir'
      if not os.path.exists(cachedir):
        os.mkdir(cachedir)
      lp = launchpad.Launchpad.login_anonymously(
          'lp2gh', 'production', cachedir)
      self.__conn = lp
    return self.__conn

  def project(self, name):
    return self.conn.projects[name]
