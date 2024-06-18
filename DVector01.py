#Brandon Bowles

import os
import sys
import time

#Set max value for nodes that distance vector is unaware of
maxValue = sys.maxsize

#Set value for infinity per Lab instructions
infinity = 16

#List to store boolean value to detect if system is stable
stableStatus = []

#Variable that tells if system status is stable or not
systemStatus = False

#Empty List to store links/edges
links = []

#Empty dictionary to create network topology
network = {}

#Empty dictionary to store distance vector information
distanceVectors = {}

#Variable to keep count of nodes
nodeCount = 0

#Function that handles opening files
def openFile(filename):
    if filename == 'exit':
        sys.exit()
    else:
        file1 = open(filename, 'r')
    return file1

#Add node to network topology and build the list of links
def addNode(node):
    
    #global network
    global nodeCount

    #Check if node is already present in network
    if node in network:
        pass
    else:
        
        nodeCount = nodeCount + 1
        network[node] = []

#Add edge and cost to network topology and build the list of links       
def addEdge(node, neighbor, cost):
    
    #Check to see if node is present in network
    if node not in network:
        print("Node", node, "not present in network.")

    #Check to see if neighbor node is present in network
    elif neighbor not in network:
        print("Neighbor node", neighbor, "not present in network.")
    else:
        tempEdgeList = [int(neighbor), int(cost)]
        network[node].append(tempEdgeList)

#Function to initialize the set up of the distance vectors   
def initializeVectors(node):
    
    #Check if node is already present in distance vector
    if node in distanceVectors:
        print ("Node", node, "already exists.")
    
    # If node not present in distance vector, then initialize distance vector for node 
    # and add '0' for distance of node from itself
    else:
        distanceVectors[node] = []
        emptyListEntry = []
       
        for i in range(nodeCount):
            if i == int(node)-1:
                distanceVectors[node].append(0)
            else:
                distanceVectors[node].append(emptyListEntry)

#Function to add costs to distance vectors    
def addVectorCost(node, neighbor, cost):

    #Check to see if node is present in distance vectors
    if node not in distanceVectors:
        print("Distance vector", node, "not present.")

    #Check to see if node is neighbor and add distance/cost
    else:
        for key in distanceVectors:
            if key == node:
                
                #iterate through each index in the nodes distance vector
                for i in range(nodeCount):
                
                    #Check if index is a neighbor node
                    if i == int(neighbor)-1:
                        distanceVectors[key][i] = int(cost)
                
                    #if index is not for neighbor node or node itself then populate infinite/max value at index    
                    elif distanceVectors[key][i]==[]:
                        distanceVectors[key][i] = maxValue

# Initialize the values for the list that is supposed to keep track of 
# boolean values to evaluate whether all shorterst paths have been found and the system is stable
def initializeStability():
    for i in range(nodeCount):
        stableStatus.append(False)

# This is a function to test if the system is stable.
# The theory behind this function is supposed to be that once all boolean values evaluate to True for each node,
# then all shortest paths have been found and the system is stable.  However, I have not been able to get this method
# fully functional.  It always stops about 1 iteration short of finding all the shortest paths leaving one of the 
# distance values incorrect for node 2.
def isSystemStable(node, boolValue):
    boolValue 
    #Set Value of node status to True or False
    stableStatus[int(node)-1] = boolValue

    #Check if all entries are true to check is system is stable
    if all(stableStatus): 
        return True
    else:
        return False

#Function that runs the Bellman-Ford algorithm
def bellFord(node, neighbor, cost):
    global systemStatus
    newCost = 0
    
    #Iterate over each node in distance vector
    for y in range(nodeCount):
        
        #Bellman-Ford equation computation
        newCost = min(int(cost) + distanceVectors[neighbor][y], distanceVectors[node][y])
        
        # Set values for nodes that distance vector is not aware of
        # and print distance vector with updated cost
        if distanceVectors[node][y] == maxValue:
            distanceVectors[node][y] = newCost
            systemStatus = isSystemStable(node, False)
            print("\n--UPDATED DISTANCE VECTOR--")
            print ("Distance Vector", node, ":", distanceVectors[node])

        # Set new values if new cost is less than current cost at position in distance vector 
        # and print distance vector with updated cost
        elif newCost < distanceVectors[node][y]:
            distanceVectors[node][y] = newCost
            systemStatus = isSystemStable(node, False)
            print("\n--UPDATED DISTANCE VECTOR--")
            print ("Distance Vector", node, ":", distanceVectors[node])
        else:
            systemStatus = isSystemStable(node, True)
            
    #Run Bellman-Ford for distance vectors of neighbor nodes since graph is not directed    
    for y in range(nodeCount):
        
        #Bellman-Ford equation computation
        newCost = min(int(cost) + distanceVectors[node][y], distanceVectors[neighbor][y])
        
        # Set values for nodes that distance vector is not aware of
        # and print distance vector with updated cost
        if distanceVectors[neighbor][y] == maxValue:
            distanceVectors[neighbor][y] = newCost
            systemStatus = isSystemStable(neighbor, False)
            print("\n--UPDATED DISTANCE VECTOR--")
            print ("Distance Vector", neighbor, ":", distanceVectors[neighbor])

        # Set new values if new cost is less than current cost at position in distance vector 
        # and print distance vector with updated cost    
        elif newCost < distanceVectors[neighbor][y]:
            distanceVectors[neighbor][y] = newCost
            systemStatus = isSystemStable(neighbor, False)
            print("\n--UPDATED DISTANCE VECTOR--")
            print ("Distance Vector", neighbor, ":", distanceVectors[neighbor])
        else:
            systemStatus = isSystemStable(neighbor, True)

