# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""A ninja generator for simple projects. No configuration files, replaced by
ridiculously regimented project structure that you probably won't like.
"""

import glob
import optparse
import os
import re
import subprocess
import sys


SELF = os.path.abspath(__file__)
BASEDIR = os.path.dirname(SELF)


def Run(args, cwd=None):
  assert isinstance(args, list)
  subprocess.check_call(args, shell=True, cwd=cwd)


def GitPullOrClone(remote):
  base = os.path.splitext(os.path.basename(remote))[0]
  if not os.path.exists('third_party/%s/.git' % base):
    Run(['git', 'clone', remote], cwd='third_party')
  else:
    Run(['git', 'pull'], cwd='third_party/%s' % base)


def SvnCheckoutOrUp(remote, name, subdir=None):
  cwd = 'third_party'
  if subdir:
    cwd = os.path.join(cwd, subdir)
  if not os.path.exists('third_party/%s/.svn' % name):
    Run(['svn', 'checkout', remote, name], cwd=cwd)
  cwd = os.path.join(cwd, name)
  Run(['svn', 'up'], cwd=cwd)


def DEP_ninja(action):
  if action == 'sync':
    GitPullOrClone('https://github.com/martine/ninja.git')
    if os.path.exists('third_party/ninja/ninja.bootstrap.exe'):
      Run(['ninja.bootstrap.exe'], cwd='third_party/ninja')
    elif os.path.exists('third_party/ninja/ninja.exe'):
      Run(['ninja.exe'], cwd='third_party/ninja')
    elif os.path.exists('third_party/ninja/ninja'):
      Run(['ninja'], cwd='third_party/ninja')
    else:
      Run([sys.executable, 'bootstrap.py'], cwd='third_party/ninja')


def DEP_googletest(action):
  if action == 'sync':
    SvnCheckoutOrUp('http://googletest.googlecode.com/svn/trunk/', 'googletest')


CFLAGS = [
    '/Zi', '/W4', '/WX', '/GR-',
    '/wd4100',
    '/wd4530',
    '/wd4800',
    '/D_WIN32_WINNT=0x0501',
    '/D_CRT_SECURE_NO_WARNINGS',
    '/DNOMINMAX',
    '/Isrc',
    '/Ithird_party',
  ]
CFLAGS_DEBUG = [
    '/D_DEBUG',
    '/MDd',
  ]
CFLAGS_RELEASE = [
    '/Ox',
    '/GL',
    '/DNDEBUG',
    '/MD',
  ]
ARFLAGS = [
  ]
ARFLAGS_DEBUG = [
  ]
ARFLAGS_RELEASE = [
    '/LTCG',
  ]
LDFLAGS = [
    '/DEBUG',
  ]
LDFLAGS_DEBUG = [
  ]
LDFLAGS_RELEASE = [
    '/LTCG',
  ]


ALL_AUX_SNG = glob.glob(os.path.join(BASEDIR, 'sng_*.py'))
for helper in ALL_AUX_SNG:
  execfile(helper, globals())


def UpdateDeps():
  if not os.path.exists('third_party'):
    os.makedirs('third_party')
  for name, func in globals().iteritems():
    if name.startswith('DEP_'):
      func('sync')


def GetFromDeps(into, action):
  for name, func in globals().iteritems():
    if name.startswith('DEP_'):
      result = func(action)
      if result:
        into.extend(result)


def ForwardSlash(path):
  return os.path.normpath(path).replace('\\', '/')


def ScanForIncludeAndUpdateLibs(src_path, libs, libtags):
  with open(src_path, 'r') as f:
    contents = f.read()
    for libtag, libname in libtags:
      if libtag in contents:
        libs.add(libname)


def ScanForRCDATA(src_path):
  deps = []
  with open(src_path, 'r') as f:
    contents = f.read()
    for mo in re.finditer(r'RCDATA "(.*)"', contents):
      deps.append(ForwardSlash(mo.group(1)))
  return deps


def Compile(n, target, libtags):
  objs = []
  libs = set()
  if isinstance(target, tuple):
    root_path = target[1]
    strip_len = 0
  else:
    root_path = os.path.join('src', target)
    strip_len = 4
  for topdir, dirnames, filenames in os.walk(root_path):
    for filename in filenames:
      ext = os.path.splitext(filename)[1]
      src_path = ForwardSlash(os.path.join(topdir, filename))
      if ext in ('.cc', '.cpp', '.cxx'):
        ScanForIncludeAndUpdateLibs(src_path, libs, libtags)
        obj_path = '$builddir/' + ForwardSlash(
            src_path[strip_len:] + '.obj').replace('/', '.')
        variables = None
        if '_test' in filename or '-test' in filename:
          variables = (('cflags', '$cflags_test'),)
        n.build(obj_path, 'cxx', src_path, variables=variables)
        objs.append(obj_path)
      elif ext == '.rc':
        obj_path = '$builddir/' + ForwardSlash(
            src_path[strip_len:] + '.res').replace('/', '.')
        used = ScanForRCDATA(src_path)
        n.build(obj_path, 'rc', src_path, implicit=used)
        objs.append(obj_path)
  return objs, list(libs)


def BinaryAndRuleForTarget(target):
  if isinstance(target, tuple):
    return '$builddir/' + target[0] + '.lib', 'lib'
  if target.endswith('_dll'):
    return '$builddir/' + target[:-4] + '.dll', 'linkdll'
  elif target.endswith('_exe'):
    return '$builddir/' + target[:-4] + '.exe', 'link'
  else:
    return '$builddir/' + target + '.lib', 'lib'


def BuildLibTags(target, targets):
  libtags = []
  for t in targets:
    if target == t:
      continue
    if isinstance(t, tuple):
      libtags.append(('#include "%s/' % t[0], '$builddir/%s.lib' % t[0]))
    elif not t.endswith('_dll') and not t.endswith('_exe'):
      libtags.append(('#include "%s/' % t, '$builddir/%s.lib' % t))
  return libtags
  

def Generate(is_debug):
  if not os.path.exists('out'):
    os.makedirs('out')
  sys.path.append('third_party/ninja/misc')
  import ninja_syntax
  with open('build.ninja', 'wb') as output_file:
    n = ninja_syntax.Writer(output_file)
    n.comment('Generated by sng.py')
    n.newline()

    n.variable('ninja_required_version', '1.3')
    n.newline()

    n.comment('The arguments passed to configure.py, for rerunning it.')
    n.variable('configure_args', ' '.join(sys.argv[1:]))

    assert sys.platform == 'win32'
    n.variable('builddir', 'out')

    cflags = CFLAGS
    GetFromDeps(cflags, 'cflags')
    if is_debug:
      cflags += CFLAGS_DEBUG
      GetFromDeps(cflags, 'cflags_debug')
    else:
      cflags += CFLAGS_RELEASE
      GetFromDeps(cflags, 'cflags_release')
    n.variable('cflags', cflags)
    n.variable('rcflags', [x for x in cflags
                           if x.startswith('/I') or x.startswith('/D')] + [
                               '/I.'])

    cflags_test = cflags[:]
    cflags_test += [
        '-Ithird_party/googletest/include',
      ]
    GetFromDeps(cflags_test, 'cflags_test')
    n.variable('cflags_test', cflags_test)
    n.newline()

    arflags = ARFLAGS
    GetFromDeps(arflags, 'arflags')
    if is_debug:
      arflags += ARFLAGS_DEBUG
      GetFromDeps(arflags, 'arflags_debug')
    else:
      arflags += ARFLAGS_RELEASE
      GetFromDeps(arflags, 'arflags_release')
    n.variable('arflags', arflags)
    n.newline()

    ldflags = LDFLAGS
    GetFromDeps(ldflags, 'ldflags')
    if is_debug:
      ldflags += LDFLAGS_DEBUG
      GetFromDeps(ldflags, 'ldflags_debug')
    else:
      ldflags += LDFLAGS_RELEASE
      GetFromDeps(ldflags, 'ldflags_release')
    n.variable('ldflags', ldflags)
    n.newline()

    n.rule('cxx',
           command=('cl /nologo /showIncludes $cflags -c $in '
                    '/Fo$out /Fd$out.pdb'),
           description='CXX $out',
           deps='msvc')
    n.rule('lib',
           command='lib /nologo $arflags /out:$out $in',
           description='LIB $out')
    n.rule('link',
           command='link /nologo $in $libs $ldflags /out:$out /pdb:$out.pdb',
           description='LINK $out')
    n.rule('linkdll',
           command=('link /nologo $in $libs $ldflags /DLL '
                    '/out:$out /pdb:$out.pdb'),
           description='LINK DLL $out')
    n.rule('rc',
           command='rc /nologo /r /fo$out $rcflags $in',
           description='RC $out')
    n.newline()

    targets = [os.path.basename(x) for x in glob.glob('src/*')]
    GetFromDeps(targets, 'targets')
    all_binaries = []
    all_test_objs = []
    all_test_libs = []
    for target in targets:
      objs, libs = Compile(n, target, BuildLibTags(target, targets))
      no_test_objs = [x for x in objs if '_test' not in x and '-test' not in x]
      test_objs = [x for x in objs if '_test' in x or '-test' in x]
      all_test_objs += test_objs
      name, rule = BinaryAndRuleForTarget(target)
      n.build(name, rule, no_test_objs + libs)
      if test_objs:
        all_test_libs.append(name)
      all_binaries.append(name)

    if all_test_objs:
      gtest_obj = '$builddir/gtest-all.obj'
      gtest_main = '$builddir/gtest_main.obj'
      gtest_cflags = '$cflags_test /wd4100 /Ithird_party/googletest'
      n.build(gtest_obj, 'cxx',
              'third_party/googletest/src/gtest-all.cc',
              variables=(('cflags', gtest_cflags),))
      n.build(gtest_main, 'cxx',
              'third_party/googletest/src/gtest_main.cc',
              variables=(('cflags', gtest_cflags),))
      test_binary = '$builddir/tests.exe'
      n.build(test_binary, 'link',
              all_test_objs + [gtest_obj, gtest_main] + all_test_libs)
      all_binaries.append(test_binary)
      n.newline()

    n.comment('Regenerate build file if build script changes.')
    n.rule('configure',
           command=sys.executable + ' ' + SELF + ' ' + '$configure_args',
           generator=1)
    build_files = [SELF, 'third_party/ninja/misc/ninja_syntax.py'] + \
                  ALL_AUX_SNG
    n.build('build.ninja', 'configure', implicit=build_files)
    n.newline()

    n.build('all', 'phony', all_binaries)


def main():
  parser = optparse.OptionParser()
  parser.add_option("-d", "--debug",
                    action="store_true", dest="debug", default=False,
                    help="build Debug build (default Release)")
  parser.add_option("-u", "--update-deps",
                    action="store_true", dest="update_deps", default=False,
                    help="Pull or update third party dependencies")

  (options, args) = parser.parse_args()
  if len(args) != 0:
    parser.error('unexpected args')

  if options.update_deps:
    UpdateDeps()
  Generate(options.debug)
  return 0


if __name__ == '__main__':
  sys.exit(main())
