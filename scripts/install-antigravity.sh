#!/usr/bin/env bash
set -euo pipefail

# install-antigravity.sh
# Installs or uninstalls the grounded-expert skill for Google Antigravity
# by symlinking hosts/antigravity/ (never plugin/) into an Antigravity skills folder.
# Skill folder locations: https://antigravity.google/docs/skills

# Follow symlinks to this script (e.g. ~/bin/install-antigravity -> clone) so
# REPO_DIR is the clone, not the link's folder. macOS lacks readlink -f.
SCRIPT="${BASH_SOURCE[0]}"
while [[ -L "$SCRIPT" ]]; do
  LINK_DIR="$(cd -P "$(dirname "$SCRIPT")" && pwd)"
  SCRIPT="$(readlink "$SCRIPT")"
  [[ "$SCRIPT" == /* ]] || SCRIPT="${LINK_DIR}/${SCRIPT}"
done
# Physical paths so symlink comparisons survive /tmp -> /private/tmp style aliases.
REPO_DIR="$(cd -P "$(dirname "$SCRIPT")/.." && pwd)"
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
fi

GLOBAL_TARGET="${HOME}/.gemini/config/skills/grounded-expert"
CLI_TARGET="${HOME}/.gemini/antigravity-cli/skills/grounded-expert"
WORKSPACE_TARGET="${CWD}/.agents/skills/grounded-expert"
if [[ "$MODE" == "workspace" ]]; then
  TARGET="$WORKSPACE_TARGET"
elif [[ "$CLI" -eq 1 ]]; then
  TARGET="$CLI_TARGET"
else
  TARGET="$GLOBAL_TARGET"
fi
LABEL="${MODE}$([[ "$CLI" -eq 1 ]] && echo " (CLI)" || true)"

# True only if the path (default TARGET) is a symlink to this checkout's
# hosts/antigravity. Compares the link text, not the resolved target, so a
# dangling link we created (e.g. after the clone moved) still counts as ours.
is_our_link() {
  local path="${1:-$TARGET}"
  [[ -L "$path" ]] && [[ "$(readlink "$path")" == "$SKILL_SRC" ]]
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
    for other in "$GLOBAL_TARGET:--global" "$CLI_TARGET:--global --cli" "$WORKSPACE_TARGET:--workspace"; do
      other_path="${other%%:*}"
      if [[ "$other_path" != "$TARGET" ]] && is_our_link "$other_path"; then
        echo "Found this checkout's link at ${other_path}; remove it with: $(basename "$0") ${other#*:} --uninstall"
      fi
    done
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
if [[ "$MODE" == "workspace" ]]; then
  # The link holds an absolute path on this machine; committing it breaks for teammates.
  echo "Note: this is an absolute symlink. Add '.agents/skills/grounded-expert' to your project's .gitignore so it is not committed."
fi
