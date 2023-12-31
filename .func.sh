#!/bin/sh

[ -f "$DOTFILES/funcs/py_venv.sh" ] && . "$DOTFILES/funcs/py_venv.sh"

clean() {
  # python_project_clean || return 1
  python_clean || return 1
  rm -rf .pytest_cache || return 1
}

build() {
  python_clean || return 1
  python_build || return 1
  python_deploy_global || return 1
}

gen() {
  python_tools_gen || return 1
  python_venv_gen || return 1
}

up() {
  COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker compose up
}

_test() {
  python_test_pytest
}
