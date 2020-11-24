from socket import *
from netifaces import *                                 ## module to get ip address
from sys import *      
from threading import *
from _thread import *


server_status = True                                    ## true for on and restart ans False for server OFF
stop = False                                            ## ON till false ,if stop == true server stops



def servers_state():
    global server_status ,stop
    while True:
        cmd = input()
        if cmd == 'restart':
            server_status =True
        elif cmd == 'stop':
            stop = True
            server_status = False
            break

    


def client_request(client_socket,address):
    print("sending message`")
    global serversocket
    while True:

        message = client_socket.recv(1024)
        message = message.decode()
        print(message)
        print(serversocket)










if __name__ == "__main__":
    #global server_status,stop
    print("wait")
    print(server_status,stop)
    

    client = list()


    addrs = ifaddresses('eth0')                         ## addrs == {17: [{'addr': '00:0c:29:4d:9f:5a', 'broadcast': 'ff:ff:ff:ff:ff:ff'}],
                                                        ##          2: [{'addr': '192.168.211.128', 'netmask': '255.255.255.0', 'broadcast': '192.168.211.255'}],
                                                        ##          10: [{'addr': 'fe80::20c:29ff:fe4d:9f5a%eth0', 'netmask': 'ffff:ffff:ffff:ffff::/64'}]} 
    
    IP = str(addrs[2][0]['addr'])
    serversocket = socket(AF_INET,SOCK_STREAM)
    #print(IP)
    if len(argv) > 1:
        port = int(argv[1])
    else :
        print("Usage : python3 server.py port number")
        exit()
    

    try:
        serversocket.bind(('',port))                      # as bind invoke auditing
    except :
        print("Provide valid port number or change the port number")
        exit()

    serversocket.listen(20)

    print("Connect server on ( " + IP +',' + str(port) + ')' )
    print("Url : http//" + IP +':'+ str(port)+ "   The file name")
   
    start_new_thread(servers_state,())

    while stop == False:
        #print("hello world")
        try:
            clnt_socket, address = serversocket.accept()
            print(clnt_socket,address,'\n\n\n\n')
            #user = clnt_socket.recv(1024)
            #user = str(user.decode())
            #print(user)
            start_new_thread(client_request,(clnt_socket,address))
            
        except error:
            print("not connected")
            
    serversocket.close()






