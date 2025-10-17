#!/bin/bash
# Example 1: Basic Random MAC Spoofing
# This script demonstrates the simplest use case

echo "======================================"
echo "Example 1: Basic Random MAC Spoofing"
echo "======================================"

# Auto-detect interface and apply random MAC
echo "[*] Changing MAC to random address..."
sudo python3 ../macspoofx.py --mode random --verbose

# Show current status
echo ""
echo "[*] Current interface status:"
ip link show | grep -A 1 "state UP"

# Reset after testing
echo ""
read -p "Press Enter to reset MAC to original..."
sudo python3 ../macspoofx.py --mode reset --verbose

echo ""
echo "[+] Example completed!"
