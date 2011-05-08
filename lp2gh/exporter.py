import sys

class Exporter(object):
  def emit(self, message):
    print >> sys.stderr, message
