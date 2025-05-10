# HASH WATERMARK: f4442691a8dcb41258233448d5429f4064778242e0d75f4f92e9ef464c3263ae
# MADE BY JAKE MAYER


import networkx as nx
import matplotlib.pyplot as plt
import string
import random

# class for SDN controller
class sdn:
    def __init__(self):
        self.graph = nx.Graph()
        self.flowtables = {}
        plt.ion()
        plt.show()
        self.pos = None
        self.colors = {}
        n = 8
        m = 12

        # initiallization for intial nodes
        routers = ["R" + str(i+1) for i in range(n)]
        self.add_node(n)
        unlinked = ["R" + str(i+1) for i in range(n)]
        for i in range(m):
            if(len(unlinked)>0):
                a = unlinked.pop(random.randint(0,len(unlinked)-1))
            else:
                a = routers[random.randint(0,n-1)]
            b = a
            while b == a or self.graph.has_edge(a,b):
                b = routers[random.randint(0,n-1)]
            
            self.graph.add_edge(a,b,weight=0)
            
        self.pos = nx.shell_layout(self.graph)
        self.update_graph()
            
    #function for ading multiple nodes to the graph
    def add_node(self, n):
        n = int(n)
        s = ""
        j=0
        for i in range(n):
            j += 1
            node = "R"+ str(j)
            #avoid duplicating nodes that exist
            while node in self.flowtables:
                j += 1
                node = "R"+ str(j)

            self.graph.add_node(node)

            #setup blank flowtables for each node
            self.flowtables[node] = {}
            self.colors[node] = "lightblue"
            s += str(node) + " "
        if s == "":
            print("No nodes could be made.")
            return
        
        ## print what nodes were created
        print("Node",end="")
        if n>1:
            print("s",end="")
        print(f" {s}added.")

        # update graph
        self.pos = nx.shell_layout(self.graph)
        self.update_graph()

    # function for adding links to the graph
    def add_link(self, nums):
        nodes = []
        # verify that nodes exist before linking
        for n in nums:
            try:
                temp = int(n)
                nodes.append("R" + n)
            except ValueError:
                print("Please use only numbers.")
                return
        s = ""
        if not all(node in self.graph.nodes() for node in nodes):
            print("Missing nodes.")
            return
        
        #link all nodes in the args sequentially with a loop
        for i in range(len(nodes)-1): 
            n1 = nodes[i]
            n2 = nodes[i+1]
            #check if edge already exists
            if self.graph.has_edge(n1,n2) or n1 == n2:
                if len(nodes)<3:
                    break
                continue
            self.graph.add_edge(n1,n2,weight=0)
            s += str(n1) + "-" + str(n2) + " "

        # print the results
        if s == "":
            print("No links could be made.")
            return
        print("Link",end="")
        if len(nodes)>2:
            print("s",end="")
        print(f" {s}added.")

        #update graph
        self.pos = nx.shell_layout(self.graph)
        self.update_graph()
    
    #function to remove a node
    def delete_node(self, nums):

        #check if nodes exist to be removed
        nodes = []
        for n in nums:
            try:
                temp = int(n)
                nodes.append("R" + n)
            except ValueError:
                print("Please use only numbers.")
                return
        s = ""
        for node in nodes:
            if self.graph.has_node(node):

                #remove node, tables, and colors for graph
                self.graph.remove_node(node)
                self.flowtables.pop(node)
                self.colors.pop(node)
                s += str(node) + " "

        #print results
        if s == "":
            print("No nodes to remove.")
            return
        print("Node",end="")
        if len(nodes)>1:
            print("s",end="")
        print(f" {s}removed.")

        #update graph
        self.pos = nx.shell_layout(self.graph)
        self.update_graph()        

    #function for deleting links
    def delete_link(self, nums):
        s = ""
        nodes = []

        #verify args and wheter nodes exist
        for n in nums:
            try:
                temp = int(n)
                nodes.append("R" + n)
            except ValueError:
                print("Please use only numbers.")
                return
        s = ""
        if not all(node in self.graph.nodes() for node in nodes):
            print("Missing nodes.")

        #check for links and remove them
        for i in range(len(nodes)-1): 
            n1 = nodes[i]
            n2 = nodes[i+1]
            if self.graph.has_edge(n1,n2):
                self.graph.remove_edge(n1,n2)
                s += str(n1) + "-" + str(n2) + " "
        
        #print results
        if s == "":
            print("No links to remove.")
            return
        print("Link",end="")
        if len(nodes)>2:
            print("s",end="")
        print(f" {s}removed.")

        #update graph
        self.pos = nx.shell_layout(self.graph)
        self.update_graph()

    #function to update the graph
    def update_graph(self):
        plt.clf()

        #pull dict of colors from private variable
        colors = [self.colors[n] for n in self.graph.nodes()]

        #create the graph
        
        plt.title("SDN Graph")
        nx.draw(self.graph, self.pos, with_labels=True, node_color=colors)

        #add labels to showcase link utilization
        labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=labels)

        #allow for graph to process
        plt.pause(0.01)
    
    #function to update flow tables
    def update_flows(self, src):

        #use dijkstra algorithm for shortest path to every accessible node
        lengths, paths = nx.single_source_dijkstra(self.graph,src)
        for dst, path in paths.items():
            if src != dst:

                # store results in flowtables
                self.flowtables[src][dst] = path[0]
                for i in range(len(path)-1):
                        self.flowtables[path[i]][dst] = path[i+1]

    #function for sending flows on the graph
    def send_flows(self,nums,crit=False):
        srcs = []

        #loop through every arg item
        for n in nums:

            #validate inputs
            try:
                temp = int(n)
                if not self.graph.has_node("R"+n):
                    print("Missing nodes.")
                    return
                srcs.append("R" + n)
            except ValueError:
                print("Please use only numbers.")
                return
            
        #begin sending flows
        for i in range(len(srcs)-1):
            src = srcs[i]
            dst = srcs[i+1]
            #update for latest paths
            self.update_flows(src)
            #go to next flow if no path exists
            if self.flowtables[src][dst] == {}:
                print(f"No path from {src} to {dst}.")
                continue
            path = []

            #set color of goal
            self.colors[dst] = "orange"

            #loop through flowtables until the end is reached
            while True:

                #change color of current node
                self.colors[src]= "lime"

                #update graph to make flow animated
                self.update_graph()
                plt.pause(0.5)

                #add node to path traversed 
                path.append(src)

                #change color of previous node
                self.colors[src] = "yellow"

                #leave loop if destination is reached
                if(src == dst):
                    break
                #adjust to next node using flowtables
                src = self.flowtables[src][dst]

                #increment usage value of link between nodes (influences load balancing as well)
                self.graph[path[-1]][src]["weight"]+=1

            #reset node colors
            for node in path:
                self.colors[node] = "lightblue"
            
            #update graph
            self.update_graph()
            plt.pause(0.5)
        
        
    #function to print flowtables
    def print_table(self, n = None):
        src=""

        #validate input
        try:
            temp = int(n)
            src = "R" + n
        except ValueError:
            print("Please use only numbers.")
            return
        
        #verify node exists
        if not self.graph.has_node(src):
            print("Node Missing.")
            return
        
        #update flows for latest flow table
        self.update_flows(src)

        col1_width = 12
        col2_width = 12
        total_width = col1_width + col2_width + 5

        #crazy print statements to make flowtable look pretty
        print(f"+{"-" * (total_width - 2)}+")
        print(f"| {src} Routing Table".ljust(total_width - 1) + "|")
        print(f"+{"-" * (total_width - 2)}+")
        print(f"| {'Destination':<{col1_width}}| {'Next Hop':<{col2_width}}|")
        print(f"+{"-" * (col1_width+1) +"+"+"-" * (col1_width+1)}+")
        for dst, path in self.flowtables[src].items():
            print(f"| {dst:<{col1_width}}| {path:<{col2_width}}|")
        print(f"+{"-" * (total_width - 2)}+")
