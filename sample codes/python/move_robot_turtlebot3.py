#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

class MoveTB3(object):

    def __init__(self):
    
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.cmd_vel_subs = rospy.Subscriber('/cmd_vel', Twist, self.cmdvel_callback)
        self.last_cmdvel_command = Twist()
        self._cmdvel_pub_rate = rospy.Rate(10)


    def cmdvel_callback(self,msg):
        self.last_cmdvel_command = msg
    
    def compare_twist_commands(self,twist1,twist2):
        LX = twist1.linear.x == twist2.linear.x
        LY = twist1.linear.y == twist2.linear.y
        LZ = twist1.linear.z == twist2.linear.z
        AX = twist1.angular.x == twist2.angular.x
        AY = twist1.angular.y == twist2.angular.y
        AZ = twist1.angular.z == twist2.angular.z
        equal = LX and LY and LZ and AX and AY and AZ
        if not equal:
            rospy.logwarn("The Current Twist is not the same as the one sent, Resending")
        return equal

    def move_robot(self, twist_object):
        # We make this to avoid Topic loss, specially at the start
        current_equal_to_new = False
        while (not (current_equal_to_new)):
            self.cmd_vel_pub.publish(twist_object)
            self._cmdvel_pub_rate.sleep()
            current_equal_to_new = self.compare_twist_commands(twist1=self.last_cmdvel_command,
                                    twist2=twist_object)
                                    
    def clean_class(self):
        # Stop Robot
	rospy.loginfo("Initiate STOP ROBOT")  
        twist_object = Twist()
        twist_object.angular.z = 0.0
	twist_object.linear.x = 0.0
        self.move_robot(twist_object)
	stop_robot = True
	rospy.loginfo("STOPPING ROBOT")

def main():
    rospy.init_node('move_robot_node', anonymous=True)
    
    stop_robot = False    

    moveTB3_object = MoveTB3()
    twist_object = Twist()
    # Make it start turning
    twist_object.angular.z = 0.5
    
    rate = rospy.Rate(5)
    
    print('stop robot status?',stop_robot)

    while not stop_robot:
        moveTB3_object.move_robot(twist_object)
        rate.sleep()

    
if __name__ == '__main__':
    main()
