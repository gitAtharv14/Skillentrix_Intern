import requests
import time
import os
import sys
import csv
from datetime import datetime

# --- CONFIGURATION ---
API_KEY = 'YOUR_ACTUAL_API_KEY_HERE' 
FILE_NAME = 'logs.txt'
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
REPORT_NAME = f"audit_report_{timestamp}.csv"
HEADERS = {
    "x-apikey": API_KEY,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
}

def init_colors():
    if sys.platform == "win32": os.system('color')
    return '\033[96m', '\033[92m', '\033[91m', '\033[93m', '\033[1m', '\033[0m'

C1, C2, C3, C4, BOLD, END = init_colors()

def check_ip(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=12)
        if response.status_code == 401: return "AUTH_ERROR", 0, "N/A", "N/A"
        if response.status_code == 429: return "RATE_LIMIT", 0, "N/A", "N/A"
        if response.status_code == 404: return f"{C2}CLEAN/NEW{END}", 0, "N/A", "N/A"
        if response.status_code != 200: return f"HTTP_{response.status_code}", 0, "N/A", "N/A"
        
        attr = response.json()['data']['attributes']
        m_count = attr.get('last_analysis_stats', {}).get('malicious', 0)
        country = attr.get('country', 'Unknown')
        isp = attr.get('as_owner', 'Unknown')
        
        if m_count > 5: status = f"{C3}🚨 MALICIOUS{END}"
        elif m_count > 0: status = f"{C4}⚠️  SUSPICIOUS{END}"
        else: status = f"{C2}✅ SAFE{END}"
        
        return status, m_count, country, isp
    except Exception:
        return "CONN_ERROR", 0, "N/A", "N/A"

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{C1}{'='*80}{END}\n{BOLD}    MALICIOUS IP INTELLIGENCE AUDIT{END}\n{C1}{'='*80}{END}")
    
    results = []
    # Professional Directory Management
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # Update the REPORT_NAME to save inside that folder
    full_report_path = os.path.join('reports',REPORT_NAME)
    try:
        with open(FILE_NAME, 'r') as f:
            ips = [line.strip() for line in f if line.strip()]
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Audit Started. Target: {len(ips)} IPs\n")

        for i, ip in enumerate(ips):
            status, flags, country, isp = check_ip(ip)
            results.append({"ip": ip, "status": status, "flags": flags, "country": country, "isp": isp, "time": datetime.now().isoformat()})
            
            print(f" [{i+1}/{len(ips)}] {BOLD}{ip.ljust(15)}{END} | {status} ({flags} flags) | {country} | {isp[:25]}")
            
            if i < len(ips) - 1: time.sleep(8)

 # SAVING THE CORPORATE DELIVERABLE FILE 
        # Use full_report_path instead of REPORT_NAME
        with open(full_report_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["ip", "status", "flags", "country", "isp", "time"])
            writer.writeheader()
            for r in results:
                # Clean ANSI for CSV storage
                r_clean = r.copy()
                r_clean['status'] = r['status'].split(' ')[-1].replace('✅','SAFE').replace('🚨','MALICIOUS').replace('⚠️','SUSPICIOUS')
                writer.writerow(r_clean)

        print(f"\n{C2}{BOLD}✔ Intelligence Exported to: {full_report_path}{END}")

    except KeyboardInterrupt:
        # Also update the emergency save path here
        with open(full_report_path, 'w', newline='') as f:
             writer = csv.DictWriter(f, fieldnames=["ip", "status", "flags", "country", "isp", "time"])
             writer.writeheader()
             for r in results:
                 r_clean = r.copy()
                 r_clean['status'] = r['status'].split(' ')[-1].replace('✅','SAFE').replace('🚨','MALICIOUS').replace('⚠️','SUSPICIOUS')
                 writer.writerow(r_clean)
        print(f"\n{C3}!! USER ABORT DETECTED. Partial data saved to {full_report_path}.{END}")
if __name__ == "__main__":
    main()