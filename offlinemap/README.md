# How to use this library

The python script provided here is for distance based triggering. The sensor_msgs are converted to rgb images and also makes it GPS stamped.

`python odmtag.py`

After the MAV has clicked the images, run the provided bash script as `./odmrun.sh`. Before that change the line 4 of this script. This script ensures that the images are copied inside the odm_ws location and the odm library is executed properly. The directory is named by the current time for easy management. The result is shown after it is produced.

### Note: Please go through the AerialRoboticsIITK/ODM's README for configuring the parameters. Read opendm/config.py for more details 