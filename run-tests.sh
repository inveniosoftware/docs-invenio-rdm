#!/bin/sh
# SPDX-FileCopyrightText: 2019 CERN.
# SPDX-FileCopyrightText: 2019 Northwestern University.
# SPDX-License-Identifier: MIT

npx markdownlint-cli docs/*
awesome_bot --allow-dupe --skip-save-results --allow-redirect docs/**/*.md
mkdocs build -v
rm -rf site/
