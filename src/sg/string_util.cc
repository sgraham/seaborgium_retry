// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include "sg/string_util.h"

#include <stdarg.h>

vector<wstring> StringSplit(const wstring& str, wchar_t break_at) {
  vector<wstring> result;
  wstring current;
  for (const auto& i : str) {
    if (i == break_at) {
      result.push_back(current);
      current = wstring();
      continue;
    }
    current.push_back(i);
  }
  result.push_back(current);
  return result;
}

wstring Format(const wchar_t* msg, ...) {
  va_list ap;
  va_start(ap, msg);
  wchar_t buf[2048];
  vswprintf_s(buf, sizeof(buf), msg, ap);
  va_end(ap);
  return buf;
}
