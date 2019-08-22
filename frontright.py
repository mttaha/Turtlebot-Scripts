#!/usr/bin/env python 

import rospy
import re
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from math import radians 

class Obstacle():
	def __init__(self):
		self.LIDAR_ERR = 0.05
		self.cmd_vel = rospy.Publisher('/cmd_vel', Twist,queue_size=10)
		self.obstacle()

	def get_centre(self):
        	msg = rospy.wait_for_message("scan", LaserScan)
        	self.scan_filterc = [3.5]
		self.scan_filterr = [3.5]
		self.scan_filterl = [3.5]
		self.scan_filterb = [3.5]

        	for i in range(360):
            		if i <= 15 or i > 335:
                		if msg.ranges[i] >= self.LIDAR_ERR:
                    			self.scan_filterc.append(msg.ranges[i])
			elif i <= 280 and i >= 260:
				if msg.ranges[i] >= self.LIDAR_ERR:
                    			self.scan_filterr.append(msg.ranges[i])
			elif i <= 100 and i >= 80:
		        	if msg.ranges[i] >= self.LIDAR_ERR:
		            		self.scan_filterl.append(msg.ranges[i])
			elif i <= 195 and i >= 165:
				if msg.ranges[i] >= self.LIDAR_ERR:
					self.scan_filterb.append(msg.ranges[i])
	def readFile(self):
		f = open("file.txt", "r+")
		steps = f.readLines()
		f.close()
		return steps[0] 
	def writeFile(self,count):
		f = open("file.txt","w+")
		f.write(count)
		f.close()

	def obstacle(self):
		self.r = rospy.Rate(5)
		self.twist = Twist()
		

		count = 0
		data = self.readFile();
		if(count!=data):				
			while count<5:
			
				self.get_centre()

				self.twist.linear.x = 0.2
			
				if min(self.scan_filterr) > 0.2:
					if min(self.scan_filterl) < 0.2:
						if min(self.scan_filterc) > 0.2:
							rospy.sleep(1)
							self.cmd_vel.publish(self.twist)
							count +=1
							rospy.loginfo('+1')
						else:
							self.twist.linear.x = 0.0
							self.twist.angular.z = 0.0
							self.cmd_vel.publish(self.twist)
							rospy.loginfo('C!')
					else:
						self.twist.linear.x = 0.0
						self.twist.angular.z = 0.0
						self.cmd_vel.publish(self.twist)
						rospy.loginfo('L!')
				else:
					self.twist.linear.x = 0.0
					self.twist.angular.z = 0.0
					self.cmd_vel.publish(self.twist)
					rospy.loginfo('R!')
			self.writeFile(count)
		else:
			rospy.loginfo('Cant proceed forward')
						
						
		rospy.on_shutdown(self.shutdown)
		rospy.loginfo('Destination reached')
	
	def shutdown(self):
        	# stop turtlebot
        	rospy.loginfo("terminate")
		self.twist.linear.x = 0.0
        	self.cmd_vel.publish(self.twist)
        	

def main():
    rospy.init_node('turtlebot3_obstacle')
    try:
        obstacle = Obstacle()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
