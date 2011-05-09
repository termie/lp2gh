import re


invalid_re = re.compile(r'[^a-zA-Z0-9_ ,.\-]')


def create_label(repo, label, color=None):
  labels = repo.labels()
  params = {'name': translate_label(label)}
  if color:
    params['color'] = color
  return labels.append(**params)


def translate_label(label):
  """GitHub only allows certain characters in labels.

  Specifically, alphanum and _ ,.-

  """
  return invalid_re.sub('_', label)
