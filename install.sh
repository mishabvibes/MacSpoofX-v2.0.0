#!/bin/bash

# MacSpoofX Installation Script
# For Kali Linux
# Educational purposes only

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                  MacSpoofX Installation                      ║
║          Advanced MAC Address Spoofing Tool                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}[!] This tool is designed for Linux (Kali Linux recommended)${NC}"
    exit 1
fi

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${YELLOW}[!] This script requires sudo privileges for some installations${NC}"
   echo -e "${YELLOW}[!] You may be prompted for your password${NC}"
fi

echo -e "${CYAN}[*] Checking system requirements...${NC}\n"

# Check Python version
echo -e "${CYAN}[*] Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}[+] Python 3 found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}[-] Python 3 not found. Please install Python 3.7 or higher${NC}"
    exit 1
fi

# Check pip
echo -e "${CYAN}[*] Checking pip installation...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}[+] pip3 found${NC}"
else
    echo -e "${YELLOW}[!] pip3 not found. Installing...${NC}"
    sudo apt update
    sudo apt install -y python3-pip
fi

# Check macchanger
echo -e "\n${CYAN}[*] Checking macchanger installation...${NC}"
if command -v macchanger &> /dev/null; then
    MACCHANGER_VERSION=$(macchanger --version 2>&1 | head -n1)
    echo -e "${GREEN}[+] macchanger found: $MACCHANGER_VERSION${NC}"
else
    echo -e "${YELLOW}[!] macchanger not found. Installing...${NC}"
    sudo apt update
    sudo apt install -y macchanger
    echo -e "${GREEN}[+] macchanger installed successfully${NC}"
fi

# Check iptables
echo -e "\n${CYAN}[*] Checking iptables installation...${NC}"
if command -v iptables &> /dev/null; then
    echo -e "${GREEN}[+] iptables found${NC}"
else
    echo -e "${YELLOW}[!] iptables not found. Installing...${NC}"
    sudo apt install -y iptables
fi

# Check ethtool (optional but recommended)
echo -e "\n${CYAN}[*] Checking ethtool installation...${NC}"
if command -v ethtool &> /dev/null; then
    echo -e "${GREEN}[+] ethtool found${NC}"
else
    echo -e "${YELLOW}[!] ethtool not found. Installing (optional, recommended)...${NC}"
    sudo apt install -y ethtool
fi

# Install Python dependencies
echo -e "\n${CYAN}[*] Installing Python dependencies...${NC}"

if [ -f "requirements.txt" ]; then
    echo -e "${CYAN}[*] Installing from requirements.txt...${NC}"
    pip3 install -r requirements.txt --user
else
    echo -e "${CYAN}[*] Installing individual packages...${NC}"
    pip3 install --user prettytable schedule netifaces colorama
fi

echo -e "${GREEN}[+] Python dependencies installed${NC}"

# Make script executable
echo -e "\n${CYAN}[*] Making macspoofx.py executable...${NC}"
if [ -f "macspoofx.py" ]; then
    chmod +x macspoofx.py
    echo -e "${GREEN}[+] macspoofx.py is now executable${NC}"
else
    echo -e "${RED}[-] macspoofx.py not found in current directory${NC}"
    exit 1
fi

# Create symbolic link (optional)
echo -e "\n${CYAN}[*] Would you like to create a system-wide command 'macspoofx'? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    SCRIPT_PATH=$(pwd)/macspoofx.py
    sudo ln -sf "$SCRIPT_PATH" /usr/local/bin/macspoofx
    echo -e "${GREEN}[+] Created symlink: You can now run 'sudo macspoofx' from anywhere${NC}"
fi

# Test installation
echo -e "\n${CYAN}[*] Testing installation...${NC}"
if python3 -c "import prettytable, schedule, netifaces, colorama" 2>/dev/null; then
    echo -e "${GREEN}[+] All Python modules imported successfully${NC}"
else
    echo -e "${RED}[-] Some Python modules failed to import${NC}"
    exit 1
fi

# Display summary
echo -e "\n${GREEN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              Installation Completed Successfully!            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${CYAN}Quick Start:${NC}"
echo -e "${YELLOW}  List interfaces:${NC}    sudo python3 macspoofx.py --list-interfaces"
echo -e "${YELLOW}  Random MAC:${NC}         sudo python3 macspoofx.py --mode random"
echo -e "${YELLOW}  Custom MAC:${NC}         sudo python3 macspoofx.py --mode custom --custom-mac 00:11:22:33:44:55"
echo -e "${YELLOW}  Reset MAC:${NC}          sudo python3 macspoofx.py --mode reset"
echo -e "${YELLOW}  View help:${NC}          sudo python3 macspoofx.py --help"

echo -e "\n${CYAN}Documentation:${NC}"
echo -e "  README.md       - Complete documentation"
echo -e "  USAGE_GUIDE.md  - Practical examples and scenarios"

echo -e "\n${RED}⚠️  IMPORTANT REMINDER:${NC}"
echo -e "${YELLOW}This tool is for educational purposes only.${NC}"
echo -e "${YELLOW}Only use on networks you own or have explicit permission to test.${NC}"
echo -e "${YELLOW}Unauthorized MAC spoofing may violate laws.${NC}"

echo -e "\n${GREEN}Happy ethical hacking! 🐧🔒${NC}\n"
