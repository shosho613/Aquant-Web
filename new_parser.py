import re
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTRect, LTTextBox, LTCurve, LTText, LTLine
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from Event import Event
from Graph import Graph

class Arrow(object):

    def __init__(self, arrow):
        self.obj = arrow
        self.label = None
        self.source = None
        self.dest = None
        self.connected_to = None #if leading to another arrow
        self.direction = None #direction arrow is leading from

    def set_label(self, label):
        self.label = label
    
    def set_source(self, source_rect):
        self.source = source_rect
    
    def set_dest(self, dst_rect):
        self.dest = dst_rect
    
    def set_connected_to(self,arrow):
        self.connected_to = arrow

class new_Parser(object):
    def __init__(self,pdf_name):
        self.rect_content = {}
        self.rects = []
        self.boxes = []
        self.arrows = []
        self.arrow_labels = []
        self.root_event = None
        self.pdf_name = pdf_name
        self.graph = None
    

    def with_pdf(self, fn, *args):
        result = None
        try:
            fp = open(self.pdf_name, "rb")

            # create a parser object associated with the file object
            parser = PDFParser(fp)
            # create a PDFDocument object that stores the document structure
            doc = PDFDocument(parser)
            # connect the parser and document obj
            parser.set_document(doc)
            if doc.is_extractable:
                # apply the function and return the result
                result = fn(doc, *args)
                fp.close()
        except IOError:
            print("IOError")
            pass
        return result


    def getLayout(self,doc, pagenum):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for i, page in enumerate(PDFPage.create_pages(doc)):
            if i + 1 == pagenum:
                interpreter.process_page(page)  # find page, process it using interpreter
                break
        # get page layout
        layout = device.get_result()
        return layout
    
    # sifts layout objects into specific lists
    def categorize_layout(self,doc, pagenum):
        layout = self.getLayout(doc, pagenum)
        pointer = None
        line = None
        for lt_obj in layout:
            if isinstance(lt_obj, LTCurve) and not isinstance(lt_obj, LTRect) and not isinstance(lt_obj, LTLine):
                arrow = Arrow(lt_obj)
                self.arrows.append(arrow)
            if isinstance(lt_obj, LTRect):
                self.rects.append(lt_obj)
            if isinstance(lt_obj, LTTextBox):
                print(lt_obj)
                self.boxes.append(lt_obj)
            if isinstance(lt_obj, LTText):
                for line in lt_obj:
                    str = line.get_text()
                    if "Yes" == re.sub("\s+", "", str) or "No" == re.sub("\s+", "", str):
                        self.arrow_labels.append(line)

    @staticmethod
    def isTextLine_inRect(rect, line):
        if rect.x0 <= line.x0 and rect.y1 >= line.y1 and rect.x1 >= line.x1 and rect.y0 <= line.y0:
            return True
        else: return False

    def remove_duplicate_rects(self):
        toremove = set([])
        for i in range(0, len(self.rects)):
            for j in range(1, len(self.rects)):
                rect1 =  self.rects[i]
                rect2 = self.rects[j]
                if rect1 is not None and rect2 is not None:
                    if rect1.x0 == rect2.x0 and rect1.x1 == rect2.x1 and rect1.y0 == rect2.y0 and rect1.y1 == rect2.y1 and j != i :
                        #print("this is i: %d" % (i))
                        #print("this is j: %d" % (j))
                        self.rects[j] = None
        for rect in self.rects:
            if rect is None:
                self.rects.remove(rect)
        print(len(self.rects))

    # find the text content in boxes
    def recognize_textboxes(self):
        #print(self.boxes)
        id = 0
        for rect in self.rects:
            #print(rect)
            box_content = ""
            for box in self.boxes:
                for line in box:
                    if self.isTextLine_inRect(rect,
                                         line):  # compare the boundaries of the rectangle to each textline within textbox
                        box_content += line.get_text()  # if so, add to box_content
                        #print("added, box content is now %s" % (box_content))                        
                

            if box_content != "":
                #self.rects.remove(rect)
                #print("box xontent is %s" % (box_content))
                self.rect_content[rect] = Event(id,box_content)
                id+=1
        self.root_event = Event(id, self.boxes[0].get_text())
                
       


    def add_connections(self):
        print(len(self.arrows))
        self.set_arrow_sources()
        self.set_arrow_connections()
        self.set_arrow_destination()
        for arrow in self.arrows:
            if arrow.source is not None and arrow.dest is not None:
                print("here")
                print(self.rect_content[arrow.source])
                print(arrow.direction)
                print(arrow.obj)
                #print("Label:")
                #print(arrow.label)
                print("------------")
                print(self.rect_content[arrow.dest])
    
    #to do: organize vertical labels.  
    def set_arrow_sources(self):
        for arrow in self.arrows:
            
            src_tuple = self.trace_arrow_src(arrow.obj)
            
            if src_tuple is not None:
                print(src_tuple)
                arrow.set_source(src_tuple[0])
                arrow.direction = src_tuple[1]
    
    def set_arrow_connections(self):
        for arrow in self.arrows:
            arrow_connect = self.is_arrow_connected(arrow.obj)
            if arrow_connect is not None:
                arrow.connected_to = Arrow(arrow_connect)
    
    def set_arrow_destination(self):
        for arrow in self.arrows:
            if arrow.connected_to is None:
                dst_rect = self.trace_arrow_dst(arrow.obj, arrow.direction)
                arrow.set_dest(dst_rect)
                label = self.get_arrow_label(arrow.obj)
                if label is not None:
                    arrow.label = label
                
            else:
                dst_rect = self.trace_arrow_dst(arrow.connected_to.obj, arrow.direction)
                arrow.set_dest(dst_rect)
                label = self.get_arrow_label(arrow.obj)
                if label is not None:
                    arrow.label = label


    #this will trace arrow to its destination coordinates, and return the rectangle if it points to one, or return a arrow if it points to one
    def trace_arrow_dst(self,arrow, direction):
        destX = arrow.x1
        destY = arrow.y1
        if direction is 'right':
            return self.closest_rect_right_arrow(arrow)
        if direction is 'above':
            return self.closest_rect_belowarrow(arrow)
        if direction is 'left':
            proximity = 100
            closest_rect = None
            for rect in self.rect_content:
                if proximity > destX - rect.x1 > 0 and rect.y1 > destY > rect.y0:
                    proximity = destX - rect.x1
                    closest_rect = rect
            return closest_rect

    #return the rectangle it is point out from eg rect->arrow / arrow<-rect
    def trace_arrow_src(self,arrow):
        srcX = arrow.x0
        srcY = arrow.y0
        closest_rect_left = None
        closest_rect_right = None
        closest_rect_above = None
        Yproximity_left = 100
        Yproximity_right = 100
        Xproxmity_above = 20
        for rect in self.rect_content:
            if rect.y1 > srcY > rect.y0: #if within boundries of height, means it comes out of side of rect
                if 0 < rect.x0 - srcX < Yproximity_left:  #check if rect pointing out of left side
                    Yproximity_left = rect.x0 - srcX
                    closest_rect_left = rect
                if 0 < srcX - rect.x1 < Yproximity_right:
                    Yproximity_right = srcX - rect.x1
                    closest_rect_right = rect
                    #if closest_rect_right is not None:
                        #print(self.rect_content[closest_rect_right])
        if Yproximity_left < Yproximity_right:
            #self.rects.remove(closest_rect_left)
            return (closest_rect_left, "left") #return rect and that arrow is coming out of left
        elif Yproximity_left > Yproximity_right:
            #self.rects.remove(closest_rect_right)
            return (closest_rect_right, "right")
        if self.closest_rect_abovearrow(arrow) is not None:
            return(self.closest_rect_abovearrow(arrow), "above")
    

    #checks if arrow is connected to another arrow, if it is, return that arrow, else return None
    def is_arrow_connected(self,arrow):
        dstX = arrow.x1
        dstY = arrow.y1
        Xproximity = 40
        Yproximity = 50
        arrow_connected = None
        for arr in self.arrows:
            a = arr.obj
            if not(a.x1 == arrow.x1 and a.x0 == arrow.x0 and a.y0 == arrow.y0 and a.y1 == arrow.y1):
                #print("here")
                if a.y0 < dstY < a.y1:
                    #print(dstX-a.x0)
                    if 0 < dstX- a.x0 < Xproximity:
                        Xproximity = dstX - a.x0
                        arrow_connected = a
                elif a.x0 < dstX < a.x1:
                    if 0 < a.y0 - dstY < Yproximity:
                        Yproximity =  a.y0 - dstY
                        arrow_connected = a
                
        if arrow_connected is None:
            return None
        elif arrow_connected is not None:
            #print("found connected")
            self.is_arrow_connected(arrow_connected)
        return arrow_connected







