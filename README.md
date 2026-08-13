🛡️ Ghost-Aegis: Defensive Suite (Sentinel Edition v2.0)
"Securing endpoints, automating threat intelligence, and defending the digital perimeter."

Ghost-Aegis is a modular, Python-based Endpoint Detection & Response (EDR) and Blue Team defense dashboard built with CustomTkinter. Designed with an uncompromising focus on proactive defense, Ghost-Aegis equips security analysts and system administrators with real-time network visibility, threat intelligence integration, automated neutralization, and system hardening controls.

🚀 Key FeaturesReal-Time Network Sentinel: Sweeps active TCP connections, resolves remote hostnames, performs instant geolocation lookups, and flags suspicious external traffic.

Automated Threat Intelligence (AbuseIPDB Integration): Automatically queries global threat feeds for active remote connections and evaluates abuse confidence scores in real-time.

Automated Neutralization (Auto-Kill): Instantly terminates high-risk processes communicating with malicious infrastructure (Confidence Score $\ge 80\%$).

JIT (Just-In-Time) Administration: Streamlines least-privilege access by granting temporary administrative elevation with scheduled automatic lockdown timelines.

Granular Process Control: Built-in PID killswitch allowing analysts to manually isolate and neutralize rogue processes directly from the dashboard.Modern Cyber-Dark UI: Built using CustomTkinter featuring a sleek, high-contrast command center interface complete with custom severity color-tagging (Trusted, System, Warning, Threat, Auto-Kill).

🛠️ Tech Stack & Dependencies
Language: Python 3.x

GUI Framework: CustomTkinter

System Telemetry: psutil, subprocess, platform, socket

API & Networking: requests

Configuration Security: python-dotenv for secure environment variable management.