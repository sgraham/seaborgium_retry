// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include "sg/cmdline.h"

#include "sg/debug_engine.h"
#include "sg/string_util.h"

namespace {

struct Commands {
  wchar_t* name;
  bool (Cmdline::*func)(const vector<wstring>& argv,
                        wstring* result,
                        wstring* err);
} commands[] = {
  { L"ver", &Cmdline::CmdVersion },
};

}  // namespace

Cmdline::Cmdline() {
}

bool Cmdline::Execute(const wstring& command, wstring* result, wstring* err) {
  vector<wstring> parts = StringSplit(command, L' ');
  if (parts.empty()) {
    *result = *err = wstring();
    return true;
  }

  for (const auto& command : commands) {
    if (parts[0] == command.name)
      return (this->*command.func)(parts, result, err);
  }
  *err = Format(L"unrecognized command '{}'", parts[0].c_str());
  return false;
}

void Cmdline::SetDebugEngine(DebugEngine* debug_engine) {
  debug_engine_ = debug_engine;
}

bool Cmdline::CmdVersion(const vector<wstring>& argv,
                         wstring* result,
                         wstring* err) {
  if (argv.size() != 1) {
    *err = L"unexpected arguments to 'ver'";
    return false;
  }
  *result = debug_engine_->GetVersion();
  return true;
}
