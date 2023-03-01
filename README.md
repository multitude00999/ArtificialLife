# Evolving 3D creature

Following is a submission for assignment 7 of Artificial life [course](https://www.mccormick.northwestern.edu/mechanical/academics/courses/descriptions/495-artificial-life.html). 


# flow diagram of how 3D morphologies are created
![flow](./random_3d_morphology.png)

# Flow diagram of how body is mutated

## mutation 1 Add or remove sensor
![diagram2](./mutateBody.png)

## mutation 2 Add or remove a link
![diagram5](./mutateBodyParts.png)

# Flow diagram of how brain is mutated
![diagram3](./mutateBrain.png)

# Task

## Task 1
Task here is to evovle a 3D creature that can go towards a target location (ball in this task).

### Fitness curve task 1
![diagram4](./chase_the_ball_fitness_curves.png)

### Fitness curve task 2
![diagram5](./Fitness_Move_Fast.png)

## Task 2
Task here is to reach as far as possible from the origin (i.e running fast) 

# Demo

Youtube video [link](https://youtu.be/3HQX4aXXnlA)


# Installation

Follow instruction given [here](https://www.reddit.com/r/ludobots/wiki/installation/)

# Running the code

After installing pyrosim and pybullet, clone the repository and change into the directory.
Now run ```python3 search.py``` . It'll run parallel hill climber five times. In starting it'll show a random creature and then it'll show evolved creature for each run.




# world 

World contains only two things (the horizontal plane) and spherical ball

# Creature

Creature has a 3D morphology with number of links ranging between [3,5] and number of joints ranging between [2,4] joints (revolute) with axis of rotation randomly assigned along x, y or z direction. 

# Brain

Brain contains random number of sensor nueorons and ranodm number of motor neurons each connected to a joint. each of this motor neuron is connected to all of the sensor neurons. There are no hidden neurons. 

## flow diagram of brain for 3 sensor nueuron and 2 motor neuron

![flow](./SensorMotorNeuronConnection.png)

# References

The codebase is developed as part of [ludobots course](https://www.reddit.com/r/ludobots/).

Simulation is built using Pyrosim [git](https://github.com/jbongard/pyrosim).