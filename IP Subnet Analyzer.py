import tkinter as tk
from tkinter import ttk, messagebox
import ipaddress

def is_valid_ip(ip_str):
    """Verifies if the string is a valid IP address."""
    try:
        ipaddress.IPv4Address(ip_str)
        return True
    except ValueError:
        return False

def is_valid_mask(mask_str):
    """Verifies if the string is a valid mask."""
    # Check CIDR notation
    if mask_str.startswith('/'):
        try:
            cidr = int(mask_str[1:])
            return 0 <= cidr <= 32
        except ValueError:
            return False
    
    # Check decimal notation
    try:
        parts = mask_str.split('.')
        if len(parts) != 4:
            return False
        
        decimal_values = [int(part) for part in parts]
        binary_mask = ''.join([bin(part)[2:].zfill(8) for part in decimal_values])
        
        # A valid mask must have continuous 1s followed by continuous 0s
        return '01' not in binary_mask
    except:
        return False

def apply_mask():
    # Get the IP address from the input field
    ip_addr = ip_entry.get().strip()
    
    # Get the mask from the input field
    mask_input = mask_entry.get().strip()
    
    # Validate inputs
    if not is_valid_ip(ip_addr):
        messagebox.showerror("Invalid IP", "Enter a valid IP address (e.g. 192.168.1.1)")
        return
    
    if not is_valid_mask(mask_input):
        messagebox.showerror("Invalid Mask", "Enter a valid mask (e.g. /24 or 255.255.255.0)")
        return
    
    try:
        # Convert the mask to CIDR notation if it's in decimal notation
        if mask_input.startswith('/'):
            # It's already in CIDR notation (e.g. /24)
            mask_cidr = int(mask_input[1:])
        else:
            # It's in decimal notation (e.g. 255.255.255.0)
            # Convert to CIDR notation
            mask_parts = [int(part) for part in mask_input.split('.')]
            binary_mask = ''.join([bin(part)[2:].zfill(8) for part in mask_parts])
            mask_cidr = binary_mask.count('1')
        
        # Create the network address using the ipaddress module
        network = ipaddress.IPv4Network(f"{ip_addr}/{mask_cidr}", strict=False)
        
        # Get the network address (this applies the mask to the IP)
        network_addr = network.network_address
        
        # Get the broadcast address (last address in the network)
        broadcast_addr = network.broadcast_address
        
        # Calculate the first and last usable host address
        if mask_cidr < 31:  # If the network has more than 2 addresses
            first_host = ipaddress.IPv4Address(int(network_addr) + 1)
            last_host = ipaddress.IPv4Address(int(broadcast_addr) - 1)
        else:  # For /31 and /32, all addresses are hosts
            first_host = network_addr
            last_host = broadcast_addr
        
        # Calculate the total number of addresses
        total_hosts = 2 ** (32 - mask_cidr)
        usable_hosts = max(0, total_hosts - 2) if mask_cidr < 31 else total_hosts
        
        # Get the mask in decimal notation
        mask_decimal = str(ipaddress.IPv4Address(int('1' * mask_cidr + '0' * (32 - mask_cidr), 2)))
        
        # Update the result field (mask application)
        result_var.set(str(network_addr))
        
        # Update network information
        network_info_var.set(
            f"Network address: {network_addr}/{mask_cidr} ({mask_decimal})\n"
            f"First host address: {first_host}\n"
            f"Last host address: {last_host}\n"
            f"Broadcast address: {broadcast_addr}\n"
            f"Total number of addresses: {total_hosts}\n"
            f"Usable host addresses: {usable_hosts}"
        )
        
        # Convert to binary for display
        ip_octets = [int(octet) for octet in ip_addr.split('.')]
        ip_binary = '.'.join([bin(octet)[2:].zfill(8) for octet in ip_octets])
        
        # Create the mask in binary format
        mask_int = (0xFFFFFFFF >> (32 - mask_cidr)) << (32 - mask_cidr)
        mask_octets = [(mask_int >> (8 * i)) & 0xFF for i in range(3, -1, -1)]
        mask_binary = '.'.join([bin(octet)[2:].zfill(8) for octet in mask_octets])
        
        # Convert the result (network address) to binary
        network_octets = [int(octet) for octet in str(network_addr).split('.')]
        network_binary = '.'.join([bin(octet)[2:].zfill(8) for octet in network_octets])
        
        # Convert the broadcast address to binary
        broadcast_octets = [int(octet) for octet in str(broadcast_addr).split('.')]
        broadcast_binary = '.'.join([bin(octet)[2:].zfill(8) for octet in broadcast_octets])
        
        # Update the binary display
        binary_info_var.set(
            f"Input IP (binary):      {ip_binary}\n"
            f"Mask (binary):          {mask_binary}\n"
            f"Network addr (binary):  {network_binary}\n"
            f"Broadcast addr (binary):{broadcast_binary}"
        )
        
    except Exception as e:
        result_var.set("Error")
        network_info_var.set("Error in network calculation")
        binary_info_var.set("")
        messagebox.showerror("Error", str(e))

