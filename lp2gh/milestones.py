import sys

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
                            or None),
          'summary': ms.summary,
          'active': ms.is_active,
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


def import_(repo, milestones):
  o = {}
  ms = repo.milestones()
  for x in milestones:
    params = {'title': x['name'],
              'state': x['active'] and 'open' or 'closed'}
    if x['date_targeted']:
      params['due_on'] = x['date_targeted']

    if x['summary']:
      params['description'] = x['summary']

    try:
      rv = ms.append(**params)
      print rv
      url = rv['url']
      id_ = url.split('/')[-1]
      o[x['name']] = id_
    except Exception as e:
      print >> sys.stderr, e
  return o
