# MacSpoofX v2.0.0

## Advanced MAC Address Spoofing Tool for Kali Linux

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Kali%20Linux-red.svg)
![License](https://img.shields.io/badge/license-Educational-green.svg)

---

## ⚠️ DISCLAIMER

**This tool is for educational purposes only.**

MacSpoofX is designed for network administrators, security researchers, and ethical hackers to test network security configurations on their own networks or networks they have explicit permission to test.

**WARNING:**
- Unauthorized MAC address spoofing may violate local, state, or federal laws
- Only use this tool on networks you own or have written authorization to test
- The authors are not responsible for any misuse or damage caused by this tool
- Always obtain proper authorization before conducting security testing

---

## 📋 Table of Contents

- [Features](#features)
- [Technical Overview](#technical-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Command-Line Arguments](#command-line-arguments)
- [Usage Examples](#usage-examples)
- [Spoofing Modes](#spoofing-modes)
- [Advanced Features](#advanced-features)
- [Kali Linux Integration](#kali-linux-integration)
- [Output Formats](#output-formats)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Core Functionality
- **Multiple Spoofing Modes**: Random, custom, vendor-specific, sequence, and reset modes
- **Auto-Detection**: Automatically detects available network interfaces
- **Scheduled Changes**: Set time intervals for automatic MAC address rotation
- **Multi-Threading**: Spoof multiple interfaces concurrently for efficiency
- **Stealth Mode**: Reduce network noise with iptables integration

### Kali Linux Integration
- **macchanger**: Primary MAC spoofing engine
- **iptables**: Advanced packet filtering and stealth capabilities
- **ip/ethtool**: Interface management and driver information
- **netifaces**: Python network interface enumeration

### User Experience
- **Colorful CLI**: Beautiful colored terminal output for better readability
- **PrettyTable**: Clean tabular display of results and interface information
- **Verbose Logging**: Detailed debug information when needed
- **Progress Tracking**: Real-time feedback on spoofing operations

### Data Management
- **Export Options**: Save results in JSON or CSV format
- **Change History**: Track all MAC address modifications
- **Comprehensive Logging**: Log file for audit trails

---

## 🔬 Technical Overview

### How MAC Spoofing Works

MAC (Media Access Control) addresses are hardware identifiers assigned to network interface controllers (NICs) at the Data Link Layer (Layer 2) of the OSI model. Each MAC address is a 48-bit identifier typically displayed as six groups of two hexadecimal digits (e.g., `00:1A:2B:3C:4D:5E`).

**Spoofing Process:**

1. **Interface Down**: The network interface must be brought offline
   ```bash
   ip link set <interface> down
   ```

2. **MAC Modification**: The MAC address is changed in kernel space
   ```bash
   macchanger -r <interface>  # Random MAC
   ```

3. **Interface Up**: The interface is brought back online with the new MAC
   ```bash
   ip link set <interface> up
   ```

4. **Verification**: The new MAC address is verified and logged

**Technical Details:**
- Changes are temporary and persist only until reboot or interface restart
- The modification occurs in the kernel's network stack
- The physical hardware MAC remains unchanged
- All network communications use the spoofed MAC address

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     MacSpoofX Core                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐      ┌──────────────────┐        │
│  │ MACAddressValidator│    │ NetworkInterface │        │
│  │   - Validation  │      │     Manager      │        │
│  │   - Formatting  │      │  - Detection     │        │
│  └─────────────────┘      │  - Status        │        │
│                           │  - Configuration │        │
│                           └──────────────────┘        │
│                                                         │
│  ┌─────────────────┐      ┌──────────────────┐        │
│  │   MACChanger    │      │  IPTablesManager │        │
│  │  - Random Mode  │      │  - Stealth Mode  │        │
│  │  - Custom Mode  │      │  - Filtering     │        │
│  │  - Vendor Mode  │      │  - Rules Mgmt    │        │
│  │  - Reset Mode   │      └──────────────────┘        │
│  └─────────────────┘                                   │
│                                                         │
│  ┌─────────────────┐      ┌──────────────────┐        │
│  │ OutputManager   │      │   MacSpoofX      │        │
│  │  - JSON Export  │      │  Main Controller │        │
│  │  - CSV Export   │      │  - Scheduling    │        │
│  │  - Tables       │      │  - Threading     │        │
│  └─────────────────┘      │  - Orchestration │        │
│                           └──────────────────┘        │
└─────────────────────────────────────────────────────────┘
          │                          │
          ▼                          ▼
┌─────────────────┐        ┌──────────────────┐
│ Kali Linux      │        │  Network Stack   │
│ Built-in Tools  │        │  - Kernel Space  │
│ - macchanger    │        │  - NIC Drivers   │
│ - iptables      │        │  - Layer 2       │
│ - ip/ethtool    │        └──────────────────┘
└─────────────────┘
```

---

## 📦 Prerequisites

### System Requirements
- **Operating System**: Kali Linux (2020.1 or later recommended)
- **Python**: Version 3.7 or higher
- **Privileges**: Root/sudo access (required for network operations)

### Pre-installed on Kali Linux
The following tools are typically pre-installed on Kali Linux:
- `macchanger` - MAC address manipulation utility
- `iptables` - Packet filtering framework
- `ip` (iproute2) - Network interface management
- `ethtool` - Network driver and hardware settings tool

### Python Dependencies
The following Python packages will be automatically installed if missing:
- `prettytable` - ASCII table formatting
- `schedule` - Job scheduling library
- `netifaces` - Network interface information
- `colorama` - Colored terminal output

---

## 🚀 Installation

### Step 1: Clone or Download

```bash
# Navigate to your preferred directory
cd ~/Tools

# If you have the files, navigate to the directory
cd mac-spoofing-tool
```

### Step 2: Verify macchanger Installation

```bash
# Check if macchanger is installed
macchanger --version

# If not installed, install it
sudo apt update
sudo apt install macchanger -y
```

During installation, you may be asked if you want macchanger to run automatically. Choose **No** to maintain manual control.

### Step 3: Install Python Dependencies

The script will automatically install missing Python packages on first run. Alternatively, install them manually:

**For Kali Linux 2023+ (Recommended):**
```bash
# Use apt for cleanest installation
sudo apt update
sudo apt install -y python3-prettytable python3-schedule python3-netifaces python3-colorama
```

**Alternative methods:**
```bash
# Method 1: Re-run updated installer (handles everything)
./install.sh

# Method 2: pip with --break-system-packages (safe for Kali)
pip3 install --break-system-packages prettytable schedule netifaces colorama

# Method 3: Virtual environment (most isolated)
python3 -m venv macspoofx-env
source macspoofx-env/bin/activate
pip install -r requirements.txt
```

**Got "externally-managed-environment" error?**  
👉 See [INSTALL_TROUBLESHOOTING.md](INSTALL_TROUBLESHOOTING.md) for detailed solutions.

### Step 4: Make Script Executable

```bash
# Add execute permissions
chmod +x macspoofx.py
```

### Step 5: Verify Installation

```bash
# List available interfaces
sudo python3 macspoofx.py --list-interfaces

# View help
sudo python3 macspoofx.py --help
```

---

## 💻 Usage

### Basic Syntax

```bash
sudo python3 macspoofx.py [OPTIONS]
```

**Important**: Always run with `sudo` or as root, as MAC address modification requires elevated privileges.

---

## 🎛️ Command-Line Arguments

| Argument | Short | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `--interface` | `-i` | string | auto-detect | Network interface to spoof |
| `--mode` | `-m` | choice | random | Spoofing mode (random, custom, vendor, sequence, reset) |
| `--custom-mac` | `-c` | string | None | Custom MAC address for custom mode |
| `--timeout` | `-t` | integer | 0 | Time between changes in seconds (0 = one-time) |
| `--verbose` | `-v` | flag | False | Enable detailed output and logging |
| `--output` | `-o` | string | None | Save results to file (JSON or CSV) |
| `--stealth` | `-s` | flag | False | Enable stealth mode with iptables |
| `--list-interfaces` | `-l` | flag | False | List all network interfaces and exit |

---

## 📚 Usage Examples

### Example 1: Basic Random MAC Spoofing

```bash
# Auto-detect interface and apply random MAC
sudo python3 macspoofx.py --mode random

# Specify interface explicitly
sudo python3 macspoofx.py --interface eth0 --mode random
```

### Example 2: Custom MAC Address

```bash
# Set a specific MAC address
sudo python3 macspoofx.py --mode custom --custom-mac 00:11:22:33:44:55

# With verbose output
sudo python3 macspoofx.py -m custom -c 00:AA:BB:CC:DD:EE -v
```

### Example 3: Vendor-Specific Spoofing

```bash
# Use a random vendor MAC (keeps OUI, randomizes NIC portion)
sudo python3 macspoofx.py --mode vendor

# With stealth mode
sudo python3 macspoofx.py --mode vendor --stealth
```

### Example 4: Scheduled MAC Rotation

```bash
# Change MAC every 60 seconds
sudo python3 macspoofx.py --mode random --timeout 60

# Change every 5 minutes (300 seconds) with logging
sudo python3 macspoofx.py -m random -t 300 -v -o changes.json
```

### Example 5: Stealth Mode Operation

```bash
# Enable stealth mode to reduce network noise
sudo python3 macspoofx.py --mode random --stealth

# Stealth with scheduled changes
sudo python3 macspoofx.py -m random -s -t 120
```

### Example 6: Reset to Original MAC

```bash
# Restore permanent hardware MAC address
sudo python3 macspoofx.py --mode reset

# Reset with verbose output
sudo python3 macspoofx.py -m reset -v
```

### Example 7: Export Results

```bash
# Export to JSON
sudo python3 macspoofx.py -m random -o results.json

# Export to CSV
sudo python3 macspoofx.py -m random -t 30 -o mac_changes.csv
```

### Example 8: List All Interfaces

```bash
# Display all available network interfaces
sudo python3 macspoofx.py --list-interfaces
```

### Example 9: Complete Professional Setup

```bash
# Advanced configuration with all features
sudo python3 macspoofx.py \
  --interface wlan0 \
  --mode random \
  --timeout 180 \
  --stealth \
  --verbose \
  --output /var/log/macspoofx_results.json
```

---

## 🎭 Spoofing Modes

### 1. Random Mode (Default)
**Command**: `--mode random`

- Generates completely random MAC addresses
- Uses `macchanger -r` command
- New MAC is unpredictable
- Best for maximum anonymity

**Example Output:**
```
[+] MAC changed from 00:11:22:33:44:55 to a8:7b:39:2f:c1:d4
```

### 2. Custom Mode
**Command**: `--mode custom --custom-mac XX:XX:XX:XX:XX:XX`

- Set a specific MAC address of your choice
- Useful for testing MAC filtering
- Requires valid MAC format (6 pairs of hex digits)
- Accepts both `:` and `-` separators

**Example:**
```bash
sudo python3 macspoofx.py -m custom -c 00:DE:AD:BE:EF:00
```

### 3. Vendor Mode
**Command**: `--mode vendor`

- Uses vendor-specific OUI (Organizationally Unique Identifier)
- Keeps the first 3 octets from known manufacturers
- Randomizes the last 3 octets
- Appears as legitimate hardware from recognized vendors

**Example:**
```
[+] MAC changed to 00:1A:2B:XX:XX:XX  (Vendor: Cisco Systems)
```

### 4. Sequence Mode
**Command**: `--mode sequence`

- Currently implements random generation
- Future enhancement: Sequential MAC generation
- Useful for testing multiple addresses systematically

### 5. Reset Mode
**Command**: `--mode reset`

- Restores original permanent MAC address
- Uses `macchanger -p` command
- Returns interface to factory hardware MAC
- Essential for cleanup after testing

**Example:**
```
[+] MAC reset from a8:7b:39:2f:c1:d4 to 00:11:22:33:44:55
```

---

## 🔥 Advanced Features

### Scheduled MAC Rotation

Automatically rotate MAC addresses at specified intervals:

```bash
# Change MAC every 2 minutes
sudo python3 macspoofx.py --mode random --timeout 120
```

**Use Cases:**
- Continuous anonymity
- Evading time-based detection
- Testing dynamic MAC filtering
- Long-duration penetration tests

**Process:**
1. Initial MAC change is applied immediately
2. Subsequent changes occur at specified intervals
3. Each change is logged to history
4. Press `Ctrl+C` to stop gracefully

### Stealth Mode

Reduce network fingerprinting with iptables integration:

```bash
sudo python3 macspoofx.py --mode random --stealth
```

**What Stealth Mode Does:**
- Limits broadcast traffic to reduce network noise
- Configures iptables rules for packet filtering
- Minimizes ICMP echo requests
- Reduces ARP broadcast visibility

**Technical Implementation:**
```bash
# Example iptables rules applied
iptables -A OUTPUT -o <interface> -m pkttype --pkt-type broadcast -j DROP
iptables -A OUTPUT -o <interface> -p icmp --icmp-type echo-request -j DROP
```

### Multi-Threaded Operations

While not exposed as a CLI option in the current version, the codebase supports multi-threaded spoofing for testing multiple interfaces simultaneously.

**Future CLI Integration:**
```bash
# Planned feature
sudo python3 macspoofx.py --mode random --all-interfaces
```

### Verbose Logging

Detailed operational information:

```bash
sudo python3 macspoofx.py --mode random --verbose
```

**Verbose Output Includes:**
- Interface up/down operations
- macchanger command execution
- iptables rule application
- Detailed error messages
- Timestamp for each operation

**Log File Location:** `macspoofx.log` in the current directory

---

## 🐧 Kali Linux Integration

### macchanger

**Primary MAC spoofing engine**

MacSpoofX leverages `macchanger`, a powerful GNU/Linux utility designed specifically for viewing and manipulating MAC addresses.

**Key macchanger Commands Used:**
```bash
macchanger -r <interface>    # Random MAC
macchanger -m XX:XX:XX:XX:XX:XX <interface>  # Set specific MAC
macchanger -a <interface>    # Random vendor MAC
macchanger -p <interface>    # Reset to permanent MAC
macchanger -s <interface>    # Show current and permanent MAC
```

**Installation Check:**
```bash
which macchanger
macchanger --version
```

### iptables

**Advanced packet filtering**

The tool integrates with iptables for stealth mode and MAC-based filtering.

**Capabilities:**
- MAC address-based packet filtering
- Broadcast traffic suppression
- ICMP request blocking
- Custom rule management

**Check iptables:**
```bash
iptables --version
sudo iptables -L  # List current rules
```

### ip (iproute2)

**Interface management**

Modern Linux networking tool used for:
- Interface status checks
- Bringing interfaces up/down
- Retrieving current MAC addresses
- IP address information

**Common Commands:**
```bash
ip link show                    # List all interfaces
ip link set <interface> down    # Disable interface
ip link set <interface> up      # Enable interface
ip addr show <interface>        # Show interface details
```

### ethtool

**Hardware information**

Retrieve NIC driver and hardware details:
```bash
ethtool -i <interface>    # Driver information
ethtool -P <interface>    # Permanent MAC address
```

---

## 📊 Output Formats

### Console Output

**Standard Output:**
```
╔══════════════════════════════════════════════════════════════╗
║                      MacSpoofX v2.0.0                        ║
║            Advanced MAC Address Spoofing Tool                ║
║                 For Educational Use Only                     ║
╚══════════════════════════════════════════════════════════════╝

[*] Auto-detected wireless interface: wlan0

[*] Interface Information:
    Interface:     wlan0
    Current MAC:   00:11:22:33:44:55
    Permanent MAC: 00:11:22:33:44:55
    Status:        UP
    IP Address:    192.168.1.100
    Driver:        iwlwifi

[*] Starting MAC spoofing on wlan0...
[*] Mode: random

[+] MAC spoofing successful!
[+] New MAC address: a8:7b:39:2f:c1:d4
```

### JSON Export

**Command:**
```bash
sudo python3 macspoofx.py -m random -o results.json
```

**Output Structure:**
```json
[
  {
    "timestamp": "2024-01-15T14:30:45.123456",
    "interface": "wlan0",
    "mode": "random",
    "old_mac": "00:11:22:33:44:55",
    "new_mac": "a8:7b:39:2f:c1:d4",
    "custom_mac": null
  },
  {
    "timestamp": "2024-01-15T14:32:15.789012",
    "interface": "wlan0",
    "mode": "custom",
    "old_mac": "a8:7b:39:2f:c1:d4",
    "new_mac": "00:de:ad:be:ef:00",
    "custom_mac": "00:de:ad:be:ef:00"
  }
]
```

### CSV Export

**Command:**
```bash
sudo python3 macspoofx.py -m random -t 60 -o changes.csv
```

**Output Format:**
```csv
timestamp,interface,mode,old_mac,new_mac,custom_mac
2024-01-15T14:30:45.123456,wlan0,random,00:11:22:33:44:55,a8:7b:39:2f:c1:d4,
2024-01-15T14:31:45.234567,wlan0,random,a8:7b:39:2f:c1:d4,b2:3c:8d:1f:a9:e3,
```

### Table Output

**Interface List:**
```
+-------------------+MAC Change History------------------+
| timestamp         | interface | mode   | old_mac           | new_mac           |
+-------------------+-----------+--------+-------------------+-------------------+
| 2024-01-15T14:30  | wlan0     | random | 00:11:22:33:44:55 | a8:7b:39:2f:c1:d4 |
| 2024-01-15T14:31  | wlan0     | random | a8:7b:39:2f:c1:d4 | b2:3c:8d:1f:a9:e3 |
+-------------------+-----------+--------+-------------------+-------------------+
```

---

## 📝 Logging

### Log File Location

**Default**: `macspoofx.log` in the current working directory

### Log Format

```
2024-01-15 14:30:45,123 - __main__ - INFO - Interface wlan0 brought down
2024-01-15 14:30:45,456 - __main__ - INFO - MAC changed from 00:11:22:33:44:55 to a8:7b:39:2f:c1:d4
2024-01-15 14:30:45,789 - __main__ - INFO - Interface wlan0 brought up
```

### Log Levels

- **INFO**: Standard operational messages
- **WARNING**: Non-critical issues (e.g., ethtool not found)
- **ERROR**: Failures that prevent operations
- **DEBUG**: Detailed technical information (verbose mode only)

### Enable Verbose Logging

```bash
sudo python3 macspoofx.py --mode random --verbose
```

---

## 🔧 Troubleshooting

### Permission Denied Errors

**Problem:**
```
[-] This script requires root privileges
[!] Please run with: sudo python3 macspoofx.py
```

**Solution:**
```bash
sudo python3 macspoofx.py --mode random
```

### macchanger Not Found

**Problem:**
```
macchanger is not installed. Install with: apt install macchanger
```

**Solution:**
```bash
sudo apt update
sudo apt install macchanger -y
```

### Interface Not Found

**Problem:**
```
[-] No network interfaces found
```

**Solution:**
```bash
# List available interfaces
ip link show

# Or use the tool's built-in listing
sudo python3 macspoofx.py --list-interfaces
```

### Invalid MAC Address Format

**Problem:**
```
[-] Invalid MAC address format: 00-11-22-33-44
```

**Solution:**
Ensure MAC address follows the correct format:
- 6 pairs of hexadecimal digits
- Separated by colons (`:`) or hyphens (`-`)
- Example: `00:11:22:33:44:55`

### Network Disconnection After Spoofing

**Problem:** Lost network connectivity after MAC change

**Solution:**
```bash
# Reset to original MAC
sudo python3 macspoofx.py --mode reset

# Restart network manager
sudo systemctl restart NetworkManager

# Or manually bring interface back up
sudo ip link set <interface> up
```

### Python Dependencies Missing

**Problem:**
```
ModuleNotFoundError: No module named 'prettytable'
```

**Solution:**
The script attempts auto-installation. If it fails:
```bash
sudo pip3 install prettytable schedule netifaces colorama
```

### iptables Stealth Mode Issues

**Problem:** Stealth mode not working as expected

**Solution:**
```bash
# Check iptables rules
sudo iptables -L -v

# Flush all rules if needed
sudo iptables -F

# Restart the tool
sudo python3 macspoofx.py -m random -s
```

---

## 🎯 Best Practices

### 1. Always Get Authorization

- Never use this tool on networks you don't own or control
- Obtain written permission before security testing
- Document all testing activities

### 2. Test in Isolated Environments First

```bash
# Create a test network
# Use virtual machines or isolated lab networks
# Verify tool behavior before production use
```

### 3. Backup Original MAC Address

```bash
# Record original MAC before testing
sudo python3 macspoofx.py --list-interfaces

# Or use macchanger
macchanger -s <interface>
```

### 4. Use Reset Mode After Testing

```bash
# Always restore original MAC when done
sudo python3 macspoofx.py --mode reset
```

### 5. Enable Logging for Audits

```bash
# Keep detailed logs of all changes
sudo python3 macspoofx.py -m random -v -o audit_trail.json
```

### 6. Understand Legal Implications

- MAC spoofing may violate:
  - Computer Fraud and Abuse Act (CFAA) in the USA
  - Computer Misuse Act in the UK
  - Similar laws in other jurisdictions
- Only use for legitimate security testing

### 7. Monitor Network Impact

```bash
# Use wireshark or tcpdump to observe traffic
sudo tcpdump -i <interface> -e

# Monitor system logs
sudo tail -f /var/log/syslog
```

### 8. Schedule Wisely

- Don't use aggressive timeout values (< 30 seconds)
- Consider network stability
- Monitor for disconnections

```bash
# Reasonable timeout for testing
sudo python3 macspoofx.py -m random -t 300  # 5 minutes
```

---

## 🔬 Technical Details

### MAC Address Structure

```
   OUI (Organizationally Unique Identifier)     NIC (Network Interface Controller)
   ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                     ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
   00    :    1A    :    2B    :    3C    :    4D    :    5E
   └─────┴─────────┴─────────┴─────────┴─────────┴─────────┘
   First 24 bits (Vendor)          Last 24 bits (Device)
```

**Bit Significance:**
- **Bit 0 (LSB of first octet)**: Unicast (0) or Multicast (1)
- **Bit 1**: Globally unique (0) or Locally administered (1)

### OSI Model Layer 2 Operations

```
┌─────────────────────────────────────┐
│   Application Layer (7)             │
├─────────────────────────────────────┤
│   Presentation Layer (6)            │
├─────────────────────────────────────┤
│   Session Layer (5)                 │
├─────────────────────────────────────┤
│   Transport Layer (4)               │
├─────────────────────────────────────┤
│   Network Layer (3) - IP            │
├─────────────────────────────────────┤
│   Data Link Layer (2) - MAC ◄──┐   │  ← MAC Spoofing operates here
├─────────────────────────────────────┤
│   Physical Layer (1)                │
└─────────────────────────────────────┘
```

### Kernel Space Operations

MAC address changes occur in kernel space through netlink sockets:

1. **Userspace Request**: macchanger/ip command
2. **Netlink Communication**: Message to kernel
3. **Kernel Processing**: Update network device structure
4. **Driver Notification**: NIC driver updated
5. **Hardware Register**: Some NICs update registers (if supported)

### Detection and Mitigation

**How MAC Spoofing Can Be Detected:**

1. **Network Monitoring**:
   - Multiple devices with same MAC
   - Rapid MAC changes from same physical port
   - MAC-IP binding inconsistencies

2. **Switch Port Security**:
   - Sticky MAC learning
   - Maximum MAC addresses per port
   - Violation actions (shutdown, restrict, protect)

3. **DHCP Snooping**:
   - Validates DHCP messages
   - Builds trusted MAC-IP bindings
   - Drops spoofed requests

4. **802.1X Authentication**:
   - Port-based network access control
   - Requires authentication before network access
   - MAC alone insufficient for access

**Mitigation Strategies:**
```bash
# Example Cisco switch configuration
switch(config-if)# switchport port-security
switch(config-if)# switchport port-security maximum 1
switch(config-if)# switchport port-security violation shutdown
switch(config-if)# switchport port-security mac-address sticky
```

---

## 🤝 Contributing

Contributions are welcome for educational improvements!

### How to Contribute

1. **Fork the Repository**: Create your own fork
2. **Create a Branch**: `git checkout -b feature/improvement`
3. **Make Changes**: Implement your feature or fix
4. **Test Thoroughly**: Ensure all functionality works
5. **Submit Pull Request**: Describe your changes

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update documentation for new features
- Maintain educational focus
- Test on Kali Linux before submitting

### Future Enhancements

- [ ] GUI interface (Tkinter/PyQt)
- [ ] Bluetooth MAC spoofing support
- [ ] MAC address vendor lookup database
- [ ] Network monitoring integration (Wireshark)
- [ ] Automated testing against MAC filtering
- [ ] Profile management (save/load configurations)
- [ ] Integration with other Kali tools (airmon-ng, etc.)
- [ ] Real-time network traffic analysis
- [ ] Docker container support
- [ ] Advanced sequence generation algorithms

---

## 📄 License

**Educational Use Only**

This tool is provided for educational and authorized security testing purposes only. The authors and contributors are not responsible for any misuse or damage caused by this software.

**Terms of Use:**
- ✅ Authorized security testing
- ✅ Educational research
- ✅ Network administration on owned infrastructure
- ✅ Penetration testing with written permission
- ❌ Unauthorized network access
- ❌ Bypassing security controls without permission
- ❌ Any illegal activities

---

## 📞 Support

### Resources

- **Kali Linux Documentation**: https://www.kali.org/docs/
- **macchanger Manual**: `man macchanger`
- **iptables Guide**: `man iptables`
- **Python Documentation**: https://docs.python.org/3/

### Getting Help

1. **Check Troubleshooting Section**: Most issues are covered above
2. **Review Logs**: Check `macspoofx.log` for errors
3. **Verbose Mode**: Run with `-v` for detailed output
4. **System Logs**: Check `/var/log/syslog` for system-level errors

---

## ⚡ Quick Reference

### Common Commands Cheat Sheet

```bash
# List interfaces
sudo python3 macspoofx.py -l

# Random MAC
sudo python3 macspoofx.py -m random

# Custom MAC
sudo python3 macspoofx.py -m custom -c 00:11:22:33:44:55

# Vendor MAC
sudo python3 macspoofx.py -m vendor

# Reset to original
sudo python3 macspoofx.py -m reset

# Scheduled changes (every 60 seconds)
sudo python3 macspoofx.py -m random -t 60

# Stealth mode
sudo python3 macspoofx.py -m random -s

# Verbose logging
sudo python3 macspoofx.py -m random -v

# Export to JSON
sudo python3 macspoofx.py -m random -o results.json

# Full featured
sudo python3 macspoofx.py -i wlan0 -m random -t 120 -s -v -o mac_log.json
```

### Verification Commands

```bash
# Check current MAC
ip link show <interface>

# View with macchanger
macchanger -s <interface>

# Monitor network traffic
sudo tcpdump -i <interface> -e -n

# Check iptables rules
sudo iptables -L -v

# View system logs
sudo tail -f /var/log/syslog
```

---

## 🎓 Educational Objectives

This tool is designed to teach:

1. **Network Protocols**: Understanding Layer 2 (Data Link) operations
2. **Linux Networking**: Interface management, kernel operations
3. **Security Testing**: Ethical hacking methodologies
4. **Python Programming**: System administration, subprocess management
5. **Tool Integration**: Combining multiple utilities effectively
6. **Defensive Security**: Understanding attack vectors to improve defenses

---

## 🌟 Acknowledgments

- **macchanger**: Aitor Beriain and contributors
- **Kali Linux**: Offensive Security team
- **Python Community**: For excellent libraries and documentation
- **Security Researchers**: For advancing ethical hacking education

---

## 📌 Version History

### v2.0.0 (Current)
- Complete rewrite with modular architecture
- Integration with Kali Linux built-in tools
- Multi-threading support
- Stealth mode with iptables
- JSON/CSV export capabilities
- Comprehensive error handling
- Extensive documentation

### v1.0.0
- Initial release
- Basic MAC spoofing functionality

---

## 🔐 Security Notice

**Remember:**
- This tool modifies network identifiers
- Use only in controlled, authorized environments
- Understand your local laws and regulations
- Practice responsible disclosure
- Respect privacy and security of others

**"With great power comes great responsibility"** - Use this knowledge ethically.

---

**MacSpoofX v2.0.0** | Educational Security Research | Kali Linux Platform

For educational purposes only. Happy ethical hacking! 🐧🔒