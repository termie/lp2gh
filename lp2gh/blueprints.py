import gflags

from lp2gh import client
from lp2gh import exporter
from lp2gh import util


FLAGS = gflags.FLAGS


IMPLEMENTATION_STATUS = ['Unknown',
                         'Not started',
                         'Deferred',
                         'Needs Infrastructure',
                         'Blocked',
                         'Started',
                         'Slow progress',
                         'Good progress',
                         'Beta Available',
                         'Needs Code Review',
                         'Deployment',
                         'Implemented']


DEFINITION_STATUS = ['Approved',
                     'Pending Approval',
                     'Review',
                     'Drafting',
                     'Discussion',
                     'New',
                     'Superseded',
                     'Obsolete']


LIFECYCLE_STATUS = ['Not started',
                    'Started',
                    'Complete']


PRIORITIES = ['Not',
              'Undefined',
              'Low',
              'Medium',
              'High',
              'Essential']


def specification_to_dict(spec):
  assignee = spec.assignee
  drafter = spec.drafter
  dependencies = spec.dependencies
  milestone = spec.milestone
  bugs = spec.bugs
  return {'assignee': assignee and assignee.name or None,
          'bugs': [x.id for x in spec.bugs],
          'definition_status': spec.definition_status,
          'dependencies': [x.name for x in spec.dependencies],
          'date_created': util.to_timestamp(spec.date_created),
          'drafter': drafter and drafter.name or None,
          'implementation_status': spec.implementation_status,
          'lifecycle_status': spec.lifecycle_status,
          'milestone': milestone and milestone.name or None,
          'name': spec.name,
          'priority': spec.priority,
          'summary': spec.summary,
          'title': spec.title,
          'whiteboard': spec.whiteboard,
          'url': spec.specification_url,
          'lp_url': spec.web_link,
          }


def list_specifications(project):
  return project.all_specifications


def export(project, only_active=None):
  o = []
  c = client.Client()
  p = c.project(project)
  e = exporter.Exporter()
  specifications = list_specifications(p)
  for x in specifications:
    e.emit('fetching %s' % x.title)
    rv = specification_to_dict(x)
    o.append(rv)
  return o
