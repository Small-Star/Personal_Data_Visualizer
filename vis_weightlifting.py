'''
Created on Aug 16, 2015

'''
'''IMPORTS'''
from constants import *

from visualizer_node_lib import *
from body_node_lib import *
from vis_graphs_lib import *

from HTMLParser import HTMLParser
import re
import datetime
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot
import numpy as np

class Weightlifting_HTML_Parser(HTMLParser):
    ''' Input an xml file, return a list of relevant text lines'''
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.lines = []                                                 #stores the parsed data; each element is a tuple of the form (date,type,string)

        self.cr_date = datetime.date(2003,7,29)                         #Default value - this should always be overwritten

        self.corl_flag = 'L'                                            #Toggles cardio or lift

        self.date_str_re = re.compile(r'\d\d\/\d\d\/\d\d')              #ex: '03/22/2014'
        self.start_time_re = re.compile(r'Start Time - ')               #ex: 'Start Time - 01:23'
        self.end_time_re = re.compile(r'End Time - ')                   #ex: 'End Time - 01:23'  note: optionally, there is a date subsequent to the time 
        self.weight_re = re.compile(r'Weight - ')
        self.bodyfat_re = re.compile(r'Bodyfat - ')
        self.type_re = re.compile(r'Workout: ')
        
        self.cardio_flag_re = re.compile(r'Cardio:')
        self.lifting_flag_re = re.compile(r'Lifting:')
        
        self.rating_re = re.compile(r'Rating: ')
        self.notes_re = re.compile(r'Notes: ')
        
        self.lift_re = re.compile(r' - ')
                
    def handle_data(self, data):
        try:
            if re.match(self.date_str_re,data) != None:
                self.cr_date = datetime.date(int(data[-5:-1]),int(data[:2]),int(data[3:5]))
            elif re.match(self.start_time_re,data) != None:
                st_time = datetime.datetime(self.cr_date.year,self.cr_date.month,self.cr_date.day,int(data[13:15]),int(data[16:]))
                self.lines.append((self.cr_date,'STARTTIME',st_time))
            elif re.match(self.end_time_re,data) != None:
                e_time = datetime.datetime(int(data[23:]),int(data[17:19]),int(data[20:22]),int(data[11:13]),int(data[14:16]))
                self.lines.append((self.cr_date,'ENDTIME',e_time))
            elif re.match(self.weight_re,data) != None:
                d = re.split('lbs',data[9:])[0]
                if re.match('\d',d) != None:        #Check to make sure the weight is an actual value, and  is not N/A
                    d = float(d)
                    self.lines.append((self.cr_date,'WEIGHT',d))
            elif re.match(self.bodyfat_re,data) != None:
                if data[-1:] == '%':     #Don't use bodyfats measured in mms; just drop those
                    self.lines.append((self.cr_date,'BODYFAT',float(data[10:-1])))
            elif re.match(self.type_re,data) != None:
                self.lines.append((self.cr_date,'TYPE',data[9:]))
            elif re.match(self.cardio_flag_re,data) != None:
                self.corl_flag = 'C'
            elif re.match(self.lifting_flag_re,data) != None:
                self.corl_flag = 'L'
            elif re.match(self.rating_re,data) != None:
                self.lines.append((self.cr_date,'RATING',data[8:]))
            elif re.match(self.notes_re,data) != None:
                self.lines.append((self.cr_date,'NOTES',data[7:]))

            elif re.match(self.lift_re,data) != None:
                if self.corl_flag == 'C':                       #Cardio
                    d = data.split(' - ')
                    self.lines.append((self.cr_date,'CARDIO',(d[1],d[-1])))   #tuple is type, duration (can be floors or minutes)
                elif self.corl_flag == 'L':
                    d = data.split(' - ')           #Splits into '', Lift Name, Lifts
                    l = d[2].split(', ')            #Splits Lifts by csv
                    for el in l:
                        if len(el.split('x')) == 2: #This is not a multi-set lift
                            self.lines.append((self.cr_date,'LIFT',(d[1],el)))                              #Appends a tuple of (Lift Name, Weightxrep)
                        elif len(el.split('x')) == 3: #This is a multi-set lift
                            for x in range(int(re.split('[IF]',el.split('x')[-1])[0])):
                                reconstituted_el = str(el.split('x')[0] + 'x' + el.split('x')[1])           #Make a number of entries corresponding to the third value
                                self.lines.append((self.cr_date,'LIFT',(d[1],reconstituted_el)))            #Appends a tuple of (Lift Name, Weightxrep)
        except ValueError:
            print "Value Error (Weightlifting): " + data
        except IndexError:
            print "Index Error (Weightlifting): " + self.cr_date
      
    def update_nodes(self,day_nodes):
        bnode = body_node()
        prev_cd = datetime.date(1,1,1)

        for line in range(len(self.lines)):            
            if self.lines[line][0] != prev_cd:                      #If the creation date of the current line doesn't match the most previous creation date, a new day is starting
                
                if prev_cd != datetime.date(1,1,1):                 #If this isn't the first node
                    day_nodes[self.lines[line-1][0].toordinal()].set_bnode(bnode)       #Pin the old body node to the immediately previous creation date

                bnode = body_node(self.lines[line][0])              #Make a new blank body node
                prev_cd = self.lines[line][0]                       #Update the previous creation date
            
