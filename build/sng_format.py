def DEP_format(action):
  if action == 'sync':
    GitPullOrClone('https://github.com/vitaut/format.git')
  elif action == 'targets':
    return [('format', 'third_party/format')]
