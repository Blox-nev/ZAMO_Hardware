'''
------------------------------------------------------------------------------------------------------------------------------------
                                                       CHOOSE GOD WHILE U STILL CAN

							    | NEV V4.1 beta |
                                                            MAIN HARDWARE CODE
                                                             REV: 11/11/2018


#NOTE: On the proxy i have to develop a datarecieved function that closes the port after recieving data(self.transport.loseConnection


SETUP
pip install Twisted


NOTE:#2 useR and pwd are the same on all Neo

---------------------------------------------------------------------------------------------------------------------------------------

=============:HOME_UNIT_MAIN_CODE
'''


from twisted.python import log
import ast # Convert str to dic
from twisted.enterprise import adbapi
from twisted.internet.defer import Deferred
from twisted.internet import protocol, reactor
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.serialport import SerialPort





#Comment these out and see what happens
client_list = []
usb_list =[]
DBvalue = []


#=================================================================
#---------------| ALARM DATABASE CLASS |
#=================================================================

#DB connection pool
#dbname,username,passwd must be string formated.*****************
dbpool = adbapi.ConnectionPool("MySQLdb",
                               db = "HOME_storage",
                               user = "hardware_root", #%(netdata.User) NOTE: ROOTPASSWORD
                               passwd = "Neohome", #%(netdata.Pwd)
                               cp_reconnect = True )



"""
Alarm DB: This class does database connection so far it
1 update alarm operation.
2 update

"""


#=============================================| Database |


class Alarm_DB():

    def __init__(self):
        self.DBvalue = []#ALL ALARM TABLES
        self.alarmstate = []#Data to cloud ((tuple list),)
        self.lights_state = []


#-------|DATA BASE ALARM SELECT 
#This select the entire alarm database

    def Select_Alarm_table(self):
       # query = ("SELECT * FROM Alarm WHERE AlarmCND AND AlarmOOS AND AlarmSR =  AlarmCND AND AlarmOOS AND AlarmSR")
        query = ("SELECT * FROM Alarm")

        # result from alarm database to use you call Select_Alarm_table()
        return dbpool.runQuery(query)\
               .addCallback(self.Alarm_Result)\
               .addCallback(self.db_to_Cloud)\
               .addErrback(self.errorquery)



    # (Callback) This function hold data from alarm database
    def Alarm_Result(self,result):

        print "result:",type(result)#turple
        Alarm_rows = result [0:60]

        for row in Alarm_rows:
            Alarm_state = row

            dbID = Alarm_state  [0];
            dbName = Alarm_state [1];
            dbCND = Alarm_state  [2];
            dbOOS = Alarm_state [3];
            dbSR = Alarm_state [4];

            #NEED A FUNCTION THAT LOOKS FOR (1,1,1,1) for in
            ignition = (dbCND,dbOOS,dbSR)

        
            if ignition == (1L,1L,1L):
                   arduino.buzzor('1')

        return result




#-----|

    def db_to_Cloud(self,result):
        Alarm = result
        print ('Alarm_data to cloud:{}' .format(Alarm))
        self.alarmstate = '{}' .format(Alarm)
           

#---------------------------------------------------------------------------------------------|LIGHTS SELECT 
    def Select_Lights_table(self):
        Lights_query = ("SELECT * FROM Lights")

        return dbpool.runQuery(Lights_query)\
               .addCallback(self.Lights_Result)\
               .addCallback(self.Lights_to_cloud)\
               .addErrback(self.errorquery)


    def Lights_Result(self,Lights):

        print "Lights:",type(Lights)
        Lights_rows = Lights [0:50]
        for Light_row in Lights_rows:
            LIGHT = Light_row

        return Lights



#-----|  
    def Lights_to_cloud(self,Lights):
       # Light = {'lights':Lights}
        Light = Lights
        print ('Lights_data to cloud:{}'.format(Light))
        self.lights_state = '{}'.format(Light)


#---------------------------------------------------------------------------------------------|

    # Errback
    def errorquery(self,result):
        print "error received", result
        return result


#---|Alarm updator functions
    def doresetCND(self,AlarmCND):
        query = ("UPDATE Alarm SET AlarmCND = '%s'" % (AlarmCND))
        return dbpool.runQuery(query)#.addCallback(self.recieveResult)

    def doUpdateCND(self,AlarmID,AlarmCND):
    	query = ("UPDATE Alarm SET AlarmCND = '%s' WHERE id ='%s'" %(AlarmID,AlarmCND))#ID , CND
        return dbpool.runQuery(query)#.addCallback(self.recieveResult)

    #This set and reset SR table(time delay shoud be incorporated on
    #this function for activate delay purposes
    def doUpdateSR(self,AlarmSR):
    	query = ("UPDATE Alarm SET AlarmSR = '%s'" % (AlarmSR))
        return dbpool.runQuery(query)#.addCallback(self.recieveResult)

    #NOTE : out of state pir should be forced to 0 everything else should be 1
    #This is for out of service
    #it forces a selected pir OOS to 0 takes it offline
    #(update alarm where id == x) <---
    def doUpdateOOS(self,AlarmID,AlarmOOS):
   	query = ("UPDATE Alarm SET AlarmOOS = '%s' WHERE id = '%s'" % (AlarmID,AlarmOOS))
        return dbpool.runQuery(query)#.addCallback(self.recieveResult)


