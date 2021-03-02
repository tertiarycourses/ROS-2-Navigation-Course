#!/usr/bin/env python

import rospy
import os,sys
import actionlib

# move_base is the package that takes goals for navigation
# there are different implemenetations with a common interface
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# You need to know the coordinates that the map you are working
# in is. I estimated these numbers using the turtlebot3_world
# map from Turtlebot3. The center of the map is (0.0, 0.0, 0.0); each grid is 1m.

#The first waypoint array is x,y,z location. 
#The second one is a "quaternion" defining an orientation. 
# Quaternions are a different mathematical represetnation 
#for "euler angles", yaw, pitch and roll.

#path planning sequences (loop phase)
waypoints = [
    [ (-0.5, 0.0, 0.0),
     (0.0, 0.0, 0.0, 1.0)],
    [ (0.0, 2.0, 0.0),
      (0.0, 0.0, 0.0, 1.0)], 
    [ (2.0, 0.0, 0.0),
      (0.0, 0.0, 0.0, 1.0)], 
    [ (0.0, -2.0, 0.0),
      (0.0, 0.0, 0.0, 1.0)], 
    [ (-2.0, 0.0, 0.0),
      (0.0, 0.0, 0.0, 1.0)], 
]


def goal_pose(pose):
	goal_pose = MoveBaseGoal()
	goal_pose.target_pose.header.frame_id = 'map'
	goal_pose.target_pose.pose.position.x = pose[0][0]
	goal_pose.target_pose.pose.position.y = pose[0][1]
	goal_pose.target_pose.pose.position.z = pose[0][2]
	goal_pose.target_pose.pose.orientation.x = pose[1][0]
	goal_pose.target_pose.pose.orientation.y = pose[1][1]
	goal_pose.target_pose.pose.orientation.z = pose[1][2]
	goal_pose.target_pose.pose.orientation.w = pose[1][3]
	return goal_pose

# Main program starts here
if __name__ == '__main__':
	rospy.init_node('Navigation_Node')
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

   	 # wait for action server to be ready
    	client.wait_for_server()

    	# Loop until ^c; delete this line if you want the TB3 to stop at the last waypoint
    	while not rospy.is_shutdown():

        	# repeat the waypoints over and over again
        	for pose in waypoints:
            		goal = goal_pose(pose)
            		print("Going for goal: ", goal)
            		client.send_goal(goal)
            		client.wait_for_result()

