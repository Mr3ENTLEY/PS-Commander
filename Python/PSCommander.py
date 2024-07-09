"""
Date: July 8, 2024
Written By: Jeffrey Bentley
Name: PSCommander
Description: PS Commander is a versatile and user-friendly GUI application designed to execute and manage PowerShell commands efficiently. Built using the CustomTkinter library, this application offers a simplistic experience for both novice and advanced users of PowerShell.
"""

"""
Date: July 8, 2024
Written By: Jeffrey Bentley
Name: PSCommander
Description: PS Commander is a versatile and user-friendly GUI application designed to execute and manage PowerShell commands efficiently. Built using the CustomTkinter library, this application offers a simplistic experience for both novice and advanced users of PowerShell.
"""

import customtkinter as ctk
from tkinter import PhotoImage, messagebox, filedialog
import subprocess
import threading
import time
import csv

# Dictionary of regular preset commands
preset_commands = {
    "System Information": "Get-CimInstance -ClassName Win32_ComputerSystem | Format-List *",
    "List Disk Drives": "Get-WmiObject -Class Win32_DiskDrive | Select-Object DeviceID, Model, Size, MediaType",
    "List Network Adapters": "Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, MacAddress",
    "List Active Network Connections": "Get-NetTCPConnection | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State",
    "List Printers": "Get-Printer | Select-Object Name, DriverName, PortName, Shared",
    "List Installed Software": "Get-WmiObject -Class Win32_Product | Select-Object Name, Vendor, Version, InstallDate",
    "List Processes": "Get-Process | Select-Object Name, Id, CPU, Responding, Path",
    "List Services": "Get-Service | Select-Object DisplayName, Status, ServiceType, StartType",
    "Check System Uptime": "Get-CimInstance Win32_OperatingSystem | Select-Object LastBootUpTime, @{Name='Uptime';Expression={[DateTime]::Now - [Management.ManagementDateTimeConverter]::ToDateTime($_.LastBootUpTime)}}"
}

# Dictionary of help mode preset commands
preset_help = {
    "System Information": "Get-Help Get-CimInstance",
    "List Disk Drives": "Get-Help Get-WmiObject",
    "List Network Adapters": "Get-Help Get-NetAdapter",
    "List Active Network Connections": "Get-Help Get-NetTCPConnection",
    "List Printers": "Get-Help Get-Printer",
    "List Installed Software": "Get-Help Get-WmiObject",
    "List Processes": "Get-Help Get-Process",
    "List Services": "Get-Help Get-Service",
    "Check System Uptime": "Get-Help Get-CimInstance"
}

# Global variable for help mode toggle
help_toggle = None

def toggle_help_commands():
    global preset_commands, preset_help, help_toggle

    if help_toggle.get():
        return preset_help
    else:
        return preset_commands

def run_command(command, output_text, progress_var, root):
    try:
        progress_var.set(0)
        
        process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        output_text.delete(1.0, ctk.END)

        def read_stdout():
            total_output = ""
            for line in iter(process.stdout.readline, ''):
                total_output += line
                output_text.insert(ctk.END, line)
                root.update_idletasks()
                progress_var.set(len(total_output) / 10)  # Increment based on length of output
            process.stdout.close()

        def read_stderr():
            total_output = ""
            for line in iter(process.stderr.readline, ''):
                total_output += line
                output_text.insert(ctk.END, line)
                root.update_idletasks()
                progress_var.set(len(total_output) / 10)  # Increment based on length of output
            process.stderr.close()

        threading.Thread(target=read_stdout, daemon=True).start()
        threading.Thread(target=read_stderr, daemon=True).start()

        while process.poll() is None:
            time.sleep(0.1)
            root.update_idletasks()

        progress_var.set(100)
        root.update_idletasks()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def submit_command(command_entry, output_text, progress_var, root):
    command = command_entry.get("1.0", ctk.END).strip()
    if command:
        output_text.delete(1.0, ctk.END)
        progress_var.set(0)
        commands = toggle_help_commands()
        if help_toggle.get():
            # Find the corresponding command label in help mode dictionary
            for label, cmd in commands.items():
                if label == command:
                    command = cmd
                    break
        threading.Thread(target=run_command, args=(command, output_text, progress_var, root), daemon=True).start()
    else:
        messagebox.showwarning("Warning", "Please enter a PowerShell command.")

