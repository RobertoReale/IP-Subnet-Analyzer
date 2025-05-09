# IP Subnet Analyzer

A Python desktop application that helps network administrators and IT students analyze IP subnets by applying subnet masks to IP addresses and calculating essential network information.

## Features

- **IP Address and Subnet Mask Analysis**: Apply subnet masks to IP addresses and visualize the results
- **Multiple Mask Input Formats**: Support for both CIDR notation (e.g., `/24`) and decimal notation (e.g., `255.255.255.0`)
- **Comprehensive Network Information**: Calculate and display:
  - Network address
  - First and last usable host addresses
  - Broadcast address
  - Total number of addresses in the network
  - Number of usable host addresses
- **Binary Representation**: See binary representations of IP addresses, masks, and results for educational purposes
- **Input Validation**: Automatic validation of IP addresses and subnet masks
- **User-Friendly Interface**: Clean, intuitive Tkinter GUI

## Installation

### Prerequisites
- Python 3.6 or higher
- Tkinter (usually comes with Python installation)
- ipaddress module (standard library in Python 3.x)

### Steps
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ip-subnet-analyzer.git
   cd ip-subnet-analyzer
   ```

2. Run the application:
   ```
   python subnet_analyzer.py
   ```

## Usage

1. Enter an IPv4 address in the "IP Address" field (e.g., `192.168.1.1`)
2. Enter a subnet mask in either:
   - CIDR notation (e.g., `/24`)
   - Decimal notation (e.g., `255.255.255.0`)
3. Click "Apply Mask" or press Enter
4. View the network address in the result section
5. Examine detailed network information and binary representations

### Example

**Input:**
- IP: `102.201.225.140`
- Mask: `/25` (or `255.255.255.128`)

**Results:**
- Network address: `102.201.225.128/25`
- First host address: `102.201.225.129`
- Last host address: `102.201.225.254`
- Broadcast address: `102.201.225.255`
- Total addresses: `128`
- Usable hosts: `126`

## How It Works

The application performs the following operations:
1. Validates the IP address and subnet mask inputs
2. Converts the mask to CIDR notation if in decimal format
3. Uses Python's `ipaddress` module to calculate network information
4. Displays the results, including binary representations for educational purposes

The fundamental operation is a bitwise AND between the IP address and the subnet mask, which produces the network address.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Python `ipaddress` module for the core network calculations
- Tkinter for the GUI framework

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/ip-subnet-analyzer](https://github.com/yourusername/ip-subnet-analyzer)
