import json
from new_parser import new_Parser
from PDF_Parser import PDF_Parser
from Graph import Graph
from Event import Event
import csv

class JSON_Converter(object):


    def __init__(self):
        self.graph = None
        self.json_rep = {}
        self.pdf_parser = None
        self.nodeIds = {} # this dict keys the client-generated nodeID to the server side ID used 
    
    def create_parser(self, filename):
        self.pdf_parser = new_Parser(filename)
        print(self.pdf_parser.pdf_name)
    
    def get_graph_from_filename(self,pdf_name, page_num):
        pdf_parser = PDF_Parser(pdf_name)
        #pdf_parser = new_Parser(pdf_name)
        print(pdf_parser.pdf_name)
        result_graph = pdf_parser.with_pdf(pdf_parser.build_graph_from_pdf, page_num)
        self.graph = result_graph
        self.graph.create_tree()
        return result_graph
    
    def get_json_basic_graph(self):
        self.json_rep['basic'] = []
        eventArrs = self.graph.get_connected_components()
        for events in eventArrs:
            print(events)
            i = len(events) - 1
            while i > 0:
                print(i)
                child = self.graph.get_event(events[i])
                parent = self.graph.get_event(events[i-1])
                self.json_rep['basic'].append({
                'Name': "node" + str(child.id) ,
                'content': child.content,
                'eventtype': 'None',
                'ReportingPerson': "node" + str(parent.id)   
                })
                i -= 1
            if i == 0:
                child = self.graph.get_event(events[i])

                self.json_rep['basic'].append({
                'Name': "node" + str(child.id) ,
                'content': child.content,
                'eventtype': 'None', 
                })

         
        with open('data.txt', 'w') as outfile:  
            json.dump(self.json_rep, outfile)
    

    def get_JSON_nodes(self):
        self.json_rep['nodes'] = []
        for event in self.graph.events:
            if event is not None:
                idString = 'node' + str(event.id)
                self.json_rep['nodes'].append({
                    "Name" : idString,
                    "Content" : event.content,
                    "eventtype" : event.type,
                })

    def convert_to_json_nodes(self,addedEvents):
        id = self.graph.get_num_events() + 1
        rep = []
        print(addedEvents)
        for event in addedEvents:
            print(event)
            if not (event == 'undefined' or event == ''):
                self.graph.add_event(Event(id, event))
                idString = 'node' + str(id)
                rep.append({
                    'Name' : idString,
                    "Content" : event,
                    "eventtype" : "N"
                })
                id += 1
        return rep


    def get_JSON_connectors(self):
        self.json_rep['connectors'] = []
        id = 0
        for event in self.graph.events:
            if event is not None:
                for e,w in event.get_connections().items():
                    sourceID = 'node' + str(event.id)
                    targetID = 'node' + str(e.id)
                    if w == 3:
                        content ="Label!"
                    if w == 2:
                        content = "Yes"
                    if w == 1:
                        content = "No"
                    self.json_rep['connectors'].append({
                        "id" : 'connector' + str(id),
                        "sourceID" : sourceID,
                        "targetID" : targetID,
                        "content" : content
                    })
                    id += 1
        
    def get_json_graph(self):
        self.graph.create_tree()
        self.get_JSON_nodes()
        self.get_JSON_connectors()
    
    def get_raw_graph(self):
        self.graph.create_tree()
        result = []
        for event in self.graph.events:
            result.append({
                "id" : str(event.id),
                "content" : str(event.content),
                "eventtype" : str(event.type),
                "connections" : self.get_event_rep(event.get_connections())
            })
        return result

    def get_event_rep(self, events):
        result = []
        for event in events:
            result.append({
                "id" : str(event.id),
                "content" : str(event.content),
                "eventtype" : str(event.type),
            })
        return result


    
    def set_types(self, events):
        for event in events:
            id = int(event['id'].split('node')[1])
            eventtype = 'N'
            if str(event['eventtype']) == 'O':
                eventtype = 'O'
            elif str(event['eventtype']) == 'S':
                eventtype = 'S'
            self.graph.get_event(id).set_type(eventtype)
    
    def run_algo(self):
        self.graph.get_connected_components()
        self.graph.observation_solution()
        print(self.graph.obser_solutions)
    
    def create_csv(self):
        with open("output.csv", "w+") as csvfile:
            filewriter = csv.writer(csvfile)
            map = self.graph.obser_solutions
            filewriter.writerow(["Observation", "Solution"])
            for o,solutions in map.items():
                print(self.graph.get_event(o))
                if len(solutions) > 0 :
                    print(solutions)
                    for s in solutions:
                        try:
                            print(self.graph.get_event(o))
                            print(self.graph.get_event(s))
                            filewriter.writerow([self.graph.get_event(o).get_content().replace('\n',''), self.graph.get_event(s).get_content().replace('\n','')])
                        except UnicodeError:
                            pass
        return csv
    
    def add_nodes(self, stringArr):
        currentID = 0
        nodeArr = json.loads(stringArr)
        self.graph = Graph(len(nodeArr))
        for node in nodeArr:
            id = currentID
            self.nodeIds[node['id']] = id
            currentID += 1
            print(node['addInfo'][0])
            event = Event(int(id), node['annotations'][0]['content'])
            if node['addInfo'][0]['eventtype'] == 'O':
                event.set_type('O')
            elif node['addInfo'][0]['eventtype'] == 'S':
                event.set_type('S')
            else:
                event.set_type('N')
            self.graph.add_event(event)

    def add_connections(self, stringArr):
        connectionArr = json.loads(stringArr)
        for c in connectionArr:
            try:
                print(c)
                sourceID = self.nodeIds[c['sourceID']]
                targetID = self.nodeIds[c['targetID']]
                self.graph.connect_events_from_id(sourceID,targetID, c['annotations'][0]['content'])
            except Exception as e: 
                print(e)





    


def main():
    jc = JSON_Converter()
    jc.get_graph_from_filename("Rational Troubleshooting guide.pdf", 36)
    for i in jc.graph.get_events():
        print(repr(i))
    jc.get_json_basic_graph()
    print(json.dumps(jc.json_rep, indent=4))

if __name__ == "__main__":
    main()

