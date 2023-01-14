#!/bin/bash -e

CURRENT_VERSION=$(cat gosundpy/version.py | awk '{print $3}')
echo "current version is ${CURRENT_VERSION}"

if [[ -z $VERSION ]]; then
    echo "VERSION must be set, ex: VERSION=\"0.2.0\" ./scripts/release.sh"
    exit 1
fi

echo "updating version to \"${VERSION}\""
echo "version = \"${VERSION}\"" > gosundpy/version.py

rm -rf dist

chng="CHANGELOG.md"
echo "adding version to changelog"
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

echo "adding unreleased version to changelog"
echo "# CHANGELOG

## Unreleased

$(tail -n +3 $chng)" > $chng
git add CHANGELOG.md
git cm -m "Updating CHANGELOG.md for Unreleased"
git push

echo "Creating new release in github"
echo "Release title: v${VERSION}"
echo "Content: copy CHANGELOG entry for this version, use two hashes (##) for headers"
open https://github.com/purple4reina/gosundpy/releases/new
