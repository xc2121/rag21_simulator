#!/usr/bin/env python

# notwendige Bibliotheken importieren
import rospy
import numpy as np
import bibInv

from std_msgs.msg import Float64

# Eingabe von erwuenschter Pose des Endeffektors:
# [x, y, z, x, y, z], [mm, mm, mm, rad, rad, rad]
pose = np.array([120, 0, 120, 0, 0, 0])
# Berechnung der entsprechenden Gelenkenpositionen.
joint_pos = bibInv.calc_inv_kin(pose)
print(joint_pos)

if __name__ == '__main__':
    pub1 = rospy.Publisher('/arm/joint1_position_controller/command', Float64, queue_size=10)
    pub2 = rospy.Publisher('/arm/joint2_position_controller/command', Float64, queue_size=10)
    pub3 = rospy.Publisher('/arm/joint3_position_controller/command', Float64, queue_size=10)
    pub4 = rospy.Publisher('/arm/joint4_position_controller/command', Float64, queue_size=10)
    pub5 = rospy.Publisher('/arm/joint5_position_controller/command', Float64, queue_size=10)
    pub6 = rospy.Publisher('/arm/joint6_position_controller/command', Float64, queue_size=10)

    rospy.init_node('RobotCommandPublisher', anonymous=True)

    rate = rospy.Rate(1) # 1hz
    while not rospy.is_shutdown():
        pub1.publish(float(joint_pos[0]))
        pub2.publish(float(joint_pos[1]))
        pub3.publish(float(joint_pos[2]))
        pub4.publish(float(joint_pos[3]))
        pub5.publish(float(joint_pos[4]))
        rate.sleep()