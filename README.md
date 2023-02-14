# Random 1D creature morphologies

Following is a submission for assignment 6 of Artificial life [course](https://www.mccormick.northwestern.edu/mechanical/academics/courses/descriptions/495-artificial-life.html). 



# Demo

Youtube video [link](https://www.youtube.com/shorts/amqdrVkNZ_M)

[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/YamqdrVkNZ_M/0.jpg)](http://www.youtube.com/watch?v=amqdrVkNZ_M)


# Installation

Follow instruction given [here](https://www.reddit.com/r/ludobots/wiki/installation/)

# Running the code

After installing pyrosim and pybullet, clone the repository and change into the directory.
Now run ```python3 generate_random_1d_morphologies.py``` . It'll generate a random snake. You can re run this command for more random morphologies.

# Task

Task here is to generate random 1D morphologies. The links are randomly assigned a sensor. Green links have sensor while blue links don't have sensor.

# world 

World contains only two things (the horizontal plane) and spherical ball

# Creature

Creature here is a snake with 10 links and 9 joints (revolute) with axis of rotation as Y axis. Links with green color have sensor while links with blue color don't have seonsor.


# Brain

Brain contains random number of sensor nueorons and 9 motor neurons each connected to a joint. each of this motor neuron is connected to all of the sensor neurons. There are no hidden neurons

# References

The codebase is developed as part of [ludobots course](https://www.reddit.com/r/ludobots/).

Simulation is built using Pyrosim [git](https://github.com/jbongard/pyrosim).