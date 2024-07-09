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

def toggle_settings(settings_frame, main_frame):
    if settings_frame.winfo_viewable():
        settings_frame.grid_remove()
        main_frame.grid()
    else:
        main_frame.grid_remove()
        settings_frame.grid()

def toggle_mode(root, mode):
    if mode.get() == "Dark":
        root.configure(bg="#333333")
        style.configure("TButton", background="#666666", foreground="black")
        style.configure("TLabel", background="#333333", foreground="white")
        style.configure("TFrame", background="#333333")
        style.configure("TText", background="#444444", foreground="white")
    else:
        root.configure(bg="#ffffff")
        style.configure("TButton", background="#cccccc", foreground="black")
        style.configure("TLabel", background="#ffffff", foreground="black")
        style.configure("TFrame", background="#ffffff")
        style.configure("TText", background="#ffffff", foreground="black")

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
    root.rowconfigure(2, weight=0)
    root.rowconfigure(3, weight=0)
    root.rowconfigure(4, weight=1)
    root.rowconfigure(5, weight=0)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=0)

    # Main frame for command input and output
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, rowspan=6, columnspan=2, sticky="nsew")

    commands_label = ttk.Label(main_frame, text="Enter Command", font=("Helvetica", 12, "bold"))
    commands_label.grid(row=0, column=0, pady=(10, 5), sticky="nsew")

    command_entry = tk.Text(main_frame, height=4, width=100, bg="#444444", fg="white")
    command_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

    preset_commands = {
        "List Processes": "Get-Process",
        "List Services": "Get-Service",
        "System Logs": "Get-EventLog -LogName System",
        "Operating System Info": "Get-WmiObject Win32_OperatingSystem",
        "Network Adapters": "Get-NetAdapter"
    }

    preset_frame = ttk.Frame(main_frame)
    preset_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    for index, (label, command) in enumerate(preset_commands.items()):
        button = ttk.Button(preset_frame, text=label, command=lambda cmd=command: load_command(command_entry, cmd))
        button.grid(row=0, column=index, padx=5, pady=5, sticky="ew")

    submit_button = ttk.Button(main_frame, text="Submit Command", command=lambda: submit_command(command_entry, output_text))
    submit_button.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

    output_label = ttk.Label(main_frame, text="Output", font=("Helvetica", 12, "bold"))
    output_label.grid(row=3, column=0, pady=(10, 5), sticky="nsew")

    output_frame = ttk.Frame(main_frame)
    output_frame.grid(row=4, column=0, sticky="nsew")
    main_frame.rowconfigure(4, weight=1)

    scrollbar = tk.Scrollbar(output_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    output_text = tk.Text(output_frame, height=15, width=100, yscrollcommand=scrollbar.set, bg="#444444", fg="white")
    output_text.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=output_text.yview)

    clear_button = ttk.Button(main_frame, text="Clear Output", command=lambda: clear_output(output_text))
    clear_button.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="ew")

    settings_button = ttk.Button(main_frame, text="Settings", command=lambda: toggle_settings(settings_frame, main_frame))
    settings_button.grid(row=5, column=0, pady=10)

    # Settings frame
    settings_frame = ttk.Frame(root)
    settings_frame.grid(row=0, column=0, rowspan=6, columnspan=2, sticky="nsew")
    settings_frame.grid_remove()

    settings_label = ttk.Label(settings_frame, text="Settings Page", font=("Helvetica", 12, "bold"))
    settings_label.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

    mode_label = ttk.Label(settings_frame, text="Select Mode:", font=("Helvetica", 10))
    mode_label.grid(row=1, column=0, pady=10, padx=20, sticky="w")

    mode = tk.StringVar(value="Dark")
    mode_toggle = ttk.Combobox(settings_frame, textvariable=mode, values=["Dark", "Light"])
    mode_toggle.grid(row=1, column=1, pady=10, padx=20, sticky="w")

    mode_toggle.bind("<<ComboboxSelected>>", lambda event: toggle_mode(root, mode))

    close_settings_button = ttk.Button(settings_frame, text="Close Settings", command=lambda: toggle_settings(settings_frame, main_frame))
    close_settings_button.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")

    command_entry.grid(sticky="ew")
    output_frame.rowconfigure(0, weight=1)
    output_frame.columnconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
