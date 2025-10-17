#!/bin/bash
# Example 4: Stealth Mode Operation
# This script demonstrates stealth mode with iptables

echo "================================"
echo "Example 4: Stealth Mode Testing"
echo "================================"

OUTPUT_FILE="stealth_test_$(date +%Y%m%d_%H%M%S).json"

echo "[*] Backup current iptables rules..."
sudo iptables -L -v > iptables_before.txt
echo "[+] Saved to: iptables_before.txt"

echo ""
echo "[*] Starting stealth mode MAC spoofing..."
echo "[*] This will:"
echo "    1. Change MAC to random address"
echo "    2. Enable iptables stealth rules"
echo "    3. Reduce network visibility"
echo ""

sudo python3 ../macspoofx.py \
    --mode random \
    --stealth \
    --output $OUTPUT_FILE \
    --verbose

echo ""
echo "[*] Stealth mode enabled!"
echo "[*] Checking iptables rules..."
sudo iptables -L -v > iptables_after.txt

echo ""
echo "[*] Comparing iptables (before vs after):"
echo "    Before: $(wc -l < iptables_before.txt) lines"
echo "    After:  $(wc -l < iptables_after.txt) lines"

echo ""
read -p "Press Enter to disable stealth mode and reset..."

# Reset (this should clean up iptables rules automatically)
sudo python3 ../macspoofx.py --mode reset

# Verify cleanup
echo ""
echo "[*] Verifying iptables cleanup..."
sudo iptables -L -v > iptables_final.txt

echo ""
echo "[*] Results:"
echo "    Before stealth: iptables_before.txt"
echo "    With stealth:   iptables_after.txt"
echo "    After cleanup:  iptables_final.txt"
echo "    Activity log:   $OUTPUT_FILE"

echo ""
echo "[+] Example completed!"
