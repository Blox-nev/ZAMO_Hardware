#                        UPDATED 12/11/18
#                ----  HARDWHERE_HOME_TABLES  ----



'''

#Standalone pydal outside web2py

#updating
sudo apt-get dist-upgrade
sudo apt-get update

#instalation
pip install pyDAL

#msqlconnector
sudo apt-get install python-mysqldb

#This file creates database tables on HOMES database
#Manually create a Home_Hardware database and create user hommy and give privillages
#using MSQL_home_setup script

run this from python like any python script

V 2.1.1
'''

#from pydal import DAL and Field
from pydal import DAL, Field


#Root user 
db = DAL('mysql://hardware_root:Neohome@localhost/HOME_storage')
   #use root#msql://user:password@localhost/database



#HARDWHERE_home tables


#---------Cloud_IP addres
#stores cloud IP
db.define_table('IP',
   Field('NevIP','string'),
   Field('CloudIP','string')
   )

#----------alarm
#motion sensors = 1/0
#panic button = 1/0
db.define_table('Alarm',
   Field('AlarmNAME','string'),
   Field('AlarmCND', 'integer'),
   Field('AlarmOOS','integer'),
   Field('AlarmSR', 'integer')
   )

#-----------Lights
#state from payload = 1/0
#feedback from switches = on/off
db.define_table('Lights',
   Field('Name','string'),
   Field('onCode','string'),
   Field('offCode','string'),
   Field('state','string')
   )

#--------Irrigation
#feedback will be the result of the database state 1=on 0=off
#need a python script to monitor irrigation state changes
db.define_table('irrigation',
   Field('Cntrl','string'),
   Field('Name','string'),
   Field('state','string')
   )

#-------Plugs
#This is for future use when i have RF plugs
#need a python script to monitor plugs state changes
db.define_table('plugs',
   Field('Name','string'),
   Field('onbin','string'),
   Field('offbin','string'),
   Field('state','string')
   )

#-------Curtain
#This is for future use when i have RF curtain
#need a python script to monitor curtain state changes
db.define_table('curtain',
   Field('Name','string'),
   Field('onbin','string'),
   Field('offbin','string'),
   Field('state','string')
   )

#--------Remote Control
#RF gate
#RF Aircon
#anything RF and TVs RADIOs goes in here
db.define_table('rf_signal',
   Field('Name','string'),
   Field('code','string')
   )

#---------Cam_ip addres
#stores camera IP
db.define_table('Cam_ip',
   Field('Name','string'),
   Field('IP','string')
   )

#---------Motivation
#This is subscrition and is valid for 35 days
#i use a python script that reads payload activ variable
#and update Activator to 1 counts down and update
#Activator back to 0 when time laps

db.define_table('Motivation',
   Field('Activator','string')
   )


