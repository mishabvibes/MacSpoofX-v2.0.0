# MacSpoofX Examples

This directory contains practical example scripts demonstrating various use cases of MacSpoofX.

## \ud83d\udcda Available Examples

### Example 1: Basic Random MAC Spoofing
**File**: `example1_basic_random.sh`

The simplest use case - change MAC to a random address and reset.

```bash
chmod +x example1_basic_random.sh
sudo ./example1_basic_random.sh
```

**What it demonstrates:**
- Auto-detection of network interface
- Random MAC generation
- Resetting to original MAC

---

### Example 2: Custom MAC Address Spoofing
**File**: `example2_custom_mac.sh`

Set specific MAC addresses for testing MAC filtering.

```bash
chmod +x example2_custom_mac.sh
sudo ./example2_custom_mac.sh
```

**What it demonstrates:**
- Setting custom MAC addresses
- Verification of changes
- Multiple MAC changes in sequence

---

### Example 3: Scheduled MAC Rotation
**File**: `example3_scheduled_rotation.sh`

Automatically rotate MAC addresses at regular intervals.

```bash
chmod +x example3_scheduled_rotation.sh
sudo ./example3_scheduled_rotation.sh
```

**What it demonstrates:**
- Scheduled automatic changes
- JSON logging
- Long-running operations
- Graceful shutdown (Ctrl+C)

---

### Example 4: Stealth Mode Operation
**File**: `example4_stealth_mode.sh`

Enable stealth mode with iptables integration.

```bash
chmod +x example4_stealth_mode.sh
sudo ./example4_stealth_mode.sh
```

**What it demonstrates:**
- iptables integration
- Stealth mode features
- Rule cleanup
- Before/after comparison

---

### Example 5: Network Monitoring During Spoofing
**File**: `example5_network_monitoring.sh`

Monitor network traffic while performing MAC spoofing.

```bash
chmod +x example5_network_monitoring.sh
sudo ./example5_network_monitoring.sh
```

**What it demonstrates:**
- Packet capture with tcpdump
- Network analysis
- Connectivity testing
- Traffic inspection

---

## \ud83d\ude80 Quick Start

### Run All Examples

```bash
# Make all scripts executable
chmod +x *.sh

# Run examples in order
sudo ./example1_basic_random.sh
sudo ./example2_custom_mac.sh
sudo ./example3_scheduled_rotation.sh
sudo ./example4_stealth_mode.sh
sudo ./example5_network_monitoring.sh
```

### Prerequisites

All examples require:
- Root/sudo privileges
- MacSpoofX installed in parent directory
- Kali Linux or compatible Linux distribution

Some examples may require additional tools:
- `tcpdump` (Example 5)
- `tshark` (Example 5, optional)
- `jq` (for JSON analysis)

---

## \ud83d\udcdd Output Files

Examples generate various output files:

| Example | Output Files | Description |
|---------|-------------|-------------|
| 1 | None | Console output only |
| 2 | None | Console output only |
| 3 | `rotation_log_*.json` | MAC change history |
| 4 | `stealth_test_*.json`<br>`iptables_*.txt` | Activity log and iptables snapshots |
| 5 | `capture_*.pcap`<br>`monitoring_log_*.json` | Packet capture and activity log |

---

## \ud83d\udd27 Customization

### Modify Intervals

Edit example scripts to change timing:

```bash
# In example3_scheduled_rotation.sh
INTERVAL=30  # Change to desired seconds
```

### Change Interfaces

Specify different interface:

```bash
# Add to command
sudo python3 ../macspoofx.py --interface wlan0 --mode random
```

### Custom MAC Addresses

Edit example2 to use your own MACs:

```bash
# In example2_custom_mac.sh
CUSTOM_MAC_1="00:11:22:33:44:55"  # Your MAC here
```

---

## \u26a0\ufe0f Important Notes

1. **Always run with sudo**: MAC spoofing requires root privileges
2. **Authorized networks only**: Use only on networks you own or have permission to test
3. **Reset when done**: Always reset MAC to original after testing
4. **Monitor for issues**: Watch for network disruptions
5. **Review logs**: Check generated files for audit trails

---

## \ud83d\udd0d Analysis Commands

### View JSON Logs

```bash
# Pretty print JSON
cat rotation_log_*.json | jq '.'

# Count changes
cat rotation_log_*.json | jq '. | length'

# Extract specific fields
cat rotation_log_*.json | jq '.[] | {timestamp, old_mac, new_mac}'
```

### Analyze Packet Captures

```bash
# View with tcpdump
sudo tcpdump -r capture_*.pcap -n -e

# View with tshark
tshark -r capture_*.pcap

# Open in Wireshark
wireshark capture_*.pcap
```

### Check iptables

```bash
# View current rules
sudo iptables -L -v

# Compare before/after
diff iptables_before.txt iptables_after.txt
```

---

## \ud83d\udc1b Troubleshooting

### Permission Denied

```bash
# Ensure script is executable
chmod +x example*.sh

# Run with sudo
sudo ./example1_basic_random.sh
```

### Interface Not Found

```bash
# List available interfaces
ip link show

# Edit script to specify interface
# Add --interface <name> to macspoofx.py command
```

### Tool Not Found

```bash
# Install missing tools
sudo apt update
sudo apt install tcpdump tshark jq
```

### Network Disconnection

```bash
# Emergency reset
sudo python3 ../macspoofx.py --mode reset
sudo systemctl restart NetworkManager
```

---

## \ud83c\udfaf Learning Objectives

These examples teach:

1. **Basic Operations**: Understanding MAC spoofing mechanics
2. **Scheduling**: Automating security tasks
3. **Stealth Techniques**: Reducing detection footprint
4. **Network Analysis**: Monitoring and analyzing traffic
5. **Tool Integration**: Combining multiple security tools
6. **Logging**: Maintaining audit trails
7. **Cleanup**: Proper restoration procedures

---

## \ud83d\udcda Additional Resources

- **Main Documentation**: ../README.md
- **Usage Guide**: ../USAGE_GUIDE.md
- **Security Guidelines**: ../SECURITY.md
- **Tool Help**: `sudo python3 ../macspoofx.py --help`

---

## \u2705 Best Practices

When running examples:

1. **Test in safe environment** - Use isolated lab networks
2. **Read the script first** - Understand what it will do
3. **Backup configurations** - Save original settings
4. **Monitor actively** - Watch for issues during execution
5. **Document results** - Keep records of testing
6. **Clean up** - Reset changes and remove temporary files

---

**Happy learning! \ud83d\udc27\ud83d\udd12**

*For educational purposes only. Always obtain proper authorization.*
