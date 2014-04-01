// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef SG_STRING_UTIL_H_
#define SG_STRING_UTIL_H_

#include "sg/config.h"

#include "format/format.h"
using fmt::Format;

vector<wstring> StringSplit(const wstring& str, wchar_t break_at);

#endif  // SG_STRING_UTIL_H_
