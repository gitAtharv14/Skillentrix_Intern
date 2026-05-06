# Skillentrix_Intern
Major Project - IP Intelligence Utility.


# 🛠️ What is this?
I built this tool for my 4th-semester Major Project to help automate the way we check network logs for threats. Instead of manually checking every IP, this script pulls data from VirusTotal to tell us where an IP is from, who owns it, and if it's dangerous.

# 🚀 How to Run (Windows vs. Kali Linux) :

I designed this script to be "plug-and-play" on both systems. Here is how I set it up:

**For Windows (My Development Environment)**
1. Python Check: Make sure you have Python installed. You can check by typing `python --version` in your Command Prompt.
2. Install Library: Open your terminal and type:
   `pip install requests`
3. Run it: Go to your project folder and type:
   `python ip_intel.py`

**For Kali Linux (Testing Environment)**
1. Update Python: Kali usually has Python, but ensure the library is there by typing:
   `pip3 install requests`
2. Permissions: If the script doesn't run, you might need to give it permission:
   `chmod +x ip_intel.py`
3. Run it: Type:
   `python3 ip_intel.py`

## 📂 Where are the results?
I added a feature that automatically creates a folder called `reports/`. 
* Every time you run a scan, a new CSV file is saved there with a timestamp.
* Even if you stop the script halfway (Ctrl+C), it will still save whatever it found up to that point so no data is lost.

##SECURITY :
I’ve removed my actual API key from the script for the final submission to follow security best practices. To run the tool, just sign up for a free account at VirusTotal and paste your key into the API_KEY variable at the top of the script.

## 📝 A Small Note :
I'm using a free-tier API key, so I programmed a 08-second delay between IPs to make sure the service doesn't block us. Also, for security reasons, make sure your `logs.txt` file is in the same folder as the script before starting.

---
**Atharv Toraskar** 
