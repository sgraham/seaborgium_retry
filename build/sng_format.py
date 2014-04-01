def DEP_format(action):
  if action == 'sync':
    GitPullOrClone('https://github.com/vitaut/format.git')
  elif action == 'cflags':
    return ['-DFMT_USE_INITIALIZER_LIST=1', '-DFMT_USE_VARIADIC_TEMPLATES=1']
  elif action == 'local_cflags':
    return ['-Dmain=format_test_main']
  elif action == 'targets':
    return [('format', 'third_party/format')]
