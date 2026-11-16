#!/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

AIRFLOW_VERSION=3.4.0
PYTHON_VERSION=3.13
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

source "${REPO_DIR}/.venv/bin/activate"

if ! command -v airflow >/dev/null; then
  uv pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
fi

# To include provider packages (like AWS, Google, or Snowflake),
# pass them as extras using the same constraint file:
# uv pip install "apache-airflow[amazon,google]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

export AIRFLOW_HOME="${REPO_DIR}/.airflow"
export AIRFLOW__CORE__DAGS_FOLDER="${REPO_DIR}/3-4-0"
export AIRFLOW__CORE__LOAD_EXAMPLES=False
airflow db migrate


echo "starting local airflow..."
echo "view the UI at http://localhost:8080"
echo ""

LOCAL_AIRFLOW_CREDS="$(cat "${AIRFLOW_HOME}/simple_auth_manager_passwords.json.generated")"
echo "login with username admin, and pass: $(echo "$LOCAL_AIRFLOW_CREDS" | jq -r '.admin')"
echo ""

# .airflow/simple_auth_manager_passwords.json.generated

# Launch the local UI
airflow standalone
