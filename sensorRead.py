"""
Pawel Krystkiewicz 1.09.2018
READING SENSORS' STATUS
"""
import requests

#CONST DATA
user=''
password=''
hub=''

#DICITIONARY WITH SENSORS' DETAILS
sensor={
0:{'MAC':'00:00:00:00:00:00:00:00','status':'unknown'},
1:{'MAC':'00:00:00:00:00:00:00:01','status':'unknown'},
2:{'MAC':'00:00:00:00:00:00:00:02','status':'unknown'}
}

#REQUEST.GET FUNCTION
def getAnswer(ID):
    url='/['+sensor.get(ID,{}).get('MAC')+']!' #fill with own url adress to device
    r = requests.get(url, auth=(user, password))

    #CHECK IF URL IS CORRECT AND MAC IS PRESENT
    if r.status_code!=200:
        print "MAC adress for ID",ID," not found on server."
        return

    #GET XML FROM DEVICE
    xml=r.text

    #CHECK IF MAC ADDRESS MATCHES
    recievedMAC= xml.split('[', 1)[1].split(']')[0]
    if sensor.get(ID,{}).get('MAC') != recievedMAC:
        print "Error! MACs does not match!"

    #DECODE VALUE FROM BASE64 TO READABLE
    secret=xml.split('value":"', 1)[1].split('"')[0]
    decoded=secret.decode('base64')

    #print "ID:",ID,"msg: ",decoded #<-HELPFUL DEBUG MSG, SHOWING DECODED STRING WITH INFO FROM DEVICE

    #UPDATE DEVICE STATUS from XML file -> read if connected or diconnected or different
    if "connected:" in decoded:
        sensor[ID]['status']="Connected"
    elif "disconnected:" in decoded:
        sensor[ID]['status']="Disconnected"
    else:
        sensor[ID]['status']="unknown"

    #SHOW STATUS TO USER
    print 'Sensor ID',ID,"with status: " + sensor[ID]['status']
    #END OF FUNCTION---------------------

#EXECUTE FUNCTION
#LOOP THROUGH ALL ELEMENTS IN DICTIONARY (ALL DEVICES)
for i in range(0, len(sensor)):
    getAnswer(i)

raw_input("Task finished.\nPress Enter to continue...")