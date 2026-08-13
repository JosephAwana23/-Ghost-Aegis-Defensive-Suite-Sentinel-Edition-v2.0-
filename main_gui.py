import os
from dotenv import load_dotenv

# This tells Python to find your hidden .env file and load the secrets into memory
load_dotenv()

import customtkinter as ctk
import subprocess
import threading
import sys
import platform
import psutil  
import socket  
import requests
from datetime import datetime, timedelta

# Note: Ensure your 'main.py' (jit_engine) is in the same folder.
# A direct `import main` can fail in some IDEs or when the script is run
# from a different working directory, so we load it explicitly from this file's folder.
try:
    import importlib.util
    from pathlib import Path

    _main_path = Path(__file__).resolve().with_name("main.py")
    if _main_path.exists():
        spec = importlib.util.spec_from_file_location("jit_engine_main", _main_path)
        if spec and spec.loader:
            jit_engine = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(jit_engine)
        else:
            jit_engine = None
    else:
        jit_engine = None
except Exception:
    jit_engine = None

# --- GLOBAL CONFIG ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GhostAegisApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. INITIAL STATE ---
        self.radar_enabled = False
        self.title("Ghost-Aegis | Defensive Suite")
        self.geometry("950x850") 

        # --- 2. BUILD THE UI CONTAINERS ---
        self.label = ctk.CTkLabel(self, text="GHOST-AEGIS", font=("Fixedsys", 32, "bold"), text_color="#00FF00")
        self.label.pack(pady=15)

        self.status_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.status_frame.pack(pady=10, padx=20, fill="x")
        self.status_label = ctk.CTkLabel(self.status_frame, text="🛡️ SYSTEM HARDENED", text_color="green", font=("Consolas", 14))
        self.status_label.pack(pady=5)

        self.button_container = ctk.CTkFrame(self, fg_color="transparent")
        self.button_container.pack(pady=10, fill="both", expand=True)

        self.left_frame = ctk.CTkFrame(self.button_container)
        self.left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        ctk.CTkLabel(self.left_frame, text="ACCESS CONTROL", font=("Arial", 12, "bold"), text_color="#3b8ed0").pack(pady=10)

        self.right_frame = ctk.CTkFrame(self.button_container)
        self.right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)
        ctk.CTkLabel(self.right_frame, text="SYSTEM DEFENSE", font=("Arial", 12, "bold"), text_color="#3b8ed0").pack(pady=10)

        # --- 3. ADD BUTTONS (Left Column) ---
        self.jit_button = ctk.CTkButton(self.left_frame, text="JIT Admin (15m)", command=self.run_jit)
        self.jit_button.pack(pady=10, padx=20)
        
        self.audit_button = ctk.CTkButton(self.left_frame, text="Audit Admins", command=self.run_audit)
        self.audit_button.pack(pady=10, padx=20)
        
        self.info_button = ctk.CTkButton(self.left_frame, text="System Info", command=self.show_sys_info)
        self.info_button.pack(pady=10, padx=20)

        self.about_button = ctk.CTkButton(
            self.left_frame, 
            text="About Ghost-Aegis", 
            fg_color="gray", 
            hover_color="#333333", 
            command=self.show_about_window
        )
        self.about_button.pack(pady=10, padx=20)

        # --- 4. ADD BUTTONS (Right Column) ---
        self.stealth_button = ctk.CTkButton(self.right_frame, text="Stealth Mode", fg_color="purple", hover_color="#5a2d82", command=self.run_stealth)
        self.stealth_button.pack(pady=10, padx=20)
        
        self.clean_button = ctk.CTkButton(self.right_frame, text="Emergency Clean", fg_color="#880808", hover_color="#660000", command=self.run_cleanup)
        self.clean_button.pack(pady=10, padx=20)

        self.sentinel_button = ctk.CTkButton(self.right_frame, text="Network Sentinel", fg_color="#1f538d", command=self.network_sentinel_callback)
        self.sentinel_button.pack(pady=10, padx=20)

        self.radar_button = ctk.CTkButton(self.right_frame, text="Start Radar", fg_color="#1f538d", hover_color="#14375e", command=self.toggle_radar)
        self.radar_button.pack(pady=10, padx=20)

        # --- NEW: KILLSWITCH UI ---
        self.kill_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.kill_frame.pack(pady=15, padx=20)
        
        self.pid_entry = ctk.CTkEntry(self.kill_frame, placeholder_text="Enter PID...", width=100)
        self.pid_entry.pack(side="left", padx=(0, 5))
        
        self.kill_button = ctk.CTkButton(self.kill_frame, text="Kill PID", fg_color="#880808", hover_color="#660000", width=80, command=self.terminate_process_callback)
        self.kill_button.pack(side="left")

        # --- 5. CONSOLE SECTION ---
        self.console = ctk.CTkTextbox(self, height=400, width=900, font=("Consolas", 12), fg_color="#000000", text_color="#00FF00")
        self.console.pack(pady=20, padx=20)
        
        # Clean & Sleek Dark-Mode Color Tags
        self.console.tag_config("threat", foreground="#FF3333")   # Neon Red
        self.console.tag_config("warn", foreground="#FF7518")     # Safety Orange
        self.console.tag_config("trusted", foreground="#00FF00")  # Matrix Green
        self.console.tag_config("system", foreground="#00E5FF")   # Cyber Cyan
        self.console.tag_config("review", foreground="#FFBF00")   # Crisp Amber
        
        self.log_event("Ghost-Aegis System Ready. Monitoring active.", "trusted")

    # --- THE ABOUT WINDOW LOGIC ---
    def show_about_window(self):
        about_win = ctk.CTkToplevel(self)
        about_win.title("About Ghost-Aegis")
        about_win.geometry("420x480")
        about_win.attributes("-topmost", True)

        ctk.CTkLabel(about_win, text="GHOST-AEGIS", font=("Fixedsys", 28, "bold"), text_color="#00FF00").pack(pady=20)
        ctk.CTkLabel(about_win, text="Version 1.0.0 | 'Sentinel Edition'", font=("Arial", 10, "italic")).pack()

        mission_text = (
            "Goal: To Save the World through Internet Safety.\n\n"
            "Ghost-Aegis is a defensive suite designed for Blue Team "
            "practitioners. It provides real-time network visibility, "
            "geolocation intelligence, and automated system hardening."
        )
        
        mission_box = ctk.CTkTextbox(about_win, width=380, height=130, font=("Arial", 12))
        mission_box.insert("0.0", mission_text)
        mission_box.configure(state="disabled", fg_color="#2b2b2b")
        mission_box.pack(pady=20, padx=20)

        ctk.CTkLabel(about_win, text="Project Lead:", font=("Arial", 12, "bold"), text_color="#3b8ed0").pack()
        ctk.CTkLabel(about_win, text='[H "Joseph Awana"A / Gemini]', font=("Consolas", 16)).pack(pady=5)
        
        ctk.CTkLabel(about_win, text="Built with Python, CustomTkinter, and Psutil", font=("Arial", 9)).pack(pady=(15, 0))
        ctk.CTkButton(about_win, text="CLOSE", fg_color="#444444", command=about_win.destroy).pack(pady=20)

    # --- LOGGING ENGINE ---
    def log_event(self, message, tag=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        try:
            with open("ghost_aegis.log", "a") as f:
                f.write(log_entry)
        except: pass
        
        self.console.configure(state="normal")
        if tag:
            self.console.insert("end", log_entry, tag)
        else:
            self.console.insert("end", log_entry)
        self.console.configure(state="disabled")
        self.console.see("end")

    # --- SYSTEM LOGIC ---
    def run_jit(self):
        dialog = ctk.CTkInputDialog(text="Enter username to elevate:", title="JIT Elevation")
        target_user = dialog.get_input()
        if target_user:
            try:
                subprocess.run(["net", "localgroup", "Administrators", target_user, "/add"], check=True)
                self.log_event(f"JIT Elevation SUCCESS: {target_user} granted Admin.", "trusted")
                exec_time = (datetime.now() + timedelta(minutes=15)).strftime("%H:%M")
                self.log_event(f"Lockdown scheduled for {exec_time}.", "review")
            except Exception as e:
                self.log_event(f"JIT Error: {e}", "threat")

    def run_audit(self):
        self.log_event("Auditing Admin group...", "review")
        try:
            result = subprocess.run(["net", "localgroup", "Administrators"], capture_output=True, text=True, check=True)
            self.log_event(result.stdout)
        except Exception as e:
            self.log_event(f"Audit failed: {e}", "threat")

    def show_sys_info(self):
        try:
            cmd = "Get-CimInstance Win32_OperatingSystem | Select-Object -ExpandProperty Caption"
            os_name = subprocess.check_output(["powershell", "-Command", cmd], text=True).strip()
            self.log_event(f"SYSTEM INFO: {os_name} | NODE: {platform.node()}", "system")
        except:
            self.log_event(f"SYSTEM INFO: Windows | NODE: {platform.node()}", "system")

    def run_stealth(self):
        self.log_event("STEALTH MODE ACTIVE", "warn")

    def run_cleanup(self):
        self.log_event("! INITIATING CLEANUP PROTOCOL !", "threat")

    # --- THREAT INTELLIGENCE ENGINE ---
    def check_ip_reputation(self, ip_address):
        """Queries AbuseIPDB. Returns the abuse confidence score (0-100)."""
        url = 'https://api.abuseipdb.com/api/v2/check'
        
        # Safely pull the key from the hidden environment file!
        api_key = os.getenv('ABUSEIPDB_API_KEY')
        
        headers = {
            'Accept': 'application/json',
            'Key': api_key 
        }
        querystring = {'ipAddress': ip_address, 'maxAgeInDays': '30'}

        try:
            # Short timeout so it doesn't freeze the GUI for too long
            response = requests.get(url, headers=headers, params=querystring, timeout=3.0)
            if response.status_code == 200:
                data = response.json()
                return data['data']['abuseConfidenceScore']
        except Exception as e:
            pass # Fail silently so the radar doesn't crash on network errors
        return 0

    def get_ip_location(self, ip):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=1.5).json()
            if response.get("status") == "success":
                return f"{response.get('city')}, {response.get('countryCode')}"
            return "Unknown Loc"
        except: return "Loc Error"

    def network_sentinel_callback(self):
        self.log_event("[*] Initiating Deep Network Audit...", "system")
        trusted_domains = ['google.com', 'github.com', 'microsoft.com', 'akamai', 'azure']
        
        try:
            result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, check=True)
            lines = result.stdout.splitlines()
            self.log_event(f"{'STATUS':<10} {'PROCESS':<15} {'REMOTE HOST / LOCATION':<45} {'PID':<6}")
            
            found_active = False
            for line in lines:
                parts = line.split()
                if len(parts) >= 5 and "ESTABLISHED" in parts:
                    ip_only = parts[2].rsplit(':', 1)[0].replace('[', '').replace(']', '')
                    pid_str = parts[-1]
                    
                    if pid_str.isdigit():
                        pid = int(pid_str)
                    else:
                        continue
                    
                    if ip_only not in ["127.0.0.1", "0.0.0.0", "::1"]:
                        try:
                            proc_name = psutil.Process(pid).name()
                        except:
                            proc_name = "Unknown"

                        location = self.get_ip_location(ip_only)
                        
                        try: 
                            hostname = socket.getfqdn(ip_only)
                        except: 
                            hostname = ip_only
                        
                        display_host = f"{hostname} ({location})"
                        
                        # --- INTELLIGENCE & AUTOMATED NEUTRALIZATION ROUTING ---
                        status, tag_name = "[REVIEW]", "review"
                        
                        if any(d in hostname.lower() for d in trusted_domains):
                            status, tag_name = "[TRUSTED]", "trusted"
                        elif proc_name.lower() in ["svchost.exe", "lsass.exe"]:
                            status, tag_name = "[SYSTEM]", "system"
                        else:
                            # Query AbuseIPDB for reputation
                            score = self.check_ip_reputation(ip_only)
                            
                            # CRITICAL THREAT: Automatic Intervention Threshold (Score >= 80%)
                            if score >= 80:
                                status, tag_name = "[AUTO-KILL]", "threat"
                                display_host = f"{display_host} | SCORE: {score}% - TERMINATING PROCESS"
                                
                                # Execute Automated Neutralization
                                try:
                                    target_proc = psutil.Process(pid)
                                    killed_name = target_proc.name()
                                    target_proc.terminate()
                                    
                                    self.log_event(
                                        f"⚡ [NEUTRALIZED] High Threat Detected ({score}% Abuse Score). "
                                        f"Killed {killed_name} (PID: {pid}) communicating with {ip_only}!", 
                                        "threat"
                                    )
                                except Exception as kill_err:
                                    self.log_event(f"⚠️ [KILL FAILED] Could not terminate PID {pid}: {kill_err}", "threat")
                            
                            # SUSPICIOUS THREAT: Warning Level (Score 25% - 79%)
                            elif score >= 25:
                                status, tag_name = "[THREAT]", "threat"
                                display_host = f"{display_host} | SCORE: {score}%"
                            elif score > 0:
                                status, tag_name = "[WARN]", "warn"
                                display_host = f"{display_host} | SCORE: {score}%"
                        
                        self.log_event(f"{status:<10} {proc_name:<15} {display_host:<45} {pid:<6}", tag=tag_name)
                        found_active = True

            if not found_active: self.log_event("No active external connections.")
        except Exception as e: self.log_event(f"Audit Failed: {e}", "threat")

        if self.radar_enabled:
            # Schedule next sweep
            self.after(30000, self.network_sentinel_callback)

    def toggle_radar(self):
        self.radar_enabled = not self.radar_enabled
        if self.radar_enabled:
            self.radar_button.configure(text="Stop Radar", fg_color="#e67e22")
            self.log_event("[!] RADAR ENABLED: Sweeping every 30s...", "warn")
            self.network_sentinel_callback()
        else:
            self.radar_button.configure(text="Start Radar", fg_color="#1f538d")
            self.log_event("[!] RADAR DISABLED.", "review")

    def terminate_process_callback(self):
        pid_str = self.pid_entry.get().strip()
        if pid_str.isdigit():
            try:
                p = psutil.Process(int(pid_str))
                process_name = p.name()
                p.terminate()
                self.log_event(f"[X] Terminated {process_name} (PID: {pid_str}) successfully.", "threat")
                self.pid_entry.delete(0, 'end') # Clear the entry box after killing
            except Exception as e: 
                self.log_event(f"Kill Error: {e}", "threat")
        else:
            self.log_event("Invalid PID entered.", "warn")

if __name__ == "__main__":
    app = GhostAegisApp()
    app.mainloop()