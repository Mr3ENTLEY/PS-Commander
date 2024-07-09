"""
Date: July 8, 2024
Written By: Jeffrey Bentley
Name: PSCommander
Description: PS Commander is a versatile and user-friendly GUI application designed to execute and manage PowerShell commands efficiently. Built using the Tkinter library in Python, this application offers a simplistic experience for both novice and advanced users of PowerShell.
"""
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess

def run_command(command, output_text):
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        output_text.delete(1.0, tk.END)  # Clear previous output
        output_text.insert(tk.END, result.stdout)  # Display new output
    except Exception as e:
        messagebox.showerror("Error", str(e))

def submit_command(command_entry, output_text):
    command = command_entry.get("1.0", tk.END).strip()  # Get command from text box
    if command:
        run_command(command, output_text)
    else:
        messagebox.showwarning("Warning", "Please enter a PowerShell command.")

def clear_output(output_text):
    output_text.delete(1.0, tk.END)

def open_settings():
    # Function to create and open the settings window
    settings_window = tk.Toplevel()
    settings_window.title("Settings")
    
    # Example settings UI (you can customize this)
    label = tk.Label(settings_window, text="Settings Page")
    label.pack(padx=20, pady=20)

    close_button = tk.Button(settings_window, text="Close", command=settings_window.destroy)
    close_button.pack(pady=10)

def load_command(command_entry, command):
    command_entry.delete("1.0", tk.END)  # Clear existing text
    command_entry.insert(tk.END, command.strip())  # Load new command

def create_gui():
    root = tk.Tk()
    root.title("PowerShell Commander")

    # Set background color to dark grey
    root.configure(bg="#333333")

    # Configure the root window to be resizable
    root.rowconfigure(0, weight=0)  # Commands entry row
    root.rowconfigure(1, weight=0)  # Commands buttons row
    root.rowconfigure(2, weight=1)  # Output title row
    root.rowconfigure(3, weight=4)  # Output row (expandable)
    root.rowconfigure(4, weight=0)  # Clear and submit button row
    root.rowconfigure(5, weight=0)  # Settings button row
    root.columnconfigure(0, weight=1)  # Column for all widgets
    root.columnconfigure(1, weight=0)  # Column for buttons

    # Title for Commands Section
    commands_label = tk.Label(root, text="Enter Command", font=("Helvetica", 12, "bold"), bg="#333333", fg="white")
    commands_label.grid(row=0, column=0, pady=(10, 5), sticky="nsew")  # Centered, sticky to center

    # Text entry for command
    command_entry = tk.Text(root, height=6, width=100, bg="#444444", fg="white")
    command_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

    # Preset commands dictionary
    preset_commands = {
        "List Processes": "Get-Process",
        "List Services": "Get-Service",
        "System Logs": "Get-EventLog -LogName System",
        "Operating System Info": "Get-WmiObject Win32_OperatingSystem",
        "Network Adapters": "Get-NetAdapter"
    }

    # Frame for preset buttons
    preset_frame = tk.Frame(root, bg="#333333")
    preset_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

    # Create buttons for preset commands horizontally
    for index, (label, command) in enumerate(preset_commands.items()):
        button = tk.Button(preset_frame, text=label, command=lambda cmd=command: load_command(command_entry, cmd), bg="#666666", fg="white")
        button.grid(row=0, column=index, padx=5, pady=5, sticky="ew")

    # Title for Output Section
    output_label = tk.Label(root, text="Output", font=("Helvetica", 12, "bold"), bg="#333333", fg="white")
    output_label.grid(row=3, column=0, pady=(10, 5), sticky="nsew")  # Centered, sticky to center

    # Frame for output and scrollbar
    output_frame = tk.Frame(root, bg="#333333")
    output_frame.grid(row=4, column=0, sticky="nsew")

    # Scrollbar for text widget
    scrollbar = tk.Scrollbar(output_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Text widget for displaying output
    output_text = tk.Text(output_frame, height=15, width=100, yscrollcommand=scrollbar.set, bg="#444444", fg="white")
    output_text.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=output_text.yview)

    # Button to clear output
    clear_button = tk.Button(root, text="Clear Output", command=lambda: clear_output(output_text), bg="#666666", fg="white")
    clear_button.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="ew")

    # Button to submit command
    submit_button = tk.Button(root, text="Submit Command", command=lambda: submit_command(command_entry, output_text), bg="#666666", fg="white")
    submit_button.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

    # Button to open settings
    settings_button = tk.Button(root, text="Settings", command=open_settings, bg="#666666", fg="white")
    settings_button.grid(row=5, column=0, pady=10)

    # Make the text widget and command entry expand with the window
    command_entry.grid(sticky="nsew")
    output_frame.rowconfigure(0, weight=1)
    output_frame.columnconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