#---|IP updator functions
#====================================Some work requred here i need to build a user table and use it as reference
    def update_IP(self,NevIP,CloudIP):
        query = ("UPDATE IP SET NevIP = '%s',CloudIP = '%s'" %(NevIP,CloudIP))
        return dbpool.runQuery(query)






#---| update-Lights
#This only update and store data in the database
    def update_Lights(self,Name,light_onCode,light_offCode,state,ID):
        query = ("UPDATE Lights SET Name = '%s',onCode = '%s',offCode = '%s', state = '%s' WHERE id = '%s'" %(Name,light_onCode,light_offCode,state,ID))
        return dbpool.runQuery(query)

#---|Update-Irrigation
#NOTE I might need to develop or rather include id on this function id to say update irrigation on id X
    def update_Irrigation(self,IrrigatE_cntrl,IrrigatE_name,IrrigatE_state,ID):
        #NOTE In the brackets below is the database table names eg UPDATE irrigation. irrigation is the table
        query = ("UPDATE irrigation SET Cntrl = '%s', Name = '%s', State = '%s' WHERE id = '%s' " %(irrigatE_cntrl,irrigatE_name,IrrigatE_state,ID))
        return dbpool.runQuery(query)

#---|Update-Plugs
#This is for future use when i have RF plugs
#need a python script to monitor plugs state changes

    def update_plugs(self,id,Name,onbin,offbin,state):
        query = ("UPDATE plugs SET Name = '%s',onbin = '%s',offbin = '%s', state = '%s' WHERE id = '%s'" %(id,Name,onbin,offbin,state ))
        return dbpool.runQuery(query)


#---|Update-Curtain
#This is for future use when i have RF curtain
#need a python script to monitor curtain state changes



#---|Update-Remotes
#Gates


#Aircon
#TV,Radio etc


#---|Update-Cam
#stores camera IP





#=====================================================================
#---------------| ARDUINO OPERATION | PROTOCOL
#=====================================================================
# Note: This class can be used when developing GPS modules
class Arduclient(Protocol):

    def __init__(self, network):
        self.network = network
        #list of arduinos if many are used
        self.usb_list = []

    def buzzor(self,x):
        for usb in usb_list:
            usb.transport.write(x)

#---------------| CND Updater |

# Order in the string formating is very important CND , ID. CND is fixed to 1
# ID is the active pir signal
# dataReceived this method collects data from serial port on arduino
# db.Select_Alarm_table() is more like refresh it will supply updated data from db

    def dataReceived(self,data):
        todb = data
        AlarmID = data
        if todb == AlarmID :
            print ' PIR :%s' % AlarmID
 	    db.doUpdateCND('1','%s' % AlarmID)
            db.Select_Alarm_table()
            #This is for when a PIR state change immedietly t$his will update the cloud
        reactor.connectTCP("172.20.10.2", 5678, LucyFactory())#IP ADRESS FOMATINING NOTE THIS IS CLOUDIP

    #This method make a connection to arduino
    def connectionMade(self):
        usb_list.append(self)
        print 'Arduino Connected and ready'
        # This sends data to arduino
        Arduclient.sendLine(self, 'AT\r\n')

    #sendLine is important it is used in the above code
    def sendLine(self, cmd):
        print 'data to arduino || --->>>', cmd
        self.transport.write(cmd + "\r\n")


#=====================================================================
#---------------| NEV SERVER RECIEVED DATA
#=====================================================================

'''
# TCP Handle all network connection happen here
#NOTE : this is the new protocol use

ONCODE: {'NEVIP':'172.20.10.13','CLOUDIP':'192.20.10.13','USER':'pi','PWD':'Blox123','LIGHTID':1 ,'LIGHTNAME':'Passage', 'LIGHT_ONCODE':1111 ,'LIGHT_OFFCODE':0000,'LIGHT_STATE':1,'ALARMS/R':1,'ALARMOOSID':9,'ALARMOOSSTATE':1,'RF':10000111110000,'IRRIGATE': 1,'IRRIGATION_NAME':'lawn','IRRIGATION_ID': 1 ,'IRRIGATION_STATE':1}

OFFCODE: {'NEVIP':'172.20.10.13','CLOUDIP':'192.20.10.13','USER':'pi','PWD':'Blox123','LIGHTID':3 , 'LIGHTNAME':'Thulani','LIGHT_ONCODE':1113 ,'LIGHT_OFFCODE':3333,'LIGHT_STATE':0,'ALARMS/R':0 ,'ALARMOOSID':9,'ALARMOOSSTATE':0,'RF':10000111110000,'IRRIGATE': 1',IRRIGATION_NAME':'lawn''IRRIGATION_ID': 1 ,':'IRRIGATION_STATE' :0}


'''

