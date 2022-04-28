# gcp-update-bq-parameterized-script-action
GitHub Action to parameterized BigQuery SQL script at General Mills


# Usage:
Create a github workflow file under .github/workflows that follows the Workflow Example below.

## Inputs

| Parameter           | Required | Info                                                                          |
| --------------------| -------- | ------------------------------------------------------------------------------|
| `ddl_read_folder_path`  | `true`   | Directory path to the sql files which needs to be processed with the parameters passed in param_string. Defaults to the "data_pipeline/ddl_scripts/output/" path.
| `ddl_write_folder_path`  | `true`   | Directory path to write the processed files
| `param_string`     | `true`   | Parameter string for substitution. format: key=value,key=value,
| `debug`     | `false`   | Boolean value True/False - if True will enable logging. Defaults to "False"

## Example

```yaml
name: Workflow Example
on:
  push:
    branches:
      - master
jobs:
    update-parameterized-script:
      name: JOB 1. Set & Execute in Development
      container: google/cloud-sdk:latest   # Job will run in this Docker image
      runs-on: gcp
      env:
        GCP_PROJECT_ID: cnf-data-dev-d4cc14
        CNF_PROJECT_ID: cnf-dlf-dev-8dbb70

      steps:
        #===============================================#
        - name: Checkout
          uses: actions/checkout@v2

        #===============================================#
        - name: Run Parameterized Script
          uses: GeneralMills/gcp-update-bq-parameterized-script-action@add-action
          with:
            param_string: "CNF_PROJECT_ID=${{env.CNF_PROJECT_ID}},PROJECT_ID=${{env.GCP_PROJECT_ID}}"
            ddl_read_folder_path: data_pipeline/ddl_scripts/output/
            ddl_write_folder_path: data_pipeline/ddl_scripts/output/dev
            debug: 'False'
    
```

### Explaining the workflow:
1. on -> push -> branches: master: This will be triggered when a push is made to the master branch.
1. runs-on: gcp: This uses GCP based github runners.
1. env: This sets the github action environment variables, allowing us to use these variables for the job.
1. Checkout: this step causes the repo to be checked out, allowing the action to read the "*.sql" file in the repo path.
1. Run Parameterized Script: this is the main action that runs a python scripts in the background. It takes the directory path which have the sql files, path where we wont to store the processed files and parameter string for subsitution.

### Workflow Secrets Needed:
No secrets are needed to run action.

# Local Dev Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements_test.txt
```


## Testing and Linting

This repo is instrumented with various testing and linting tools to maintain
code readability and correctness. Some of the tools include

* `pytest`
* `mypy`
* `flake8`
* `black`

!!!hint
    If you have a tests fail make sure you have all local packages installed. 
### Run the linting script

This script will apply formatting and fixes to your local environment.

```sh
./scripts/lint.sh
```

### Run the check script

This script will run all linting checks on your local environment. This is the
same script that is run as part of the CI/CD process.

```sh
./scripts/check.sh
```

### Run the test script

This script will run all Python tests in the `tests/` directory. This is the
same script that is run as part of the CI/CD process.

```sh
./scripts/test.sh
```

## Deployment

To make the action live, push it to the main branch.

Use tags to reference versions of your action: [create a version tag](https://github.com/actions/toolkit/blob/master/docs/action-versioning.md)