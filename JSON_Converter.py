import json
from PDF_Parser import PDF_Parser
from Graph import Graph

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
        self.json_rep['connections'] = []
        for event in self.graph.events:
            self.json_rep['nodes'].append({
                'id': event.id,
                'content': event.content,
                'type': None
            })
            for e,weight in event.get_connections().items():
                if weight == 2:
                    content = "Yes"
                elif weight == 1:
                    content = "No"
                else:
                    content = "Label Connection!"
                self.json_rep['connections'].append({
                    'id': "%s->%s"%(event.id, e.id),
                    'sourceID': event.id,
                    'targetID': e.id,
                    'content': content
                })
        with open('data.txt', 'w') as outfile:  
            json.dump(self.json_rep, outfile)


def main():
    jc = JSON_Converter()
    jc.get_graph_from_filename("Rational Troubleshooting guide.pdf", 36)
    for i in jc.graph.get_events():
        print(repr(i))
    jc.get_json_graph()
    print(json.dumps(jc.json_rep, indent=4))

if __name__ == "__main__":
    main()

