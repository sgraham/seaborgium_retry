// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef SG_CMDLINE_H_
#define SG_CMDLINE_H_

#include "sg/config.h"
class DebugEngine;

class Cmdline {
 public:
  Cmdline();

  void Execute(const string& command);
  void SetDebugEngine(DebugEngine* debug_engine);

 private:
  DebugEngine* debug_engine_;
};

#endif  // SG_CMDLINE_H_
