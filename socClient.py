import socket
import csv
import time
from time import sleep
csvfile = "temp.csv"
f = open(csvfile, "w")
f.truncate()
f.close()

host = '192.168.0.25'
port = 5560

#def setupSocket():
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
    #return s
tempC1=0

while True:
    #command = input("Enter your command: ")
    command = "GET"
    #if command =='EXIT':
    #    s.send(str.encode(command))
    #    break
    #elif command == 'KILL':
    #    s.send(str.encode(command))
    #    break
    #print("command will be sent: "+command)
    s.send(str.encode(command))
    #s.send(command)
    reply = s.recv(1024)
    #print(reply.decode('utf-8'))
    tempC=reply.decode('utf-8')
    #print(reply)
    timeC = time.strftime("%I")+':' +time.strftime("%M")+':'+time.strftime("%S")
    data=[tempC,timeC]
    #print(data[0]+data[1])
    with open(csvfile, "a")as output:
        writer = csv.writer(output, delimiter=",", lineterminator = '\n')
        writer.writerow(data)

    sleep(1)

    # SoX must be installed using 'sudo apt-get install sox' in the terminal
    import os

    if tempC1==0:
        tempC1=tempC

    if tempC>tempC1:
        frequency=5000
    elif tempC1==tempC:
        frequency=1000
    else:
        frequency=500

    duration=100
    tempC1=tempC
    if duration==100:
        duration=200
    else:
        duration=100
    os.system('play -n synth %s sin %s' % (duration/1000, frequency))

s.close()
