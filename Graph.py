import Event
# A representation of graph using Adjacency List
class Graph(object):
    def __init__(self,num_events):
        self.events = [None] * num_events
        self.root_event = None
        self.contains_error = False
        self.obser_solutions = {} #key is observation, value is list of applicable solutions
        self.event_trees = []


    def add_event(self, event):
        if event.id > len(self.events):
            print(len(self.events))
            newArr = [None] * 2 * len(self.events)
            for e in self.events:
                if e is not None:
                    newArr[e.id] = e
            self.events = newArr
            self.events[event.id] = event
        else: 
            self.events[event.id] = event

    def get_events(self):
        return self.events
    
    def get_num_events(self):
        result = 0
        for e in self.events:
            if e is not None:
                result += 1
        return result
    def get_event(self,id):
        return self.events[id]
    
    def set_root_event(self, root):
        self.root_event = root
        self.add_event(root)
 

    def print_graph(self):
        for i in self.events:
            if i is not None:
                #temp = self.events[i]
                print("ID %d: %s" % (i.get_id(), i.get_content()))
                self.print_graph_helper(i.get_connections())

    def print_graph_helper(self,events):
        for event,weight in events.items():
            if weight == 3:
                self.contains_error = True
            print("\t ID %d: %s with weight = %d " % (event.get_id(), event.get_content(), weight))
    
    def connect_events_from_id(self,id1, id2,type):
        self.events[id1].add_connection(self.events[id2],type)

    def change_connection_label(self, id1,id2,new_label):
        self.events[id1].set_weight(self.events[id2],new_label)

    
    def remove_events_from_id(self,id1,id2):
        self.events[id1].remove_connection(self.events[id2])

    #Normal Depth-First-Search using eventids adapted for connected components
    def DFS_cc(self, temp, vertex, visited):
        visited[vertex] = True 
        temp.append(vertex) 
        for event in self.events[vertex].get_connections(): 
            if visited[event.id] == False: 
                temp = self.DFS_cc(temp, event.id, visited)
        return temp 
  
    #getting connected event-components using DFS 
    def get_connected_components(self): 
        visited = [] 
        cc = [] 
        for i in range(len(self.events)):
            if self.events[i] is not None:
                visited.append(False) 
        for event in self.events:
            if event is not None:
                if visited[event.id] == False: 
                    temp = [] 
                    cc.append(self.DFS_cc(temp, event.id, visited))
        self.event_trees = cc
        return cc


    def get_total_event_connections(self,id):
        event = self.events[id]
        if event.get_connections() is None:
            return 0
        result = 0
        for e in event.get_connections():
            result += self.get_total_event_connections(e.get_id())
        return event.get_num_connections() + result

    #from an initial source observation, find all yes/no direct connecting solutions,
    #and every solution that can be reached using only yes connections
    def DFS(self, event_id,visited,temp):
        visited[event_id] = True
        #print("this is the event id %d " % (event_id))
        event = self.events[event_id]
        for e in event.get_connections():
            if visited[e.id] is False and e.type is "S":
                temp.append(e.id)
                print("appended %d" %(e.id))
                self.DFS(e.id, visited,temp)
            elif visited[e.id] is False:
                self.DFS(e.id,visited,temp)

    #from src_event, @return list of all reachable nodes.
    def reachable_events(self,src_id, tree_arr,visited):
        temp = []
        print(src_id)
        for t in tree_arr:
            visited[t] = False
        event = self.get_event(src_id)
        for e in event.get_connections():
            print("connection %d" %(e.id))
            if visited[e.id] is False and (event.get_weight(e) == 2 or event.get_weight(e) == 3)  and e.type is "S":
                temp.append(e.id)
                print("appended %d" %(e.id))
                self.DFS(e.id, visited, temp)
            elif visited[e.id] is False and event.type is "O":
                #temp.append(e.id)
                print('got to elif')
                self.DFS(e.id,visited,temp)
        return temp

    def observation_solution(self):
        visited = {}
        for tree in self.event_trees:
            for t in tree:
                visited[t] = False
            for t in tree:
                self.obser_solutions[t] = self.reachable_events(t,tree,visited)
    
    def create_tree(self):
        if self.root_event is not None:
            self.root_event.set_type("O")
        self.get_connected_components()
        for tree in self.event_trees:
            if self.root_event is not None:
                if tree[0] != self.root_event.id:
                    print(tree)
                    root = self.get_event(self.root_event.id)
                    self.connect_events_from_id(self.root_event.id, tree[0], "Yes")
       # print(repr(self.get_event(root.id)))









    def __str__(self):
        return self.events



