import sys
import urllib2

from github3 import client


r = client.Client(sys.argv[1], sys.argv[2]).repo(sys.argv[3], sys.argv[4])

p = (1, 20)

milestones = r.milestones()
for i in range(*p):
  print 'creating milestone %s' % i
  milestones.append(title='Foo%s' % i)

issues = r.issues()
for i in range(*p):
  try:
    print 'creating issue for milestone %s' % i
    issues.append(title='Bar %s' % i, body='Baz', milestone=i)
  except urllib2.HTTPError:
    print >> sys.stderr, 'Assigning to milestone %s failed.' % i

for i in range(*p):
  try:
    print 'creating issue without milestone, then updating to milestone %s' % i
    new_issue = issues.append(title='Qux %s' % i, body='Baz')
    issue = r.issue(new_issue['number'])
    issue.update({'milestone': i, 'state': 'closed'})
  except urllib2.HTTPError:
    print >> sys.stderr, 'Assigning to milestone %s failed.' % i
