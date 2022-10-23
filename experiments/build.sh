#!/bin/bash

# tests for learning https://github.com/con2/emrichen

emrichen --template-format yaml --output-file=./output/add-default.yaml --output-format yaml ./input/add.in.yaml
emrichen --template-format yaml --define foo=bar --define apiServerAddress=9.9.9.9 --output-file=./output/add-cli.yaml --output-format yaml ./input/add.in.yaml
emrichen --template-format yaml --var-file=./input/add.var.yaml --output-file=./output/add-var-file.yaml --output-format yaml ./input/add.in.yaml

# we have to ensure he output dir exists
#emrichen --template-format yaml --var-file=./input/add.var.yaml --output-file=./output/is-this-created/add-var-file.yaml --output-format yaml ./input/add.in.yaml
