#!/usr/bin/env bash
set -euo pipefail

# install-antigravity.sh
# Installs or uninstalls grounded-expert for Google Antigravity / Gemini CLI.

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_SRC="${REPO_DIR}/plugin"
GLOBAL_SKILLS_DIR="${HOME}/.gemini/config/skills"
GLOBAL_TARGET="${GLOBAL_SKILLS_DIR}/grounded-expert"
WORKSPACE_TARGET="$(pwd)/.agents/skills/grounded-expert"

MODE="global"
ACTION="install"

usage() {
  local exit_code="${1:-0}"
  cat <<EOF
Usage: $(basename "$0") [options]

Options:
  --global        Target ~/.gemini/config/skills/grounded-expert (default)
  --workspace     Target current project's .agents/skills/grounded-expert
  --uninstall     Remove the grounded-expert symlink for the selected target
  -h, --help      Show this help message
EOF
  exit "$exit_code"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --global)
      MODE="global"
      shift
      ;;
    --workspace)
      MODE="workspace"
      shift
      ;;
    --uninstall)
      ACTION="uninstall"
      shift
      ;;
    -h|--help)
      usage 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage 1
      ;;
  esac
done

if [[ "$MODE" == "global" ]]; then
  TARGET="$GLOBAL_TARGET"
else
  TARGET="$WORKSPACE_TARGET"
fi

if [[ "$ACTION" == "uninstall" ]]; then
  echo "Uninstalling grounded-expert (${MODE})..."
  if [[ -L "$TARGET" ]]; then
    rm "$TARGET"
    echo "Removed symlink: $TARGET"
  elif [[ -e "$TARGET" ]]; then
    echo "Error: $TARGET is an actual directory/file (not a symlink). Refusing to delete." >&2
    exit 1
  else
    echo "Notice: $TARGET does not exist. Nothing to uninstall."
  fi
  echo "Uninstall complete."
  exit 0
fi

# Install action
echo "Installing grounded-expert for Antigravity (${MODE})..."

if [[ ! -f "${PLUGIN_SRC}/SKILL.md" ]]; then
  echo "Error: ${PLUGIN_SRC}/SKILL.md not found. Ensure repository is intact." >&2
  exit 1
fi

mkdir -p "$(dirname "$TARGET")"

# Safe check: only replace if it's already a symlink; never delete real directory
if [[ -L "$TARGET" ]]; then
  rm "$TARGET"
elif [[ -e "$TARGET" ]]; then
  echo "Error: $TARGET already exists and is not a symlink." >&2
  echo "Refusing to overwrite actual files. Please backup or remove it manually." >&2
  exit 1
fi

ln -s "$PLUGIN_SRC" "$TARGET"
echo "Successfully linked ${PLUGIN_SRC} -> ${TARGET}"
echo ""
echo "grounded-expert skill is now installed for Antigravity (${MODE})!"
echo "Target: ${TARGET}/SKILL.md"
