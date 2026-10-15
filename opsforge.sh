#!/usr/bin/env bash
# ==============================================================================
# 🔥 OpsForge — Universal Setup & Production Runner Script
# Works idempotently on Linux (Ubuntu, Debian, Fedora, Arch) and Android (Termux)
# ==============================================================================

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PID_FILE="$SCRIPT_DIR/.opsforge.pid"
LOG_FILE="$SCRIPT_DIR/opsforge.log"
DEPS_MARKER="$SCRIPT_DIR/venv/.deps_installed"

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

# Check if running in Termux
IS_TERMUX=false
if [ -n "$TERMUX_VERSION" ] || [ -d "/data/data/com.termux" ]; then
    IS_TERMUX=true
fi

# Locate Python 3
PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo -e "${RED}❌ Error: Python 3 is not installed or not in PATH.${NC}"
    exit 1
fi

# ------------------------------------------------------------------------------
# 1. Idempotent Environment Setup
# ------------------------------------------------------------------------------
setup_environment() {
    # 1. Create venv if missing
    if [ ! -d "venv" ] || [ ! -f "venv/bin/python" ]; then
        echo -e "${CYAN}📦 Creating virtual environment in ./venv...${NC}"
        "$PYTHON_BIN" -m venv venv || {
            echo -e "${RED}❌ Failed to create virtual environment.${NC}"
            if [ "$IS_TERMUX" = true ]; then
                echo -e "${YELLOW}👉 Run: pkg install python${NC}"
            else
                echo -e "${YELLOW}👉 Make sure python3-venv is installed (e.g. sudo apt install python3-venv)${NC}"
            fi
            exit 1
        }
    fi

    # 2. Check if dependencies are already up-to-date
    local req_hash=""
    if [ -f "requirements.txt" ]; then
        if command -v md5sum >/dev/null 2>&1; then
            req_hash=$(md5sum requirements.txt | awk '{print $1}')
        elif command -v shasum >/dev/null 2>&1; then
            req_hash=$(shasum requirements.txt | awk '{print $1}')
        fi
    fi

    local needs_install=false
    if [ ! -f "$DEPS_MARKER" ]; then
        needs_install=true
    elif [ -n "$req_hash" ]; then
        local saved_hash
        saved_hash=$(cat "$DEPS_MARKER" 2>/dev/null || echo "")
        if [ "$saved_hash" != "$req_hash" ]; then
            needs_install=true
        fi
    fi

    if [ "$needs_install" = true ]; then
        echo -e "${CYAN}📥 Installing / verifying dependencies from requirements.txt...${NC}"
        ./venv/bin/pip install --disable-pip-version-check -r requirements.txt
        if [ -n "$req_hash" ]; then
            echo "$req_hash" > "$DEPS_MARKER"
        else
            touch "$DEPS_MARKER"
        fi
        echo -e "${GREEN}✓ Dependencies verified.${NC}"
    fi
}

# ------------------------------------------------------------------------------
# 2. Systemd Service Setup (User Mode — No Sudo Required)
# ------------------------------------------------------------------------------
setup_systemd() {
    if [ "$IS_TERMUX" = true ]; then
        echo -e "${YELLOW}ℹ️  Termux on Android does not use systemd.${NC}"
        echo -e "${CYAN}👉 Use background daemon mode instead: ${BOLD}./opsforge.sh daemon${NC}"
        return 0
    fi

    if ! command -v systemctl >/dev/null 2>&1; then
        echo -e "${RED}❌ systemctl not found on this system.${NC}"
        return 1
    fi

    echo -e "${CYAN}⚙️  Configuring user systemd service for OpsForge...${NC}"
    local user_unit_dir="$HOME/.config/systemd/user"
    mkdir -p "$user_unit_dir"

    local service_file="$user_unit_dir/opsforge.service"
    cat > "$service_file" <<EOF
[Unit]
Description=OpsForge — DevOps Learning & Practice Dashboard
After=network.target

[Service]
Type=simple
WorkingDirectory=$SCRIPT_DIR
Environment=PATH=$SCRIPT_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=FLASK_ENV=production
Environment=OPSFORGE_NO_BROWSER=1
ExecStart=$SCRIPT_DIR/venv/bin/python $SCRIPT_DIR/run.py --prod --no-browser
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
EOF

    systemctl --user daemon-reload
    systemctl --user enable opsforge.service
    systemctl --user restart opsforge.service

    echo -e "${GREEN}✅ OpsForge user service installed and started!${NC}"
    echo -e "   • Status:  ${BOLD}systemctl --user status opsforge.service${NC}"
    echo -e "   • Logs:    ${BOLD}journalctl --user -u opsforge.service -f${NC}"
    echo -e "   • Stop:    ${BOLD}systemctl --user stop opsforge.service${NC}"
    echo -e "   • Address: ${CYAN}http://127.0.0.1:5000${NC}"
}

# ------------------------------------------------------------------------------
# 3. Server Controls
# ------------------------------------------------------------------------------
start_prod() {
    setup_environment
    echo -e "${GREEN}🚀 Launching OpsForge in Production Mode...${NC}"
    exec ./venv/bin/python run.py --prod "$@"
}

start_dev() {
    setup_environment
    echo -e "${YELLOW}🛠️  Launching OpsForge in Development Mode...${NC}"
    exec ./venv/bin/python run.py --dev "$@"
}

