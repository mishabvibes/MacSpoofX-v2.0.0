#!/bin/bash
# Example 3: Scheduled MAC Rotation
# This script demonstrates automatic MAC rotation

echo "===================================="
echo "Example 3: Scheduled MAC Rotation"
echo "===================================="

# Configuration
INTERVAL=30  # seconds between changes
OUTPUT_FILE="rotation_log_$(date +%Y%m%d_%H%M%S).json"

echo "[*] Configuration:"
echo "    Interval: $INTERVAL seconds"
echo "    Output: $OUTPUT_FILE"
echo ""

echo "[*] Starting scheduled MAC rotation..."
echo "[*] Press Ctrl+C to stop"
echo ""

# Start rotation with timeout
sudo python3 ../macspoofx.py \
    --mode random \
    --timeout $INTERVAL \
    --output $OUTPUT_FILE \
    --verbose

# This runs until Ctrl+C is pressed
# The cleanup happens automatically in the script

echo ""
echo "[+] Rotation stopped"
echo "[*] Results saved to: $OUTPUT_FILE"

# Display summary
if [ -f "$OUTPUT_FILE" ]; then
    echo ""
    echo "[*] Summary of changes:"
    echo "    Total changes: $(cat $OUTPUT_FILE | jq '. | length')"
    echo ""
    echo "[*] View full log with: cat $OUTPUT_FILE | jq '.'"
fi

echo ""
echo "[+] Example completed!"
