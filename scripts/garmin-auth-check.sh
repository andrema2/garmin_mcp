#!/usr/bin/env bash
set -euo pipefail

docker mcp tools call list_activities limit=1 --verbose
