# Port-Scanner
This project is a Python-based port scanner that detects open ports on a target system using TCP socket connections. It is inspired by basic functionality of tools like Nmap and is designed for educational purposes.The application supports both command-line execution and a graphical user interface (GUI) built using Tkinter.
## Features
* Scan a target host (IP or domain)
* Custom port range scanning
* Detect open ports
* Service identification (HTTP, SSH, etc.)
* Basic banner grabbing
* Timeout handling for efficiency
* Multithreading for faster scanning
* User-friendly GUI (Tkinter)
## Technologies Used
* Python
* socket
* concurrent.futures (multithreading)
* Tkinter (GUI)
## How to Run
### 1. Clone the Repository
git clone https://github.com/yourusername/Port-Scanner.git
cd Port-Scanner
### 2. Run Command-Line Version
python scanner.py scanme.nmap.org 20 100
### 3. Run GUI Version
python scanner_ui.py
## Example Output
Target: scanme.nmap.org
Scanning ports 20–100...

Port 22 (ssh) -> Open
Port 80 (http) -> Open

Scan Complete.
## Learning Outcomes
* Understanding TCP socket communication
* Working with ports and network services
* Implementing concurrency using multithreading
* Building GUI applications with Tkinter
* Basic cybersecurity and network reconnaissance concepts
## Author
Tejveer Singh
