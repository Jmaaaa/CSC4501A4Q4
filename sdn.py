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
        letters = list(string.ascii_uppercase[:12])
        self.add_node(letters)
        web=[]
        while len(letters) > 0:
            letter = letters.pop(random.randint(0,len(letters)-1))
            if len(web)==0:
                web.append(letter)
            else:
                self.add_link([letter,web[random.randint(0,len(web)-1)]])
                web.append(letter)
            
            

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
            if self.graph.has_edge(n1,n2):
                if len(nodes)<3:
                    break
                continue
            self.graph.add_edge(n1,n2)
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
        plt.title("lol")
        plt.pause(0.01)
        #nx.draw_networkx_edge_labels()
    
    def update_flows(self, id):
        #nx.all_shortest_paths()

        lengths, paths = nx.single_source_dijkstra(self.graph,id)
        for dst, path in paths.items():
            if id != dst:
                self.flowtables[id][dst] = path[0]
                for i in range(len(path)-1):
                        self.flowtables[path[i]][dst] = path[i+1]

    def send_flow(self,src,dst,crit=False):
        self.update_flows(src)
        path = []
        while True:
            self.colors[src]= "lime"
            self.update_graph()
            plt.pause(0.5)
            path.append(src)
            self.colors[src] = "yellow"
            if(src == dst):
                break
            src = self.flowtables[src][dst]
        for node in path:
            self.colors[node] = "lightblue"
        self.update_graph()
        plt.pause(0.5)
            
    def send_flows(self,n,flow,dst,crit=False):
        flows = [flow for j in range(int(n))]
        done = [False for flow in flows]
        colors = ["lime","teal","pink"]
        paths = [[] for flow in flows]
        while not all(done):
            for i in range(len(flows)):
                if(done[i]):
                    continue
                src = flows[i]
                self.update_flows(src)
                paths[i].append(src)
                if(src == dst):
                    done[i]= True
                    continue
                flows[i] = self.flowtables[src][dst]
                self.graph[src][flows[i]]['weight'] = 10
                self.colors[flows[i]]=colors[i%3]
                self.colors[paths[i][-1]] = "yellow"
                plt.pause(0.3)
                self.update_graph()
        for path in paths:
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
        if len(args) > 3:
            controller.send_flows(args[1],args[2],args[3])
        else:
            controller.send_flow(args[1],args[2])
    elif a0 == "table":
        controller.print_table(args[1])
    elif a0 == "end":
        break
    elif a0 == "del":
        if args[1].lower() == "link":
            controller.delete_edge(args[2:])
        else:
            controller.delete_node(args[1:])