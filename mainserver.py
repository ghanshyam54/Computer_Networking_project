from socket import *
from netifaces import *                                 ## module to get ip address
from sys import *      
from threading import *
from _thread import *
import os
import time
from urllib.parse import *
from collections import defaultdict 
import gzip
#import tp
import random
import json
import datetime
import time
from wsgiref.handlers import format_date_time           ## to get the time in server format
import logging                                          ## to store the server axcess logs
import base64
from configparser import ConfigParser
from http import cookies

config_object = ConfigParser()
config_object.read("config.ini")
userinfo = config_object["USERINFO"]
serverinfo = config_object["SERVERCONFIG"]
#print(type(serverinfo["urllen"]))
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

f_handler = logging.FileHandler('Access.log')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
#logger.info('Im ghanshyam')


#errlogger = logging.getLogger(__name__)
#errlogger.setLevel(logging.ERROR)
#c_handler = logging.FileHandler('Error.log')
#c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#c_handler.setFormatter(c_format)
#errlogger.addHandler(c_handler)
       
        



class server():
    maxurl = 300
    def __init__(self,ip,port,serversocket):
        self.server_status = True                                    ## true for on and restart ans False for server OFF
        self.stop = False                                            ## ON till false ,if stop == true server stops
        self.close = False
        self.serversocket = serversocket
        self.IP = ip
        self.port = port
        self.state = True
        self.clients = []
        self.path = serverinfo["ROOT"]
        self.maxurllen = int(serverinfo["urllen"])
        self.size = int(serverinfo["chunk_size"])  
        self.__username = userinfo["username"]
        self.__password = userinfo["password"]
        


    def servers_state(self):
        while True:
            cmd = input()
            if cmd == 'stop':
                self.stop = True
            elif cmd == 'start':
                self.stop = False
            elif cmd == 'close':
                self.close = True
                self.stop = True
                exit()


    
    def start(self):
        while self.close == False:
            while self.stop == False:
                try:
                    clnt_socket, address = self.serversocket.accept()
                    self.clients.append(clnt_socket)
                    start_new_thread(self.client_request,(clnt_socket,address))
            
                except :
                    #errlogger.error(f"{E}")

                    print("Server Stop")
                    break;


    def status_code(self,clnt_socket,code,request_line,address,lst_modified=None,location = None):
        type_ = 1
        message  = ""
        length = 0
        #message  +="HTTP/1.1 404 Not Found\r\n"
        if code == 200:
            message  +="HTTP/1.1 200 OK\r\n"
            data = "<!DOCTYPE html><html><head><title>200</title></head><body><h1>Standard response for successful HTTP requests. </h1></body></html>"
            length = len(data)
        elif code == 201:
            message += "HTTP/1.1 201 Created\r\n"
            ## Location: http://www.w3.org/pub/WWW/People.html
            message += location + "\r\n"
            data = "<!DOCTYPE html><html><head><title>201</title></head><body><h1>201 Created new resource</h1></body></html>"
 
            length = len(data)


        elif code == 202:
            message  +="HTTP/1.1 202 Accepted\r\n"

            data = "<!DOCTYPE html><html><head></head><body><h1>202 Request is accepted for Processing</h1></body></html>"
            length = len(data)

            
        ##"NO message to be included for 202 and 304"
        elif code == 204:
            message  +="HTTP/1.1 204  No Content\r\n"
            type_ = 2

        elif code == 414:
            message  +="HTTP/1.1 " + str(code) + "Request-URI Too Long\r\n"
            data = "<!DOCTYPE html><html><head><title>"+str(code)+ "</title></head><body><h1>Request-URI Too Long</h1></body></html>"
            length = len(data)

        elif code == 411:
            message  +="HTTP/1.1 411 Length Required\r\n"
            data = "<!DOCTYPE html><html><head><title>411</title></head><body><h1>Length Required</h1><p>The request did not specify the length of its content, which is required by the requested resource</p></body></html>"
            length = len(data)


        elif code == 406:
            message  +="HTTP/1.1 " +str(code)+ " Not Acceptable\r\n"
            data = "<!DOCTYPE html><html><head><title>"+str(code)+ "</title></head><body><h1>Not Acceptable\/h1></body></html>"
            length = len(data)

                            ##accept enc therre server cant fulfil acc to accept-encoding header 
        elif code == 405:
            message  +="HTTP/1.1 " +str(code)+  " Method not allow\r\n"        ## refer to allow
            data = "<!DOCTYPE html><html><head><title>"+str(code)+ "</title></head><body><h1>Method not allow\/h1></body></html>"
            length = len(data)
            message += "Alow: GET, HEAD, POST, PUT,DELETE"
      
        elif code == 404:
            message  +="HTTP/1.1 "+str(code)+" Not Found\r\n"
            data = "<!DOCTYPE html><html><head><title>"+str(code)+ "</title></head><body><h1>404 Not Found</h1></body></html>"
            length = len(data)

        elif code == 403:
            message  +="HTTP/1.1 " +str(code)+ " Forbidden\r\n"
            data = "<!DOCTYPE html><html><head><title>"+str(code)+ "</title></head><body><h1>403 Forbidden</h1></body></html>"
            length = len(data)
        
        elif code == 401:
            message += 'HTTP/1.1 401 Unauthorized \r\n'
            message += 'WWW-Authenticate: Basic\r\n'
            data = "<!DOCTYPE html><html><head><title>401 Unauthorise</title></head><body><h1>401 UNAUTHORISE</h1></body></html>"

        elif code == 400:
            message  +="HTTP/1.1 400 Bad Request\r\n"
            data = "<!DOCTYPE html><html><head><title>400 Bad Request</title></head><body><h1>400 Bad Request</h><br> <p>the server cannot or will not process the request </p></body></html>"
            length = len(data)
        elif code == 501:
            message  +="HTTP/1.1 501 Not Implemented\r\n"
            data = "<!DOCTYPE html><html><head><title>501 Not Implemented</title></head><body><h1>400 Bad Request</h><br> <p>the server cannot or will not process the request </p></body></html>"
            length = len(data)
        


        elif code == 505:
            message += "Support Version - HTTP/1.1 \n Rest Unsupported\r\n"
            type_ = 2

        elif code == 304:
            message += "HTTP/1.1 304 Not Modified\r\n"
            message += "Date: " + format_date_time(time.time()) + "\r\n"
            message += "Last-Modified:" + lst_modified + "\r\n"
            type_ = 2

        t =time.ctime().split(" ")
        m  = t[0] + ", " + t[2] + " " + t[1] + " " + t[4] + " " +t[3]+ " " + "GMT\r\n"
                   
        message += "Server AG/1.1  \r\n"
        message += "Date: "  + m
        if type_ == 1:
            #message += "Cache-Control: no-cache, max-age=3600 \r\n"
            message += "Content-Type: text/html\r\n"
            message += "Content-Length: " + str(length) + "\r\n"
            message += "Connection: Closed\r\n\r\n"

            message += data
        #print(message)
        message = message.encode()
        clnt_socket.send(message)
        clnt_socket.close()
        

        logger.info(f"{address[0]} {address[1]} {request_line} {code} {length}")
        if int(code) >=  400:
            with open('Error.log',"a+") as fd:
                fd.write(f"{time.ctime()} - {address[0]} - {address[1]}  - {request_line} -  {code}\n")



        



    def get_ext_or_type(self, ext_type,indication):


        file_type = {'.txt':'text/plain', '.html':'text/html', '.png':'image/png','.jpg':'image/jpg', '.ico': 'image/x-icon',  '.gif': 'image/gif', '.php':'application/x-www-form-urlencoded', '': 'text/plain', '.jpeg':'image/webp', '.pdf': 'application/pdf', '.js': 'application/javascript', '.css': 'text/css', '.mp3' : 'audio/mpeg'}

        
        
        file_ext = {'text/html': '.html','text/plain': '.txt', 'image/png': '.png', 'image/gif': '.gif', 'image/jpg': '.jpg','image/x-icon':'.ico', 'image/webp': '.jpeg', 'application/x-www-form-urlencoded':'.json', 'image/jpeg': '.jpeg', 'application/pdf': '.pdf', 'audio/mpeg': '.mp3', 'video/mp4': '.mp4'}
        
        ## get file type from the extention
        if indication == "type":
            try:
                message = ext_type.split('/')
                type_  = message[-1].split('.')[-1]
                return file_type['.' + type_]
            except :
                return ''

        ## Use in put and post request
        ## from type provides the file extension
        elif indication == "ext":
            try :
                ext = file_ext[ext_type]
                return ext
            except :
                return ''





    def post_req(self,h_lines,file_loc,client,file_content,byte_format,address,request_line):
        file_json = self.path + "POST_DATA.json"
        if h_lines['Content-Length'] == '': 
            self.status_code(client,411,reqest_line,address)
            return

        while len(file_content) < int(h_lines['Content-Length']):
            if not byte_format :
                file_content += client.recv(self.size).decode()
            else:
                file_content += client.recv(self.size)
        
        
        if h_lines['Content-Type'] == 'application/x-www-form-urlencoded': 
            x = datetime.datetime.now()
            date = x.strftime("%c")
            filedata={}
            filedata["address :"] = address
            filedata["Date :"] = date
            filedata["Data :"] = file_content
            if os.path.exists(file_json):
                with open("POST_DATA.json","a+") as fd:
                    json.dump(filedata, fd)
                    self.status_code(client,200,request_line,address)                                                                                 # no new file created 
                    fd.close()
            else:
                with open("POST_DATA.json","a+") as fd:
                    json.dump(filedata,fd)
                location = "Location: http://" + self.IP + ":"+ str(self.port) + "/POST_DATA.json"  

                self .status_code(client,201,request_line,address,None,location)
                fd.close()
        else:
            base_name = "Post"
            x = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
            base_name += x
            extension = self.get_ext_or_type(h_lines["Content-Type"],"ext")               
            if extension != "":
                
                x = base_name + extension 
                base_name = self.path +file_loc +base_name   +extension
                
                if isinstance(file_content,str):

                    with open(base_name,'w+') as fp:
                        fp.write(file_content)
                        size = os.path.getsize(base_name)
                else:
                    with open(base_name,'wb+') as fp:
                        fp.write(file_content)
                        size = os.path.getsize(base_name)
                fp.close()
                location = "Location: http://" + self.IP + ":"+ str(self.port) + file_loc+x  

                self .status_code(client,201,request_line,address,None,location)
 
            else :
                self.status_code(client,403,request_line,address)
                return


            x = datetime.datetime.now()
            date = x.strftime("%c")
            filedata={}
            filedata["address :"] = address
            filedata["Date :"] = date
            filedata["file_name :"] = base_name
            if os.path.exists(file_json):
                with open("POST_DATA.json","a+") as fd:
                    json.dump(filedata, fd)
                    fd.close()
            else:
                with open("POST_DATA.json","a+") as fd:
                    json.dump(filedata,fd)
                    fd.close()










    def make_and_check_dir(self,path):
        if not  os.path.exists(path):
            x = path.split('.')
            if len(x) > 1:
                loc = x[0].split('/')
                loc =  '/'.join(loc[:-1])
                if not os.path.exists(loc):
                    os.makedirs(loc)
                return False
            else:
                os.makedirs(path)
                return True
    







    def put_req(self,h_lines,file_loc,client,file_content,byte_format,address,request_line):
        if h_lines['Authorization'] != '':
            authorization = h_lines['Authorization'].split(" ")

            authorization =authorization[1].encode("ascii")
            base64_byte = base64.b64decode(authorization)
            authorization = base64_byte.decode("ascii")
            author = authorization.split(':')
            if self.__username == author[0] and self.__password == author[1]:
                pass
            else :
                self.status_code(client,401,request_line,address)
                return
        else :
            self.status_code(client,401,request_line,address)
            return





        if h_lines['Content-Length'] == '' :
            self.status_code(client_socket,411,request_line,address)
            return

        while len(file_content) < int(h_lines['Content-Length']):
            if not byte_format :
                file_content += client.recv(self.size).decode()
            else:
                file_content += client.recv(self.size)
            
        file_name = file_loc   
        file_loc = self.path + file_loc
        if os.path.exists(file_loc):
            if os.path.isfile(file_loc):
                if os.access(file_loc,os.W_OK):
                    if isinstance(file_content,str):

                         with open(file_loc,'w') as fp:
                            fp.write(file_content)
                            size = os.path.getsize(file_loc)
                    else:
                        with open(file_loc,'wb') as fp:
                            fp.write(file_content)
                            size = os.path.getsize(file_loc)
                    
                    fp.close()
                    self.status_code(client,204,request_line,address)


                else:
                    self.status_code(client,403,request_line,address)
                    return


            elif os.path.isdir(file_loc):
                base_name = "Put"
                x = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                base_name += x
                extension = self.get_ext_or_type(h_lines["Content-Type"],"ext")
                
                print(extension)
                if extension != "":
                    base_name +=  extension
                    if isinstance(file_content,str):

                        with open(file_loc + base_name,'w') as fp:
                            fp.write(file_content)
                            size = os.path.getsize(file_loc)
                    else:
                        with open(file_loc + base_name,'wb') as fp:
                            fp.write(file_content)
                            size = os.path.getsize(file_loc)


                    fp.close()
                    location = "Location: http://" + self.IP + ":"+ str(self.port) +'/'+ base_name 
                    self .status_code(client,201,request_line,address,None,location)
 
                        
                else:
                    self.status_code(client,403,request_line,address)

                    print("Extension not available")


            
        else:

            is_dir = self.make_and_check_dir(file_loc)
            if not is_dir :                                                                                                 ##not a dir so it is file to be created
                if isinstance(file_content,str):

                    with open(file_loc,'w') as fp:
                        fp.write(file_content)
                        size = os.path.getsize(file_loc)
                else:
                    with open(file_loc,'wb') as fp:
                        fp.write(file_content)
                        size = os.path.getsize(file_loc)
                fp.close()
                location = "Location: http://" + self.IP + ":"+ str(self.port) + '/'+file_name 
                self .status_code(client,201,request_line,address,None,location)
 
            else:
                base_name = "Put"
                x = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                base_name += x
                extension = self.get_ext_or_type(h_lines["Content-Type"],"ext")               
                print(extension)
                if extension != "":
                    base_name +=  extension
                    if isinstance(file_content,str):

                        with open(file_loc + base_name,'w') as fp:
                            fp.write(file_content)
                            size = os.path.getsize(file_loc)
                    else:
                        with open(file_loc + base_name,'wb') as fp:
                            fp.write(file_content)
                            size = os.path.getsize(file_loc)
                    fp.close()
                    location = "Location: http://" + self.IP + ":"+ str(self.port) + '/'+base_name 
                    self .status_code(client,201,request_line,address,None,location)
 

                else :
                    self.status_code(client,403,request_line,address)



        
    def delete_req(self,h_lines,file_loc,client,request_line,address):
        if h_lines['Authorization'] != '':
            authorization = h_lines['Authorization'].split(" ")

            authorization =authorization[1].encode("ascii")
            base64_byte = base64.b64decode(authorization)
            authorization = base64_byte.decode("ascii")
            author = authorization.split(':')
            if self.__username == author[0] and self.__password == author[1]:
                pass
            else :
                self.status_code(client,401,request_line,address)
                return
        else :
            self.status_code(client,401,request_line,address)
            return

        

        file_name = file_loc
        message = ""
        del_file_loc = self.path + "/delete"
        file_loc = self.path + file_loc
        if not os.path.exists(file_loc):
            self.status_code(client,404,request_line,address)
            return
        if not os.path.exists(del_file_loc):
            os.mkdir(del_file_loc)

        if os.path.isfile(file_loc):
            decision = 1
            if os.access(file_loc,os.R_OK & os.W_OK):
                try:
                    os.replace(file_loc,del_file_loc + file_name)
                    print("Replace")
                except:
                    os.remove(file_loc)
                    print("REmove")

                finally:
                    print("finally")
                    x = random.randint(1,124234)
                    if x %6 == 0:
                        decision = 0
                        ## 202 code for action is not perform but sure will occure
                        self.status_code(client,202,request_line,address)
                    else:
                        if x%2:
                            self.status_code(client,200,request_line,address)
                        elif decision:
                            self.status_code(client,204,request_line,address)
            else:
                self.status_code(client,403,request_line,address)

        else:
            self.status_code(client,400,request_line,address)




            
    def GET_req(self,request,lines,file_loc,client,request_line,address):
        file_data = file_loc.split('?')                                         ####if in get  request data is return 
        file_loc = file_data[0]

        ## data through the form is send 
        if len(file_data) >1:
            temp = file_data[1].split('&')
            file_data = {}
            for data in temp:
                data = data.split("=")
                file_data[data[0]] = " ".join(data[1].split('+'))
            
        else:
            file_data = None
        

        message = ""
        is_file = False
        is_dir = False
        filename = self.path +file_loc


        if len(file_loc) > self.maxurllen:
            self.status_code(client,414,request_line,address)
            client.close()
            return

        if file_loc == '/' and file_data == None:                       ##if the data send from the get request is then it will work
            is_file = True
            filename =  self.path + '/index.html'
        elif file_loc == '/favicon.ico':
            is_file= True
            filename = self.path + '/logo.jpg'
        
        elif os.path.isdir(filename):
            is_dir = True
            if file_data :
                with open("GET_DATA.json","a+") as fd:
                    json.dump(file_data, fd)
                    fd.close()
                    return
            data = "\n\n"           
            files = os.listdir(filename)
            for f in files:
                link = "http://"+ str(self.IP) +":" +str(self.port) + file_loc + '/' + f 
                data += "<a href=" +link + ">" + link + "</a><br>"
            temp_data =  bytes("<!DOCTYPE html><html><head><title>content of dir</title></head><body><h1>CONTENT of DIR \n\n<br>" + data +  "\n\n</h1></body></html>",'utf-8')
            size = len(temp_data)

        elif os.path.isfile(filename):
            is_file = True
        else :
            self.status_code(client,404,request_line,address)
            return
        if is_file:
            if os.access(filename,os.R_OK):
                with open(filename,'rb') as fp:
                    temp_data = fp.read()
                    size = os.path.getsize(filename)
                    fp.close()
            else:
                self.status_code(client,403,request_line,address)
                return
 
        if 'gzip' in lines['Accept-Encoding']:
            c_encode = 1
            temp_data = gzip.compress(temp_data)
        else :
            c_encode = 0



        message += "HTTP/1.1 200 OK\r\n"
        t =time.time()
        message += "Date: "  + format_date_time(t) + "\r\n"           
        message += "Server: Ghanshyam_Atharva/1.1\r\n"        
        if is_file:
            t = os.path.getmtime(filename)
            m = format_date_time(t)

            if lines['If-Modified-Since'] == m :
                self.status_code(client,304,address,request_line,m,address)
                return
            else:
                message += "Last-Modified: " + m + '\r\n'         
        message += "Accept-Ranges: bytes\r\n"
        message += "Content-Length: " + str(size) + "\r\n"
        message += "Content-Type: "+ self.get_ext_or_type(file_loc,"type") +"; charset=ISO-8859-4\r\n"
        ## tells weather the client may cache or not
        message += "Cache-Control: max-age=3600\r\n"
        if c_encode == 1:
            message += "Content-Encoding: gzip\r\n"
        else:
            message += "Vary: Accept-Encoding\r\n"
        if lines['Cookie'] == "":
            expiration = datetime.datetime.now() + datetime.timedelta(days=1)
            message += "Set-Cookie: session=" + serverinfo["cookie"] + "; expires=" + expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")+"; version=1\r\n"
            serverinfo["cookie"] =str(int(serverinfo["cookie"]) + 1)
            with open("cookie.log",'a+') as fd:
                fd.write(f'{address[0]} - {address[1]} - {serverinfo["cookie"]} - {expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")} - 1 \n')
                fd.close()
            with open('config.ini','w') as congf:
                config_object.write(congf)
                congf.close()
        message += "Connection: Closed\r\n\r\n"
        message = message.encode()
        message += temp_data

        ## if request is get send data else if head is there no data data to be send
        '''
        if request == 'GET':
            if lines['Content-Range'] != '':
                temp = lines['Content-Range'].split(' ')
                temp = temp[1].split('/')
                temp = temp[0].split('-')
                try:
                    #206
                    message += temp_data[temp[0]:temp[1]]
                except :
                    pass                    
            else:
                message += temp_data
        '''
        logger.info(f"{address[0]} {address[1]} {request_line} 200 {size}")        
        client.send(message)
        client.close()









    def client_request(self,client_socket,address):
        
        while True:
            message = None
            file_content = None


            ## if the image/video/mp3 is send the except is executed 
            try: 
                message = client_socket.recv(self.size)
            except:
                return
            message = message.split(b'\r\n\r\n')
            message[0] = message[0].decode()
            
            try :
                byte_format = False
                
                m = message[1].decode()
                message[1] = m
            except :
                #errlogger.error(f"{address[0]} {address[1]} {E}")
                byte_format = True

            if len(message)> 1:
                file_content = message[1]
                
            header = message[0].split('\r\n')
            request_line = header.pop(0).split(' ')
            "contain the file name or the directory or in care of get request the data is also there" 
            file_loc = request_line[1]
            
            "this is the version of the server"
            version =  request_line[2]

            "Version unsuported Error is send"
            if version != "HTTP/1.1":
                self.status_code(client_socket,505,' '.join(request_line),address)



            header_lines = defaultdict(str)
            for header_line in header:
                temp = header_line.split(': ')
                header_lines[temp[0]] = temp[1]

               


            if request_line[0] == 'GET':
                self.GET_req('GET',header_lines,file_loc,client_socket,' '.join(request_line),address)
                break
            elif  request_line[0] == 'HEAD':
                self.GET_req("HEAD",header_lines,file_loc,client_socket,' '.join(request_line),address)
                break

            elif request_line[0] == 'PUT':
                self.put_req(header_lines,file_loc,client_socket,file_content,byte_format,address,' '.join(request_line))

                break
            elif request_line[0] == "POST":
                self.post_req(header_lines,file_loc,client_socket,file_content,byte_format,address,' '.join(request_line))
                break
            elif request_line[0] == "DELETE":
                self.delete_req(header_lines,file_loc,client_socket,''.join(request_line),address)
            else:
                self.status_code(client_socket,405,' '.join(request_line),address)


                


    def __del__(self):
        self.serversocket.close()



            



