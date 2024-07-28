from clover import srv
from std_srvs.srv import Trigger
import rospy
import math

i = None

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
set_yaw = rospy.ServiceProxy('set_yaw', srv.SetYaw)
land = rospy.ServiceProxy('land', Trigger)


def navigate_wait(x=0, y=0, z=0, speed=0.5, frame_id='body', auto_arm=False):
    res = navigate(x=x, y=y, z=z, yaw=float('nan'), speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    if not res.success:
        raise Exception(res.message)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < 0.2:
            return
        rospy.sleep(0.2)


def land_wait():
    land()
    while get_telemetry().armed:
        rospy.sleep(0.2)


def wait_yaw():
    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if abs(telem.yaw) < math.radians(1):
            return
        rospy.sleep(0.2)


navigate_wait(z=1.25, frame_id='body', auto_arm=True)
for i in range(0, 7, 3):
    navigate_wait(x=i, y=0, z=0, frame_id='body', speed=2)
set_yaw(yaw=math.radians(90), frame_id='body')
wait_yaw()
navigate_wait(x=1, y=0, z=0, frame_id='body', speed=1)
set_yaw(yaw=math.radians(90), frame_id='body')
wait_yaw()
for i in range(0, 7, 3):
    navigate_wait(x=i, y=0, z=0, frame_id='body', speed=1.5)
set_yaw(yaw=math.radians(-90), frame_id='body')
wait_yaw()
navigate_wait(x=1, y=0, z=0, frame_id='body', speed=1)
set_yaw(yaw=math.radians(-90), frame_id='body')
wait_yaw()
for i in range(0, 7, 3):
    navigate_wait(x=i, y=0, z=0, frame_id='body', speed=1.5)
set_yaw(yaw=math.radians(90), frame_id='body')
wait_yaw()
navigate_wait(x=1, y=0, z=0, frame_id='body', speed=1)
set_yaw(yaw=math.radians(90), frame_id='body')
wait_yaw()
for i in range(0, 7, 3):
    navigate_wait(x=i, y=0, z=0, frame_id='body', speed=1.5)
land_wait()

