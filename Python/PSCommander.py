"""
Date: July 8, 2024
Written By: Jeffrey Bentley
Name: PSCommander
Description: PS Commander is a versatile and user-friendly GUI application designed to execute and manage PowerShell commands efficiently. Built using the Tkinter library in Python, this application offers a simplistic experience for both novice and advanced users of PowerShell.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import threading
import time

def run_command(command, output_text, progress_var, root):
    try:
        progress_var.set(0)
        root.update_idletasks()  # Ensure GUI is updated
        
        # Run the PowerShell command asynchronously
        process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        output_text.delete(1.0, tk.END)  # Clear previous output

        # Read stdout and stderr in separate threads to prevent blocking
        def read_stdout():
            for line in iter(process.stdout.readline, ''):
                output_text.insert(tk.END, line)
                root.update_idletasks()  # Update GUI to show the command output
                progress_var.set(progress_var.get() + 0.5)  # Increment progress bar
            process.stdout.close()

        def read_stderr():
            for line in iter(process.stderr.readline, ''):
                output_text.insert(tk.END, line)
                root.update_idletasks()  # Update GUI to show the command output
                progress_var.set(progress_var.get() + 0.5)  # Increment progress bar
            process.stderr.close()

        # Start threads for reading stdout and stderr
        threading.Thread(target=read_stdout, daemon=True).start()
        threading.Thread(target=read_stderr, daemon=True).start()

        # Wait for the process to finish
        while process.poll() is None:
            time.sleep(0.1)
            progress_var.set(progress_var.get() + 0.5)
            root.update_idletasks()  # Update GUI

        # Ensure progress bar reaches 100% at completion
        progress_var.set(100)
        root.update_idletasks()  # Final update of GUI

    except Exception as e:
        messagebox.showerror("Error", str(e))

def submit_command(command_entry, output_text, progress_var, root):
    command = command_entry.get("1.0", tk.END).strip()  # Get command from text box
    if command:
        # Clear output before running new command
        output_text.delete(1.0, tk.END)
        # Reset progress bar
        progress_var.set(0)
        # Run command asynchronously
        threading.Thread(target=run_command, args=(command, output_text, progress_var, root), daemon=True).start()
    else:
        messagebox.showwarning("Warning", "Please enter a PowerShell command.")

def clear_output(output_text):
    output_text.delete(1.0, tk.END)

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

    main_frame = ttk.Frame(root)
    main_frame.pack(expand=True, fill=tk.BOTH)

    commands_label = ttk.Label(main_frame, text="Enter Command", font=("Helvetica", 12, "bold"))
    commands_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

    command_entry = tk.Text(main_frame, height=4, width=100, bg="#444444", fg="white")
    command_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

    submit_button = ttk.Button(main_frame, text="Submit Command", command=lambda: submit_command(command_entry, output_text, progress_var, root))
    submit_button.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(main_frame, variable=progress_var, maximum=100, mode="determinate")
    progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    preset_commands = {
        "List Processes": "Get-Process | Select-Object -First 100",
        "List Services": "Get-Service | Select-Object -First 100",
        "System Information": "Get-CimInstance -ClassName Win32_ComputerSystem",
        "List Disk Drives": "Get-WmiObject -Class Win32_DiskDrive | Select-Object -First 100",
        "List Network Adapters": "Get-NetAdapter | Select-Object -First 100",
        "List Printers": "Get-Printer | Select-Object -First 100",
        "List Installed Software": "Get-WmiObject -Class Win32_Product | Select-Object -First 100",
        "Check System Uptime": "Get-CimInstance Win32_OperatingSystem | Select-Object LastBootUpTime, @{Name='Uptime';Expression={[datetime]::Now - $_.LastBootUpTime}}"
    }

    preset_frame = ttk.Frame(main_frame, style="Custom.TFrame")
    preset_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    scrollbar = tk.Scrollbar(preset_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    command_list = tk.Listbox(preset_frame, yscrollcommand=scrollbar.set, bg="#333333", fg="white", selectbackground="#555555", selectforeground="white", font=("Courier", 10))
    command_list.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=command_list.yview)

    for label, command in preset_commands.items():
        command_list.insert(tk.END, label)

    def load_command_from_list(event):
        selection = command_list.curselection()
        if selection:
            index = selection[0]
            label = command_list.get(index)
            load_command(command_entry, preset_commands[label])

    command_list.bind("<<ListboxSelect>>", load_command_from_list)

    output_label = ttk.Label(main_frame, text="Output", font=("Helvetica", 12, "bold"))
    output_label.grid(row=4, column=0, pady=(10, 5), sticky="w")

    output_frame = ttk.Frame(main_frame)
    output_frame.grid(row=5, column=0, sticky="nsew")
    main_frame.rowconfigure(5, weight=1)
    main_frame.columnconfigure(0, weight=1)

    scrollbar_output = tk.Scrollbar(output_frame)
    scrollbar_output.pack(side=tk.RIGHT, fill=tk.Y)

    output_text = tk.Text(output_frame, height=15, width=100, yscrollcommand=scrollbar_output.set, bg="#444444", fg="white")
    output_text.pack(expand=True, fill=tk.BOTH)
    scrollbar_output.config(command=output_text.yview)

    clear_button = ttk.Button(main_frame, text="Clear Output", command=lambda: clear_output(output_text))
    clear_button.grid(row=5, column=1, padx=10, pady=(10, 10), sticky="ew")

    root.mainloop()

if __name__ == "__main__":
    create_gui()
