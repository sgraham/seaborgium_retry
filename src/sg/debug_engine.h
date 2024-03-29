// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef SG_DEBUG_ENGINE_H_
#define SG_DEBUG_ENGINE_H_

#include "sg/config.h"

class DebugEngine {
 public:
  virtual ~DebugEngine();
  virtual wstring GetVersion() const = 0;
};

#endif  // SG_DEBUG_ENGINE_H_
