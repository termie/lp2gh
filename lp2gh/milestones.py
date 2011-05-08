import gflags

from lp2gh import client
from lp2gh import exporter
from lp2gh import util


FLAGS = gflags.FLAGS
gflags.DEFINE_boolean('only_active_milestones', False,
                      'should we include closed bugs')



def milestone_to_dict(ms):
  date_targeted = ms.date_targeted
  return {'name': ms.name,
          'date_targeted': (date_targeted and util.to_timestamp(date_targeted)
                            or None)
          }


def list_milestones(project, only_active=None):
  if only_active is None:
    only_active = FLAGS.only_active_milestones
  if only_active:
    return project.active_milestones
  return project.all_milestones


def export(project, only_active=None):
  o = []
  c = client.Client()
  p = c.project(project)
  e = exporter.Exporter()
  milestones = list_milestones(p, only_active=only_active)
  for x in milestones:
    e.emit('fetching %s' % x.title)
    rv = milestone_to_dict(x)
    o.append(rv)
  return o