# given the pointer part of the arrow, return what is the closest rectangle
    def closest_rect_belowarrow(self,curve):
        # (curve)
        proximity = 60  ##common pixel distance between arrow and rectangle it points to
        closest_rect = None
        for rect in self.rect_content:
            if proximity > curve.y1 - rect.y1 > 0 and rect.x1 > curve.x0 > rect.x0:
                proximity = curve.y1 - rect.y1
                closest_rect = rect
        return closest_rect

    # given the line part of the arrow, return what is the closest rectangle(above)
    def closest_rect_abovearrow(self,curve):
        # print(curve) 
        proximity = 100  # common pixel distance range between rectangle and beginning of arrow.
        closest_rect = None
        for rect in self.rect_content:
            if proximity > rect.y0 - curve.y0 > 0 and rect.x1 > curve.x0 > rect.x0:
                proximity = rect.y0 - curve.y0
                closest_rect = rect
        return closest_rect


    # given the arrow, return what is the closest rectangle to the left of it RECT->curve
    def closest_rect_left_arrow(self,curve):
        proximity = 100
        closest_rect = None
        for rect in self.rect_content:
            if proximity > curve.x1 - rect.x1 > 0 and rect.y1 > curve.y0 > rect.y0:
                proximity = curve.x1 = rect.x1
                closest_rect = rect
        return closest_rect


    # given the arrow, return what is the closest rectangle to the right of it curve->RECT
    def closest_rect_right_arrow(self,curve):
        proximity = 100
        closest_rect = None
        for rect in self.rect_content:
            if proximity > rect.x0 - curve.x0 > 0 and rect.y1 > curve.y0 > rect.y0:
                proximity = rect.x0 - curve.x0
                closest_rect = rect
        return closest_rect

    def build_graph_from_pdf(self,doc, pagenum):
        self.categorize_layout(doc, pagenum)
        self.remove_duplicate_rects()
        self.recognize_textboxes()
        #self.process_labels()

        self.add_connections()
        G = Graph(len(self.rect_content.values()) + 1)
        print(len(self.rect_content.values()))
        #G.set_root_event(self.root_event)
        print(repr(G.root_event))
        for arrow in self.arrows:
            if arrow.source is not None and arrow.dest is not None:
                source_event = self.rect_content[arrow.source]
                dst_event = self.rect_content[arrow.dest]
                source_event.add_connection(dst_event, arrow.label)
        for value_tuple in self.rect_content.values():
            G.add_event(value_tuple)
        return G

    #return true if given arrow is closest to given line
    @staticmethod
    def textline_labels_arrow(line, curve, h_proximity, y_proximity):
        return new_Parser.arrow_labels_horizontally(line,curve,h_proximity) or new_Parser.arrow_labels_vertically(line,curve,y_proximity)

    @staticmethod
    def arrow_labels_horizontally(line, curve, proximity):
        return proximity > line.x0 - curve.x0 > 0 and (line.y1 > curve.y1 or curve.y0 > line.y0)

    @staticmethod
    def arrow_labels_vertically(line,curve,proximity):
        return proximity > line.y0 - curve.y0 > 0 and (line.x1 > curve.x1 or curve.x0 > line.x0)

    # given an arrow, return str of its label
    def get_arrow_label(self,curve):
        closest_label = None
        h_proximity = 20
        y_proximity = 20
        for label in self.arrow_labels:
            if new_Parser.textline_labels_arrow(label, curve,h_proximity, y_proximity):
                closest_label = label
                h_proximity = label.x0 - curve.x0
                y_proximity = label.y0 - curve.y0
        if closest_label is not None:
            str = closest_label.get_text()
            self.arrow_labels.remove(closest_label)
            return str
        else: return None
def main():
    pdf_parser = new_Parser("ComplexTree.pdf")
    print(pdf_parser.pdf_name)
    result = pdf_parser.with_pdf(pdf_parser.build_graph_from_pdf, 60)
    print("printing graph")
    for event in result.events:
        print(repr(event))



if __name__ == "__main__":
    main()