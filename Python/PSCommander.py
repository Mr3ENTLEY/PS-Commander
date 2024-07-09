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
    
    label = ttk.Label(settings_window, text="Settings Page")
    label.pack(padx=20, pady=20)

    close_button = ttk.Button(settings_window, text="Close", command=settings_window.destroy)
    close_button.pack(pady=10)

def load_command(command_entry, command):
    command_entry.delete("1.0", tk.END)  # Clear existing text
    command_entry.insert(tk.END, command.strip())  # Load new command

def create_gui():
    root = tk.Tk()
    root.title("PowerShell Commander")
    root.configure(bg="#333333")

    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#666666", foreground="black")
    style.configure("TLabel", background="#333333", foreground="white")
    style.configure("TFrame", background="#333333")
    style.configure("TText", background="#444444", foreground="white")

    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=0)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3, weight=4)
    root.rowconfigure(4, weight=0)
    root.rowconfigure(5, weight=0)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=0)

    commands_label = ttk.Label(root, text="Enter Command", font=("Helvetica", 12, "bold"))
    commands_label.grid(row=0, column=0, pady=(10, 5), sticky="nsew")

    command_entry = tk.Text(root, height=6, width=100, bg="#444444", fg="white")
    command_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

    preset_commands = {
        "List Processes": "Get-Process",
        "List Services": "Get-Service",
        "System Logs": "Get-EventLog -LogName System",
        "Operating System Info": "Get-WmiObject Win32_OperatingSystem",
        "Network Adapters": "Get-NetAdapter"
    }

    preset_frame = ttk.Frame(root)
    preset_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

    for index, (label, command) in enumerate(preset_commands.items()):
        button = ttk.Button(preset_frame, text=label, command=lambda cmd=command: load_command(command_entry, cmd))
        button.grid(row=0, column=index, padx=5, pady=5, sticky="ew")

    output_label = ttk.Label(root, text="Output", font=("Helvetica", 12, "bold"))
    output_label.grid(row=3, column=0, pady=(10, 5), sticky="nsew")

    output_frame = ttk.Frame(root)
    output_frame.grid(row=4, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(output_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    output_text = tk.Text(output_frame, height=15, width=100, yscrollcommand=scrollbar.set, bg="#444444", fg="white")
    output_text.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=output_text.yview)

    clear_button = ttk.Button(root, text="Clear Output", command=lambda: clear_output(output_text))
    clear_button.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="ew")

    submit_button = ttk.Button(root, text="Submit Command", command=lambda: submit_command(command_entry, output_text))
    submit_button.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

    settings_button = ttk.Button(root, text="Settings", command=open_settings)
    settings_button.grid(row=5, column=0, pady=10)

    command_entry.grid(sticky="nsew")
    output_frame.rowconfigure(0, weight=1)
    output_frame.columnconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
