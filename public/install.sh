#!/usr/bin/env bash
# shell-drill installer for Red Hat Enterprise Linux 9/10
# Designed for disposable VM snapshots

set -e

echo "=========================================================="
echo "Installing shell-drill: RHEL 9/10 Terminal Muscle-Memory Trainer"
echo "=========================================================="

INSTALL_DIR="/usr/local/bin"
TARGET="${INSTALL_DIR}/shell-drill"

# Check root or sudo
if [ "$EUID" -ne 0 ]; then
    INSTALL_DIR="${HOME}/.local/bin"
    mkdir -p "${INSTALL_DIR}"
    TARGET="${INSTALL_DIR}/shell-drill"
fi

# Download or copy shell-drill
if [ -f "./shell-drill" ]; then
    cp ./shell-drill "${TARGET}"
elif [ -f "./shell_drill.py" ]; then
    cp ./shell_drill.py "${TARGET}"
else
    curl -sSL -o "${TARGET}" "${APP_URL:-http://localhost:3000}/shell-drill" || curl -sSL -o "${TARGET}" "https://raw.githubusercontent.com/shell-drill/rhel/main/shell-drill"
fi

chmod +x "${TARGET}"

echo "[✓] Successfully installed shell-drill to: ${TARGET}"
echo ""
echo "To start the interactive curses trainer, run:"
echo "    ${TARGET}"
echo ""
echo "Or with specific category:"
echo "    shell-drill --category \"Service Management\""
echo "=========================================================="
