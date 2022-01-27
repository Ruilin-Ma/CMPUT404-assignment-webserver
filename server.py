#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Ruilin Ma 2022
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        #received request and decode the message
        self.data = self.request.recv(1024).strip()
        decodeMsg = self.data.decode().split()
        # print ("decodeMsg is: ", decodeMsg[1].strip('/'))
        print ("Got a request of: %s\n" % self.data)

        #check 404 and 405
        if decodeMsg == [] or "../" in decodeMsg[1]:
            self.request.sendall(bytearray("HTTP/1.1 404 Not FOUND\r\n",'utf-8'))
        elif decodeMsg[0] != "GET":
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not ALLOWED\r\n",'utf-8'))
        
        #rebuild resource address 
        newAddress = "./www"+decodeMsg[1]

        #check the resourse type and exist (dir or file)
        #https://www.w3resource.com/python-exercises/python-basic-exercise-85.php
        if os.path.isdir(newAddress):  
            if newAddress[-1] == '/':
                # print("file type is: ", newAddress[-4:])  
                newAddress += 'index.html'
                file = open(newAddress, "r")
                txt = file.read().replace('\n', '')
                contentType = "text/html"
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:" + contentType + "\r\n\r\n" + txt +"\r\n",'utf-8'))
                file.close()
            elif newAddress[-1] != '/':
                self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently Location:" + newAddress + "/" + "\r\n\r\n",'utf-8'))  
                
                
        elif os.path.isfile(newAddress):  
            file = open(newAddress, "r")
            txt = file.read().replace('\n', '')
            if newAddress[-4:] == ".css":
                contentType = "text/css"
                # print ("HTTP/1.1 200 OK\r\nContent-Type:" + contentType + "\r\n" + txt +"\r\n")
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:" + contentType + "\r\n\r\n" + txt +"\r\n",'utf-8'))
            elif newAddress[-5:] == ".html":
                contentType = "text/html"
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:" + contentType + "\r\n\r\n" + txt +"\r\n",'utf-8'))
            else:
                self.request.sendall(bytearray("HTTP/1.1 404 Not FOUND\r\n",'utf-8'))
            file.close()
        else:
            # print("result is: ",os.path.isdir('./www/deep/deep/'))
            self.request.sendall(bytearray("HTTP/1.1 404 Not FOUND\r\n",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
