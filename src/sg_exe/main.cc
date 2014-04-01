// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include <stdio.h>
#include "SDL/include/SDL.h"

int main() {
  if (SDL_Init(SDL_INIT_VIDEO) != 0) {
    fprintf(stderr, "SDL_Init failed: %s\n", SDL_GetError());
    return 1;
  }

  SDL_Window* win = SDL_CreateWindow(
      "Seaborgium", 100, 100, 640, 480, SDL_WINDOW_SHOWN);
  if (!win) {
    fprintf(stderr, "SDL_CreateWindow failed: %s\n", SDL_GetError());
    return 1;
  }

  SDL_Quit();
  return 0;
}
