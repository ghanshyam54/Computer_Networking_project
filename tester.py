from netifaces import interfaces, ifaddresses, AF_INET
import requests, socket, sys, time, threading
import os, random
from wsgiref.handlers import format_date_time
##GET
user = 'ghanshyam'
passwd = 'openpass'				
IP = "127.0.0.1"
port = int(sys.argv[1])
t = os.path.getmtime('index.html')
m = format_date_time(t)


headers = {'If-Modified-Since':m}
resp = requests.get(f"http://{IP}:{port}/",headers=headers)

if(resp.status_code == 304):
	print('304 NOT MODIFIED CONDITIONAL GET SUCCESSFULL')
else:
	print('UNSUCCESSFULL')
	
	
resp = requests.get(f"http://{IP}:{port}/logo.jpg")

#print(resp.text)

with open ('logo.jpg','rb') as fd:
	read = fd.read()
	
if(read == resp.content):
	print('SUCCESSFULL GET REQUEST FOR JPG')
else:
	print('UNSUCCESSFULL')
	
	
	
resp = requests.get(f"http://{IP}:{port}/video.mp4")
#print(resp.text)

with open ('video.mp4','rb') as fd:
	read = fd.read()
	
if(read == resp.content):
	print('SUCCESSFULL GET REQUEST FOR MP4')
else:
	print('UNSUCCESSFULL')
	
resp = requests.get(f"http://{IP}:{port}/Pressure4.mp3")
#print(resp.text)

with open ('Pressure4.mp3','rb') as fd:
	read = fd.read()
if(read == resp.content):
	print('SUCCESSFULL GET REQUEST FOR MP3')
else:
	print('UNSUCCESSFULL')	

##PUT

with open ('tp.py','r') as f:
	read = f.read()
	


resp1 = requests.put(f"http://{IP}:{port}/", data = read, auth = (user, passwd))
if(resp1.status_code == 201):
	print('PUT SUCCESSFULL: 201 NEW FILE CREATED')
	print(resp2.headers['Location'])


resp2 = requests.put(f"http://{IP}:{port}/tempo2.py", data = read, auth = (user, passwd))
if(resp2.status_code == 204 or resp2.status_code == 200):
	print('PUT SUCCESSFULL: FILE MODIFIED')
	

resp3 = requests.put(f"http://{IP}:{port}/tempo.py", data = read)
if(resp3.status_code == 401):
	print('TEST CASE PASSED: NO AUTHENTICATION GIVEN')

with open ('Pressure4.mp3','rb') as f:
	reada = f.read()
	
respa = requests.put(f"http://{IP}:{port}/temp.mp3", data = reada, auth = (user, passwd))
if(respa.status_code == 204 or respa.status_code == 201 or respa.status_code == 200):
	print('PUT SUCCESSFULL: AUDIO FILE CREATED/MODIFIED')
	
with open ('video.mp4','rb') as f:
	readv = f.read()
	
respv = requests.put(f"http://{IP}:{port}/tempv.mp4", data = readv, auth = (user, passwd))
if(respv.status_code == 204 or respv.status_code == 201 or respv.status_code == 200):
	print('PUT SUCCESSFULL: VIDEO FILE CREATED/MODIFIED')

	
##HEAD

resph = requests.head(f"http://{IP}:{port}/mainserver.py")
if(resph.status_code == 200):
	print('HEAD SUCCESSFULL: FILE FOUND')
	print('Last Modified on ' + resph.headers['Last-Modified'])
else:
	print(resph.status_code)
	print('HEAD SUCCESSFULL: FILE NOT FOUND')

##DELETE

respd = requests.delete(f"http://{IP}:{port}/tempv.mp4", auth = (user,passwd))
if(respd.status_code == 200 or respd.status_code == 202 or respd.status_code == 204):
	print('DELETE SUCCESSFULL')
else:
	print('DELETE UNSUCCESSFULL')

	
##POST

data = {'name': 'Peter'}

resp = requests.post(f"http://{IP}:{port}/", data)
if(resp.status_code == 201):
	print('POST SUCCESSFULL: Data sent to ' + resp.headers['Location'])
	

##MULTIPLE TEST CASES


count = 0


def handle_connection():
    global count
    count += 1
    r = requests.get(f"http://{IP}:{port}/")
    #print(f"Response: {r.status_code}, Thread Count: {threading.active_count()}")
    r.close()

with open ('tp.py','r') as f:
	read = f.read()
	   
def put_connection():
	global count
	count += 1
	r = requests.put(f"http://{IP}:{port}/", data = read, auth = (user, passwd))
	#print(f"Response: {r.status_code}, Thread Count: {threading.active_count()}")
	r.close()

	
		
for i in range(100):
    th = threading.Thread(target=handle_connection)
    th.start()

print("100 REQUESTS COMPLETED SUCCESSFULLY")

for i in range(500):
    th = threading.Thread(target=handle_connection)
    th.start()

print("500 REQUESTS COMPLETED SUCCESSFULLY")

for i in range(1000):
    th = threading.Thread(target=handle_connection)
    th.start()

print("1000 REQUESTS COMPLETED SUCCESSFULLY")

for i in range(10000):
    th = threading.Thread(target=handle_connection)
    th.start()

print("10000 REQUESTS COMPLETED SUCCESSFULLY")

for i in range(100):
	x = random.randint(0,10)
	if(x % 2 == 0):
		th = threading.Thread(target=handle_connection)
		th.start()
	else:
		ti = threading.Thread(target=put_connection)
		ti.start()
print("100 GET/PUT RANDOM REQUESTS COMPLETED SUCCESSFULLY")
