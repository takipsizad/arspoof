import subprocess
import ctypes, sys
def fixsheningangs():
    print("xd")
    subprocess.Popen(["powershell.exe" ,"-c", "netsh winsock reset"])
    subprocess.Popen(["powershell.exe" ,"-c", "netsh int ip reset"])
    subprocess.Popen(["powershell.exe" ,"-c", " ipconfig /release"])
    subprocess.Popen(["powershell.exe" ,"-c", "ipconfig /renew"])
    subprocess.Popen(["powershell.exe" ,"-c", "ipconfig /flushdns"])

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    fixsheningangs()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
