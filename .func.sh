#!/bin/sh

[ -f "$DOTFILES/funcs/py_venv.sh" ] && . "$DOTFILES/funcs/py_venv.sh"

bu() {
  #[ ! -f .venv/bin/python ] && return 1
  #[ -z "$VIRTUAL_ENV" ] && return 1
  #rm -rf ./dist ./build "${PROJECT_NAME}.egg-info"
  #.venv/bin/python -m build . --wheel
  # version="$(parse_version "$WORKSPACE/$PROJECT_NAME/__init__.py")" || return 1
  #.venv/bin/python -m pip install --force-reinstall dist/utils-0.0.3-py3-none-any.whl
}

clean() {
  rm -rf ./dist ./build "${PROJECT_NAME}.egg-info"
}

build() {
  [ ! -f .venv/bin/python ] && return 1
  [ -z "$VIRTUAL_ENV" ] && return 1
  clean || return 1
  .venv/bin/python -m build . --wheel || return 1
  # version="$(parse_version "$WORKSPACE/$PROJECT_NAME/__init__.py")" || return 1
  eggname="$(generate_eggname "py3-none-any.whl")" || return 1
  .venv/bin/python -m pip install --force-reinstall "dist/${eggname}" || return 1
}
