import json
from PDF_Parser import PDF_Parser
from Graph import Graph
import csv

class JSON_Converter(object):


    def __init__(self):
        self.graph = None
        self.json_rep = {}
        self.pdf_parser = None
    
    def create_parser(self, filename):
        self.pdf_parser = PDF_Parser(filename)
        print(self.pdf_parser.pdf_name)
    
    def get_graph_from_filename(self,pdf_name, page_num):
        pdf_parser = PDF_Parser(pdf_name)
        print(pdf_parser.pdf_name)
        result_graph = pdf_parser.with_pdf(pdf_parser.build_graph_from_pdf, page_num)
        self.graph = result_graph
        return result_graph
    
    def get_json_graph(self):
        self.json_rep['nodes'] = []
        eventArrs = self.graph.get_connected_components()
        for events in eventArrs:
            print(events)
            i = len(events) - 1
            while i > 0:
                print(i)
                child = self.graph.get_event(events[i])
                parent = self.graph.get_event(events[i-1])
                self.json_rep['nodes'].append({
                'Name': "node" + str(child.id) ,
                'content': child.content,
                'eventtype': 'None',
                'ReportingPerson': "node" + str(parent.id)   
                })
                i -= 1
            if i == 0:
                child = self.graph.get_event(events[i])

                self.json_rep['nodes'].append({
                'Name': "node" + str(child.id) ,
                'content': child.content,
                'eventtype': 'None', 
                })

         
        with open('data.txt', 'w') as outfile:  
            json.dump(self.json_rep, outfile)
    
    def set_types(self, events):
        for event in events:
            id = int(event['Name'].split('node')[1])
            eventtype = 'N'
            if str(event['eventtype']) == 'Observation':
                eventtype = 'O'
            elif str(event['eventtype']) == 'Solution':
                eventtype = 'S'
            self.graph.get_event(id).set_type(eventtype)
    
    def run_algo(self):
        for tree in self.graph.event_trees:
            self.graph.observation_solution(tree)
        print(self.graph.obser_solutions)
    
    def create_csv(self):
        with open("output.csv", "w+") as csvfile:
            filewriter = csv.writer(csvfile)
            map = self.graph.obser_solutions
            for o,solutions in map.items():
                if solutions:
                    to_write = []
                    to_write.append(self.graph.get_event(o).get_content())
                    for s in solutions:
                        to_write.append(self.graph.get_event(s).get_content())
                    filewriter.writerow(to_write)


    


def main():
    jc = JSON_Converter()
    jc.get_graph_from_filename("Rational Troubleshooting guide.pdf", 36)
    for i in jc.graph.get_events():
        print(repr(i))
    jc.get_json_graph()
    print(json.dumps(jc.json_rep, indent=4))

if __name__ == "__main__":
    main()

