'''
Created on Jul 19, 2015

'''

'''IMPORTS'''
from constants import *

from goal_node_lib import *
from HTMLParser import HTMLParser
import os
import sys
import re
from visualizer_node_lib import *
from vis_graphs_lib import *
from operator import add
from matplotlib import pyplot

'''CONST'''
sys.path.append(os.path.abspath("/../Diet_Visualizer"))

class Goal_HTML_Parser(HTMLParser):
    ''' Input an xml file, return a list of relevant text lines'''
    def __init__(self):
        HTMLParser.__init__(self)
        self.cr_date = datetime.date(2003,7,29)        #Default value - this should always be overwritten
        self.lines = []     #stores the parsed data; each element is a tuple of the form (date,type,string)
        self.goal_list = []

        self.goal_str_re = re.compile(r'\s*[0-9]*\)\s')         #ex: '3) '
        self.date_str_re = re.compile(r'\d\d\/\d\d\/\d\d')      #ex: '03/22/2014'
        self.status_ndnf_re = re.compile(r'NOT DONE NF - ')     #ex: 'NOT DONE NF - blahblahblah'        
        self.status_nd_re = re.compile(r'NOT DONE - ')          #ex: 'NOT DONE - blahblahblah'
        self.status_pd_re = re.compile(r'PARTIALLY DONE - ')    #ex: 'PARTIALLY DONE - blahblahblah'
                
    def handle_data(self, data):
        if re.match(self.date_str_re,data) != None:
            self.cr_date = datetime.date(int(data[-4:]),int(data[:2]),int(data[3:5]))
        elif re.match(self.goal_str_re,data) != None:
            self.lines.append((self.cr_date.__str__(),'GOALDESC',data[1:]))  #Removes prefixed newline
        elif data == 'DONE':                                      #No need for regex, this should be an exact match
            self.lines.append((self.cr_date.__str__(),'STATUS',data))  
        elif re.match(self.status_ndnf_re,data) != None:          #NOT DONE NF
            self.lines.append((self.cr_date.__str__(),'STATUS',data[:11]))  
            self.lines.append((self.cr_date.__str__(),'STATUSDESC',data[14:]))  
        elif re.match(self.status_nd_re,data) != None:            #NOT DONE
            self.lines.append((self.cr_date.__str__(),'STATUS',data[:8]))  
            self.lines.append((self.cr_date.__str__(),'STATUSDESC',data[11:]))  
        elif re.match(self.status_pd_re,data) != None:            #PARTIALLY DONE
            self.lines.append((self.cr_date.__str__(),'STATUS',data[:14]))  
            self.lines.append((self.cr_date.__str__(),'STATUSDESC',data[17:]))  
            
    def get_goals(self):
        for line in range(len(self.lines)):
            try:
                if self.lines[line][1] == 'GOALDESC':                                   #Every goal should have this line
                    g = goal(self.lines[line + 1][2],self.lines[line][0],self.lines[line][2])   #Create a new goal
                    if line + 2 < len(self.lines):                                      #Here, test to make sure we aren't overrunning the file
                        if self.lines[line + 2][1] == 'STATUSDESC':                     #Not every goal has a status description - DONE goals do not
                            g.set_action_date(self.lines[line + 2][0])                  #If it does have a status description, add it in, and add the date
                            g.set_action_string(self.lines[line + 2][2])
                    self.goal_list.append(g)
            except IndexError:
                    print 'Index Error in ' + self.lines[line][0]
                    break
        return self.goal_list

def read_data_goals(drive_path = DRIVE_PATH, goal_list = [], day_nodes = {}):
    '''Parses input file, returns an array of goals'''
    path = drive_path + INPUT_PATH_GOAL
    print path
    dirs = os.listdir(path)

    for d in dirs:
        directory_path = path + d
        full_path = path + d + '/' + INPUT_FILENAME

        #Use this line to specify a specific date for testing
        #full_path = path + '03-05-2015' + '/' + INPUT_FILENAME
        
        if os.path.isdir(directory_path) == True:
            HTML_Parser = Goal_HTML_Parser()
            if VERBOSE == True:
                print 'Opening directory: ' + d
            #Date ends up being on the 6th line
            f_name = open(full_path, 'r')

            HTML_Parser.feed(f_name.read())

            gl = HTML_Parser.get_goals()

            #Pull the date out of the first goal (kludge) and retrieve or create a new node using the date
            cur_date = datetime.date(int(gl[0].get_creation_date()[0:4]),int(gl[0].get_creation_date()[5:7]),int(gl[0].get_creation_date()[8:]))
            node = day_nodes.get(cur_date.toordinal(),day_node(cur_date))
            
            for g in gl: 
                node.add_goal(g)
    
            HTML_Parser.close()
            f_name.close()

        else:
            print 'not opening ' + str(d)

    return day_nodes


def get_range(goal_list, begin, end):
    '''From the parsed file, returns an array of all goals between the specified dates (inclusive)'''
    #for all goals in the array
        #if creation date > beginning range and < ending range
            #add goal to new array
    new_goal_list = []
    
    for g in goal_list:
        #Messy reconversion from string to datetype - FIX THIS when I get a chance
        cr_date = datetime.date(int(g.get_creation_date()[:4]),int(g.get_creation_date()[5:7]),int(g.get_creation_date()[8:10]))
        if (cr_date >= begin) and (cr_date <= end):
            new_goal_list.append(g)

    return new_goal_list

def goals_text_output(goal_list):
    '''For the given set of goals, simply outputs the status of each'''
    #for all goals in array, output the status on a newline
    for g in goal_list:
        print g.get_creation_date() + ' ' + g.get_status()
        
