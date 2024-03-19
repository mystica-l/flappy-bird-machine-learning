# flappy-bird-machine-learning
This is a program that uses pygame and python to train flappy birds using machine learning.  
It generates 50 flappy birds into a flappy bird game that has attached nerual networks.  
These neural networks are fed information from the game and uses that information to decide when to jump in the game.
The longest surviving birds are then altered to slowly evolve into flappy bird gods!  

## How It's Made:
### Tech Used: Python, Pygame
I created this project using python and pygame for a couple of different reasons. To start, I wanted to become more familiar with python and be able to incorporte the language into future projects if I so desired.  
I also created this project because I wanted to become more familiar with the concept of machine learning which I thought was extremely interesting and wanted to challenge myself to put it into practice.  
I also wanted to use python due to it's access to the pygame module which I felt was the most simple way of displaying a game type program like this to a screen.  
I started off by making a simple flappy bird game before removing the player control and incorporating neural networks. The neural networks contain 8 neurons in the hidden layer.  
Each neuron has a set of 5 randomly assigned weights for each input (bird height, bird velocity, horizontal distance to pipe, vertical distance to top pipe and bottom pipe) and a randomly assigned bias.  
The sum of these weights times their inputs and biases are then put through another set of weights in which neuron has it's own weight in the neural network.  
The sum of the nueron's output times their weights plus the biases give an activation value and determine whether or not the bird should jump at any given moment.  
Then, fitness scores are given to each bird and the most successful birds are evolved by slightly tweaking their initially random weights before eventually creating a flappy bird that can handle any set of pipes.  

## How to Run:
Step 1: Install Python  
Step 2: Install pygame  
```bash
pip install pygame
```

Step 3: 