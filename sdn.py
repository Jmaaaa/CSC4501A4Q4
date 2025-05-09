import networkx as nx
import matplotlib.pyplot as plt
import string
import random

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
        letters = list(string.ascii_uppercase[:n])
        self.add_node(letters)
        unwebbed = list(string.ascii_uppercase[:n])
        for i in range(m):
            if(len(unwebbed)>0):
                a = unwebbed.pop(random.randint(0,len(unwebbed)-1))
            else:
                a = letters[random.randint(0,len(letters)-1)]
            b = a
            while b == a or self.graph.has_edge(a,b):
                b = letters[random.randint(0,len(letters)-1)]
            
            self.graph.add_edge(a,b,weight=0)
            
        self.pos = nx.shell_layout(self.graph)
        self.update_graph()
            

    def add_node(self, nodes):
        s = ""
        for node in nodes:
            if node in self.flowtables:
                if len(nodes)<2:
                    break
                continue
            self.graph.add_node(node)
            self.flowtables[node] = {}
            self.colors[node] = "lightblue"
            s += str(node) + " "
        if s == "":
            print("No nodes could be made.")
            return
        print("Node",end="")
        if len(nodes)>1:
            print("s",end="")
        print(f" {s}added.")
        self.pos = nx.spring_layout(self.graph)
        self.update_graph()

    def add_link(self, nodes):
        s = ""
        if not all(node in self.graph.nodes() for node in nodes):
            print("Missing nodes.")
            return
        for i in range(len(nodes)-1): 
            n1 = nodes[i]
            n2 = nodes[i+1]
            if self.graph.has_edge(n1,n2) or n1 == n2:
                if len(nodes)<3:
                    break
                continue
            self.graph.add_edge(n1,n2,weight=0)
            s += str(n1) + "-" + str(n2) + " "
        if s == "":
            print("No links could be made.")
            return
        print("Link",end="")
        if len(nodes)>2:
            print("s",end="")
        print(f" {s}added.")
        self.pos = nx.spring_layout(self.graph)
        self.update_graph()
        
    def delete_node(self, nodes):
        s = ""
        for node in nodes:
            if self.graph.has_node(node):
                self.graph.remove_node(node)
                self.flowtables.pop(node)
                self.colors.pop(node)
                s += str(node) + " "
        if s == "":
            print("No nodes to remove.")
            return
        print("Node",end="")
        if len(nodes)>1:
            print("s",end="")
        print(f" {s}removed.")
        self.pos = nx.spring_layout(self.graph)
        self.update_graph()        

    def delete_edge(self, nodes):
        s = ""
        if not all(node in self.graph.nodes() for node in nodes):
            print("Missing nodes.")
        for i in range(len(nodes)-1): 
            n1 = nodes[i]
            n2 = nodes[i+1]
            if self.graph.has_edge(n1,n2):
                self.graph.remove_edge(n1,n2)
                s += str(n1) + "-" + str(n2) + " "
        if s == "":
            print("No links to remove.")
            return
        print("Link",end="")
        if len(nodes)>2:
            print("s",end="")
        print(f" {s}removed.")
        self.pos = nx.spring_layout(self.graph)
        self.update_graph()

    def update_graph(self):
        plt.clf()
        colors = [self.colors[n] for n in self.graph.nodes()]

        nx.draw(self.graph, self.pos, with_labels=True, node_color=colors)

        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels)
        plt.title("lol")
        plt.pause(0.01)
        #nx.draw_networkx_edge_labels()
    
    def update_flows(self, src):

        lengths, paths = nx.single_source_dijkstra(self.graph,src)
        for dst, path in paths.items():
            if src != dst:
                self.flowtables[src][dst] = path[0]
                for i in range(len(path)-1):
                        self.flowtables[path[i]][dst] = path[i+1]

    def send_flows(self,srcs,crit=False):
        for i in range(len(srcs)-1):
            src = srcs[i]
            dst = srcs[i+1]
            self.update_flows(src)
            path = []
            self.colors[dst] = "orange"
            while True:
                self.colors[src]= "lime"
                self.update_graph()
                plt.pause(0.5)
                path.append(src)
                self.colors[src] = "yellow"
                if(src == dst):
                    break
                src = self.flowtables[src][dst]
                self.graph[path[-1]][src]["weight"]+=1
            for node in path:
                self.colors[node] = "lightblue"
            self.update_graph()
            plt.pause(0.5)
        
        

    def print_table(self, src = None):
        if not self.graph.has_node(src):
            return
        self.update_flows(src)
        print(f"{src} {"Destination":>5} {"Bext Hop":>10}")
        for dst, path in self.flowtables[src].items():
            print(f"{dst:>5} {path:>10}")

        # for src,table in self.flowtables.items():
        #     print(f"{src} {"dst":>5} {"path":>10}")
        #     self.update_flows(src)
        #     for dst, path in table.items():
        #         print(f"{dst:>5} {path:>10}")
            


controller = sdn()
print("welcome to SDN")
while True:
    
    cmd = input(">> ").strip()
    args = cmd.split()
    a0 = args[0].lower()

    if a0 == "node":
        controller.add_node(args[1:])
    elif a0 == "link":
        controller.add_link(args[1:])
    elif a0 == "send":
        controller.send_flows(args[1:])
    elif a0 == "table":
        controller.print_table(args[1])
    elif a0 == "end":
        break
    elif a0 == "del":
        if args[1].lower() == "link":
            controller.delete_edge(args[2:])
        else:
            controller.delete_node(args[1:])