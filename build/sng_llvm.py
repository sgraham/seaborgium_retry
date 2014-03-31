def DEP_lldb(action):
  if action == 'sync':
    SvnCheckoutOrUp('http://llvm.org/svn/llvm-project/llvm/trunk', 'llvm')
    SvnCheckoutOrUp(
        'http://llvm.org/svn/llvm-project/cfe/trunk', 'clang',
        subdir='llvm/tools')
    SvnCheckoutOrUp(
        'http://llvm.org/svn/llvm-project/lldb/trunk', 'lldb',
        subdir='llvm/tools')
    SvnCheckoutOrUp(
        'http://llvm.org/svn/llvm-project/lld/trunk', 'lld',
        subdir='llvm/tools')
    build = 'out/llvm'
    if not os.path.exists(build):
      os.makedirs(build)
    Run(['cmake',
         '-G', 'Ninja',
         '../../third_party/llvm',
         '-DLLVM_ENABLE_CXX11=ON'],
         cwd=build)
    Run(['ninja', 'clang', 'lld', 'lldb'], cwd=build)
