# MacSpoofX Usage Guide

## Practical Examples and Scenarios

### \ud83c\udfaf Scenario-Based Usage

---

## 1. Basic Network Testing

### Scenario: Test MAC filtering on your network
```bash
# Step 1: Record current MAC
sudo python3 macspoofx.py --list-interfaces

# Step 2: Change to random MAC
sudo python3 macspoofx.py --interface wlan0 --mode random --verbose

# Step 3: Test network connectivity
ping -c 4 8.8.8.8

# Step 4: Reset to original
sudo python3 macspoofx.py --mode reset
```

---

## 2. Privacy Testing

### Scenario: Simulate device anonymity for privacy research
```bash
# Rotate MAC every 5 minutes
sudo python3 macspoofx.py \
  --mode random \
  --timeout 300 \
  --stealth \
  --output privacy_test.json \
  --verbose
```

**What happens:**
- New MAC every 5 minutes
- Stealth mode reduces network fingerprinting
- All changes logged to JSON
- Press Ctrl+C to stop

---

## 3. Vendor Spoofing

### Scenario: Test as different manufacturers
```bash
# Spoof as a random known vendor
sudo python3 macspoofx.py --mode vendor

# Example: This might give you a MAC like:
# 00:1A:2B:XX:XX:XX (Cisco Systems)
# 00:50:56:XX:XX:XX (VMware)
# DC:A6:32:XX:XX:XX (Raspberry Pi)
```

---

## 4. Penetration Testing Workflow

### Scenario: Authorized pentest on corporate network
```bash
# Phase 1: Reconnaissance
sudo python3 macspoofx.py --list-interfaces

# Phase 2: Initial access testing
sudo python3 macspoofx.py \
  --interface eth0 \
  --mode random \
  --verbose \
  --output pentest_phase1.json

# Phase 3: Document and reset
sudo python3 macspoofx.py --mode reset

# Review results
cat pentest_phase1.json
```

---

## 5. DHCP Pool Exhaustion Testing

### Scenario: Test DHCP server resilience
```bash
# WARNING: Only on your own test network!

# Rapid MAC changes to request multiple IPs
sudo python3 macspoofx.py \
  --mode random \
  --timeout 30 \
  --output dhcp_test.csv
```

**After each change:**
1. New MAC is applied
2. System requests new DHCP lease
3. Different IP assigned (if successful)
4. Results logged to CSV

---

## 6. Wireless Security Testing

### Scenario: Test wireless MAC filtering bypass
```bash
# Step 1: Put wireless card in monitor mode (if needed)
sudo airmon-ng start wlan0

# Step 2: Identify allowed MAC (passive scanning)
sudo airodump-ng wlan0mon

# Step 3: Spoof to allowed MAC
sudo airmon-ng stop wlan0mon
sudo python3 macspoofx.py \
  --interface wlan0 \
  --mode custom \
  --custom-mac 00:11:22:33:44:55

# Step 4: Attempt connection
sudo systemctl restart NetworkManager
```

---

## 7. Multi-Interface Testing

### Scenario: Spoof multiple interfaces for load testing
```bash
# Note: Current CLI doesn't expose this, but code supports it
# Future feature - currently requires code modification

# In Python script:
interfaces = ['eth0', 'wlan0', 'eth1']
app.execute_multithreaded_spoofing(interfaces)
```

---

## 8. Scheduled Rotation for Anonymity

### Scenario: Long-term monitoring with rotating identity
```bash
# Background process with 10-minute intervals
nohup sudo python3 macspoofx.py \
  --mode random \
  --timeout 600 \  # 10 minutes
  --stealth \
  --output /var/log/mac_rotation.json \
  --verbose > /dev/null 2>&1 &

# Check process
ps aux | grep macspoofx

# Stop when done
sudo pkill -f macspoofx.py
```

---

## 9. Forensics and Auditing

### Scenario: Generate audit trail for compliance
```bash
# Comprehensive logging setup
sudo python3 macspoofx.py \
  --interface eth0 \
  --mode random \
  --timeout 120 \
  --verbose \
  --output /home/kali/audits/mac_test_$(date +%Y%m%d_%H%M%S).json

# Later, review all changes
cat /home/kali/audits/mac_test_*.json | jq '.'
```

