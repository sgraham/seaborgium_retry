// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include "sg/cmdline.h"

#include "sg/debug_engine.h"
#include "sg/string_util.h"

Cmdline::Cmdline() {
}

bool Cmdline::Execute(const wstring& command, wstring* result, wstring* err) {
  vector<wstring> parts = StringSplit(command, L' ');
  if (parts.empty()) {
    *result = *err = wstring();
    return true;
  }
  // TODO(scottmg): Table dispatch.
  if (parts[0] == L"ver") {
    *result = debug_engine_->GetVersion();
    return true;
  }
  *err = Format(L"Unrecognized command '{}'", parts[0].c_str());
  return false;
}

void Cmdline::SetDebugEngine(DebugEngine* debug_engine) {
  debug_engine_ = debug_engine;
}