def clear_output(output_text):
    output_text.delete(1.0, ctk.END)

def load_command(command_entry, command):
    command_entry.delete("1.0", ctk.END)
    command_entry.insert(ctk.END, command.strip())

def export_to_csv():
    global preset_commands

    # Ask user for file save location
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Command Label", "PowerShell Command"])
                for label, command in preset_commands.items():
                    csv_writer.writerow([label, command])
            messagebox.showinfo("Export Successful", f"Commands exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export commands: {str(e)}")

def create_gui():
    global preset_commands

    ctk.set_appearance_mode("System")  # Use a light appearance mode
    ctk.set_default_color_theme("blue")  # Choose a blue color theme

    root = ctk.CTk()
    root.title("PowerShell Commander")
    root.geometry("800x600")

    # Set ICO file as application icon
    icon_path = "E:/DEV/Local/EXE/Visual Basic/Python/PSCommander.ico"
    root.iconbitmap(icon_path)

    main_frame = ctk.CTkFrame(root)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    export_button = ctk.CTkButton(main_frame, text="Export to CSV", font=("Segoe UI", 14, "bold"), command=export_to_csv)
    export_button.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

    commands_label = ctk.CTkLabel(main_frame, text="Enter Command", font=("Segoe UI", 14, "bold"))
    commands_label.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="w")

    command_entry = ctk.CTkTextbox(main_frame, height=8, width=60, font=("Calibri", 14))
    command_entry.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

    submit_button = ctk.CTkButton(main_frame, text="Submit Command", font=("Segoe UI", 14, "bold"), command=lambda: submit_command(command_entry, output_text, progress_var, root))
    submit_button.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="ew")

    global help_toggle
    help_toggle = ctk.BooleanVar()
    help_button = ctk.CTkCheckBox(main_frame, text="Help Mode", font=("Segoe UI", 14), variable=help_toggle, command=lambda: load_preset_commands(preset_frame, help_toggle.get()))
    help_button.grid(row=3, column=0, padx=10, pady=(10, 5), sticky="w")

    progress_var = ctk.DoubleVar()
    progress_bar = ctk.CTkProgressBar(main_frame, variable=progress_var, width=600)
    progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    preset_frame = ctk.CTkFrame(main_frame)
    preset_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def load_preset_commands(frame, help_mode):
        global preset_commands, preset_help

        commands = toggle_help_commands() if help_mode else preset_commands

        for widget in frame.winfo_children():
            widget.destroy()

        for idx, (label, command) in enumerate(commands.items(), start=1):
            preset_button = ctk.CTkButton(frame, text=label, font=("Segoe UI", 14), command=lambda cmd=command: load_command(command_entry, cmd))
            preset_button.grid(row=0, column=idx, padx=5, pady=5, sticky="ew")

    load_preset_commands(preset_frame, help_toggle.get())

    output_frame = ctk.CTkFrame(main_frame)
    output_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    main_frame.rowconfigure(6, weight=1)
    main_frame.rowconfigure(7, weight=1)
    main_frame.columnconfigure(0, weight=1)

    scrollbar_output = ctk.CTkScrollbar(output_frame)
    scrollbar_output.pack(side="right", fill="y")

    output_text = ctk.CTkTextbox(output_frame, height=10, font=("Consolas", 14))
    output_text.pack(expand=True, fill="both")
    scrollbar_output.configure(command=output_text.yview)

    clear_button = ctk.CTkButton(main_frame, text="Clear Output", font=("Segoe UI", 14, "bold"), command=lambda: clear_output(output_text))
    clear_button.grid(row=8, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")

    root.mainloop()

if __name__ == "__main__":
    create_gui()
