from binaryTree import *
import random
import copy
import numpy as np
import math

# Function to create a new equation in form of a BTS
# RECIEVES the number of variables that the equation should have
# RETURNS a Tree
def createEquation(num):

	# Different signs, variables and numbers you can use
	signs = ['+','-','*','/','^']
	variables = ['x','y','z','m','k']
	numbers = ['1','2','3','4','5','6','7','8','9']

	# Create a new tree
	newTree = Tree()
	cont = 0
	addToEquation = True
	lastWasPow = False

	# Keep adding to the acuation utill you have NUM different variables
	while (addToEquation):
		if lastWasPow:
			newTree.addNode('2')
			newTree.addNode(random.choice(signs[:4]))
			lastWasPow = False
		else:
			# Select a random number
			randomNum = random.uniform(0,1)
			# Insert a random number and a random sign
			# Or choose a variable and then add a sign
			if (randomNum < 0.2):
				newTree.addNode(random.choice(numbers))
				sign = random.choice(signs)
				if sign == '^':
					lastWasPow = True
				newTree.addNode(sign)
			else:
				var = random.choice(variables[:num])
				# Checks if variable has already been added or if it's a new variable
				if (var == variables[cont]):
					cont += 1
				newTree.addNode(var)
				sign = random.choice(signs)
				if sign == '^':
					lastWasPow = True
				newTree.addNode(sign)

			# Checks if you already have NUM different variables
			if (cont >= num):
				randomNum = random.uniform(0,1)
				if(randomNum > 0.05):
					addToEquation = False
	
	if lastWasPow:
		newTree.addNode('2')
		lastWasPow = False
	else:
		# Adds a new number or a new variable to the ecuation so it dosn't finish in a sign
		randomNum = random.uniform(0,1)
		if (randomNum < 0.5):
			newTree.addNode(random.choice(numbers))
		else:
			var = random.choice(variables[:num])
			if (var == variables[cont]):
				cont += 1
			newTree.addNode(var)

	# Returns new tree
	return newTree




# Solves the equation in form of a binary tree
# Recieves a node and solves for his left and right side
def solveEquation(node,values):
	# Check if node is a number or variable
	if (node.left == None):
		# Asigns value to the variables
		if (node.data == 'x'):
			return values[0]
		elif (node.data == 'y'):
			return values[1]
		elif (node.data == 'z'):
			return values[2]
		elif (node.data == 'm'):
			return values[3]
		elif (node.data == 'k'):
			return values[4]
		else:
			# If it is a number return the value of the number
			return float(node.data)
	else:
		# Operate depending on the sign.
		# Gets the value on the left side and on the right side
		if node.data == '+':
			return float(solveEquation(node.left,values)) + float(solveEquation(node.right,values))
		elif node.data == '-':
			return float(solveEquation(node.left,values)) - float(solveEquation(node.right,values))
		elif node.data == '^':
			return math.pow(float(solveEquation(node.left,values)),float(solveEquation(node.right,values)))
		elif node.data == '*':
			return float(solveEquation(node.left,values)) * float(solveEquation(node.right,values))
		elif node.data == '/':
			# Checks if a divition over zero is going to be made.
			# Returns 0 if you are going to divide over zero
			a = float(solveEquation(node.left,values))
			b = float(solveEquation(node.right,values))
			if(b == 0):
				return 0
			else:
				return a/b
		else:
			return 0



# Function for selecting random node
# Recieves the root of the BST
def selectCrossNode(root):
	# Sets actualNode as the root
	actualNode = root

	# Checks if node is leaf
	while (actualNode.left != None):
		# Creates ranodm number
		randNum = random.uniform(0, 1)

		# Selects to go right or left 
		# 50/50 chance
		if (randNum < 0.5):
			actualNode = actualNode.left
		else:
			actualNode = actualNode.right

		# Creates second random number
		randNum = random.uniform(0,1)

		# Decides if actual node will be selected
		# 50/50 chance it will be selected
		if (randNum < 0.5):
			return actualNode

	# If the node is leaf it will return the node
	return actualNode


# Function for crossing 2 trees at a random node
# RECIEVES 2 BST 
# RETURNS 2 new BST
def cross(tree1, tree2,numVar):
	# Control variable to check if you have all the variables
	hasAll = False
	variables = ['x','y','z','m','k']

	# Repeat untill you get two trees with all the variables
	while(not hasAll):
		# Create a copy of the original trees
		nT1 = copy.deepcopy(tree1)
		nT2 = copy.deepcopy(tree2)
		# Select the 2 points to cross
		node1 = selectCrossNode(nT1.root)
		node2 = selectCrossNode(nT2.root)

		# Makes copy of first node
		temp = copy.deepcopy(node1)

		# Puts data of second node in first node
		node1.data = node2.data
		node1.left = node2.left
		node1.right = node2.right
		# Puts data of first copy of original first node into second node
		node2.data = temp.data
		node2.left = temp.left
		node2.right = temp.right

		# Check if you have all the variables needed
		cont = 0
		for i in range(0,numVar):
			if variables[i] in nT1.printTree(nT1.root) and variables[i] in nT2.printTree(nT2.root):
				cont += 1
		if cont >= numVar:
			hasAll = True
			
		# if 'x' in nT1.printTree(nT1.root) and 'y' in nT1.printTree(nT1.root) and 'z' in nT1.printTree(nT1.root):
		# 	if 'x' in nT2.printTree(nT2.root) and 'y' in nT2.printTree(nT2.root) and 'z' in nT1.printTree(nT2.root):
		# 		hasAll = True


	# Returns the 2 new trees
	return nT1, nT2


