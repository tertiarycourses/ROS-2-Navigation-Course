#!/usr/bin/env python
 
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import quaternion_from_euler
from nav_msgs.msg import Odometry

def callback(msg):				#define a function called 'callback' that receives a parameter named 'msg'
	print msg.pose.pose
	
	global px, py, pz, ox, oy, oz, ow
	px = msg.pose.pose.position.x
	py = msg.pose.pose.position.y
	pz = msg.pose.pose.position.z

	ox = msg.pose.pose.orientation.x
	oy = msg.pose.pose.orientation.y
	oz = msg.pose.pose.orientation.z
	ow = msg.pose.pose.orientation.w


rospy.init_node('init_pos')
odom_sub = rospy.Subscriber("/odom", Odometry, callback)
pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size = 10)

rospy.sleep(3)
checkpoint = PoseWithCovarianceStamped()

checkpoint.pose.pose.position.x = px
checkpoint.pose.pose.position.y = py
checkpoint.pose.pose.position.z = pz
 
[x,y,z,w]=quaternion_from_euler(0.0,0.0,0.0)
checkpoint.pose.pose.orientation.x = ox
checkpoint.pose.pose.orientation.y = oy
checkpoint.pose.pose.orientation.z = oz
checkpoint.pose.pose.orientation.w = ow
 
print checkpoint
pub.publish(checkpoint)
	
