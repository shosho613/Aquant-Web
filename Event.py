import re
class Event(object):

    def __init__(self,id,content):
        self.content = content
        self.id = id
        self.type = None
        self.connected_events = {} # <key,value> = <event, weight>

    def get_content(self):
        return self.content

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def set_type(self, type): # O = observation, S= solution, N = neither/disregard
        self.type = type

    def get_connections(self):
        return self.connected_events

    def get_num_connections(self):
        if len(self.connected_events) == None:
            return 0
        else: return len(self.connected_events)

    def add_connection(self, event,connection_type):
        if connection_type == None:
            self.connected_events[event] = 3
            print("added event with NONE connection %s" % (event))
        elif "Yes" == re.sub("\s+", "", connection_type):
            self.connected_events[event] = 2
            print("added event with yes connection %s" % (event))
        elif "No" == re.sub("\s+", "", connection_type):
            self.connected_events[event] = 1
            print("added event with no connection %s" % (event))
    
    def remove_connection(self,event):
        self.connected_events.pop(event)

    def get_weight(self,event):
        return self.connected_events[event]

    def set_weight(self,event,new_weight):
        if "Yes" == re.sub("\s+", "", new_weight):
            self.connected_events[event] = 2
            print("added event with yes connection %s" % (event))
        elif "No" == re.sub("\s+", "", new_weight):
            self.connected_events[event] = 1
            print("added event with no connection %s" % (event))



    def __str__(self):
        return self.content

    def __repr__(self):
        return "<Event> %s, %d, %d, %s" %(self.content, self.id, self.get_num_connections(), self.get_type())