#!/bin/bash -e

if [[ -z $VERSION ]]; then
    echo "VERSION must be set, ex: VERSION=0.2.0"
    exit 1
fi

echo "updating version to ${VERSION}"
echo "version = \"${VERSION}\"" > gosundpy/version.py

echo "committing changes"
git add gosundpy/version.py
git cm -m "Updating version to ${VERSION}"
git push
git tag "v${VERSION}"
git push --tags

echo packaging
python3 setup.py sdist

echo "installing twine"
pip3 install twine

echo "uploading to PyPI"
twine upload dist/*

echo "creating new release in github"
open https://github.com/purple4reina/gosundpy/releases/new