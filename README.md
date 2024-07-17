# PowerShell Commander

PowerShell Commander is a Python application that provides a graphical user interface (GUI) for executing common PowerShell commands. This tool is designed to be user-friendly for both casual users and IT professionals.

## Features

- Execute predefined PowerShell commands using a GUI.
- View detailed system information and hardware configurations.
- Export command results to CSV files.
- Toggle between command and help mode for PowerShell commands.
- View command execution progress in real-time.
- Clear command output with a single button.

## Predefined Commands

The application includes a set of predefined PowerShell commands:

- **System Information**: `Get-CimInstance -ClassName Win32_ComputerSystem | Format-List *`
- **List Disk Drives**: `Get-WmiObject -Class Win32_DiskDrive | Select-Object DeviceID, Model, Size, MediaType`
- **List Network Adapters**: `Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, MacAddress`
- **List Active Network Connections**: `Get-NetTCPConnection | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State`
- **List Printers**: `Get-Printer | Select-Object Name, DriverName, PortName, Shared`
- **List Installed Software**: `Get-WmiObject -Class Win32_Product | Select-Object Name, Vendor, Version, InstallDate`
- **List Processes**: `Get-Process | Select-Object Name, Id, CPU, Responding, Path`
- **List Services**: `Get-Service | Select-Object DisplayName, Status, ServiceType, StartType`
- **Check System Uptime**: `Get-CimInstance Win32_OperatingSystem | Select-Object LastBootUpTime, @{Name='Uptime';Expression={[DateTime]::Now - [Management.ManagementDateTimeConverter]::ToDateTime($_.LastBootUpTime)}}`

## Installation

1. Clone the repository:
    
    ```bash
   git clone https://github.com/your-username/PowerShell-Commander.git

2. Install the required dependencies:
    ```bash
    pip install customtkinter

3. Run the application:

    ```bash
    python powershell_commander.py

## Usage

    Enter Command: Type or select a command to execute.
    Submit Command: Click to run the entered command.
    Help Mode: Toggle to view PowerShell help documentation for commands.
    Export to CSV: Save the list of predefined commands to a CSV file.
    Clear Output: Clear the output display area.

## Contributing

Contributions are welcome! Please follow these steps:

    Fork the repository.
    Create a new branch (git checkout -b feature-branch).
    Make your changes.
    Commit your changes (git commit -m 'Add new feature').
    Push to the branch (git push origin feature-branch).
    Create a new Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

Special thanks to the contributors and the open-source community for their support and contributions.
