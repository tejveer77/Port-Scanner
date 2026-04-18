import socket
import concurrent.futures
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox


# Scan a single port
def scan_port(target, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))

            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "Unknown"

                banner = "No banner"
                try:
                    s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                    data = s.recv(1024)
                    if data:
                        banner = data.decode(errors="ignore").strip().replace("\r", " ").replace("\n", " ")
                except:
                    pass

                return (port, service, banner)

    except:
        return None

    return None


# Perform scan
def perform_scan():
    target = target_entry.get().strip()
    start_port = start_port_entry.get().strip()
    end_port = end_port_entry.get().strip()
    timeout = timeout_entry.get().strip()
    workers = workers_entry.get().strip()

    if not target or not start_port or not end_port:
        messagebox.showerror("Input Error", "Please fill target, start port, and end port.")
        return

    try:
        start_port = int(start_port)
        end_port = int(end_port)
        timeout = float(timeout) if timeout else 0.5
        workers = int(workers) if workers else 100
    except ValueError:
        messagebox.showerror("Input Error", "Port values must be integers. Timeout must be numeric.")
        return

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        messagebox.showerror("Input Error", "Use valid ports between 1 and 65535, and start port must be <= end port.")
        return

    result_text.delete(1.0, tk.END)
    status_label.config(text="Resolving target...")
    scan_button.config(state=tk.DISABLED)

    def scan_thread():
        try:
            target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            root.after(0, lambda: messagebox.showerror("Error", "Unable to resolve hostname"))
            root.after(0, lambda: status_label.config(text="Scan failed"))
            root.after(0, lambda: scan_button.config(state=tk.NORMAL))
            return

        start_time = time.time()
        open_ports = []

        root.after(0, lambda: result_text.insert(tk.END, f"Target: {target} ({target_ip})\n"))
        root.after(0, lambda: result_text.insert(tk.END, f"Scanning ports {start_port}-{end_port}...\n\n"))
        root.after(0, lambda: status_label.config(text="Scanning..."))

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(scan_port, target_ip, port, timeout)
                for port in range(start_port, end_port + 1)
            ]

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    port, service, banner = result
                    open_ports.append((port, service, banner))
                    root.after(
                        0,
                        lambda p=port, s=service, b=banner:
                        result_text.insert(tk.END, f"Port {p} ({s}) -> Open | Banner: {b[:60]}\n")
                    )

        end_time = time.time()

        def finish_scan():
            result_text.insert(tk.END, "\nScan Complete.\n")
            result_text.insert(tk.END, f"Time Taken: {round(end_time - start_time, 2)} seconds\n")

            if not open_ports:
                result_text.insert(tk.END, "No open ports found.\n")
            else:
                result_text.insert(tk.END, "\nOpen Ports Summary:\n")
                for port, service, banner in sorted(open_ports, key=lambda x: x[0]):
                    result_text.insert(tk.END, f"- Port {port} ({service}) -> {banner[:60]}\n")

            status_label.config(text="Scan complete")
            scan_button.config(state=tk.NORMAL)

        root.after(0, finish_scan)

    threading.Thread(target=scan_thread, daemon=True).start()


# Clear output
def clear_output():
    result_text.delete(1.0, tk.END)
    status_label.config(text="Ready")


# Main window
root = tk.Tk()
root.title("Port Scanner UI")
root.geometry("800x600")
root.resizable(False, False)

# Title
title_label = tk.Label(root, text="Port Scanner", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Target Host/IP:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
target_entry = tk.Entry(input_frame, width=25)
target_entry.grid(row=0, column=1, padx=5, pady=5)
target_entry.insert(0, "scanme.nmap.org")

tk.Label(input_frame, text="Start Port:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
start_port_entry = tk.Entry(input_frame, width=10)
start_port_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
start_port_entry.insert(0, "20")

tk.Label(input_frame, text="End Port:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
end_port_entry = tk.Entry(input_frame, width=10)
end_port_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
end_port_entry.insert(0, "100")

tk.Label(input_frame, text="Timeout (sec):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
timeout_entry = tk.Entry(input_frame, width=10)
timeout_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
timeout_entry.insert(0, "0.5")

tk.Label(input_frame, text="Workers:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
workers_entry = tk.Entry(input_frame, width=10)
workers_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
workers_entry.insert(0, "100")

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

scan_button = tk.Button(button_frame, text="Start Scan", width=15, command=perform_scan, bg="lightgreen")
scan_button.grid(row=0, column=0, padx=10)

clear_button = tk.Button(button_frame, text="Clear", width=15, command=clear_output, bg="lightgray")
clear_button.grid(row=0, column=1, padx=10)

# Status label
status_label = tk.Label(root, text="Ready", font=("Arial", 10, "italic"))
status_label.pack(pady=5)

# Output box
result_text = tk.Text(root, wrap="word", width=95, height=25)
result_text.pack(padx=10, pady=10)

# Scrollbar
scrollbar = ttk.Scrollbar(root, command=result_text.yview)
scrollbar.place(x=775, y=180, height=400)
result_text.config(yscrollcommand=scrollbar.set)

root.mainloop()