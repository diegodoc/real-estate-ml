#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = real-estate-ml
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python

#################################################################################
# DATA COLLECTION COMMANDS                                                      #
#################################################################################
#
## Collect data from OLX
#.PHONY: scrape-olx
#scrape-olx:
#	$(PYTHON_INTERPRETER) -m real_estate_ml.scraping.collectors.olx_collector

## Collect data from ZAP
#.PHONY: scrape-zap
#scrape-zap:
#	$(PYTHON_INTERPRETER) -m real_estate_ml.scraping.collectors.zap_collector

## Collect data from all sources
#.PHONY: scrape-all
#scrape-all: scrape-olx scrape-zap

#################################################################################
# DATA PROCESSING COMMANDS                                                     #
#################################################################################

## Process dataset
.PHONY: data
data:
	$(PYTHON_INTERPRETER) real_estate_ml/dataset.py

## Train model
.PHONY: train
train:
	$(PYTHON_INTERPRETER) real_estate_ml/modeling/train.py

## Generate predictions
.PHONY: predict
predict:
	$(PYTHON_INTERPRETER) real_estate_ml/modeling/predict.py

## Generate EDA reports
.PHONY: eda
eda:
	$(PYTHON_INTERPRETER) real_estate_ml/eda.py

## Run complete pipeline
.PHONY: pipeline
pipeline: data eda train predict

#################################################################################
# DEVELOPMENT COMMANDS                                                         #
#################################################################################

## Create conda environment
.PHONY: create_environment
create_environment:
	conda env create -f environment.yml

## Update conda environment
.PHONY: update_environment
update_environment:
	conda env update -f environment.yml --prune

## Install Python dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using ruff
.PHONY: lint
lint:
	ruff format --check
	ruff check

## Format source code with ruff
.PHONY: format
format:
	ruff check --fix
	ruff format

## Make dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) real_estate_ml/dataset.py

## Collect data from OLX API
.PHONY: scrape
scrape:
	$(PYTHON_INTERPRETER) -m real_estate_ml.scraping.olx_api_collector

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