# Function to allow user to adjust the cost of a link, print out the updated link with new cost
# and check is link value is infinity and detect line failure  
def adjustLink(linkSelection, newLinkCost):

    links[int(linkSelection)-1][2] = newLinkCost
    print("\nUpdated Link List: ", links)

    if int(newLinkCost) >= infinity:
        print ("\nLink", linkSelection,"is no longer connected...")

#Function to print out complete list of distance vectors
def printVectors():
    for i in distanceVectors:
        
        print ("Distance Vector", i, ":", distanceVectors[i]) 
    
while True:
    
    
    #Ask user for file name and open file
    filename = input('Please enter file name or type "exit" to quit: ').lower()
    
    #Check for invalid filename, and allow user option to exit program
    try:
        file1 = openFile(filename)
    except FileNotFoundError:
        print("Invalid filename...\n")
        continue

    #Read each line of file into list
    Lines = file1.readlines()

    #split each item in list and store in list of Links
    for item in Lines:
        x = item.split()
        links.append(x)

    #Add nodes to network/router table dictionary
    for i in range(len(links)):
        for j in range(len(links[i])):
            if j != 2:
                addNode(links[i][j])

    #Add edges/links to network/router table dictionary
    for i in range(len(links)):
        addEdge(links[i][0], links[i][1], links[i][2])
        addEdge(links[i][1], links[i][0], links[i][2])
        
    #Sort list of links
    #links.sort()       

    #Store number of edges/links
    linkCount = int(len(links))

    #Sort network dictionary in order of node #
    netKeys = list(network.keys())
    netKeys.sort()
    sorted_network = {i: network[i] for i in netKeys}

    #Initialize list for testing stable status
    initializeStability()
    print("\nStable status:",stableStatus)

    #Add nodes to dictionary to store distance vector information
    for node in sorted_network:
        initializeVectors(node)

    #Add costs to distance vector information
    for nodeKey in sorted_network:
        for edge in sorted_network[nodeKey]:
            addVectorCost(nodeKey, edge[0], edge[1])

    #Print out initial list of links in the network and the network/router table
    print ("\nInitial list of links:",links)
    print ("\nNetwork table:",sorted_network)

    #Print out initial distance vectors before Bellman-Ford algorithm is ran
    print("\n------------------------")
    print("Initial Distance Vectors")
    print("------------------------")
    printVectors()

    #Variable to calculate exectution time
    t0 = time.time()

    #Setup loop to run Bellman-Ford algorithm on distance vectors and find shortest paths
    j = 0
    while j < nodeCount:
    #while systemStatus == False:    
        for i in range(linkCount):
            bellFord(links[i][0], links[i][1], links[i][2])
            
        
        j += 1

    #Print out new Stablized distance vectors with shortest paths to each node
    print("")
    print("---------------------------")
    print("Stabilized Distance Vectors")
    print("---------------------------")
    printVectors()
    
    #Variable to calculate exectution time
    t1 = time.time()

    #Calculate and print out execution time to calculate stabilized distance vectors
    totalTime1 = t1-t0
    print("\nThe total time to stabilize was: ", totalTime1)
    #print(systemStatus)
    #print(stableStatus)
    break
    
while True:
    #Ask user if they would like to adjust link cost
    adjustDecision = input("\nWould you like to adjust link cost? Please type: Yes or No? ").lower()

    #Check for user decision on whether or not to adjust link cost
    if adjustDecision == "yes":
        
        #Get user input to chooose which link to update and enter the new cost for the link
        while True:
            linkSelection = input("\nPlease choose the link you would like to adjust from 1 through {}: ".format(linkCount))

            #Check for error if user enter an invalid link number
            if int(linkSelection) < 1 or int(linkSelection) > 6:
                print("\nInvalid link")
            else: 
                break
    #Exit program if user chooses not to update link cost
    elif adjustDecision == "no":
        sys.exit()
    
    #Return to top of while loop if user does not enter any valid input
    else:
        continue
    
    #Store user input for new link cost 
    newLinkCost = input("\nPlease enter the new cost for the link: ")

    #Call function to update link and link cost
    adjustLink(linkSelection, newLinkCost)

    #Variable to calculate exectution time with updated link cost
    t2 = time.time()

    # Setup loop to run Bellman-Ford algorithm on distance vectors and 
    # find shortest paths with updated link cost from the user
    j = 0
    while j < nodeCount:
    #while systemStatus == False:    
        for i in range(linkCount):
            bellFord(links[i][0], links[i][1], links[i][2])
        
        j += 1
    #Variable to calculate exectution time with updated link cost
    t3 = time.time()

    #Calculate execution time to calculate stabilized distance vectors with user adjusted link cost
    updateTime = t3-t2
    
    #Print out updated distance vectors
    print("\n---------------------------")
    print("Updated Distance Vectors")
    print("---------------------------")
    printVectors()

    #Print out exectuion time to calculate updated distance vectors
    print("\nThe total time to update vectors was: ", updateTime)

 
