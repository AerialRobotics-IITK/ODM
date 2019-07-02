#!/usr/bin/env python
from __future__ import print_function
import os

import sys
import rospy
import math
import cv2 as cv
from std_msgs.msg import String
from sensor_msgs.msg import Image, NavSatFix
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from piexif import JpegFile

class gps_tag:

    def __init__(self):
        self.bridge = CvBridge()
        self.height_sub = rospy.Subscriber("/spedix/odom",Odometry,self.lidarCallback)
        self.gps_sub = rospy.Subscriber("/spedix/pilot/global_position/global",NavSatFix,self.gpsCallback)
        self.image_sub = rospy.Subscriber("/spedix/usb_cam/image_raw",Image,self.imgCallback)
        self.count = 0
        self.curr_pos = 0,0
        self.prev_pos = 0,0
        self.dist_trigger = 0
        self.flag = True

    def imgCallback(self,data):
        if(self.calc_dist() > self.dist_trigger):
            try:
                cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            except CvBridgeError as e:
                print(e)
                
            img_name = "img"+str(self.count)
            cv.imwrite(img_name+".jpg",cv_image)
            imgToTag = JpegFile.fromFile(img_name+".jpg")
            imgToTag.set_geo(self.gps.latitude,self.gps.longitude,self.lidar)
            imgToTag.writeFile("stamped"+img_name+".jpg")
            print("count , flag , dist_trigger",self.count , self.flag , self.dist_trigger)
            self.count+=1
            self.prev_pos = self.curr_pos

    def lidarCallback(self,data):
        self.lidar = data.pose.pose.position.z

    def gpsCallback(self,data):
        self.dist_trigger  = self.lidar*(math.tan(50.0*math.pi/180))*0.3
        print("dist_trigger",self.dist_trigger)
        self.gps = data
        return data

    def calc_dist(self):
        if self.flag:
            self.curr_pos = self.gps.longitude,self.gps.latitude
            self.prev_pos = self.curr_pos
            self.flag = False
            return 100
        else:
            self.curr_pos = self.gps.longitude,self.gps.latitude
            self.ret_dist = (self.curr_pos[1] - self.prev_pos[1])*111321 + (self.curr_pos[0] - self.curr_pos[0])*40075000*(math.cos(self.gps.latitude*math.pi/180))/360
            print("ret_dist",abs(self.ret_dist))
            return abs(self.ret_dist)
            

def main(args):
  ic = gps_tag()
  rospy.init_node('gps_tag', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
#   cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)