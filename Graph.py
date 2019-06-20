import Event
# A representation of graph using Adjacency List
class Graph(object):
    def __init__(self,num_events):
        self.events = [None] * num_events
        self.contains_error = False
        self.obser_solutions = {} #key is observation, value is list of applicable solutions


    def add_event(self, event):
        self.events[event.id] = event

    def get_events(self):
        return self.events
    
    def get_event(self,id):
        return self.events[id]


    def print_graph(self):
        for i in self.events:
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
            visited.append(False) 
        for event in self.events: 
            if visited[event.id] == False: 
                temp = [] 
                cc.append(self.DFS_cc(temp, event.id, visited))
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

        event = self.events[event_id]
        for e in event.get_connections():
            if visited[e.id] is False and e.type is "S":
                temp.append(e.id)
                self.DFS(e.id, visited,temp)
            elif visited[e.id] is False:
                self.DFS(e.id,visited,temp)

    #from src_event, @return list of all reachable nodes.
    def reachable_events(self,src_id, tree_arr):
        visited = {}
        temp = []
        for t in tree_arr:
            visited[t] = False
        event = self.get_event(src_id)
        for e in event.get_connections():
            if visited[e.id] is False and e.type is "S":
                temp.append(e.id)
                self.DFS(e.id, visited, temp)
            elif visited[e.id] is False and event.get_weight(e) == 2:
                self.DFS(e.id,visited,temp)
        return temp

    def observation_solution(self,tree_arr):
        #visited = {}
        for t in tree_arr:
            self.obser_solutions[t] = self.reachable_events(t,tree_arr)





    def __str__(self):
        return self.events



