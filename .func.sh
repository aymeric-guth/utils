#!/bin/sh

[ -f "$DOTFILES/funcs/py_venv.sh" ] && . "$DOTFILES/funcs/py_venv.sh"

build() {
  [ ! -f .venv/bin/python ] && return 1
  [ -z "$VIRTUAL_ENV" ] && return 1
  rm -rf ./dist ./build "${PROJECT_NAME}.egg-info"
  .venv/bin/python -m build . --wheel
  .venv/bin/python -m pip install --force-reinstall dist/utils-0.0.1-py3-none-any.whl
}
