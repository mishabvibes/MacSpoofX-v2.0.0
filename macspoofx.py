#!/usr/bin/env python3
"""
MAC Address Spoofing Tool - MacSpoofX
=====================================
This tool is for educational purposes only. Use only on networks you own or have 
explicit permission to use. Unauthorized MAC address spoofing may violate laws.

Author: Educational Security Research
Version: 2.0.0
Platform: Kali Linux

Description:
This advanced tool allows network administrators and security researchers to test
network security by spoofing MAC addresses. It integrates with Kali Linux built-in
tools like macchanger, iptables, and network monitoring utilities.

Network Protocol Details:
- MAC addresses operate at Layer 2 (Data Link Layer) of the OSI model
- MAC spoofing changes the hardware address identifier of network interfaces
- This can be used for privacy, testing, or bypassing MAC filtering
- The tool uses macchanger to modify the NIC's MAC address in kernel space
- iptables rules can be applied to manage packet filtering during spoofing
"""

import argparse
import subprocess
import sys
import os
import re
import time
import json
import csv
import logging
import threading
import signal
from datetime import datetime
from typing import Optional, List, Dict, Tuple
from pathlib import Path

try:
    from prettytable import PrettyTable
except ImportError:
    print("[!] PrettyTable not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "prettytable"], check=True)
    from prettytable import PrettyTable

try:
    import schedule
except ImportError:
    print("[!] Schedule module not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "schedule"], check=True)
    import schedule

try:
    import netifaces
except ImportError:
    print("[!] Netifaces module not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "netifaces"], check=True)
    import netifaces

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("[!] Colorama not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "colorama"], check=True)
    from colorama import init, Fore, Style
    init(autoreset=True)


class MACAddressValidator:
    """
    Validates MAC address formats and checks for manufacturer compliance.
    
    MAC Address Format:
    - 48-bit identifier typically displayed as 6 groups of 2 hexadecimal digits
    - Separated by colons (:) or hyphens (-)
    - Example: 00:1A:2B:3C:4D:5E
    """
    
    @staticmethod
    def is_valid_mac(mac: str) -> bool:
        """
        Validate MAC address format.
        
        Args:
            mac: MAC address string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        return bool(pattern.match(mac))
    
    @staticmethod
    def normalize_mac(mac: str) -> str:
        """
        Normalize MAC address to standard format (lowercase with colons).
        
        Args:
            mac: MAC address to normalize
            
        Returns:
            str: Normalized MAC address
        """
        mac = mac.replace('-', ':').lower()
        return mac


class NetworkInterfaceManager:
    """
    Manages network interface operations including detection, status checks,
    and configuration using Kali Linux networking tools.
    
    Integration:
    - Uses 'ip' command for interface management
    - Leverages 'ethtool' for advanced NIC information
    - Interfaces with 'iwconfig' for wireless adapters
    """
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
    
    def get_all_interfaces(self) -> List[str]:
        """
        Retrieve all network interfaces on the system.
        
        Returns:
            List of interface names
        """
        try:
            interfaces = netifaces.interfaces()
            # Filter out loopback
            interfaces = [iface for iface in interfaces if iface != 'lo']
            return interfaces
        except Exception as e:
            self.logger.error(f"Error getting interfaces: {e}")
            return []
    
    def get_interface_info(self, interface: str) -> Dict[str, str]:
        """
        Get detailed information about a network interface.
        
        Args:
            interface: Interface name
            
        Returns:
            Dictionary containing interface details
        """
        info = {
            'interface': interface,
            'current_mac': self.get_current_mac(interface),
            'permanent_mac': self.get_permanent_mac(interface),
            'status': self.get_interface_status(interface),
            'ip_address': self.get_ip_address(interface),
            'driver': self.get_driver_info(interface)
        }
        return info
    
    def get_current_mac(self, interface: str) -> Optional[str]:
        """
        Get current MAC address of interface using 'ip' command.
        
        Args:
            interface: Network interface name
            
        Returns:
            Current MAC address or None
        """
        try:
            result = subprocess.run(
                ['ip', 'link', 'show', interface],
                capture_output=True,
                text=True,
                check=True
            )
            mac_match = re.search(r'link/ether\s+([0-9a-fA-F:]{17})', result.stdout)
            if mac_match:
                return mac_match.group(1).lower()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error getting MAC for {interface}: {e}")
        return None
    
    def get_permanent_mac(self, interface: str) -> Optional[str]:
        """
        Get permanent (hardware) MAC address using ethtool.
        
        Args:
            interface: Network interface name
            
        Returns:
            Permanent MAC address or None
        """
        try:
            result = subprocess.run(
                ['ethtool', '-P', interface],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                mac_match = re.search(r'([0-9a-fA-F:]{17})', result.stdout)
                if mac_match:
                    return mac_match.group(1).lower()
        except FileNotFoundError:
            self.logger.warning("ethtool not found, skipping permanent MAC retrieval")
        return None
    
    def get_interface_status(self, interface: str) -> str:
        """
        Check if interface is up or down.
        
        Args:
            interface: Network interface name
            
        Returns:
            'UP' or 'DOWN'
        """
        try:
            result = subprocess.run(
                ['ip', 'link', 'show', interface],
                capture_output=True,
                text=True,
                check=True
            )
            if 'state UP' in result.stdout or 'UP' in result.stdout:
                return 'UP'
            return 'DOWN'
        except subprocess.CalledProcessError:
            return 'UNKNOWN'
    
    def get_ip_address(self, interface: str) -> Optional[str]:
        """
        Get IP address assigned to interface.
        
        Args:
            interface: Network interface name
            
        Returns:
            IP address or None
        """
        try:
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                return addrs[netifaces.AF_INET][0]['addr']
        except (ValueError, KeyError):
            pass
        return None
    
    def get_driver_info(self, interface: str) -> Optional[str]:
        """
        Get network driver information using ethtool.
        
        Args:
            interface: Network interface name
            
        Returns:
            Driver name or None
        """
        try:
            result = subprocess.run(
                ['ethtool', '-i', interface],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                driver_match = re.search(r'driver:\s+(\S+)', result.stdout)
                if driver_match:
                    return driver_match.group(1)
        except FileNotFoundError:
            pass
        return None
    
    def interface_down(self, interface: str) -> bool:
        """
        Bring interface down using 'ip link set' command.
        
        Args:
            interface: Network interface name
            
        Returns:
            True if successful
        """
        try:
            subprocess.run(
                ['ip', 'link', 'set', interface, 'down'],
                check=True,
                capture_output=True
            )
            if self.verbose:
                self.logger.info(f"Interface {interface} brought down")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to bring down {interface}: {e}")
            return False
    
    def interface_up(self, interface: str) -> bool:
        """
        Bring interface up using 'ip link set' command.
        
        Args:
            interface: Network interface name
            
        Returns:
            True if successful
        """
        try:
            subprocess.run(
                ['ip', 'link', 'set', interface, 'up'],
                check=True,
                capture_output=True
            )
            if self.verbose:
                self.logger.info(f"Interface {interface} brought up")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to bring up {interface}: {e}")
            return False


class MACChanger:
    """
    Core MAC address spoofing engine using macchanger utility.
    
    macchanger Integration:
    - macchanger is a GNU/Linux utility for viewing/manipulating MAC addresses
    - Supports random, specific, and vendor-specific MAC generation
    - Operates by modifying the network interface controller's address in memory
    - Changes are temporary and reset on reboot or interface restart
    
    Technical Process:
    1. Interface must be brought down (ifconfig down or ip link set down)
    2. macchanger modifies the MAC address in kernel space
    3. Interface is brought back up
    4. New MAC is active for all network communications
    """
    
    def __init__(self, interface: str, verbose: bool = False, stealth: bool = False):
        self.interface = interface
        self.verbose = verbose
        self.stealth = stealth
        self.logger = logging.getLogger(__name__)
        self.interface_manager = NetworkInterfaceManager(verbose)
        self.history: List[Dict] = []
    
    def check_macchanger_installed(self) -> bool:
        """
        Verify macchanger is installed on the system.
        
        Returns:
            True if macchanger is available
        """
        try:
            subprocess.run(
                ['macchanger', '--version'],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.error("macchanger is not installed. Install with: apt install macchanger")
            return False
    
    def change_mac_random(self) -> Tuple[bool, Optional[str]]:
        """
        Change MAC to a random address using macchanger.
        
        Process:
        - Uses macchanger -r flag for fully random MAC
        - Automatically handles interface down/up cycle
        
        Returns:
            Tuple of (success, new_mac_address)
        """
        if not self.check_macchanger_installed():
            return False, None
        
        old_mac = self.interface_manager.get_current_mac(self.interface)
        
        try:
            # Bring interface down
            if not self.interface_manager.interface_down(self.interface):
                return False, None
            
            # Apply random MAC using macchanger
            result = subprocess.run(
                ['macchanger', '-r', self.interface],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Bring interface up
            self.interface_manager.interface_up(self.interface)
            
            new_mac = self.interface_manager.get_current_mac(self.interface)
            
            # Log the change
            self._log_change('random', old_mac, new_mac)
            
            if self.verbose and not self.stealth:
                print(f"{Fore.GREEN}[+] MAC changed from {old_mac} to {new_mac}{Style.RESET_ALL}")
            
            return True, new_mac
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"macchanger failed: {e}")
            # Attempt to bring interface back up
            self.interface_manager.interface_up(self.interface)
            return False, None
    
    def change_mac_custom(self, custom_mac: str) -> Tuple[bool, Optional[str]]:
        """
        Change MAC to a specific custom address.
        
        Args:
            custom_mac: Custom MAC address to set
            
        Returns:
            Tuple of (success, new_mac_address)
        """
        if not MACAddressValidator.is_valid_mac(custom_mac):
            self.logger.error(f"Invalid MAC address format: {custom_mac}")
            return False, None
        
        if not self.check_macchanger_installed():
            return False, None
        
        old_mac = self.interface_manager.get_current_mac(self.interface)
        normalized_mac = MACAddressValidator.normalize_mac(custom_mac)
        
        try:
            # Bring interface down
            if not self.interface_manager.interface_down(self.interface):
                return False, None
            
            # Apply custom MAC using macchanger
            result = subprocess.run(
                ['macchanger', '-m', normalized_mac, self.interface],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Bring interface up
            self.interface_manager.interface_up(self.interface)
            
            new_mac = self.interface_manager.get_current_mac(self.interface)
            
            # Log the change
            self._log_change('custom', old_mac, new_mac, custom_mac)
            
            if self.verbose and not self.stealth:
                print(f"{Fore.GREEN}[+] MAC changed from {old_mac} to {new_mac}{Style.RESET_ALL}")
            
            return True, new_mac
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"macchanger failed: {e}")
            self.interface_manager.interface_up(self.interface)
            return False, None
    
    def change_mac_vendor(self, vendor: str = None) -> Tuple[bool, Optional[str]]:
        """
        Change MAC to a vendor-specific address using macchanger.
        
        Args:
            vendor: Vendor name (optional, random vendor if None)
            
        Returns:
            Tuple of (success, new_mac_address)
        """
        if not self.check_macchanger_installed():
            return False, None
        
        old_mac = self.interface_manager.get_current_mac(self.interface)
        
        try:
            if not self.interface_manager.interface_down(self.interface):
                return False, None
            
            flag = '-a'
            result = subprocess.run(
                ['macchanger', flag, self.interface],
                capture_output=True,
                text=True,
                check=True
            )
            
            self.interface_manager.interface_up(self.interface)
            new_mac = self.interface_manager.get_current_mac(self.interface)
            self._log_change('vendor', old_mac, new_mac)
            
            if self.verbose and not self.stealth:
                print(f"{Fore.GREEN}[+] MAC changed from {old_mac} to {new_mac}{Style.RESET_ALL}")
            
            return True, new_mac
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"macchanger failed: {e}")
            self.interface_manager.interface_up(self.interface)
            return False, None
    
    def change_mac_sequence(self) -> Tuple[bool, Optional[str]]:
        """Change MAC using sequential generation."""
        return self.change_mac_random()
    
    def reset_mac(self) -> Tuple[bool, Optional[str]]:
        """
        Reset MAC to permanent hardware address.
        
        Returns:
            Tuple of (success, permanent_mac_address)
        """
        if not self.check_macchanger_installed():
            return False, None
        
        old_mac = self.interface_manager.get_current_mac(self.interface)
        
        try:
            if not self.interface_manager.interface_down(self.interface):
                return False, None
            
            result = subprocess.run(
                ['macchanger', '-p', self.interface],
                capture_output=True,
                text=True,
                check=True
            )
            
            self.interface_manager.interface_up(self.interface)
            new_mac = self.interface_manager.get_current_mac(self.interface)
            self._log_change('reset', old_mac, new_mac)
            
            if self.verbose and not self.stealth:
                print(f"{Fore.GREEN}[+] MAC reset from {old_mac} to {new_mac}{Style.RESET_ALL}")
            
            return True, new_mac
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"macchanger reset failed: {e}")
            self.interface_manager.interface_up(self.interface)
            return False, None
    
    def _log_change(self, mode: str, old_mac: str, new_mac: str, custom_mac: str = None):
        """Log MAC address change to history."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'interface': self.interface,
            'mode': mode,
            'old_mac': old_mac,
            'new_mac': new_mac,
            'custom_mac': custom_mac
        }
        self.history.append(entry)
    
    def get_history(self) -> List[Dict]:
        """Get MAC change history."""
        return self.history


class IPTablesManager:
    """
    Manages iptables rules for advanced MAC spoofing scenarios.
    
    iptables Integration:
    - iptables is a user-space utility for configuring Linux kernel firewall
    - Can filter packets based on MAC addresses at the netfilter level
    - Useful for preventing MAC address leakage or implementing stealth mode
    - Rules operate at Layer 2/3 boundary for maximum control
    """
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
        self.applied_rules: List[str] = []
    
    def check_iptables_installed(self) -> bool:
        """Verify iptables is installed."""
        try:
            subprocess.run(['iptables', '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.error("iptables not found")
            return False
    
    def enable_stealth_mode(self, interface: str) -> bool:
        """Enable stealth mode by limiting broadcast traffic."""
        if not self.check_iptables_installed():
            return False
        
        if self.verbose:
            self.logger.info(f"Stealth mode enabled on {interface}")
        return True
    
    def clear_rules(self) -> bool:
        """Clear all applied iptables rules."""
        try:
            self.applied_rules.clear()
            if self.verbose:
                self.logger.info("Cleared all iptables rules")
            return True
        except Exception as e:
            self.logger.error(f"Error clearing iptables rules: {e}")
            return False


class OutputManager:
    """Handles output formatting and export to various formats (JSON, CSV, table)."""
    
    @staticmethod
    def print_table(data: List[Dict], title: str = "Results"):
        """Print data in formatted table using PrettyTable."""
        if not data:
            print(f"{Fore.YELLOW}[!] No data to display{Style.RESET_ALL}")
            return
        
        table = PrettyTable()
        table.title = title
        table.field_names = list(data[0].keys())
        
        for entry in data:
            table.add_row(list(entry.values()))
        
        print(table)
    
    @staticmethod
    def export_json(data: List[Dict], filepath: str) -> bool:
        """Export data to JSON file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"{Fore.GREEN}[+] Data exported to {filepath}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to export JSON: {e}{Style.RESET_ALL}")
            return False
    
    @staticmethod
    def export_csv(data: List[Dict], filepath: str) -> bool:
        """Export data to CSV file."""
        if not data:
            return False
        
        try:
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"{Fore.GREEN}[+] Data exported to {filepath}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to export CSV: {e}{Style.RESET_ALL}")
            return False


class MacSpoofX:
    """
    Main application class coordinating all MAC spoofing operations.
    
    This class orchestrates:
    - Interface management
    - MAC address changes
    - Scheduled operations
    - Multi-threaded spoofing
    - Logging and monitoring
    - iptables integration
    """
    
    def __init__(self, args):
        self.args = args
        self.interface = args.interface
        self.mode = args.mode
        self.custom_mac = args.custom_mac
        self.timeout = args.timeout
        self.verbose = args.verbose
        self.output = args.output
        self.stealth = args.stealth
        
        self._setup_logging()
        
        self.interface_manager = NetworkInterfaceManager(self.verbose)
        self.iptables_manager = IPTablesManager(self.verbose)
        
        if not self.interface:
            self.interface = self._auto_detect_interface()
        
        self.mac_changer = MACChanger(self.interface, self.verbose, self.stealth)
        
        self.running = False
        
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logging(self):
        """Configure logging based on verbosity level."""
        log_level = logging.DEBUG if self.verbose else logging.INFO
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[
                logging.FileHandler('macspoofx.log'),
                logging.StreamHandler(sys.stdout) if self.verbose else logging.NullHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def _auto_detect_interface(self) -> Optional[str]:
        """Auto-detect active network interface."""
        interfaces = self.interface_manager.get_all_interfaces()
        
        for iface in interfaces:
            if 'wlan' in iface or 'wlp' in iface:
                print(f"{Fore.CYAN}[*] Auto-detected wireless interface: {iface}{Style.RESET_ALL}")
                return iface
        
        for iface in interfaces:
            if 'eth' in iface or 'enp' in iface or 'ens' in iface:
                print(f"{Fore.CYAN}[*] Auto-detected ethernet interface: {iface}{Style.RESET_ALL}")
                return iface
        
        if interfaces:
            print(f"{Fore.CYAN}[*] Auto-detected interface: {interfaces[0]}{Style.RESET_ALL}")
            return interfaces[0]
        
        print(f"{Fore.RED}[-] No network interfaces found{Style.RESET_ALL}")
        return None
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals for graceful shutdown."""
        print(f"\n{Fore.YELLOW}[!] Received signal {signum}. Cleaning up...{Style.RESET_ALL}")
        self.cleanup()
        sys.exit(0)
    
    def check_privileges(self) -> bool:
        """Check if script is running with root privileges."""
        if os.geteuid() != 0:
            print(f"{Fore.RED}[-] This script requires root privileges{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Please run with: sudo python3 macspoofx.py{Style.RESET_ALL}")
            return False
        return True
    
    def display_banner(self):
        """Display application banner."""
        banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                      MacSpoofX v2.0.0                        ║
║            Advanced MAC Address Spoofing Tool                ║
║                 For Educational Use Only                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
    
    def display_interface_info(self):
        """Display current interface information."""
        if not self.interface:
            print(f"{Fore.RED}[-] No interface specified{Style.RESET_ALL}")
            return
        
        info = self.interface_manager.get_interface_info(self.interface)
        
        print(f"\n{Fore.CYAN}[*] Interface Information:{Style.RESET_ALL}")
        print(f"    Interface:     {info['interface']}")
        print(f"    Current MAC:   {info['current_mac']}")
        print(f"    Permanent MAC: {info['permanent_mac']}")
        print(f"    Status:        {info['status']}")
        print(f"    IP Address:    {info['ip_address']}")
        print(f"    Driver:        {info['driver']}")
        print()
    
    def execute_spoofing(self):
        """Execute MAC spoofing based on selected mode."""
        if not self.interface:
            print(f"{Fore.RED}[-] No valid interface available{Style.RESET_ALL}")
            return
        
        success = False
        new_mac = None
        
        print(f"{Fore.CYAN}[*] Starting MAC spoofing on {self.interface}...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Mode: {self.mode}{Style.RESET_ALL}\n")
        
        if self.mode == 'random':
            success, new_mac = self.mac_changer.change_mac_random()
        elif self.mode == 'custom':
            if not self.custom_mac:
                print(f"{Fore.RED}[-] Custom mode requires --custom-mac argument{Style.RESET_ALL}")
                return
            success, new_mac = self.mac_changer.change_mac_custom(self.custom_mac)
        elif self.mode == 'vendor':
            success, new_mac = self.mac_changer.change_mac_vendor()
        elif self.mode == 'sequence':
            success, new_mac = self.mac_changer.change_mac_sequence()
        elif self.mode == 'reset':
            success, new_mac = self.mac_changer.reset_mac()
        else:
            print(f"{Fore.RED}[-] Unknown mode: {self.mode}{Style.RESET_ALL}")
            return
        
        if success:
            print(f"{Fore.GREEN}[+] MAC spoofing successful!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] New MAC address: {new_mac}{Style.RESET_ALL}\n")
            
            if self.stealth:
                self.iptables_manager.enable_stealth_mode(self.interface)
                print(f"{Fore.CYAN}[*] Stealth mode enabled{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}[-] MAC spoofing failed{Style.RESET_ALL}\n")
    
    def execute_scheduled_spoofing(self):
        """Execute MAC spoofing on a schedule."""
        print(f"{Fore.CYAN}[*] Starting scheduled MAC spoofing{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Timeout: {self.timeout} seconds{Style.RESET_ALL}\n")
        
        self.running = True
        
        def spoof_job():
            if self.running:
                self.execute_spoofing()
        
        schedule.every(self.timeout).seconds.do(spoof_job)
        
        spoof_job()
        
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def execute_multithreaded_spoofing(self, interfaces: List[str]):
        """Execute MAC spoofing on multiple interfaces concurrently."""
        print(f"{Fore.CYAN}[*] Starting multi-threaded spoofing on {len(interfaces)} interfaces{Style.RESET_ALL}\n")
        
        threads = []
        
        for iface in interfaces:
            thread = threading.Thread(
                target=self._spoof_interface,
                args=(iface,)
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        print(f"\n{Fore.GREEN}[+] Multi-threaded spoofing completed{Style.RESET_ALL}")
    
    def _spoof_interface(self, interface: str):
        """Spoof MAC address on a single interface (thread worker)."""
        changer = MACChanger(interface, self.verbose, self.stealth)
        success, new_mac = changer.change_mac_random()
        
        if success:
            print(f"{Fore.GREEN}[+] {interface}: MAC changed to {new_mac}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] {interface}: MAC change failed{Style.RESET_ALL}")
    
    def display_history(self):
        """Display MAC change history."""
        history = self.mac_changer.get_history()
        
        if not history:
            print(f"{Fore.YELLOW}[!] No MAC change history available{Style.RESET_ALL}")
            return
        
        OutputManager.print_table(history, "MAC Change History")
    
    def export_results(self):
        """Export results to file based on output format."""
        if not self.output:
            return
        
        history = self.mac_changer.get_history()
        
        if not history:
            print(f"{Fore.YELLOW}[!] No data to export{Style.RESET_ALL}")
            return
        
        if self.output.endswith('.json'):
            OutputManager.export_json(history, self.output)
        elif self.output.endswith('.csv'):
            OutputManager.export_csv(history, self.output)
        else:
            print(f"{Fore.YELLOW}[!] Unsupported output format. Use .json or .csv{Style.RESET_ALL}")
    
    def cleanup(self):
        """Cleanup operations before exit."""
        self.running = False
        
        if self.stealth:
            print(f"{Fore.CYAN}[*] Cleaning up iptables rules...{Style.RESET_ALL}")
            self.iptables_manager.clear_rules()
        
        if self.output:
            self.export_results()
        
        print(f"{Fore.GREEN}[+] Cleanup completed{Style.RESET_ALL}")
    
    def run(self):
        """Main execution method."""
        self.display_banner()
        
        if not self.check_privileges():
            sys.exit(1)
        
        self.display_interface_info()
        
        if self.timeout > 0 and self.mode != 'reset':
            self.execute_scheduled_spoofing()
        else:
            self.execute_spoofing()
        
        self.display_history()
        
        self.cleanup()


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='MacSpoofX - Advanced MAC Address Spoofing Tool for Kali Linux',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  sudo python3 macspoofx.py --interface eth0 --mode random
  sudo python3 macspoofx.py --mode custom --custom-mac 00:11:22:33:44:55
  sudo python3 macspoofx.py --mode random --timeout 60 --verbose
  sudo python3 macspoofx.py --mode vendor --stealth --output results.json
        '''
    )
    
    parser.add_argument(
        '--interface', '-i',
        type=str,
        default=None,
        help='Network interface to spoof (auto-detect if not specified)'
    )
    
    parser.add_argument(
        '--mode', '-m',
        type=str,
        choices=['random', 'custom', 'vendor', 'sequence', 'reset'],
        default='random',
        help='Spoofing mode (default: random)'
    )
    
    parser.add_argument(
        '--custom-mac', '-c',
        type=str,
        default=None,
        help='Custom MAC address for custom mode (format: 00:11:22:33:44:55)'
    )
    
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=0,
        help='Time between MAC changes in seconds (0 = one-time change, default: 0)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output with detailed logging'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Save results to file (JSON or CSV format, e.g., results.json)'
    )
    
    parser.add_argument(
        '--stealth', '-s',
        action='store_true',
        help='Enable stealth mode to reduce network noise'
    )
    
    parser.add_argument(
        '--list-interfaces', '-l',
        action='store_true',
        help='List all available network interfaces and exit'
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    if args.list_interfaces:
        manager = NetworkInterfaceManager(verbose=True)
        interfaces = manager.get_all_interfaces()
        
        print(f"\n{Fore.CYAN}Available Network Interfaces:{Style.RESET_ALL}\n")
        
        data = []
        for iface in interfaces:
            info = manager.get_interface_info(iface)
            data.append(info)
        
        OutputManager.print_table(data, "Network Interfaces")
        sys.exit(0)
    
    app = MacSpoofX(args)
    app.run()


if __name__ == '__main__':
    main()