---

## 10. Integration with Other Kali Tools

### Scenario: Combine with network scanning
```bash
# Script example: mac_rotate_scan.sh
#!/bin/bash

for i in {1..5}; do
    echo "[*] Rotation $i"
    
    # Change MAC
    sudo python3 macspoofx.py --mode random
    
    # Wait for network
    sleep 5
    
    # Run nmap scan
    sudo nmap -sn 192.168.1.0/24 -oN scan_$i.txt
    
    # Wait before next rotation
    sleep 30
done

# Reset MAC
sudo python3 macspoofx.py --mode reset
```

---

## \ud83d\udd0d Verification Techniques

### Check if MAC changed successfully

#### Method 1: Using ip command
```bash
ip link show wlan0 | grep link/ether
```

#### Method 2: Using macchanger
```bash
macchanger -s wlan0
```

#### Method 3: Using ifconfig
```bash
ifconfig wlan0 | grep ether
```

#### Method 4: Monitor network traffic
```bash
sudo tcpdump -i wlan0 -e -n -c 10
# Look for the MAC address in the output
```

---

## \ud83d\udea8 Emergency Recovery

### If something goes wrong

#### Quick reset
```bash
# Reset MAC immediately
sudo python3 macspoofx.py --mode reset

# Restart network services
sudo systemctl restart NetworkManager

# Or manually
sudo ip link set wlan0 down
sudo ip link set wlan0 up
```

#### Complete network restart
```bash
# Stop all networking
sudo systemctl stop NetworkManager

# Reset all interfaces
for iface in $(ip link show | grep -oP '^\d+: \K[^:]+'); do
    if [ "$iface" != "lo" ]; then
        sudo ip link set $iface down
        sudo macchanger -p $iface 2>/dev/null
        sudo ip link set $iface up
    fi
done

# Start networking
sudo systemctl start NetworkManager
```

---

## \ud83d\udcca Monitoring and Analysis

### Real-time monitoring during spoofing

#### Terminal 1: Run MacSpoofX
```bash
sudo python3 macspoofx.py --mode random --timeout 60 --verbose
```

#### Terminal 2: Monitor network
```bash
watch -n 1 'ip link show wlan0 | grep "link/ether"'
```

#### Terminal 3: Monitor connectivity
```bash
while true; do
    ping -c 1 -W 1 8.8.8.8 >/dev/null 2>&1 && echo "[$(date)] ONLINE" || echo "[$(date)] OFFLINE"
    sleep 2
done
```

#### Terminal 4: Monitor DHCP
```bash
sudo tail -f /var/log/syslog | grep -i dhcp
```

---

## \ud83d\udcdd Logging Best Practices

### Structured logging for analysis

#### JSON format for programmatic access
```bash
sudo python3 macspoofx.py \
  --mode random \
  --timeout 60 \
  --output test_$(date +%Y%m%d_%H%M%S).json
```

#### CSV format for spreadsheet analysis
```bash
sudo python3 macspoofx.py \
  --mode random \
  --timeout 60 \
  --output test_$(date +%Y%m%d_%H%M%S).csv
```

#### Analyze JSON logs
```bash
# Count total changes
jq 'length' results.json

# Extract only successful random changes
jq '.[] | select(.mode == "random")' results.json

# Get unique interfaces tested
jq -r '.[].interface' results.json | sort -u

# Timeline of changes
jq -r '.[] | "\(.timestamp) | \(.old_mac) -> \(.new_mac)"' results.json
```

---

## \ud83e\uddd1\u200d\ud83d\udcbb Advanced Techniques

### Custom MAC patterns

#### Specific vendor spoofing
```bash
# Dell Inc: 00:14:22:XX:XX:XX
sudo python3 macspoofx.py --mode custom --custom-mac 00:14:22:AB:CD:EF

# Intel: 00:1B:77:XX:XX:XX
sudo python3 macspoofx.py --mode custom --custom-mac 00:1B:77:11:22:33

# Apple: 00:1E:C2:XX:XX:XX
sudo python3 macspoofx.py --mode custom --custom-mac 00:1E:C2:AA:BB:CC
```

### Stealth operations

