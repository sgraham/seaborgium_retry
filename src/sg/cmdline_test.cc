// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include "sg/cmdline.h"

#include "sg/debug_engine.h"

#include "gtest/gtest.h"

namespace {

class MockDebugEngine : public DebugEngine {
 public:
  virtual ~MockDebugEngine() {
  }

  wstring GetVersion() const override {
    return L"Mock 1.0";
  }
};

class CmdlineTest : public ::testing::Test {
 public:
  CmdlineTest() {
    cmdline.SetDebugEngine(&dbgeng);
  }

  Cmdline cmdline;
  MockDebugEngine dbgeng;
};

}  // namespace

TEST_F(CmdlineTest, BasicTokenization) {
  wstring result, err;
  EXPECT_TRUE(cmdline.Execute(L"ver", &result, &err));
  EXPECT_EQ(L"Mock 1.0", result);
  EXPECT_FALSE(cmdline.Execute(L"unknown_command", &result, &err));
  EXPECT_TRUE(err.find(L"Unrecognized command") != wstring::npos);
}

