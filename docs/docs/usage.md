# Usage Guide

This guide explains how to use the Titanic ML project.

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the environment variables if needed

## Running the Pipeline
Use the Makefile commands:
```bash
# Process the dataset
make data

# Train models
make train

# Generate predictions
make predict