#!/bin/bash

ENVIRONMENT=$1

if [ -z "$ENVIRONMENT" ]; then
  ENVIRONMENT="test"
fi

python setup.py sdist bdist_wheel

twine check dist/*

if [ "$ENVIRONMENT" == "prod" ]; then
  REPOSITORY="https://upload.pypi.org/legacy/"

else
  REPOSITORY=" https://test.pypi.org/legacy/"
fi

echo "Publishing to ${REPOSITORY}"

twine upload --repository-url "$REPOSITORY" dist/*