# Function for mutating a node
# Recieves a tree and the number of variables used
def mutate(tree, numVar):
	# Selects the node to mutate
	nodeToMutate = selectCrossNode(tree.root)

	signs = ['+','-','*','/']
	var = ['x','y','z','m','k']

	# Creates random number and if number is < 0.1 it will mutate
	randNum = random.uniform(0, 1)
	if (randNum < 0.01):
		# It will check if node is a sign or a variable and will mutate to a diferent valeue of the same type
		if nodeToMutate.data in signs:
			nodeToMutate.data = random.choice(signs)
		else:
			nodeToMutate.data = random.choice(var[:numVar])


# Function to get the error of a fuction
# RECIEVES a tree, the values to check and the expected result
# RETURNS the error (actualResult - expectedResult)
def getError (tree, values, result):
	error = 0
	cont = 0
	# Check with all the values and acumulates the error
	for i in values:
		# Solves the ecuation and returns the value
		res = solveEquation(tree.root,i)
		# Acumulates the error
		error += abs(result[cont] - res)
		cont += 1
	# Return acumulated error 
	return error


# Function to choose the best tree to cross, uses Tournament selection
# RECIEVES a list of trees, a list of values and a list of expected results
# RETURN a tree of the list
def chooseTree(trees,values,results):
	# Initiantes a new empty tree list
	treeList = []
	# Selects 3 random trees
	for i in range(0,3):
		treeList.append(random.choice(trees))

	# Get the error of the three selected trees
	errors = []
	for i in treeList:
		errors.append(getError(i,values,results))

	# Get the index of the tree with the minimum error
	index_min = np.argmin(errors)

	# Returns the best tree of the three
	return treeList[index_min]


# Function for getting a new generation
# RECIEVES a list of trees, a list of values and a list of results
# RETURNS a list of ntew trees
def getNextGen(trees,values,results,numVar):
	# Get's the size of the generation
	genSize = len(trees)
	newGen = []
	newGenSize = 0
	# Will keep crossing trees until you have a new generation of the same size as the initial population
	while (len(newGen) < genSize):
		# Choose two trees
		tree1 = chooseTree(trees,values,results)
		tree2 = chooseTree(trees,values,results)

		# Cross the two trees
		newTree1, newTree2 = cross(tree1,tree2,numVar)
		# Appends the new trees to the new generation
		newGen.append(newTree1)
		newGen.append(newTree2)

	# Return the list with the new generation of trees 
	return newGen



# Function for starting the evolution
# REVIEVES the initial population number, the number of variables, the data, the expected results and the number of generations
# RETURNS the best equation to fit the data
def start(populationNum, numVar, data, results, generations):
	initialPupulation = []
	# Create the initial population of the size of populationNum
	while len(initialPupulation) < populationNum:
		tree = createEquation(numVar)
		initialPupulation.append(tree)

	# Repeat until you have N generations
	for x in range (0, generations):
		# List the errors of the generation
		errors = []
		# Get the errors of the initial population
		for i in initialPupulation:
			equation = i.printTree(i.root)
			errors.append(getError(i,data,results))

			print(equation)

		print(errors)


		# cont = 0
		# for i in errors:
		# 	if (i < 10 and i > -10):
		# 		print("Posición", cont)
		# 	cont += 1

		# The new generation will now be the initial population
		initialPupulation = getNextGen(initialPupulation, data, results,numVar)


	# for i in initialPupulation:
	# 	equation = i.printTree(i.root)
	# 	errors.append(getError(i,data,results))
	# 	print(equation)

	# print(errors)


def main():
	initialPopulation = input("Give me the number of the initial population \n")
	numGen = input("Give me the number of generations \n")

	initialPopulation = int(initialPopulation)
	numGen = int(numGen)

	initialData = []
	expResults = []

	lines = [line.rstrip('\n') for line in open('data.txt')]
	numVar = int(lines[0])

	for d in lines[1:]:
		cont = 0
		dat = d.split()
		temp = []
		for c in dat:
			if cont < numVar:
				temp.append(float(c))
			else:
				expResults.append(float(c))
			cont += 1
		initialData.append(temp)



	# x = [[1,2,3],[1,4,5],[5,3,4],[3,2,6],[2,3,4]]
	# y = [6,18,7,3,10]

	start(initialPopulation,numVar,initialData,expResults,numGen)




main()