start_daemon() {
    setup_environment
    if [ -f "$PID_FILE" ]; then
        local pid
        pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "${YELLOW}⚠️  OpsForge daemon is already running (PID: $pid).${NC}"
            echo -e "   • Address: ${CYAN}http://127.0.0.1:5000${NC}"
            echo -e "   • Logs:    ${BOLD}tail -f $LOG_FILE${NC}"
            return 0
        fi
    fi

    echo -e "${CYAN}🚀 Starting OpsForge background daemon...${NC}"
    nohup ./venv/bin/python run.py --prod --no-browser >> "$LOG_FILE" 2>&1 &
    local new_pid=$!
    echo "$new_pid" > "$PID_FILE"

    sleep 1
    if kill -0 "$new_pid" 2>/dev/null; then
        echo -e "${GREEN}✅ OpsForge started successfully in background! (PID: $new_pid)${NC}"
        echo -e "   • Address: ${CYAN}http://127.0.0.1:5000${NC}"
        echo -e "   • Logs:    ${BOLD}tail -f $LOG_FILE${NC}"
        echo -e "   • Stop:    ${BOLD}./opsforge.sh stop${NC}"
    else
        echo -e "${RED}❌ Failed to start background daemon. Check $LOG_FILE for errors.${NC}"
        exit 1
    fi
}

stop_server() {
    local stopped=false

    # 1. Stop systemd service if active
    if command -v systemctl >/dev/null 2>&1 && [ "$IS_TERMUX" = false ]; then
        if systemctl --user is-active --quiet opsforge.service 2>/dev/null; then
            echo -e "${CYAN}⏹️  Stopping systemd user service...${NC}"
            systemctl --user stop opsforge.service
            stopped=true
        fi
    fi

    # 2. Stop PID file daemon
    if [ -f "$PID_FILE" ]; then
        local pid
        pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "${CYAN}⏹️  Stopping OpsForge daemon (PID: $pid)...${NC}"
            kill "$pid" || true
            sleep 1
            if kill -0 "$pid" 2>/dev/null; then
                kill -9 "$pid" 2>/dev/null || true
            fi
            stopped=true
        fi
        rm -f "$PID_FILE"
    fi

    if [ "$stopped" = true ]; then
        echo -e "${GREEN}✓ OpsForge stopped.${NC}"
    else
        echo -e "${YELLOW}ℹ️  No running OpsForge process or service found.${NC}"
    fi
}

show_status() {
    echo -e "${BOLD}=== OpsForge Status ===${NC}"
    
    # Check systemd
    if command -v systemctl >/dev/null 2>&1 && [ "$IS_TERMUX" = false ]; then
        if systemctl --user is-active --quiet opsforge.service 2>/dev/null; then
            echo -e " • Systemd Service: ${GREEN}Active (running)${NC}"
        else
            echo -e " • Systemd Service: ${YELLOW}Inactive${NC}"
        fi
    fi

    # Check background daemon
    if [ -f "$PID_FILE" ]; then
        local pid
        pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e " • Daemon Process:  ${GREEN}Running (PID: $pid)${NC}"
        else
            echo -e " • Daemon Process:  ${RED}Stale PID file ($pid)${NC}"
        fi
    else
        echo -e " • Daemon Process:  ${YELLOW}Not running${NC}"
    fi

    # Check Port 5000
    if command -v ss >/dev/null 2>&1; then
        if ss -tulpn 2>/dev/null | grep -q ":5000 "; then
            echo -e " • Port 5000:       ${GREEN}Listening (http://127.0.0.1:5000)${NC}"
        else
            echo -e " • Port 5000:       ${YELLOW}Not in use${NC}"
        fi
    elif command -v netstat >/dev/null 2>&1; then
        if netstat -tulpn 2>/dev/null | grep -q ":5000 "; then
            echo -e " • Port 5000:       ${GREEN}Listening (http://127.0.0.1:5000)${NC}"
        else
            echo -e " • Port 5000:       ${YELLOW}Not in use${NC}"
        fi
    fi
}

# ------------------------------------------------------------------------------
# Main Dispatcher
# ------------------------------------------------------------------------------
ACTION="${1:-prod}"

case "$ACTION" in
    prod|start|"")
        shift 2>/dev/null || true
        start_prod "$@"
        ;;
    dev)
        shift
        start_dev "$@"
        ;;
    daemon|bg)
        shift
        start_daemon "$@"
        ;;
    service|--systemd|systemd)
        setup_environment
        setup_systemd
        ;;
    stop)
        stop_server
        ;;
    restart)
        stop_server
        sleep 1
        start_daemon
        ;;
    status)
        show_status
        ;;
    setup)
        setup_environment
        echo -e "${GREEN}✅ Setup complete! Environment and dependencies ready.${NC}"
        ;;
    help|-h|--help)
        echo -e "${BOLD}OpsForge Universal Management Script${NC}"
        echo -e ""
        echo -e "Usage: ${CYAN}./opsforge.sh [command]${NC}"
        echo -e ""
        echo -e "Commands:"
        echo -e "  ${GREEN}prod${NC} (default)    Run OpsForge in production mode (Waitress WSGI)"
        echo -e "  ${GREEN}dev${NC}             Run in development mode with Flask debug server"
        echo -e "  ${GREEN}daemon${NC}          Run in background as a daemon process (ideal for Termux/headless)"
        echo -e "  ${GREEN}service${NC}         Install and start as a user systemd service (Linux/laptop)"
        echo -e "  ${GREEN}stop${NC}            Stop the background daemon or systemd service"
        echo -e "  ${GREEN}restart${NC}         Restart background service"
        echo -e "  ${GREEN}status${NC}          Check running status and port"
        echo -e "  ${GREEN}setup${NC}           Only set up virtual environment and install dependencies"
        echo -e "  ${GREEN}help${NC}            Show this help message"
        ;;
    *)
        # Forward any custom flags directly to prod runner
        start_prod "$@"
        ;;
esac
