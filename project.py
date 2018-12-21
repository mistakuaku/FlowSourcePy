from graph import Graph
import argparse, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


## This is the main file for this project.
## Check out graph.py for the rest.


##  This function is designed to parse the text files that hold the data for
##  the right flow and front flows.
##  
##  The naming convention for the files is r/f_flowsx.txt where the r/f could be
##  either the r for right flows or the f for front flows. The x represents the
##  period.
## 
##  The way the function parses the text files is exactly how you read english
##  left to right top to bottom. This is exactly how we will translate these
##  data points to our grid later as well. The top left number in each file
##  will be the top left cell on our grid.
def readFlowsText(flowsList, flowsDirection, nodes):
    for line in open(flowsDirection + str(i) + '.txt', 'r'):
        for char in '[]':
            line = line.replace(char, '')
        words = line.split(' ')
        words = [x for x in words if x != '']
        words = [x for x in words if x != '\n']
        words = [x for x in words if x != ' ']
        for string in words:
            flowsList.append(float(string))

    if int(nodes) != len(flowsList):
        print('Expected ', nodes, ' nodes, but ', len(flowsList), ' were given in r_flows.')
        quit()

## Describe later
##
def drawGraph(myMap, nodes, vert, cols):
    fig, ax = plt.subplots()

    cmap = plt.cm.ocean_r
    cax = ax.imshow(myMap, cmap=cmap, interpolation='none')
    ax.set_title('Fraction Through')

##  Start the ticks to start at -0.5 otherwise
##  the grid lines will cut the nodes in half
    ax.set_xticks(np.arange(-0.5, int(cols), 1))
    ax.set_yticks(np.arange(-0.5, int(vert)/int(cols), 1))

##  This will hide the tick labels
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])

    cbar = fig.colorbar(cax, ticks=[0, int(max(nodes)/4), int(max(nodes)/2), int(max(nodes)*.75), int(max(nodes))])
    cbar.ax.set_yticklabels(['0', int(max(nodes)/4), int(max(nodes)/2), int(max(nodes)*.75), int(max(nodes))])

    plt.rc('grid', linestyle='solid', color='black')
    ax.grid(linewidth=2)
    plt.grid(True)
    plt.show()


def drawAnimation(data, nodes, vert, cols, periods):
    fig, ax = plt.subplots()

    cmap = plt.cm.ocean_r

    ims = []

    for i in range(periods):
        im = ax.imshow(data[i], cmap=cmap, interpolation='none', animated=True)
        ims.append([im])

    ax.set_title('Fraction Through')

##  Start the ticks to start at -0.5 otherwise
##  the grid lines will cut the nodes in half
    ax.set_xticks(np.arange(-0.5, int(cols), 1))
    ax.set_yticks(np.arange(-0.5, int(vert)/int(cols), 1))

##  This will hide the tick labels
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])

    cbar = fig.colorbar(im, ticks=[0, int(max(nodes)/4), int(max(nodes)/2), int(max(nodes)*.75), int(max(nodes))])
    cbar.ax.set_yticklabels(['0', int(max(nodes)/4), int(max(nodes)/2), int(max(nodes)*.75), int(max(nodes))])

    plt.rc('grid', linestyle='solid', color='black')
    ax.grid(linewidth=2)
    plt.grid(True)

    ani = animation.ArtistAnimation(fig, ims, interval=1000)

    plt.show()



## This is a method to simplify runtime by running arguments at the command line
## instead of asking the user to input the values each time they run the program.

## Periods represents the different states the graph will be in and also the number of
## r_flows and f_flows files you'll be looking at.

## Nodes represents the number of cells in the grid in total

## Width represents the width of the grid in the x direction

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--period", type=int, dest="period", help="Number of time periods")
parser.add_argument("-n", "--nodes", type=int, dest="nodes", help="Number of nodes")
parser.add_argument("-w", "--width", type=int, dest="width", help="Width of the graph")

args = parser.parse_args()

## This conditional block here is to check whether the user gave arguments at runtime or not
## If the did not then it will ask them for the values individually like it previously ran

if args.period:
    periods = args.period
else:
    periods = input('Number of time periods:\n')

if args.nodes:
    num_nodes = args.nodes
else:
    num_nodes = input('Number of nodes:\n')

if args.width:
    num_columns = args.width
else:
    num_columns = input('What is the width of the graph:\n')


## To start our program we will first create an empty list that will contain
## a group of graphs seperated by their period.
## For example at position 0 of the list it will hold a graph that represents
## r_flows0.txt and f_flows0.txt. Position 1 of the list will hold the graph
## that is represents r_flows1.txt and f_flows1.txt and so on.

g = []

for i in range(int(periods)):
    g.append(Graph(int(num_nodes), int(num_columns)))

##  The empty list that will hold the flow values from the text files
    r_flows = []
    f_flows = []

    readFlowsText(r_flows, 'r_flows', num_nodes)
    readFlowsText(f_flows, 'f_flows', num_nodes)

    for j in range (0, (int(num_nodes))):
        #print('A')
        #print(j)
        #print('B')
        if r_flows[j] != 0:
            #print('A')
            #print(r_flows[j])
            g[i].addEdge(j, j+1, r_flows[j])
            g[i].addEdge(j+1, j, -1*(r_flows[j]))
        if f_flows[j] != 0:
            g[i].addEdge(j, j+int(num_columns), f_flows[j])
            g[i].addEdge(j+int(num_columns), j, -1*(f_flows[j]))
    #print('A')
    #print(g[i].top_order)
    #print('B')
    g[i].topologicalSort()
    #print(g[i].top_order)
    for k in range (0, (int(num_nodes))):
        print(k, ': ', g[i].graph[k])
        #print(k, ' cost: ', g[i].vert_dict[k])

#print(*r_flows)
#print('\n')
#print(*f_flows)

loop = True
if len(g) == 1:
    period = 1
else:
    period = int(periods)

while(loop):
#    if period == -1:
#        period = input('Which time period do you want to look at?\n')
    case = input('\nWhich command would you like to run?\n'
    'Enter the number of your desired command:\n'
    '1 - Display Neighbors\n'
    '2 - Fraction Through\n'
    '3 - Display Fraction Through Animation\n'
    '5 - Change time period\n'
    'Type \'quit\' to quit\n')
    if case == '1':
        x = input('Which node? \n')
        g[int(period)-1].displayWeight(int(x))
    elif case == '2':
        x = input('Which node? \n')
        y, z = g[int(period)-1].fractionThrough(int(x))
        drawGraph(y, z, num_nodes, num_columns)
    elif case == '3':
        x = input('Which node do you want to animate? \n')
        data = []
        for i in range(period):
            y, z = g[int(i)-1].fractionThrough(int(x))
            data.append(y)
        drawAnimation(data, z, num_nodes, num_columns, period)
    elif case == '5':
        if len(g) > 1:
            print('You are currently on period', period)
            period = input('Which time period do you want to look at?\n')
        else:
            period = 1
            print('Only 1 time period')
    elif case == 'quit':
        loop = False
    else:
        print('\n\nUNKNOWN COMMAND\n\n')