def show_help():
    help_text = """
    This program applies a subnet mask to an IP address and calculates information about the network.
    
    Input:
    - IP Address: Enter a valid IPv4 address (e.g. 192.168.1.1)
    - Subnet mask: Enter in CIDR format (e.g. /24) or decimal format (e.g. 255.255.255.0)
    
    Operations:
    1. Bitwise operation: applies a bitwise AND operation between the IP address and the mask,
       keeping the bits specified by the mask and setting the rest to 0.
    
    2. Network information calculation:
       - Network address: result of the bitwise operation
       - Broadcast address: all bits after the mask set to 1
       - First and last usable host address
       - Total number of addresses and usable addresses
    
    Example:
    IP: 102.201.225.140
    Mask: /25 (or 255.255.255.128)
    Network address: 102.201.225.128
    Broadcast address: 102.201.225.255
    """
    messagebox.showinfo("Help", help_text)

# Create the main window
root = tk.Tk()
root.title("IP Subnet Analyzer")
root.geometry("600x600")

# Create the main frame with padding
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a frame for inputs with a border
input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
input_frame.pack(fill=tk.X, expand=False, pady=5)

# IP address input
ttk.Label(input_frame, text="IP Address:").grid(column=0, row=0, sticky=tk.W, pady=5, padx=5)
ip_entry = ttk.Entry(input_frame, width=20)
ip_entry.grid(column=1, row=0, sticky=tk.W, pady=5, padx=5)
# Mask input
ttk.Label(input_frame, text="Mask:").grid(column=0, row=1, sticky=tk.W, pady=5, padx=5)
mask_entry = ttk.Entry(input_frame, width=20)
mask_entry.grid(column=1, row=1, sticky=tk.W, pady=5, padx=5)
ttk.Label(input_frame, text="(e.g. /25 or 255.255.255.128)").grid(column=2, row=1, sticky=tk.W, pady=5)

# Result frame
result_frame = ttk.LabelFrame(main_frame, text="Result of bitwise operation", padding="10")
result_frame.pack(fill=tk.X, expand=False, pady=5)

# Result field
result_var = tk.StringVar()
result_var.set("The result will appear here")
result_label = ttk.Label(result_frame, textvariable=result_var, font=('Arial', 12, 'bold'))
result_label.pack(fill=tk.X, pady=5)

# Network information frame
network_frame = ttk.LabelFrame(main_frame, text="Network Information", padding="10")
network_frame.pack(fill=tk.X, expand=False, pady=5)

# Container for network information
network_info_var = tk.StringVar()
network_info_var.set("Network information will appear here")
network_info = ttk.Label(network_frame, textvariable=network_info_var, font=('Arial', 10), justify=tk.LEFT)
network_info.pack(fill=tk.X, pady=5)

# Binary information
binary_frame = ttk.LabelFrame(main_frame, text="Binary Representation", padding="10")
binary_frame.pack(fill=tk.BOTH, expand=True, pady=5)

binary_info_var = tk.StringVar()
binary_info_var.set("")
binary_info = ttk.Label(binary_frame, textvariable=binary_info_var, font=('Courier', 10), justify=tk.LEFT)
binary_info.pack(fill=tk.BOTH, expand=True)

# Buttons frame
button_frame = ttk.Frame(main_frame, padding="10")
button_frame.pack(fill=tk.X, expand=False, pady=5)

# Calculate button
calculate_btn = ttk.Button(button_frame, text="Apply Mask", command=apply_mask)
calculate_btn.pack(side=tk.RIGHT, padx=5)

# Add a clear button
def clear_fields():
    ip_entry.delete(0, tk.END)
    mask_entry.delete(0, tk.END)
    result_var.set("The result will appear here")
    network_info_var.set("Network information will appear here")
    binary_info_var.set("")

clear_btn = ttk.Button(button_frame, text="Clear", command=clear_fields)
clear_btn.pack(side=tk.RIGHT, padx=5)

# Help button
help_btn = ttk.Button(button_frame, text="Help", command=show_help)
help_btn.pack(side=tk.LEFT, padx=5)

# Configure the Enter key to apply the mask
def on_enter(event):
    apply_mask()

# Associate the Enter key event with both input fields
ip_entry.bind("<Return>", on_enter)
mask_entry.bind("<Return>", on_enter)

# Start the main loop
root.mainloop()