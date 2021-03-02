#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


front_dist = 0
left_dist = 0
right_dist = 0

def shutdown():
	
	rospy.loginfo("Stop TB3")
	pub.publish(Twist())			#default Twist() has linear.x of 0 and angular.z of 0
	rate.sleep()

def callback(msg):
	global front_dist, left_dist, right_dist

	print('=========================================')
	print('s1 [0]')
	print msg.ranges[0]
	front_dist = msg.ranges[0]

	print('s2 [45]')
	print msg.ranges[45]
	left_dist = msg.ranges[45]

	print('s3 [315]')
	print msg.ranges[315]
	right_dist = msg.ranges[315]
	

rospy.init_node('exploring')			# Initiate a Node called 'exploring'
rospy.on_shutdown(shutdown)
rate = rospy.Rate(10)

while not rospy.is_shutdown():

	pub = rospy.Publisher('/cmd_vel', Twist)
	move = Twist()

	sub = rospy.Subscriber('/scan', LaserScan, callback)

	#If obstacle is at least 0.5m in front of the TB3 in either 3 directions, the TB3 will move forward, else the 		TB3 will move 90 degrees per loop until there is clearance
	if front_dist >= 0.5 and left_dist >= 0.5 and right_dist >= 0.5:
		move.linear.x = 0.3
		move.angular.z = 0.0
		rospy.loginfo("Going Straight")
	elif left_dist < 0.5:
		move.linear.x = 0.0
		move.angular.z = -1	#60 degrees to right
		rospy.loginfo("Turning 60 Right")
	elif right_dist < 0.5:
		move.linear.x = 0.0
		move.angular.z = 1	#60 degrees to left
		rospy.loginfo("Turning 60 Left")
	else:
		move.linear.x = 0.0
		move.angular.z = 1.57	#90 degrees to left
		rospy.loginfo("Turning 90 Left")

	pub.publish(move)
	rate.sleep()


rospy.spin()
