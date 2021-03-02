#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def callback(msg):
	print('s1 [0]')
	print msg.ranges[0]

	if msg.ranges[0] > 0.5:
		move.linear.x = 0.3
		move.angular.z = 0.0
	else:
		move.linear.x = 0.0
		move.angular.z = 0.0

	pub.publish(move)

rospy.init_node('obstacle_avoidance')			
sub = rospy.Subscriber('/scan', LaserScan, callback)
pub = rospy.Publisher('/cmd_vel', Twist)
move = Twist()

rospy.spin()
