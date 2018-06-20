#!/usr/bin/env python
import os

def sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i
    return ds18b20

def read(ds18b20):
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    farenheit = (celsius * 1.8) + 32
    return celsius, farenheit

def loop(ds18b20):
    while True:
        if read(ds18b20) != None:
            print ("Current temperature : %0.3f C" % read(ds18b20)[0])
            print ("Current temperature : %0.3f F" % read(ds18b20)[1])
            return read(ds18b20)[0]
        break

def kill():
    quit()

##tempC,tempF=read(sensor)

#if __name__ == '__main__':
#    try:
#        serialNum = sensor()
#        loop(serialNum)
#print(read(sensor())[0])
#tempC=round(read(sensor())[0],2)
#print(tempC)
#    except KeyboardInterrupt:
#        kill()
##################################################
import socket
import time

host = ''
port = 5560

#storedValue = "Yo, what's up?"
storedValue=str(round(read(sensor())[0],2))
print(storedValue)

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind comlete.")
    return s

def setupConnection():
    s.listen(1) # Allows one connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

def GET():
    reply = str(round(read(sensor())[0],2)) #storedValue
    return reply

def REPEAT(dataMessage):
    reply = dataMessage[1]
    return reply

def dataTransfer(conn):
    # A big loop that sends/receives data until told not to.
    while True:
        # Receive the data
        data = conn.recv(1024) # receive the data
        data = data.decode('utf-8')
        # Split the data such that you separate the command
        # from the rest of the data.
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        if command == 'GET':
            reply = GET()
        elif command == 'REPEAT':
            reply = REPEAT(dataMessage)
        elif command == 'EXIT':
            print("Our client has left us :(")
            break
        elif command == 'KILL':
            print("Our server is shutting down.")
            s.close()
            break
        else:
            reply = 'Unknown Command'
        # Send the reply back to the client
        conn.sendall(str.encode(reply))
        print("Data has been sent!")
        print(time.strftime("%I")+':' +time.strftime("%M")+':'+time.strftime("%S")+'--->'+str(reply))
    conn.close()


s = setupServer()

while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)

    except:
        break
