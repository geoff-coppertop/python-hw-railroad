#!/usr/bin/env sh
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# test.sh
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

# Remove all cached pyc files, they don't play nice with the containers
find . -name "*.pyc" -delete

# Remove test directory if exists
rm -rf reports

# Make a test report directory
mkdir reports

# Make a coverage sub-directory
mkdir reports/coverage

# Build the docker image
docker build -q -t test-image:hw-railroad .

# Run `tox` on the image. Automatically remove the container when it exits
docker run -v "$(pwd)"/reports:/reports --rm -t test-image:hw-railroad tox

# Clean dangling images that result from code changes
docker images prune -q