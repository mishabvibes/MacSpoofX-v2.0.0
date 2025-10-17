# MacSpoofX - Quick Start Guide

## \u26a1 Get Started in 5 Minutes

### \u26a0\ufe0f Important First!

**This tool is for educational purposes ONLY!**
- Only use on networks you OWN
- Get written permission for testing
- Unauthorized use may be ILLEGAL

---

## \ud83d\ude80 Installation (30 seconds)

```bash
# Navigate to the tool directory
cd mac-spoofing-tool

# Run the installer
chmod +x install.sh
./install.sh

# Installation complete! ✅
```

---

## \ud83c\udfaf Your First MAC Spoof (1 minute)

### Step 1: Check Your Interface

```bash
sudo python3 macspoofx.py --list-interfaces
```

**You'll see something like:**
```
+-------------------+-------------------+-------------------+--------+
| interface | current_mac       | permanent_mac     | status |
+-------------------+-------------------+-------------------+--------+
| wlan0     | 00:11:22:33:44:55 | 00:11:22:33:44:55 | UP     |
+-------------------+-------------------+-------------------+--------+
```

### Step 2: Spoof Your MAC

```bash
sudo python3 macspoofx.py --mode random
```

**You'll see:**
```
[+] MAC changed from 00:11:22:33:44:55 to a8:7b:39:2f:c1:d4
[+] MAC spoofing successful!
```

### Step 3: Reset When Done

```bash
sudo python3 macspoofx.py --mode reset
```

**Done! You've successfully spoofed a MAC address!** 🎉

---

## \ud83d\udcda Essential Commands

### Random MAC
```bash
sudo python3 macspoofx.py --mode random
```

### Custom MAC
```bash
sudo python3 macspoofx.py --mode custom --custom-mac 00:11:22:33:44:55
```

### Vendor MAC (appears as known manufacturer)
```bash
sudo python3 macspoofx.py --mode vendor
```

### Scheduled Changes (every 60 seconds)
```bash
sudo python3 macspoofx.py --mode random --timeout 60
```

### Stealth Mode
```bash
sudo python3 macspoofx.py --mode random --stealth
```

### Save Results
```bash
sudo python3 macspoofx.py --mode random --output results.json
```

---

## \ud83c\udfad Try the Examples

```bash
# Navigate to examples
cd examples

# Make scripts executable
chmod +x *.sh

# Try basic example
sudo ./example1_basic_random.sh

# Try scheduled rotation
sudo ./example3_scheduled_rotation.sh
```

---

## \ud83d\udd27 Common Issues

### "Permission Denied"
**Solution**: Always use `sudo`
```bash
sudo python3 macspoofx.py --mode random
```

### "macchanger not found"
**Solution**: Install macchanger
```bash
sudo apt install macchanger
```

### Network Disconnected After Spoof
**Solution**: Reset and restart network
```bash
sudo python3 macspoofx.py --mode reset
sudo systemctl restart NetworkManager
```

---

## \ud83d\udcda Learn More

- **Full Documentation**: `README.md`
- **Usage Examples**: `USAGE_GUIDE.md`
- **Security Guidelines**: `SECURITY.md`
- **Project Structure**: `PROJECT_STRUCTURE.md`

### Help Command
```bash
sudo python3 macspoofx.py --help
```

---

## \u2705 Safety Checklist

Before you start:
- [ ] I have permission to test this network
- [ ] I understand this is for education only
- [ ] I know how to reset (--mode reset)
- [ ] I've read the disclaimers

---

## \ud83c\udfaf What Can You Do?

✅ Test your own network security  
✅ Learn about MAC addresses  
✅ Practice ethical hacking skills  
✅ Understand Layer 2 protocols  
✅ Research privacy techniques  

❌ Access unauthorized networks  
❌ Bypass security without permission  
❌ Hide illegal activities  
❌ Attack or disrupt networks  

---

## \ud83d\ude80 Next Steps

1. ✅ Run basic random spoofing
2. ✅ Try custom MAC addresses
3. ✅ Experiment with scheduled rotation
4. ✅ Test stealth mode
5. ✅ Review the examples
6. ✅ Read full documentation
7. ✅ Practice responsibly!

---

## \ud83d\udcde Need Help?

1. Check `macspoofx.log` for errors
2. Review troubleshooting in README.md
3. Try examples for working code
4. Read USAGE_GUIDE.md for scenarios

---

## \ud83c\udf93 Remember

**"With great power comes great responsibility"**

Use MacSpoofX to:
- Learn about network security
- Test your own systems
- Improve your defenses
- Advance your knowledge

Always ethically, always legally, always with permission.

---

**Happy Ethical Hacking! \ud83d\udc27\ud83d\udd12**

*For educational purposes only.*
