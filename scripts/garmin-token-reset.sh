set -euo pipefail

TOK_DIR="${HOME}/.garminconnect"
BK_DIR="${HOME}/.garminconnect-backups/$(date +%Y%m%d-%H%M%S)"

mkdir -p "${BK_DIR}"

if [ -d "${TOK_DIR}" ]; then
  cp -a "${TOK_DIR}/." "${BK_DIR}/" 2>/dev/null || true
fi

rm -f "${TOK_DIR}/oauth1_token.json" \
      "${TOK_DIR}/oauth2_token.json" \
      "${TOK_DIR}/token" \
      "${TOK_DIR}/tokens.json" 2>/dev/null || true

docker mcp tools call list_activities limit=1 --verbose
