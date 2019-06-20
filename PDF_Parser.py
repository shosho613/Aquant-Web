import re
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTRect, LTTextBox, LTCurve, LTText, LTLine
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from os import path
import os

from Event import Event
from Graph import Graph


class PDF_Parser(object):
    def __init__(self,pdf_name):
        self.rect_content = {}
        self.rects = []
        self.boxes = []
        self.arrows = []
        self.arrow_labels = []
        self.pdf_name = pdf_name



    # open pdf, apply function to the PDFDocument, return the given result
    def with_pdf(self, fn, *args):
        result = None
        try:
            __location__ = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__)))
            fp = open(os.path.join(__location__, self.pdf_name), "rb");

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

    @staticmethod
    def isTextLine_inRect(rect, line):
        if rect.x0 <= line.x0 and rect.y1 >= line.y1 and rect.x1 >= line.x1 and rect.y0 <= line.y0:
            return True
        else: return False


    # sifts layout objects into specific lists
    def categorize_layout(self,doc, pagenum):
        layout = self.getLayout(doc, pagenum)
        pointer = None
        line = None
        for lt_obj in layout:
            if isinstance(lt_obj, LTCurve) and not isinstance(lt_obj, LTRect) and not isinstance(lt_obj, LTLine):
                pointer = lt_obj
                print("This is pointer: %s" % (pointer))
                self.arrows.append(lt_obj)
            if isinstance(lt_obj, LTRect):
                self.rects.append(lt_obj)
            if isinstance(lt_obj, LTTextBox):
                self.boxes.append(lt_obj)
            if isinstance(lt_obj, LTText):
                for line in lt_obj:
                    str = line.get_text()
                    if "Yes" == re.sub("\s+", "", str) or "No" == re.sub("\s+", "", str):
                        self.arrow_labels.append(line)



    # find the text content in boxes
    def recognize_textboxes(self):
        id = 0
        for rect in self.rects:
            for box in self.boxes:
                box_content = ""
                for line in box:
                    if self.isTextLine_inRect(rect,
                                         line):  # compare the boundaries of the rectangle to each textline within textbox
                        box_content += line.get_text()  # if so, add to box_content
                if box_content != "":
                    self.boxes.remove(box)  # already checked this box, so we remove.
                    event = Event(id,box_content)
                    id += 1
                    self.rect_content[rect] = event



    def add_connections(self):
        #arrow_num = 1
        for arrow in self.arrows:
            above_rect = self.closest_rect_abovearrow(arrow)
            below_rect = self.closest_rect_belowarrow(arrow)
            left_rect = self.closest_rect_left_arrow(arrow)
            right_rect = self.closest_rect_right_arrow(arrow)
            label = self.get_arrow_label(arrow)
            print(arrow)
            if left_rect is not None and right_rect is not None:
                # print("Closest Text to the left of arrow %d:" % (arrow_num))
                # print(self.rect_content[left_rect].get_content())
                # print("Closest Text to the right of arrow %d:" % (arrow_num))
                # print("With connection of %s" % (label))
                # print(self.rect_content[right_rect].get_content())
                # arrow_num += 1

                left_event = self.rect_content[left_rect]
                right_event = self.rect_content[right_rect]

                left_event.add_connection(right_event,label)

            if above_rect is not None and below_rect is not None:
                # print("Closest Text over arrow %d:" % (arrow_num))
                # print(self.rect_content[above_rect].get_content())
                # print("Closest Text below arrow %d:" % (arrow_num))
                # print("With connection of %s" % (label))
                # print(self.rect_content[below_rect].get_content())

                upper_event = self.rect_content[above_rect]
                lower_event = self.rect_content[below_rect]

                upper_event.add_connection(lower_event,label)
                #arrow_num += 1

    def build_graph_from_pdf(self,doc, pagenum):
        self.categorize_layout(doc, pagenum)
        self.recognize_textboxes()
        G = Graph(len(self.rect_content))
        self.add_connections()
        for value_tuple in self.rect_content.values():
            G.add_event(value_tuple)
        return G

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


    #return true if given arrow is closest to given line
    @staticmethod
    def textline_labels_arrow(line, curve, h_proximity, y_proximity):
        return PDF_Parser.arrow_labels_horizontally(line,curve,h_proximity) or PDF_Parser.arrow_labels_vertically(line,curve,y_proximity)

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
            if PDF_Parser.textline_labels_arrow(label, curve,h_proximity, y_proximity):
                closest_label = label
                h_proximity = label.x0 - curve.x0
                y_proximity = label.y0 - curve.y0
        if closest_label is not None:
            str = closest_label.get_text()
            self.arrow_labels.remove(closest_label)
            return str
        else: return None











def main():
    pdf_parser = PDF_Parser("Rational Troubleshooting guide.pdf")
    print(pdf_parser.pdf_name)
    result = pdf_parser.with_pdf(pdf_parser.build_graph_from_pdf, 37)
    for i in result.get_events():
        print(repr(i))

    result.print_graph()
    result.get_event(4).set_type("O")
    result.get_event(15).set_type("O")
    result.get_event(5).set_type("S")
    result.get_event(6).set_type("S")
    result.get_event(16).set_type("N")
    result.get_event(17).set_type("S")

    print("-----------------")
    cc = result.get_connected_components()
    print(cc)
    print(result.get_total_event_connections(4))
    result.observation_solution(cc[1])
    print(result.obser_solutions)


# print(result)

if __name__ == "__main__":
    main()