#Incommig_payload
class CommandRx(Protocol):
#-----------------------------------------------------------|Incoming PAYLOAD|
#       PAY_LOAD
    def dataReceived(self, data):
	#This convert string to dictionary. Data comes in a string format this
	#converts it to dictionary
        b = ast.literal_eval(data)


    # DELETE this was for test only
    #    print'INCORMING DATA',b
    #    print'type', type(b)



#--------------------------------------------------||
        nev_ip = b["NEVIP"]
        Cloud_ip = b["CLOUDIP"]

        User = b["USER"]
        Pwd = b["PWD"]

        light_ID = b["LIGHTID"] 
        light_name = b["LIGHTNAME"] 
        light_oncode = b["LIGHT_ONCODE"] 
        light_offcode = b["LIGHT_OFFCODE"]                          
        light_state = b["LIGHT_STATE"]                          


 
        Nreset = b["ALARMS/R"]
        Rf = b["RF"]

        outofservice = b["ALARMOOSID"]
        OOSstate = b["ALARMOOSSTATE"]

        Irrigate_cntrl = b["IRRIGATE"]
        Irrigate_state = b["IRRIGATION"]
        Irrigate_id =b["IRRIGATION_ID"]
        Irrigate_name =b["IRRIGATION_NAME"]

#-----------------------------------------------------||
        print 'NEV_IP',nev_ip
        print 'CLOUD_IP',Cloud_ip

        print 'Received Data || <<<--- :'
        print ''
	#This is only for test perpose not needed in production
        print 'livolo_id :', light_ID
        print 'livolo_name:',light_name
        print 'livolo_onCode:',light_oncode
        print 'livolo_offCode:',light_offcode
        print 'livolo_state:',light_state

        print 'Netreset :',Nreset #DONE
        print 'RF :',Rf #NOT TESTED
        print 'out_of_service :',outofservice #DONE
        print 'OOSstate :',OOSstate #DONE
        print 'uSer :',User #THIS WILL NOT BE STORED IN THE DATABASE
        print 'Password :',Pwd #THIS WILL NOT BE STORED IN THE DATABASE

        print 'Irrigation', Irrigate_state,'IRRIGATION_ID',Irrigate_id #NOT TESTED


#---------------|I.I.L Updater |

        db.update_IP(nev_ip,Cloud_ip)
        db.update_Irrigation(Irrigate_cntrl,Irrigate_name,Irrigate_state,ID)
        db.update_Lights(light_name,light_oncode,light_offcode,light_state,light_ID)





#---------------| OOS Updater |--|good|

# This logic line insert outofservice from cloud to db on ID x
# Notice that out_of_service variable represent an id on the table

        if OOSstate == 1:
	    #OOSstate 1 = (OOS activate, OOS id )
            db.doUpdateOOS('1',outofservice)

        elif OOSstate == 0:
	    #OOSstate 0 = (OOS de-activate, OOS id)
            db.doUpdateOOS('0',outofservice,)

#---------------| SR Updater |

#::  Reset from tcp deliver data on Nreset and this update dbSR ,
#:::60s Delay for when  activate the alarm is required
# Send data to aduino

        netreset = str(Nreset)

        if netreset == '1':
            db.doUpdateSR('1')

        else:
            db.doUpdateSR('0')
	    # The below logic line reset CND
            db.doresetCND('0')
            arduino.buzzor('0')


#===================================================================
#---------------| NEV CLIENT |
#====================================================================

class lucyClient(Protocol):

    def connectionMade(self):


         
        self.DBvalue = db.DBvalue
        self.alarmstate = db.alarmstate
        self.lights_state = db.lights_state


#-------|BLOX PROTOCOL       
        hardware_status = {
                           'alarm_status':self.alarmstate,
                           'light_status':self.lights_state
                           }





#---------------------------------------------------------------------------------------

#        hardware = (self.alarmstate,self.lights)
# NOTE : for hardware_condition in hardware:
#        if self.alrmstate > 1
        if self.DBvalue ==  self.DBvalue : # INVESTIGATE i dont think this is necessary
            self.transport.write("{}" .format(hardware_status))
#            self.transport.write("{}" .format(self.lights))
            self.transport.loseConnection()


#        else:
#            print 'OOPS NONE type recieved from data base ', self.alarmstate
#            self.transport.write("{}" .format(self.alarmstate)) # This has to go not used

    def connectionLost(self, reason):
        print ("connection Lost", reason)


class LucyFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return lucyClient()

    def clientConnectionFailed(self, connector,reason):
        print "connection failed you not connected to the internet.", reason


#====================================================================
#---------------| FACTORY PROTOCOL CLASS |
#====================================================================
class CommandRxFactory(Factory):

    protocol = CommandRx

    def __init__(self):
        self.client_list = []
        print "CommandRX stuff ???."


if __name__ == '__main__':

    tcpfactory = CommandRxFactory()
    SerialPort(Arduclient(tcpfactory), '/dev/ttyUSB0', reactor, baudrate='9600')
    reactor.listenTCP(8001, tcpfactory)

    netdata = CommandRx()
    db = Alarm_DB()
    db.Select_Alarm_table()
    db. Select_Lights_table()
    arduino = Arduclient(Protocol)
    reactor.run()

