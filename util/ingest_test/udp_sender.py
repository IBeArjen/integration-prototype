from socket import *
import sys

s = socket(AF_INET,SOCK_DGRAM)
host = 'test_file_writer'
port = 9999
buf = 1024
addr = (host,port)

file_name = "mytext.txt"

s.sendto(file_name.encode(),addr)

f = open(file_name,"rb")
item = "Transferring Data....."
print("Sending Data....")
s.sendto(item.encode(),addr)
print("Data Send....")
s.close()
f.close()