#### Minimal network footprint
```bash
# Stealth mode with vendor MAC
sudo python3 macspoofx.py \
  --mode vendor \
  --stealth \
  --output /dev/null  # No output file

# Check iptables rules applied
sudo iptables -L -v | grep -A 5 "wlan0"
```

---

## \ud83d\udee0\ufe0f Troubleshooting Common Issues

### Issue: Interface stays down after spoofing

**Solution:**
```bash
sudo ip link set <interface> up
sudo systemctl restart NetworkManager
```

### Issue: No internet after MAC change

**Solution:**
```bash
# Release and renew DHCP
sudo dhclient -r <interface>
sudo dhclient <interface>

# Or use NetworkManager
sudo nmcli device disconnect <interface>
sudo nmcli device connect <interface>
```

### Issue: Can't change MAC (device busy)

**Solution:**
```bash
# Kill processes using the interface
sudo systemctl stop NetworkManager
sudo python3 macspoofx.py --mode random
sudo systemctl start NetworkManager
```

### Issue: Permission denied even with sudo

**Solution:**
```bash
# Check if running as root
whoami

# Force root shell
sudo su
python3 macspoofx.py --mode random
exit
```

---

## \ud83d\udcca Performance Benchmarking

### Test MAC change speed

```bash
# Time a single change
time sudo python3 macspoofx.py --mode random

# Typical results:
# real    0m1.234s  (Total time)
# user    0m0.456s  (CPU time)
# sys     0m0.123s  (System time)
```

### Measure network downtime

```bash
#!/bin/bash
# test_downtime.sh

ping -c 100 192.168.1.1 > ping_before.txt &
PING_PID=$!

sleep 5

sudo python3 macspoofx.py --mode random

wait $PING_PID

# Analyze ping_before.txt for packet loss
grep "packet loss" ping_before.txt
```

---

## \ud83c\udfaf Testing Scenarios Matrix

| Scenario | Mode | Timeout | Stealth | Output | Use Case |
|----------|------|---------|---------|--------|----------|
| Quick test | random | 0 | No | None | Fast verification |
| Privacy research | random | 300 | Yes | JSON | Long-term anonymity |
| Vendor testing | vendor | 0 | No | CSV | Manufacturer simulation |
| Pentest | custom | 0 | Yes | JSON | Bypass MAC filtering |
| Load testing | random | 30 | No | CSV | DHCP stress test |
| Audit trail | random | 60 | No | JSON | Compliance logging |

---

## \ud83d\udd12 Security Considerations

### Before spoofing:
1. \u2714\ufe0f Verify you have authorization
2. \u2714\ufe0f Document original MAC address
3. \u2714\ufe0f Backup network configuration
4. \u2714\ufe0f Prepare recovery procedure
5. \u2714\ufe0f Notify relevant parties (if required)

### During spoofing:
1. \u2714\ufe0f Monitor for detection systems
2. \u2714\ufe0f Keep detailed logs
3. \u2714\ufe0f Watch for connectivity issues
4. \u2714\ufe0f Avoid aggressive timeout values
5. \u2714\ufe0f Be ready to reset immediately

### After spoofing:
1. \u2714\ufe0f Reset to original MAC
2. \u2714\ufe0f Verify network stability
3. \u2714\ufe0f Document findings
4. \u2714\ufe0f Clean up iptables rules
5. \u2714\ufe0f Archive logs securely

---

## \ud83d\udcda Additional Resources

### Learn more about MAC addresses
- IEEE OUI Database: https://standards-oui.ieee.org/
- MAC Address Lookup: https://macaddress.io/
- Wireshark OUI Database: https://www.wireshark.org/tools/oui-lookup.html

### Kali Linux documentation
- Kali Tools: https://www.kali.org/tools/
- Network Assessment: https://www.kali.org/docs/categories/network-assessment/
- Wireless Attacks: https://www.kali.org/docs/categories/wireless-attacks/

### Related tools to explore
- `aircrack-ng` suite: Wireless security testing
- `ettercap`: Network sniffing and MITM
- `Wireshark`: Packet analysis
- `tcpdump`: Command-line packet analyzer
- `nmap`: Network discovery and security auditing

---

**Remember**: Always use MacSpoofX responsibly and ethically! \ud83d\udd12\ud83d\udc27

Happy ethical hacking!
