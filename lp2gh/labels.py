def create_label(repo, label, color=None):
  labels = repo.labels()
  params = {'name': label}
  if color:
    params['color'] = color
  labels.append(**params)
