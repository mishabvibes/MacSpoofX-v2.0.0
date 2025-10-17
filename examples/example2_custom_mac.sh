#!/bin/bash
# Example 2: Custom MAC Address Spoofing
# This script shows how to set a specific MAC address

echo "========================================="
echo "Example 2: Custom MAC Address Spoofing"
echo "========================================="

# Define custom MAC addresses (examples)
CUSTOM_MAC_1="00:11:22:33:44:55"
CUSTOM_MAC_2="DE:AD:BE:EF:CA:FE"

echo "[*] Original MAC:"
ip link show | grep -A 1 "state UP" | grep "link/ether"

echo ""
echo "[*] Setting custom MAC: $CUSTOM_MAC_1"
sudo python3 ../macspoofx.py --mode custom --custom-mac $CUSTOM_MAC_1 --verbose

echo ""
echo "[*] Verifying change:"
ip link show | grep -A 1 "state UP" | grep "link/ether"

# Optional: Change to second MAC
echo ""
read -p "Change to second MAC ($CUSTOM_MAC_2)? (y/n): " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "[*] Setting second custom MAC: $CUSTOM_MAC_2"
    sudo python3 ../macspoofx.py --mode custom --custom-mac $CUSTOM_MAC_2 --verbose
    
    echo ""
    echo "[*] Current MAC:"
    ip link show | grep -A 1 "state UP" | grep "link/ether"
fi

# Reset
echo ""
read -p "Press Enter to reset to original MAC..."
sudo python3 ../macspoofx.py --mode reset --verbose

echo ""
echo "[+] Example completed!"
