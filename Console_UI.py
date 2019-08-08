from PDF_Parser import PDF_Parser
from Graph import Graph
import csv
#class to test backend using a console user interface
class Console_UI(object):

    def __init__(self):
        self.graph = None


    #user inputs the filename and pagenum to be parsed
    def get_graph_from_input(self):
        pdf_name = input("Please Enter PDF File to be parsed: ")
        #print("The pdf name is: " + pdf_name)
        page_num = eval(input("Please Enter page number of PDF File to be parsed: "))
        print(type(page_num))
        pdf_parser = PDF_Parser(pdf_name)
        result_graph = pdf_parser.with_pdf(pdf_parser.build_graph_from_pdf, page_num)
        self.graph = result_graph
        return result_graph

    #ask user to set the type of each event
    def set_event_types(self):
        for event in self.graph.get_events():
            print(event.get_content())
            type = input("Please enter the TYPE of the above event.\n S = Solution \n O = Observation \n N = None/Disregard\n")
            event.set_type(type)

    def print_help(self):
        print("Available Functions:\n p = print parsed page\n d = dump all identfying info of parsed page\n p id - print event with given id\n t= set all event types \n c = go to change screen \n r = run observation/solution algorithm\n h = print this help screen\n q- quit")
            
    def print_change(self):
        print("Changing?\n rm id id = remove connection from id to id \n")
    

    def set_trees(self):
        cc = self.graph.get_connected_components()
        print("Some pages have events that are part of an error tree but do not have an arrow connection.")
        for component in cc:
            if len(component) == 1:
                print(self.graph.get_event(component[0]))
                choice = input("Would you like to connect this loose component to other event tree(s)? y/n ")
                if choice == "y":
                    for other_component in cc:
                        print(other_component)
                        target_tree = input("This one? y/n ")
                        if target_tree == "y":
                            target_vertex = int(input("Enter the event id you would like to connect: "))
                            type = input("Enter type: (Yes/No)")
                            self.graph.connect_events_from_id(component[0],target_vertex,type)
    

    def handle_parse_errors(self):
        #for none connections:
        print("There are events with an unlabeled connection.")
        for event in self.graph.events:
            for e,weight in event.get_connections().items():
                if weight == 3:
                    real_label = input("What should be the connection label between: %s and %s" % (event.get_content(), e.get_content()))
                    self.graph.change_connection_label(event.id,e.id,real_label)

    def run_algo(self):
        self.graph.observation_solution()
        print(self.graph.obser_solutions)
    
    def write_to_csv(self):
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

    def driver(self):
        self.print_help()
        self.get_graph_from_input()
        self.graph.print_graph()
        self.handle_parse_errors()
        self.set_trees()
        self.set_event_types()
        self.run_algo()
        self.write_to_csv()





def main():
    console_ui = Console_UI()
    console_ui.driver()
    for i in console_ui.graph.get_events():
        print(repr(i))

if __name__ == "__main__":
    main()