#           '''Go through all line possibilities'''
            if self.lines[line][1] == 'STARTTIME':# or 'C' or 'N' or 'E' or 'W' or 'B':
                bnode.get_workout().set_start_time(self.lines[line][2])
            elif self.lines[line][1] == 'ENDTIME':
                bnode.get_workout().set_end_time(self.lines[line][2])
            elif self.lines[line][1] == 'WEIGHT':
                bnode.set_weight(self.lines[line][2])
            elif self.lines[line][1] == 'BODYFAT':   
                bnode.set_bodyfat(self.lines[line][2])           
            elif self.lines[line][1] == 'TYPE':
                bnode.get_workout().set_workout_type(self.lines[line][2])
            elif self.lines[line][1] == 'RATING':
                bnode.get_workout().set_rating(self.lines[line][2])
            elif self.lines[line][1] == 'NOTES':
                bnode.get_workout().set_lift_notes(self.lines[line][2])
            elif self.lines[line][1] == 'CARDIO':
                bnode.get_workout().add_cardio(self.lines[line][2]) 
            elif self.lines[line][1] == 'LIFT':            
                bnode.get_workout().add_lift(self.lines[line][2])

        try:
            day_nodes[self.lines[-1][0].toordinal()].set_bnode(bnode)                    #Pin the final body node
        except KeyError:
            print "KeyError on: " + str(self.lines[-1][0])
            
        return day_nodes

def read_weightlifting_records(drive_path = DRIVE_PATH, day_nodes = {}):
    ''' Inputs: Dict consisting of nodes corresponding to days with data. May be unfilled, filled, or partially filled.
                Drive letter in which files are located
        Outputs: Dict consisting of a set or superset of the input nodes, populated with weightlifting information'''

    path = drive_path + INPUT_PATH_LIFTS + INPUT_FILENAME
    HTML_Parser = Weightlifting_HTML_Parser()
    f_name = open(path, 'r')

    HTML_Parser.feed(f_name.read())
    day_nodes = HTML_Parser.update_nodes(day_nodes)
    
    return day_nodes

def graph_single_lift(day_nodes, lift, n=5):
    
    dates = [day_nodes[node].get_date() for node in day_nodes]
    lifts = [(day_nodes[node].get_bnode().get_workout().get_lift(lift),day_nodes[node].get_date()) for node in day_nodes if day_nodes[node].get_bnode().worked_out() == True]
    
    pruned_lifts = [x for x in lifts if x[0] != []]
    
    #print pruned_lifts[0][0]
    #print pruned_lifts[0][1]
    #print pruned_lifts[0][0][0]
    #print pruned_lifts[0][0][0][0]
    
#     fig = pyplot.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     
#     xpos = []
#     ypos = np.zeros(len(pruned_lifts))   
#     zpos = np.zeros(len(pruned_lifts))   
#     
#     dx = np.zeros(len(pruned_lifts))
#     dy = []
# 
#     dz = []
#     
#     for i in range(len(pruned_lifts)):
#         xpos.append(pruned_lifts[i][1].toordinal()) #NOTE - THE TOORDINAL IS A HACK< FIX IT #
#         dy.append(len(pruned_lifts[i][0][0]))
#         dz.append(int(re.split('x',pruned_lifts[i][0][0][-1][1])[0]))#Pulls out the weight of the last set - fix this
#     print str(re.split('x',pruned_lifts[0][0][0][-1][1])[0])
# 
#     
# 
#     ax.bar3d(xpos,ypos,zpos,dx,dy,dz)
#     ax.set_xlabel('X')
#     ax.set_ylabel('Y')
#     ax.set_zlabel('Z')


    
    fig = pyplot.figure()
    fig.canvas.set_window_title(lift + ' Lift Numbers') 
    
    ax2 = fig.add_subplot(111, projection='3d')
    for i in range(len(pruned_lifts)):
        xs = np.arange(len(pruned_lifts[i][0][0]))
        ys = []
        for j in range(len(pruned_lifts[i][0][0])):
            ys.append(int(re.split('x',pruned_lifts[i][0][0][j][1])[0]))

        # You can provide either a single color or an array. To demonstrate this,
        # the first bar of each set will be colored cyan.
        cs = 'c' * len(ys)
        
        ax2.bar(xs, ys, zs=i, zdir='y', color=cs, alpha=0.8)

    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')


#     
#     fig,ax_array = pylab.subplots(1)
#     fig.tight_layout()
#      
#     pylab.setp(ax_array[0].xaxis.get_majorticklabels(), rotation=20)
#     rects = create_bg_rects(day_nodes,100)
#     for r in rects:
#         ax_array[0].add_patch(r)
#      
#     ax_array[0].plot_date(dates,lifts[0],marker='.',linestyle=' ',color='r',label = 'Daily Calories')
#     ax_array[0].plot_date(dates,moving_avg(cals,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
#     ax_array[0].set_ylim([0,max(cals)*1.1])
#     ax_array[0].set_title('Calorie Intake')
#     ax_array[0].set_ylabel('Calories (kCal)')
#     ax_array[0].legend(loc='upper left', shadow=True, fontsize='small')
