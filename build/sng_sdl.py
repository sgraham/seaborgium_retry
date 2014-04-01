def DEP_sdl(action):
  if action == 'sync':
    HgCloneOrUpdate('http://hg.libsdl.org/SDL')
    build = 'out/sdl'
    if not os.path.exists(build):
      os.makedirs(build)
    Run(['cmake',
         '-G', 'Ninja',
         '../../third_party/SDL'],
         cwd=build)
    Run(['ninja'], cwd=build)
  elif action == 'ldflags':
    return ['-Lout/sdl']
  elif action == 'libs':
    return ['-lSDL2', '-lSDL2main']
