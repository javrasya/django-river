#!/bin/bash
set -e


ENVIRONMENT=$1

if [ -z "$ENVIRONMENT" ]; then
  ENVIRONMENT="test"
fi

if [ "$ENVIRONMENT" == "prod" ]; then
  REPOSITORY=pypi
elif [ "$ENVIRONMENT" == "test" ]; then
  REPOSITORY=testpypi
else
  echo "First argument which is the environment has to be either 'prod' or 'test' not ${ENVIRONMENT}"
  exit 1
fi

[ -e dist ] && rm -rf dist
[ -e build ] && rm -rf build
[ -e django_river.egg-info ] && rm -rf django_river.egg-info

python setup.py sdist bdist_wheel
twine check dist/*

echo "Publishing to ${REPOSITORY}"

twine upload --repository "$REPOSITORY" --config-file="${PWD}/.pypirc" dist/*
