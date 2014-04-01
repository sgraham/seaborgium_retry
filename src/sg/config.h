// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef SG_CONFIG_H_
#define SG_CONFIG_H_

#include <string>
#include <vector>
using namespace std;  // NOLINT(build/namespaces)

#if defined(_MSC_VER)
#define OS_WIN 1
#elif defined(__linux__)
#define OS_LINUX 1
#else
#error TODO
#endif

#endif  // SG_CONFIG_H_
