import logging
import asyncio
import sys
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("YesIntent")

def next_round():

    round_msg = render_template('round')

    return question(round_msg)

@ask.intent("ForwardIntent")

def driveForward(first):

	distance = int(first[0])
	if distance > 5 :
		 distance = 5
	
	if distance < 1:
		msg = render_template('none')
	else :
		voice_control_cozmo.do_drive(distance)
		msg = render_template('forward')
	return question(msg)
	
@ask.intent("BackwardIntent")

def driveBackward(first):

	distance = int(first[0])
	if distance > 5 :
		 distance = 5
	
	if distance < 1:
		msg = render_template('none')
	else :
		voice_control_cozmo.do_drive(-distance)
		msg = render_template('backward')
	return question(msg)
	
@ask.intent("TurnRightIntent")

def turnRight(first):

	degrees = int(first)
	if degrees > 360 :
		 degrees = 359
	
	if degrees < 1:
		msg = render_template('none')
	else :
		voice_control_cozmo.do_turn(-degrees)
		msg = render_template('right')
	return question(msg)	

@ask.intent("TurnLeftIntent")

def turnLeft(first):

	degrees = int(first)
	if degrees > 360 :
		 degrees = 359
	
	if degrees < 1:
		msg = render_template('none')
	else :
		voice_control_cozmo.do_turn(degrees)
		msg = render_template('left')
	return question(msg)

@ask.intent("LiftUpIntent")

def	liftUp():
	voice_control_cozmo.do_lift(1)
	msg = render_template('lift')
	return question(msg)
	
@ask.intent("LiftDownIntent")

def	liftDown():
	voice_control_cozmo.do_lift(-1)
	msg = render_template('lift')
	return question(msg)
	
class VoiceControlCozmo:
	def __init__(self, coz):
		
		self.cozmo = coz
		self.cozmo.say_text("READY.").wait_for_completed()
	
	def do_lift(self, cmd_args):
		self.cozmo.move_lift(cmd_args)
	
	def do_drive(self, cmd_args):
		#"""drive X"""
		usage = "'drive X' where X is number of seconds to drive for"
		drive_duration = float(cmd_args)
		if drive_duration > 10.0:
			drive_duration = 10.0
	
		if drive_duration < -10.0:
			drive_duration = -10.0

		if drive_duration is not None:
			drive_speed = 50
			drive_dir = "forwards"
			if drive_duration < 0:
				drive_speed = -drive_speed
				drive_duration = -drive_duration
				drive_dir = "backwards"
			self.cozmo.drive_wheels(drive_speed, drive_speed, duration=drive_duration)
			print ('I drove ' + drive_dir + ' for ' + str(drive_duration) + ' seconds!')
		return

	def do_turn(self, cmd_args):
	    usage = "'turn X' where X is a number of degrees to turn"
	    drive_angle = float(cmd_args)
	    if drive_angle > 360:
	    	drive_angle = 0

	    if drive_angle is not None:
	    	self.cozmo.turn_in_place(degrees(drive_angle)).wait_for_completed()
	    	print ("I turned " + str(drive_angle) + " degrees!")

	    return "Error: usage = " + usage
	
	def do_cube(self):
		cube = None
		look_around = self.cozmo.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
		print("looking for cube")
		try:
			cube = self.cozmo.world.wait_for_observed_light_cube(timeout=60)
		except asyncio.TimeoutError:
			print("Didn't find a cube :-(")
			return
		finally:
			look_around.stop()    

def run(sdk_conn):
	robot = sdk_conn.wait_for_robot()
	
	global voice_control_cozmo
	voice_control_cozmo = VoiceControlCozmo(robot)
	app.run(debug=True)

#	for _ in range(4):
#		robot.drive_straight(distance_mm(150), speed_mmps(50)).wait_for_completed()
#		robot.turn_in_place(degrees(90)).wait_for_completed()
	
if __name__ == '__main__':
    cozmo.setup_basic_logging()
    try:
        cozmo.connect(run)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
