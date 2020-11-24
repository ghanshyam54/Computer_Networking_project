import socket, sys, requests, threading, time
from time import process_time 

serverName = '127.0.0.1'
serverPort = int(sys.argv[1])

count = 0

  

t1 = process_time()
def handle_connection():
    global count
    count += 1
    r = requests.get(f"http://{serverName}:{serverPort}/logo.jpg")
    #print(f"Response: {r.status_code}, Thread Count: {threading.active_count()}")
    r.close()
    
    
for i in range(5000):
    th = threading.Thread(target=handle_connection)
    th.start()
t2 = process_time()
time.sleep(0.05)
print(count)
print(t2-t1)
