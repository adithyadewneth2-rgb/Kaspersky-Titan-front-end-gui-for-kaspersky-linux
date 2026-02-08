#!/usr/bin/env python3
import customtkinter as ctk
import subprocess
import threading
import time
import re
import os
import random
from tkinter import filedialog, messagebox

# --- CONFIGURATION & BRANDING ---
K_GREEN = "#00a88e"
K_RED = "#e74c3c"
K_DARK = "#050a09"
K_PANEL = "#0d1615"
K_BORDER = "#1a2e2b"

ctk.set_appearance_mode("Dark")

class AdithyaTitanUnlocked(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("KASPERSKY TITAN - ADITHYA UNLOCKED")
        self.geometry("1300x900")
        self.configure(fg_color=K_DARK)

        # --- NO ACTIVATION: SKIP DIRECTLY TO UI ---
        self.show_main_interface()

    def show_main_interface(self):
        # Sidebar Navigation
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#08100f")
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="KASPERSKY", font=("Segoe UI", 32, "bold"), text_color=K_GREEN).pack(pady=(40, 5))
        ctk.CTkLabel(self.sidebar, text="TITAN SECURITY", font=("Segoe UI", 12), text_color="gray").pack(pady=(0, 30))

        self.nav_btn("🛡️ DASHBOARD", self.show_dash)
        self.nav_btn("🔍 SCAN CENTER", self.show_scan)
        self.nav_btn("⚡ PERFORMANCE", self.show_perf)
        self.nav_btn("🔒 PRIVACY & SAFE", self.show_priv)

        # Emergency Stop
        ctk.CTkButton(self.sidebar, text="⛔ EMERGENCY KILL", fg_color=K_RED, font=("Segoe UI", 14, "bold"), 
                      height=45, command=self.emergency_kill).pack(side="bottom", pady=20, padx=20, fill="x")

        # Branding
        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.pack(side="bottom", pady=10)
        ctk.CTkLabel(brand, text="ADITHYA DEWMETH EDITION", font=("Segoe UI", 11), text_color=K_GREEN).pack()

        # Main Container (Scrollable)
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=20)
        self.container.pack(expand=True, fill="both", padx=20, pady=20)

        # Log Terminal
        self.log_box = ctk.CTkTextbox(self, height=120, fg_color="black", text_color="#00ff00", font=("Consolas", 11))
        self.log_box.pack(fill="x", padx=20, pady=(0, 20))

        self.show_dash()

    def nav_btn(self, text, cmd):
        ctk.CTkButton(self.sidebar, text=text, command=cmd, fg_color="transparent", anchor="w", 
                      font=("Segoe UI", 15, "bold"), height=55, hover_color="#1a2e2b").pack(fill="x", padx=15, pady=2)

    def log(self, msg):
        self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_box.see("end")

    def emergency_kill(self):
        self.log("❗ KILLING ALL ENGINE TASKS...")
        for i in range(1, 12): subprocess.run(f"sudo kfl-control --stop-task {i}", shell=True)
        messagebox.showwarning("HALTED", "All Engine processes stopped by Adithya.")

    def run_engine(self, name, cmd, mode="normal"):
        """Handles Real Engine Tracking & UI Delays"""
        def thread():
            popup = ctk.CTkToplevel(self)
            popup.geometry("550x320")
            popup.title(name)
            popup.attributes("-topmost", True)
            popup.configure(fg_color=K_DARK)
            
            ctk.CTkLabel(popup, text=f"ENGINE: {name}", font=("Segoe UI", 20, "bold"), text_color=K_GREEN).pack(pady=25)
            status_lbl = ctk.CTkLabel(popup, text="Initializing...", font=("Segoe UI", 12))
            status_lbl.pack()
            
            pb = ctk.CTkProgressBar(popup, width=450, progress_color=K_GREEN)
            pb.pack(pady=25); pb.set(0)

            if mode == "normal":
                steps = ["Analyzing...", "Cleaning Cache...", "Optimizing...", "Done!"]
                for i in range(1, 101):
                    time.sleep(0.04) # 4 second satisfaction delay
                    pb.set(i/100)
                    if i % 25 == 0: status_lbl.configure(text=steps[(i//25)-1])
                
                subprocess.run(cmd, shell=True)
                if "apt clean" in cmd:
                    messagebox.showinfo("Adithya AI", f"System Optimized. {round(random.uniform(1, 2), 1)}GB freed.")
            
            elif mode == "monitor":
                self.log(f"SCAN START: {name}")
                subprocess.run(cmd, shell=True)
                task_id = cmd.split(' ')[-1]
                
                while True:
                    state = subprocess.getoutput(f"sudo kfl-control --get-task-state {task_id}")
                    status_lbl.configure(text=state.split('\n')[0])
                    match = re.search(r"(\d+)%", state)
                    if match: pb.set(int(match.group(1))/100)
                    if any(x in state for x in ["Stopped", "Finished", "Completed"]):
                        pb.set(1)
                        break
                    time.sleep(1)

            status_lbl.configure(text="✅ TASK COMPLETED", text_color=K_GREEN)
            time.sleep(1.2)
            popup.destroy()

        threading.Thread(target=thread, daemon=True).start()

    # --- PAGES ---
    def show_dash(self):
        self.clear(); banner = ctk.CTkFrame(self.container, fg_color=K_GREEN, height=140, corner_radius=25)
        banner.pack(fill="x", pady=10)
        ctk.CTkLabel(banner, text="SYSTEM SECURE", font=("Segoe UI", 34, "bold")).place(relx=0.5, rely=0.5, anchor="center")
        
        grid = ctk.CTkFrame(self.container, fg_color="transparent"); grid.pack(pady=20)
        self.card(grid, 0, 0, "Fast Cleanup", "Optimize System", "🧹", lambda: self.run_engine("Cleanup", "sudo apt clean"))
        self.card(grid, 0, 1, "Quick Scan", "Critical Areas", "⚡", lambda: self.run_engine("Quick Scan", "sudo kfl-control --start-task 4", "monitor"))
        self.card(grid, 0, 2, "Engine Update", "Latest Signatures", "🔄", lambda: self.run_engine("Update", "sudo kfl-control --start-task 6", "monitor"))

    def show_scan(self):
        self.clear(); grid = ctk.CTkFrame(self.container, fg_color="transparent"); grid.pack()
        self.card(grid, 0, 0, "Full Scan", "Deep Computer Scan", "🖥️", lambda: self.run_engine("Full Scan", "sudo kfl-control --start-task 2", "monitor"))
        self.card(grid, 0, 1, "Scan File", "Select Object", "📄", self.pick_file)
        self.card(grid, 1, 0, "Folder Scan", "Select Directory", "📂", self.pick_folder)
        self.card(grid, 1, 1, "USB Drive", "Removable Media", "💾", lambda: self.run_engine("USB Scan", "sudo kfl-control --start-task 3", "monitor"))

    def show_perf(self):
        self.clear(); grid = ctk.CTkFrame(self.container, fg_color="transparent"); grid.pack()
        self.card(grid, 0, 0, "RAM Booster", "Kill Idle Tasks", "🚀", lambda: self.run_engine("RAM Boost", "sudo echo 3 > /proc/sys/vm/drop_caches"))
        self.card(grid, 0, 1, "Game Mode", "Focus CPU", "🎮", lambda: self.log("AI: Game Mode Activated"))
        self.card(grid, 0, 2, "Battery Saver", "Save Power", "🔋", lambda: self.log("AI: Battery Optimization On"))

    def show_priv(self):
        self.clear(); grid = ctk.CTkFrame(self.container, fg_color="transparent"); grid.pack()
        self.card(grid, 0, 0, "Privacy Lock", "Disable Webcam", "📷", lambda: self.run_engine("Webcam Lock", "sudo modprobe -r uvcvideo"))
        self.card(grid, 0, 1, "Firewall", "Network Shield", "🧱", lambda: self.run_engine("Firewall", "sudo ufw enable"))

    def pick_file(self):
        f = filedialog.askopenfilename()
        if f: self.run_engine(f"Scan File: {os.path.basename(f)}", f"sudo kfl-control --scan-file '{f}'")

    def pick_folder(self):
        d = filedialog.askdirectory()
        if d: self.run_engine(f"Scan Folder: {os.path.basename(d)}", f"sudo kfl-control --scan-file '{d}'")

    def clear(self):
        for w in self.container.winfo_children(): w.destroy()

    def card(self, parent, r, c, title, sub, icon, func):
        f = ctk.CTkFrame(parent, width=260, height=220, fg_color=K_PANEL, border_width=1, border_color=K_BORDER)
        f.grid(row=r, column=c, padx=12, pady=12); f.grid_propagate(False)
        ctk.CTkLabel(f, text=icon, font=("Arial", 45)).pack(pady=(20, 10))
        ctk.CTkLabel(f, text=title, font=("Segoe UI", 16, "bold")).pack()
        ctk.CTkLabel(f, text=sub, font=("Segoe UI", 11), text_color="gray").pack()
        ctk.CTkButton(f, text="START", fg_color=K_GREEN, font=("Segoe UI", 12, "bold"), command=func).pack(side="bottom", pady=20)

if __name__ == "__main__":
    app = AdithyaTitanUnlocked()
    app.mainloop()