from graph import Graph
import argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--period", type=int, dest="period", help="Number of time periods")
parser.add_argument("-n", "--nodes", type=int, dest="nodes", help="Number of nodes")
parser.add_argument("-w", "--width", type=int, dest="width", help="Width of the graph")

args = parser.parse_args()

if args.period:
    periods = args.period
else:
    periods = input('Number of time periods:\n')
#print(periods)

if args.nodes:
    num_nodes = args.nodes
else:
    num_nodes = input('Number of nodes:\n')
##print(num_nodes)

if args.width:
    num_columns = args.width
else:
    num_columns = input('What is the width of the graph:\n')
#print(num_columns)

#for line2 in sys.stdin:
#    periods = input('Number of time periods:\n')
#    num_nodes = input('Number of nodes:\n')
#    num_columns = input('What is the width of the graph:\n')

g = []

for i in range(int(periods)):
    g.append(Graph(int(num_nodes), int(num_columns)))

##  The empty list that will hold the flow values
    r_flows = []
    f_flows = []

##  Parse the right facing flow values from file.
##  The expected naming convention for the files
##  is r_flows[n].txt where n is the time period
    for line in open('r_flows' + str(i) + '.txt', 'r'):
        for char in '[]':
            line = line.replace(char, '')
            #print(line)
        words = line.split(' ')
        words = [x for x in words if x != '']
        words = [x for x in words if x != '\n']
        words = [x for x in words if x != ' ']
        #print(words)
        for string in words:
            r_flows.append(float(string))
        #print(r_flows)

    if int(num_nodes) != len(r_flows):
        print('Expected ', num_nodes, ' nodes, but ', len(r_flows), ' were given in r_flows.')
        quit()

##  Front Face
    for line in open('f_flows' + str(i) + '.txt', 'r'):
        for char in '[]':
            line = line.replace(char, '')
        #print(line)
        words = line.split(' ')
        words = [x for x in words if x != '']
        words = [x for x in words if x != '\n']
        words = [x for x in words if x != ' ']
        #print(words)
        for string in words:
            f_flows.append(float(string))
        #print(f_flows)

    if int(num_nodes) != len(f_flows):
        print('Expected ', num_nodes, ' nodes, but ', len(f_flows), ' were given in f_flows.')
        quit()

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
    for k in range (0, 100):
        #print(k, ': ', g[i].graph[k])
        print(k, ' cost: ', g[i].vert_dict[k])

#print(*r_flows)
#print('\n')
#print(*f_flows)

loop = True
if len(g) == 1:
    period = 1
else:
    period = -1

while(loop):
    if period == -1:
        period = input('Which time period do you want to look at?\n')
    case = input('\nWhich command would you like to run?\n'
    'Enter the number of your desired command:\n'
    '1 - Display Neighbors\n'
    '2 - Fraction Through\n'
    '5 - Change time period\n'
    'Type \'quit\' to quit\n')
    if case == '1':
        x = input('Which node? \n')
        g[int(period)-1].displayWeight(int(x))
    elif case == '2':
        x = input('Which node? \n')
        g[int(period)-1].fractionThrough(int(x))
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
