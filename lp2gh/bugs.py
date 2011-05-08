import gflags

from lp2gh import client
from lp2gh import exporter
from lp2gh import labels
from lp2gh import util


FLAGS = gflags.FLAGS
gflags.DEFINE_boolean('only_open_bugs', False,
                      'should we include closed bugs')


BUG_STATUS = ['New',
              'Incomplete',
              'Invalid',
              "Won't Fix",
              'Confirmed',
              'Triaged',
              'In Progress',
              'Fix Committed',
              'Fix Released']


BUG_CLOSED_STATUS = ['Invalid',
                     "Won't Fix",
                     'Fix Released']


BUG_IMPORTANCE = ['Critical',
                  'High',
                  'Medium',
                  'Low',
                  'Wishlist',
                  'Undecided']


def message_to_dict(message):
  owner = message.owner
  return {'owner': owner.name,
          'content': message.content,
          'date_created': util.to_timestamp(message.date_created),
          }


def bug_task_to_dict(bug_task):
  bug = bug_task.bug
  assignee = bug_task.assignee
  owner = bug_task.owner
  messages = list(bug.messages)[1:]
  milestone = bug_task.milestone
  duplicates = bug.duplicates
  duplicate_of = bug.duplicate_of
  return {'id': bug.id,
          'status': bug_task.status,
          'importance': bug_task.importance,
          'assignee': assignee and assignee.name or None,
          'owner': owner.name,
          'milestone': milestone and milestone.name,
          'title': bug.title,
          'description': bug.description,
          'duplicate_of': duplicate_of and duplicate_of.id or None,
          'duplicates': [x.id for x in duplicates],
          'date_created': util.to_timestamp(bug_task.date_created),
          'comments': [message_to_dict(x) for x in messages],
          'tags': bug.tags,
          'security_related': bug.security_related,
          'lp_url': bug.web_link,
          }


def list_bugs(project, only_open=None):
  if only_open is None:
    only_open = FLAGS.only_open_bugs
  return project.searchTasks(status=only_open and None or BUG_STATUS)


def translate_auto_links(bug, bug_mapping):
  """Update references to launchpad bug numbers to reference issues."""
  bug['description'] = bug['description'] + '\nTRANSLATED'
  return bug


def add_summary(bug, bug_mapping):
  """Add the summary information to the bug."""
  bug['description'] = bug['description'] + '\nSUMMARY'
  return bug

def export(project, only_open=None):
  o = []
  c = client.Client()
  p = c.project(project)
  e = exporter.Exporter()
  bugs = list_bugs(p, only_open=only_open)
  for x in bugs:
    e.emit('fetching %s' % x.title)
    rv = bug_task_to_dict(x)
    o.append(rv)
  return o


def import_(repo, bugs, milestones_map=None):
  e = exporter.Exporter()
  # set up all the labels we know
  for status in BUG_STATUS:
    try:
      e.emit('create label %s' % status)
      labels.create_label(repo, status)
    except Exception:
      pass

  for importance in BUG_IMPORTANCE:
    try:
      e.emit('create label %s' % importance)
      labels.create_label(repo, importance)
    except Exception:
      pass

  tags = []
  for x in bugs:
    tags.extend(x['tags'])
  tags = set(tags)
  for tag in tags:
    try:
      e.emit('create label %s' % tag)
      labels.create_label(repo, tag)
    except Exception:
      pass

  mapping = {}
  # first pass
  issues = repo.issues()
  for bug in bugs:
    e.emit('create issue %s' % bug['title'])
    params = {'title': bug['title'],
              'body': bug['description'],
              'labels': bug['tags'] + [bug['importance']] + [bug['status']],
              'created_at': bug['date_created'],
              }

    if bug['milestone']:
      params['milestone'] = milestones_map[bug['milestone']],

    rv = issues.append(**params)
    mapping[bug['id']] = rv['number']

  # second pass
  for bug in bugs:
    e.emit('second pass on issue %s' % bug['title'])
    bug = translate_auto_links(bug, mapping)
    bug = add_summary(bug, mapping)
    issue_id = mapping[bug['id']]
    issue = repo.issue(issue_id)
    params = {'body': bug['description']}
    if bug['status'] in BUG_CLOSED_STATUS:
      params['state'] = 'closed'
    issue.update(params)

    comments = repo.comments(issue_id)
    for msg in bug['comments']:
      # TODO(termie): username mapping
      by_line = '(by %s)' % msg['owner']
      comments.append(body='%s\n%s' % (by_line, msg['content']))