controller = sdn()

#CLI implementation here :)
print("welcome to the SDN Control Plane!")
while True:
    
    #takes input here
    cmd = input(">> ").strip()
    args = cmd.split()
    a0 = args[0].lower()

    #checks to see which command matches input and then calls corresponding funcitons
    if a0 == "node":
        controller.add_node(args[1])
    elif a0 == "link":
        controller.add_link(args[1:])
    elif a0 == "route":
        controller.send_flows(args[1:])
    elif a0 == "table":
        controller.print_table(args[1])
    elif a0 == "q":
        break
    elif a0 == "del":
        if args[1].lower() == "link":
            controller.delete_link(args[2:])
        else:
            controller.delete_node(args[1:])
    
    #A little command help menu
    elif a0 == "help":
        print("\nList of Commands: (Use numbers to represent nodes!)\n")
        print("  node x                 - Creates x number of nodes (e.g., 'node 5').")
        print("  link x1 x2 [x3...]     - Links node x1 to x2, x2 to x3, etc.")
        print("  del x1 [x2...]         - Deletes nodes x1, x2, etc.")
        print("  del link x1 x2 [x3...] - Deletes link(s) between x1 and x2, x2 and x3, and so on.")
        print("  route x1 x2 [x3...]    - Sends flow from x1 to x2 and x2 to x3 and so on.")
        print("  table x                - Displays the routing table for node x.")
        print("  q                      - Exits the program.\n")
    else:
        print("Invalid input. Enter \"help\" for a list of inputs.")
