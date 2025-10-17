#!/bin/bash
# Example 5: Network Monitoring During Spoofing
# This script monitors network changes while spoofing

echo "=============================================="
echo "Example 5: Network Monitoring During Spoofing"
echo "=============================================="

# Check if tcpdump is available
if ! command -v tcpdump &> /dev/null; then
    echo "[!] tcpdump not found. Installing..."
    sudo apt install -y tcpdump
fi

INTERFACE=$(ip route | grep default | awk '{print $5}' | head -n1)
CAPTURE_FILE="capture_$(date +%Y%m%d_%H%M%S).pcap"
LOG_FILE="monitoring_log_$(date +%Y%m%d_%H%M%S).json"

echo "[*] Configuration:"
echo "    Interface: $INTERFACE"
echo "    Capture file: $CAPTURE_FILE"
echo "    Log file: $LOG_FILE"
echo ""

# Start packet capture in background
echo "[*] Starting packet capture..."
sudo tcpdump -i $INTERFACE -w $CAPTURE_FILE -c 100 &
TCPDUMP_PID=$!

sleep 2

# Perform MAC spoofing
echo ""
echo "[*] Original MAC:"
ip link show $INTERFACE | grep "link/ether"

echo ""
echo "[*] Changing MAC address..."
sudo python3 ../macspoofx.py \
    --interface $INTERFACE \
    --mode random \
    --output $LOG_FILE \
    --verbose

echo ""
echo "[*] New MAC:"
ip link show $INTERFACE | grep "link/ether"

# Test connectivity
echo ""
echo "[*] Testing network connectivity..."
ping -c 5 8.8.8.8

# Wait for tcpdump to finish
echo ""
echo "[*] Waiting for packet capture to complete..."
wait $TCPDUMP_PID

# Analysis
echo ""
echo "[*] Packet capture complete!"
echo "[*] Analyzing capture..."

if command -v tshark &> /dev/null; then
    echo ""
    echo "[*] Top 5 MAC addresses in capture:"
    sudo tshark -r $CAPTURE_FILE -T fields -e eth.src 2>/dev/null | sort | uniq -c | sort -rn | head -5
else
    echo "[!] tshark not installed. Install wireshark for analysis:"
    echo "    sudo apt install wireshark"
fi

# Reset MAC
echo ""
read -p "Press Enter to reset MAC to original..."
sudo python3 ../macspoofx.py --mode reset --verbose

# Summary
echo ""
echo "[*] Files generated:"
echo "    Packet capture: $CAPTURE_FILE (analyze with Wireshark)"
echo "    Activity log:   $LOG_FILE"
echo ""
echo "    To analyze with Wireshark:"
echo "    wireshark $CAPTURE_FILE"

echo ""
echo "[+] Example completed!"
