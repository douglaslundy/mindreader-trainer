#!/usr/bin/env bash
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
BASE="${OPENJARVIS_HOME:-$HOME/.openjarvis}"
DEST="$BASE/skills/mindreader-trainer-v2"
STATE="$BASE/mindreader-trainer-v2"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="${DEST}.backup-${STAMP}"

mkdir -p "$(dirname "$DEST")" "$STATE"

if [ -d "$DEST" ]; then
  mv "$DEST" "$BACKUP"
  echo "Backup da skill anterior criado em: $BACKUP"
fi

cp -R "$SRC" "$DEST"
chmod +x "$DEST/scripts/progress.py" 2>/dev/null || true

echo "Instalado em: $DEST"
echo "Diretório de progresso preservado em: $STATE"

if command -v jarvis >/dev/null 2>&1; then
  echo "--- Verificação ---"
  jarvis skill info mindreader-trainer-v2 || true
  echo "Para iniciar: jarvis chat --agent orchestrator"
  echo "Dentro do chat, use: /mente"
else
  echo "O comando jarvis não está no PATH desta sessão."
  echo "Depois, confirme com: jarvis skill list && jarvis skill info mindreader-trainer-v2"
fi