def graph_goals_stacked_bar(day_nodes,num_taps=5):
    '''Takes in a list of goals, plots the statuses as a stacked time series'''
    
    #Find beginning and end dates of day_nodes
#     begin_date = datetime.date.today()
#     end_date = datetime.date(1,1,1)  
    
    #Get a list of the active dates
    dates =[day_nodes[node].get_date() for node in day_nodes]
    
    #Make 4 dicts, each representing the normalized value of the number of goals per day with the particular satus description
    done_percentage =[len(day_nodes[node].get_goals_of_status('DONE'))/(day_nodes[node].get_num_goals() + .001)*100 for node in day_nodes] #Added in the tiny fraction to prevent DBZ errors
    not_done_percentage =[len(day_nodes[node].get_goals_of_status('NOT DONE'))/(day_nodes[node].get_num_goals() + .001)*100 for node in day_nodes] #Added in the tiny fraction to prevent DBZ errors
    not_done_nf_percentage =[len(day_nodes[node].get_goals_of_status('NOT DONE NF'))/(day_nodes[node].get_num_goals() + .001)*100 for node in day_nodes] #Added in the tiny fraction to prevent DBZ errors
    partially_done_percentage =[len(day_nodes[node].get_goals_of_status('PARTIALLY DONE'))/(day_nodes[node].get_num_goals() + .001)*100 for node in day_nodes] #Added in the tiny fraction to prevent DBZ errors
    
    #Make another dict for plotting the total number of goals per day
    num_goals = [day_nodes[node].get_num_goals() for node in day_nodes]

    #Setup for the whole fig
    fig,ax_array = pylab.subplots(2)
    fig.tight_layout()
    fig.canvas.set_window_title('Goal Completion') 
    
    #Stick together some of the serieses so that everything can stack properly (using the bottom = ...)
    qualified_done_percentage = map(add,done_percentage, partially_done_percentage)
    qualified_done_percentage = map(add,qualified_done_percentage, not_done_nf_percentage)
    
    #Top plot is the qualified done plot, plots the combination of done, partially done, and not done no fault
    pylab.setp(ax_array[0].xaxis.get_majorticklabels(), rotation=20)
        #Plots the bars
    ax_array[0].bar(dates, not_done_percentage, 1,align='center',linewidth=0,color='red',label='Not Done')
    ax_array[0].bar(dates, qualified_done_percentage, 1,bottom=not_done_percentage,align='center',linewidth=0,color='green',label='Done (or Qualified)')
        #Second axis is for the number of goals and the MA
    ax_0_2 = fig.add_axes(ax_array[0].get_position(), frameon=False)
    ax_0_2.yaxis.tick_right()
    ax_0_2.plot_date(dates,num_goals,marker='',linestyle=':',linewidth=1,color='black',label='Num Tasks')
    ax_0_2.plot_date(dates,moving_avg(num_goals,num_taps),marker='',linestyle='-',color='black',label = 'Moving Avg. (' + str(num_taps) + ') taps')
    pylab.setp(ax_0_2.get_xticklabels(), visible=False)
    ax_array[0].legend(loc='upper left', shadow=True, fontsize='small')
    ax_0_2.legend(loc='upper right', shadow=True, fontsize='small')
    ax_array[0].set_title('Task Completion (Qualified)')
    ax_0_2.set_ylabel('Number of Tasks')
    ax_array[0].set_ylabel('Task Completion (Percentage)')
    ax_0_2.yaxis.set_label_position("right")
    ax_array[0].xaxis_date()
   
    #Stick together some of the serieses so that everything can stack properly (using the bottom = ...) 
    combo_nd_and_pd = map(add,not_done_percentage, partially_done_percentage)
        #Bottom plot is the fully enumerated version of the top plot
    pylab.setp(ax_array[1].xaxis.get_majorticklabels(), rotation=20)
    ax_array[1].bar(dates, not_done_percentage, 1,align='center',linewidth=0,color='red',label='Not Done')
    ax_array[1].bar(dates, partially_done_percentage, 1,bottom=not_done_percentage,align='center',linewidth=0,color='blue',label='Partially Done')
    ax_array[1].bar(dates, not_done_nf_percentage, 1,bottom=combo_nd_and_pd,align='center',linewidth=0,color='orange',label='Not Done (NF)')
    ax_array[1].bar(dates, done_percentage,1,bottom=map(add,combo_nd_and_pd,not_done_nf_percentage),align='center',linewidth=0,color='green',label='Done')
    ax_1_2 = fig.add_axes(ax_array[1].get_position(), frameon=False)
    ax_1_2.yaxis.tick_right()
    ax_1_2.plot_date(dates,num_goals,marker='',linestyle=':',linewidth=1,color='black',label='Num Tasks')
    ax_1_2.plot_date(dates,moving_avg(num_goals,num_taps),marker='',linestyle='-',color='black',label = 'Moving Avg. (' + str(num_taps) + ') taps')
    pylab.setp(ax_1_2.get_xticklabels(), visible=False)
    ax_array[1].legend(loc='upper left', shadow=True, fontsize='small')
    ax_1_2.legend(loc='upper right', shadow=True, fontsize='small')
    ax_array[1].set_title('Task Completion (Fully Enumerated)')
    ax_1_2.set_ylabel('Number of Tasks')
    ax_array[1].set_ylabel('Task Completion (Percentage)')
    ax_1_2.yaxis.set_label_position("right")
    ax_array[1].xaxis_date()
    
