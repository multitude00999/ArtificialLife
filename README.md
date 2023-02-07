# ArtificialLife

Following is a submission for assignment 5

# demo

<vidoe>

# Task

Task of the creature is to chase the ball. Robot dog will try to go newr to the speherical ball.

# world 

World contains only two things (the horizontal plane) and spherical ball

# Creature

Creature here is simulating a dog like boston dynamics [spot](https://www.youtube.com/watch?v=wlkCQXHEgjA). 
Creature has total 9 links
one torso
4 uppper limb
4 lower limb

and total 8 joints
4 between torso and upper limbs
4 between upper limb and lower limb


# fitness

Fitness is the distance of the robot dog's torso from the ball. This is calculated as

```dist = np.sqrt((xPositionTarget - xPositionRobot)**2 + (yPositionTarget-yPositionRobot)**2))```

where ball's coordiantes are (xPositionTarget, yPositionTarget) and robot's torso centre of mass coordinates are (xPositionRobot, yPositionRobot).

So in order to go close to the ball. The robot will try to minimize this distance.

# Training parameters

numSteps = 1000
waitTime = 1/1000
amplitude, frequency, offset = np.pi/4, 10, 0 
numberOfGenerations = 10
populationSize = 10
numSensorNeurons = 5
numMotorNeurons = 8
motorJointRange = 0.2