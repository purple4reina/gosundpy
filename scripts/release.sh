#!/bin/bash -e

CURRENT_VERSION=$(cat gosundpy/version.py | awk '{print $3}')
echo "current version is ${CURRENT_VERSION}"

if [[ -z $VERSION ]]; then
    echo "VERSION must be set, ex: VERSION=\"0.2.0\" ./scripts/release.sh"
    exit 1
fi

echo "updating version to \"${VERSION}\""
echo "version = \"${VERSION}\"" > gosundpy/version.py

echo "adding version to changelog"
chng="CHANGELOG.md"
echo "# CHANGELOG

## ${VERSION}
$(tail -n +4 $chng)" > $chng

echo "committing changes"
git add gosundpy/version.py
git add CHANGELOG.md
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
