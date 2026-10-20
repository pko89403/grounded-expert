#!/usr/bin/env bash
set -euo pipefail

# install-antigravity.sh
# Installs or uninstalls the grounded-expert skill for Google Antigravity
# by symlinking hosts/antigravity/ (never plugin/) into an Antigravity skills folder.
# Skill folder locations: https://antigravity.google/docs/skills

# Physical paths so symlink comparisons survive /tmp -> /private/tmp style aliases.
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
SKILL_SRC="${REPO_DIR}/hosts/antigravity"
CWD="$(pwd -P)"

MODE="global"
CLI=0
ACTION="install"

usage() {
  local exit_code="${1:-0}"
  cat <<EOF
Usage: $(basename "$0") [--global [--cli] | --workspace] [--uninstall]

Links ${SKILL_SRC} into an Antigravity skills folder.

Options:
  --global        Antigravity App/IDE: ~/.gemini/config/skills/grounded-expert (default)
  --cli           With --global: Antigravity CLI: ~/.gemini/antigravity-cli/skills/grounded-expert
  --workspace     Current project: ./.agents/skills/grounded-expert
                  (run from the target project's root, not from inside this repo)
  --uninstall     Remove the link for the selected target only
  -h, --help      Show this help message
EOF
  exit "$exit_code"
}

die() {
  echo "Error: $*" >&2
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --global) MODE="global" ;;
    --workspace) MODE="workspace" ;;
    --cli) CLI=1 ;;
    --uninstall) ACTION="uninstall" ;;
    -h|--help) usage 0 ;;
    *)
      echo "Unknown option: $1" >&2
      usage 1
      ;;
  esac
  shift
done

if [[ "$MODE" == "workspace" ]]; then
  # The workspace folder is the same for App, IDE and CLI.
  [[ "$CLI" -eq 0 ]] || die "--cli applies to --global only; --workspace already covers the CLI."
  # A workspace link inside this repo would be a self-referencing loop that git could pick up.
  if [[ "$CWD" == "$REPO_DIR" || "$CWD" == "$REPO_DIR"/* ]]; then
    die "--workspace must be run from your project's root, not from inside ${REPO_DIR}."
  fi
  TARGET="${CWD}/.agents/skills/grounded-expert"
elif [[ "$CLI" -eq 1 ]]; then
  TARGET="${HOME}/.gemini/antigravity-cli/skills/grounded-expert"
else
  TARGET="${HOME}/.gemini/config/skills/grounded-expert"
fi
LABEL="${MODE}$([[ "$CLI" -eq 1 ]] && echo " (CLI)" || true)"

# True only if TARGET is a symlink that resolves to this checkout's hosts/antigravity.
is_our_link() {
  [[ -L "$TARGET" ]] && [[ "$(cd "$TARGET" 2>/dev/null && pwd -P)" == "$SKILL_SRC" ]]
}

refuse_foreign() {
  if [[ -L "$TARGET" ]]; then
    die "${TARGET} is a symlink to '$(readlink "$TARGET")', not to ${SKILL_SRC}. Refusing to touch it; remove it manually if it is yours."
  fi
  die "${TARGET} exists and is not a symlink. Refusing to touch real files; back it up or remove it manually."
}

if [[ "$ACTION" == "uninstall" ]]; then
  if is_our_link; then
    rm "$TARGET"
    echo "Removed ${TARGET} (${LABEL})."
  elif [[ -e "$TARGET" || -L "$TARGET" ]]; then
    refuse_foreign
  else
    echo "Nothing to uninstall: ${TARGET} does not exist."
  fi
  exit 0
fi

[[ -f "${SKILL_SRC}/SKILL.md" ]] || die "${SKILL_SRC}/SKILL.md not found. Is this checkout complete?"

if is_our_link; then
  echo "Already installed: ${TARGET} -> ${SKILL_SRC} (${LABEL})."
  exit 0
fi
[[ -e "$TARGET" || -L "$TARGET" ]] && refuse_foreign

mkdir -p "$(dirname "$TARGET")"
ln -s "$SKILL_SRC" "$TARGET"
echo "Installed ${TARGET} -> ${SKILL_SRC} (${LABEL})."
