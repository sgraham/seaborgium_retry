// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include "sg/cmdline.h"
#include "sg/debug_engine.h"

Cmdline::Cmdline() {
}

void Cmdline::Execute(const string& command) {
  vector<string> TokenizeCommand();
}

void Cmdline::SetDebugEngine(DebugEngine* debug_engine) {
  debug_engine_ = debug_engine;
}
