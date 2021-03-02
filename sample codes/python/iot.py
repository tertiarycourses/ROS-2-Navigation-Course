#!/usr/bin/env python

# Import necessary packages needed to send data
import paho.mqtt.publish as publish
import psutil
from time import sleep
from math import isnan

# Import necessary packages for TB3
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import quaternion_from_euler
from nav_msgs.msg import Odometry

#####  ThingSpeak Channel Settings #####

# The ThingSpeak Channel ID
# Replace this with your Channel ID
channelID = "1290587"

# The Write API Key for the channel
# Replace this with your Write API key
apiKey = "FPFY7KPBVEFQC58Y"


#  MQTT Connection Methods

# Set useUnsecuredTCP to True to use the default MQTT port of 1883
# This type of unsecured MQTT connection uses the least amount of system resources.
useUnsecuredTCP = False

# Set useUnsecuredWebSockets to True to use MQTT over an unsecured websocket on port 80.
# Try this if port 1883 is blocked on your network.
useUnsecuredWebsockets = True

# Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.
# This type of connection will use slightly more system resources, but the connection
# will be secured by SSL.
useSSLWebsockets = False

#####   End of user configuration   #####

# The Hostname of the ThinSpeak MQTT service
mqttHost = "mqtt.thingspeak.com"

# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
	tTransport = "tcp"
	tPort = 1883
	tTLS = None

if useUnsecuredWebsockets:
	tTransport = "websockets"
	tPort = 80
	tTLS = None

if useSSLWebsockets:
	import ssl
	tTransport = "websockets"
	tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
	tPort = 443


# Create the topic string
topic = "channels/" + channelID + "/publish/" + apiKey

data1 = 0
data2 = 0
data3 = 0
data4 = 0
data5 = 0
data6 = 0
data7 = 0

###### Start of functions ######
def callback(msg):				#define a function called 'callback' that receives a parameter named 'msg'
	#print msg.pose.pose
	
	global px, py, pz, ox, oy, oz, ow
	px = msg.pose.pose.position.x
	py = msg.pose.pose.position.y
	pz = msg.pose.pose.position.z

	ox = msg.pose.pose.orientation.x
	oy = msg.pose.pose.orientation.y
	oz = msg.pose.pose.orientation.z
	ow = msg.pose.pose.orientation.w

    	# assigning values to global variables
    
    	global data1, data2, data3, data4, data5, data6, data7
    	data1 = px
    	data2 = py
    	data3 = pz
    	data4 = ox
    	data5 = oy
    	data6 = oz
    	data7 = ow

rospy.init_node('init_pos')

while not rospy.is_shutdown():
	
	odom_sub = rospy.Subscriber("/odom", Odometry, callback)

	##### Send laserdata to ThingSpeak #####

	# build the payload string
	tPayload = "field1=" + str(data1) + "&field2=" + str(data2) + "&field3=" + str(data3) + "&field4=" + str(data4) + "&field5=" + str(data5) + "&field6=" + str(data6) + "&field7=" + str(data7)

	# attempt to publish this data to the topic 
	publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

	###################################

rospy.spin()