def main():
    


    try:
        addrs = ifaddresses('eth0')					        ## addrs == {17: [{'addr': '00:0c:29:4d:9f:5a', 'broadcast': 'ff:ff:ff:ff:ff:ff'}],
                                                        		##2: [{'addr': '192.168.211.128', 'netmask': '255.255.255.0', 'broadcast': '192.168.211.255'}],
                                                        		##10: [{'addr': 'fe80::20c:29ff:fe4d:9f5a%eth0', 'netmask': 'ffff:ffff:ffff:ffff::/64'}]}  	
    
        IP = str(addrs[2][0]['addr'])
    except:
        IP = '127.0.0.1'
    if len(argv) > 1:
        port = int(argv[1])
    else :
        print("Usage : python3 server.py port number")
        exit()       
        
    serversocket = socket(AF_INET, SOCK_STREAM)
    try:
        serversocket.bind(('',port))                      # as bind invoke auditing
    except :
        #errlogger.error(f"{E}")

        print("Provide valid port number or change the port number")
        exit()


    serversocket.listen(20)
    print("Connect server on ( " + IP +',' + str(port) + ')' )
    print("Url : http//" + IP +':'+ str(port)+ "   The file name")
    s = server(IP,port,serversocket)

    start_new_thread(s.servers_state,())
    s.start()
    



if __name__ == "__main__":
    main()



