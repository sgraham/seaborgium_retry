// Copyright 2014 The Chromium Authors. All rights reserved.
//
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef SG_UTIL_H_
#define SG_UTIL_H_

void Fatal(const char* msg, ...);
void Error(const char* msg, ...);
void Log(const char* msg, ...);

#define CHECK(c) \
  if (!(c))      \
    Fatal("CHECK '" #c "' failed at %s, line %d", __FILE__, __LINE__);

#define PCHECK(c)                                                   \
  if (!(c))                                                         \
    Fatal("PCHECK '" #c "' failed at %s, line %d, GetLastError=%d", \
          __FILE__,                                                 \
          __LINE__,                                                 \
          GetLastError());

#endif  // SG_UTIL_H_
