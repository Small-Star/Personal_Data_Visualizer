'''
Created on Jun 17, 2016

'''

'''IMPORTS'''
from constants import *

from HTMLParser import HTMLParser
import re
import datetime
from visualizer_node_lib import *
from vis_graphs_lib import *

def read_data_mood(day_nodes, drive_path = DRIVE_PATH):
    ''' Inputs: Dict consisting of nodes corresponding to days with data. May be unfilled, filled, or partially filled.
                Drive path in which files are located
        Outputs: Dict consisting of a set or superset of the input nodes, populated with mood information'''
    
    path = drive_path + INPUT_PATH_MOOD + INPUT_FILENAME
    Mood_Parser = Mood_HTML_Parser()
    f_name = open(path, 'r')

    Mood_Parser.feed(f_name.read())
    n_day_nodes = Mood_Parser.get_nodes()
    
    #Integrate new info into existing day_nodes
    for k,n in n_day_nodes.iteritems():
        if n.get_date().toordinal() not in day_nodes:  #If no node exists, make a new one 
            day_nodes[n.get_date().toordinal()] = n
        else:
            day_nodes[n.get_date().toordinal()].set_mood(n.get_mood()) #Update mood of existing node
    return day_nodes

class Mood_HTML_Parser(HTMLParser):
    ''' Input an xml file, return a list of relevant text lines'''
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.day_nodes = {}      
        self.cr_date = datetime.date(2003,7,29)        #Default value - this should always be overwritten
        self.date_str_re = re.compile(r'\d\d\/\d\d\/\d\d')
        
    def handle_data(self, data):
        data_ = data.strip()    #Drop whitespace
        #Line by line parsing of input data
        if re.match(self.date_str_re,data_) != None:
            day_str_list = re.split('/',data_[:10]) #Remove cruft from date
            self.current_date = datetime.date(int(day_str_list[2]),int(day_str_list[0]),int(day_str_list[1]))
            new_day_node = day_node(self.current_date)
            self.day_nodes[self.current_date.toordinal()] = new_day_node
            self.day_nodes[new_day_node.get_date().toordinal()] = new_day_node #Add new date to dict: key is the ordinal date
            new_day_node.set_mood(((int(data_[14]),int(data_[16]),data_[17]),(int(data_[20]),int(data_[22]),data_[23])))
                    
    def get_nodes(self):
        return self.day_nodes
    
if __name__ == '__main__':
    read_data_mood({})