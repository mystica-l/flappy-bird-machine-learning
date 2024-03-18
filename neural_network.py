import numpy
import random

# Sigmoid function to compress the value to -1 <= x <= 1
def sig(x):
    x = numpy.float32(x)
    return 1/(1 + numpy.exp(-x))

# Neuron class
# Takes in x number of inputs and assigns weights to them before returning
# the sigmoid of the sum of each input * their weight
class Neuron:
    NUM_INPUTS = 5
    WEIGHT_MAX = 1.0
    WEIGHT_MIN = -1.0
    BIAS_MAX = 1.0
    BIAS_MIN = -1.0
    WEIGHT_ADJUSTMENT = 0.1
    BIAS_ADJUSTMENT = 0.1
    
    # Constructor for new neuron
    def __init__(self, *args):
        # If there is no input given
        if len(args) == 0:
            # Create weight and input arrays
            self.weight_array = []
            self.input_array = []

            # Assign random weights between the limits to each input array and add 0's to the input
            for i in range(0, self.NUM_INPUTS):
                self.weight_array.append(random.uniform(self.WEIGHT_MIN, self.WEIGHT_MAX))
                self.input_array.append(0.0)

            # Create a random value for the bias between the limits
            self.bias = random.uniform(self.BIAS_MIN, self.BIAS_MAX)

        # If an input is given, it's a previous neuron to evolve off
        else:
            # Save the old_neuron
            old_neuron = args[0]

            # Creaet weight and input arrays
            self.weight_array = []
            self.input_array = []

            # Assign slightly altered weights to each weight arrayy
            for i in range(0, self.NUM_INPUTS):
                # Old neuron weight +- a random value in bewteen the weight adjustment limits
                self.weight_array.append(old_neuron.weight_array[i] + random.uniform(-self.WEIGHT_ADJUSTMENT, self.WEIGHT_ADJUSTMENT))
                self.input_array.append(0.0)

            # Cap the max and min of the weight
            if self.weight_array[i] > self.WEIGHT_MAX:
                self.weight_array[i] = self.WEIGHT_MAX
            elif self.weight_array[i] < self.WEIGHT_MIN:
                self.weight_array[i] = self.WEIGHT_MIN

            # Slightly alter the old neuron's bias
            # Old neuron bias +- a random value in between the bias adjustment limits
            self.bias = old_neuron.bias + random.uniform(-self.BIAS_ADJUSTMENT, self.BIAS_ADJUSTMENT)
            
            # Cap the max and min of the bias
            if self.bias > self.BIAS_MAX:
                self.bias = self.BIAS_MAX
            elif self.bias < self.BIAS_MIN:
               self.bias = self.BIAS_MIN

    # Update the inputs
    def update_inputs(self, inputs):
        for i in range(0, self.NUM_INPUTS):
            self.input_array[i] = inputs[i]
    
    # Returns the sigmoid of the linear algebraic sum of each input times it's weight
    def result(self):
        sum = 0.0
        for i in range(0, self.NUM_INPUTS):
            sum += self.weight_array[i] * self.input_array[i]
        sum += self.bias
        return sig(sum)

    # Print statement for debugging
    def print(self):
        for i in range(0, 5):
            print(self.weight_array[i])

# NeuralNetwork
# Network of x neurons with assigned weights and biases
# Takes in inputs and sends them to the individual neurons
# Returns a sigmoid activation value after summing up the linear algebraic sum
# Of neuron outputs * weights
class NeuralNetwork:
    NUM_NEURONS = 8
    WEIGHT_MAX = 1
    WEIGHT_MIN = -1
    BIAS_MAX = 1
    BIAS_MIN = -1
    WEIGHT_ADJUSTMENT = 0.1
    BIAS_ADJUSTMENT = 0.1
    fitness_score = 0.0

    # Constructor for new neural network
    def __init__(self, *args):
        # If no input is given
        if len(args) == 0:
            # Create neuron and weight arrays
            self.neuron_array = []
            self.weight_array = []

            # Fill up weight array with random values between the limits
            # Fill up the neuron array with brand new neurons that start off random
            for i in range(0, self.NUM_NEURONS):
                self.weight_array.append(random.uniform(self.WEIGHT_MIN, self.WEIGHT_MAX))
                self.neuron_array.append(Neuron())
            
            # Randomly assign bias
            self.bias = random.uniform(self.BIAS_MIN, self.BIAS_MAX)

        # Otherwise, an old neural network was given as an argument
        else:
            # Create neuron and weight arrays
            self.weight_array = []
            self.neuron_array = []

            # Save the old neural network
            old_neural_network = args[0]

            # Fill up the weight array with the old neural network's weights slightly altered by the weight adjustment
            # Fill up the the neuron array with neurons that are based off the old neuron
            for i in range(0, self.NUM_NEURONS):
                self.weight_array.append(old_neural_network.weight_array[i] + random.uniform(-self.WEIGHT_ADJUSTMENT, self.WEIGHT_ADJUSTMENT))

                # Cap the max and min of the weight
                if self.weight_array[i] > self.WEIGHT_MAX:
                    self.weight_array[i] = self.WEIGHT_MAX
                elif self.weight_array[i] < self.WEIGHT_MIN:
                    self.weight_array[i] = self.WEIGHT_MIN

                self.neuron_array.append(Neuron(old_neural_network.neuron_array[i]))

            # Slightly alter the old neural network's bias
            # Old neural network's bias +- a random value in between the bias adjustment limits
            self.bias = old_neural_network.bias + random.uniform(-self.BIAS_ADJUSTMENT, self.BIAS_ADJUSTMENT)

            # Cap the max and min of the bias
            if self.bias > self.BIAS_MAX:
                self.bias = self.BIAS_MAX
            elif self.bias < self.BIAS_MIN:
                self.bias = self.BIAS_MIN

    # Update the neurons with the new inputs
    def update_inputs(self, inputs):
        for neuron in self.neuron_array:
            neuron.update_inputs(inputs)
    
    # Returns the sigmoid of the linear algebraic sum of each neuron's result times it's weight
    def activation(self):
        sum = 0.0
        for i in range(0, 8):
            sum += self.neuron_array[i].result()
        sum += self.bias
        return sig(sum)
    
    # Resets the fitness score to keep the same neural network bird across generations
    def reset_fitness(self):
        self.fitness_score = 0
    
    # Print statement for debugging
    def print(self):
        print("Network Weights")
        for i in range(0, 8):
            print(self.weight_array[i])
        for i in range(0, 8):
            print("Neuron ", i)
            print(self.neuron_array[i].print())