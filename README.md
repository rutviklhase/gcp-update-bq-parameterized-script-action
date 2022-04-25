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
    
```

### Explaining the workflow:
1. on -> push -> branches: master: This will be triggered when a push is made to the master branch.
1. runs-on: gcp: This uses GCP based github runners.
1. environment: dev: This sets the github action environment, causing the action to use repository secrets defined for dev. See the workflow secrets information below for details.
1. Checkout: this step causes the repo to be checked out, allowing the action to read the json file in the repo.
1. Import Secrets: this uses secrets defined in github repo to call out to vault to get DB Portal authentication secrets.
1. Set UP BQ Table Security: this is the main action that parses the json file and calls out to DB Portal to set security.  Its inputs include azure client data that is needed to authenticate with DB Portal.

### About the gcpBigQueryTablesSecurityFile file:
1. See the sample files below.
1. Each file must contain a `defaults` and a `tables` section.  `defaults` can be empty, if not needed.
1. These five values are required for all tables being processed: `applicationName`, `project`, `dataset`, `name`, `securityClassification`
1. Each table in the `tables` section must include a `name` value.  
1. The other values can be defined in the `tables` or `defaults` section.  
1. If values are defined in both `defaults` and `tables`, the table value is used, overriding the default.
1. See the second example for a full list of attributes available for a table definition.
1. All Groups and Service Accounts should be referenced by their email addresses.  This is one change from Hadoop security.
1. See the DB Portal API for context around those attributes.


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

## Testing Feature Branches

To test a feature branch, change  the module version in the calling workflow.  See the example below:

```yaml
name: Workflow Example
on:
  push:
    branches:
      - master
jobs:
  Set-GCP-BQ-Table-Security:
    runs-on: gcp
    steps:
      - name: Checkout
        uses: actions/checkout@v2   
      - name: Import Secrets
        uses: hashicorp/vault-action@v2.1.2
        with:
          url: ${{ env.VAULT_URL }}
          method: approle
          roleId: ${{ secrets.ROLE_ID }}
          secretId: ${{ secrets.SECRET_ID }}
          caCertificate: ${{ secrets.VAULT_CERT }}
          secrets: |
              secret/data/cloverleaf/github/prod/github-database-portal-client-id value | DATABASE_PORTAL_CLIENT_ID;
              secret/data/cloverleaf/github/prod/github-database-portal-client-secret value | DATABASE_PORTAL_CLIENT_SECRET;
      - name: Set GCP BQ Table Security
        uses: GeneralMills/gcp-bq-table-security-action@FEATURE-BRANCH-NAME
        with:
          table_security_file: GCPBigQueryTablesSecurity.json
          azure_client_id: ${{ env.DATABASE_PORTAL_CLIENT_ID }}
          azure_client_secret: ${{ env.DATABASE_PORTAL_CLIENT_SECRET }}
          azure_tenent_id: ${{ secrets.AZURE_TENENT_ID }}
          is_testing: "True"
```