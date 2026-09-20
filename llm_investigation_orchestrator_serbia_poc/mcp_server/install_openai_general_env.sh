#!/usr/bin/env bash
# Install the runtime configuration for the additive OpenAI General experiment.
set -euo pipefail

SERVICE="serbia-poc-ui.service"
SECRET_DIR="/etc/serbia-poc-ui"
SECRET_FILE="${SECRET_DIR}/openai.env"
DROPIN_DIR="/etc/systemd/system/${SERVICE}.d"

read -r -s -p "OpenAI API key: " OPENAI_API_KEY
echo
if [[ -z "${OPENAI_API_KEY}" ]]; then
  echo "No API key was entered." >&2
  exit 1
fi

sudo install -d -o root -g ubuntu -m 0750 "${SECRET_DIR}"
printf 'OPENAI_API_KEY=%s\n' "${OPENAI_API_KEY}" | sudo tee "${SECRET_FILE}" >/dev/null
sudo chown root:ubuntu "${SECRET_FILE}"
sudo chmod 0640 "${SECRET_FILE}"
unset OPENAI_API_KEY

sudo install -d -o root -g root -m 0755 "${DROPIN_DIR}"
sudo tee "${DROPIN_DIR}/openai-general.conf" >/dev/null <<'EOF'
[Service]
EnvironmentFile=/etc/serbia-poc-ui/openai.env
Environment=INTELLIGENCE_POC_OPENAI_GENERAL_ENABLED=true
Environment=INTELLIGENCE_POC_OPENAI_GENERAL_MODEL=gpt-5.6-terra
Environment=INTELLIGENCE_POC_MCP_SERVER_PATH=/opt/serbia-poc/mcp_server/server.py
EOF

sudo systemctl daemon-reload
sudo systemctl restart "${SERVICE}"
sudo systemctl is-active "${SERVICE}"
