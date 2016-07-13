'''
Created on Jul 19, 2015


'''

'''IMPORTS'''
from constants import *

from HTMLParser import HTMLParser
import re
import datetime
from visualizer_node_lib import *
from vis_graphs_lib import *

def read_data_diet(day_nodes, drive_path = DRIVE_PATH):
    ''' Inputs: Dict consisting of nodes corresponding to days with data. May be unfilled, filled, or partially filled.
                Drive path in which files are located
        Outputs: Dict consisting of a set or superset of the input nodes, populated with diet information'''

    path = drive_path + INPUT_PATH_DIET + INPUT_FILENAME
    HTML_Parser = Diet_HTML_Parser()
    f_name = open(path, 'r')

    HTML_Parser.feed(f_name.read())
    #calorie_intake = HTML_Parser.get_calorie_intake()
    #protein_intake = HTML_Parser.get_protein_intake()
    #tdee = HTML_Parser.get_tdee()
    day_nodes = HTML_Parser.get_nodes()
    return day_nodes

class Diet_HTML_Parser(HTMLParser):
    ''' Input an xml file, return a list of relevant text lines'''
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.calorie_intake = []
        self.protein_intake = []
        self.tdee = []
        self.day_nodes = {}
                
        self.date_re = re.compile(r'- \d\d\/\d\d\/\d\d\d\d')      #ex: '03/22/2014'
        self.calorie_intake_re = re.compile(r'\s*Intake: ')
        self.protein_intake_re = re.compile(r'\s*Protein: ')
        self.tdee_re = re.compile(r'\s*Est. TDEE: ')
        self.fic_re = re.compile(r'\S') #Note, this pattern is used on the BACKWARDS TDEE string
         
    def handle_data(self, data):
        #Line by line parsing of input data
        if re.match(self.date_re,data) != None:
            day_str_list = re.split('/',data[2:-1]) #Remove cruft from date
            self.current_date = datetime.date(int(day_str_list[2]),int(day_str_list[0]),int(day_str_list[1]))
            new_day_node = day_node(self.current_date)
            self.day_nodes[self.current_date.toordinal()] = new_day_node
            self.day_nodes[new_day_node.get_date().toordinal()] = new_day_node #Add new date to dict: key is the ordinal date
        elif re.match(self.calorie_intake_re,data) != None:
            node = self.day_nodes.get(self.current_date.toordinal(),day_node(datetime.date(1000,01,01))) #01/01/1000 denotes an error
            cal_int = int(re.split(self.calorie_intake_re,re.split("kcal",data)[0])[1])#Match pattern, split away extraneous stuff
            node.set_calorie_intake(cal_int)
            self.calorie_intake.append(cal_int)
        elif re.match(self.protein_intake_re,data) != None:
            node = self.day_nodes.get(self.current_date.toordinal(),day_node(datetime.date(1000,01,01))) #01/01/1000 denotes an error
            pro_int = int(re.split(self.protein_intake_re,re.split("g",data)[0])[1])#Match pattern, split away extraneous stuff
            node.set_protein_intake(pro_int)
            self.protein_intake.append(pro_int)
        elif re.match(self.tdee_re,data) != None:
            node = self.day_nodes.get(self.current_date.toordinal(),day_node(datetime.date(1000,01,01))) #01/01/1000 denotes an error
            tdee_ = int(re.split(self.tdee_re,re.split("kcal",data)[0])[1])#Match pattern, split away extraneous stuff
            node.set_tdee(tdee_)
            node.set_fic(re.search(self.fic_re,data[::-1]).group())     #Pulls out the endmost non-whitespace character
            self.tdee.append(tdee_)
        
    def get_calorie_intake(self):
        return self.calorie_intake
    def get_protein_intake(self):
        return self.protein_intake
    def get_tdee(self):
        return self.tdee
    def get_nodes(self):
        return self.day_nodes
        
def simple_graph(series1,series2):
    fig,ax1 = pylab.subplots()
    ax1.plot(range(len(series1)),series1,marker='.',linestyle=' ',color='r')
    ax1.set_ylim([0,7000])
    ax1.set_xlim([0,len(series1)])

    ax1.plot(range(len(moving_avg(series1))),moving_avg(series1),marker='',linestyle='-',color='r')
    pylab.show()

    ax2 = ax1.twinx()
    ax2.plot(range(len(series2)),series2,marker='.',linestyle=' ',color='g')
    ax2.set_ylim([0,300])
    ax2.set_xlim([0,len(series2)])
    
    ax2.plot(range(len(moving_avg(series2))),moving_avg(series2),marker='',linestyle='-',color='g')
    pylab.show()
    
def graph_diet(nodes,n=5):
    #Plots a 3 window graph of daily caloric intake, daily protein intake, and daily TDEE
    dates =[nodes[node].get_date() for node in nodes]
    cals = [nodes[node].get_calorie_intake() for node in nodes]
    prots = [nodes[node].get_protein_intake() for node in nodes]    
    tdees = [nodes[node].get_tdee() for node in nodes]
    #fics = [nodes[node].get_fic() for node in nodes]
        
    fig,ax_array = pylab.subplots(3)
    fig.tight_layout()
    fig.canvas.set_window_title('Nutrient Intake') 
    
    pylab.setp(ax_array[0].xaxis.get_majorticklabels(), rotation=20)
    rects = create_bg_rects(nodes,max(cals)*1.1)
    for r in rects:
        ax_array[0].add_patch(r)
    ax_array[0].plot_date(dates,cals,marker='.',linestyle=' ',color='r',label = 'Daily Calories')
    ax_array[0].plot_date(dates,moving_avg(cals,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
    ax_array[0].set_ylim([0,max(cals)*1.1])
    ax_array[0].set_title('Calorie Intake')
    ax_array[0].set_ylabel('Calories (kCal)')
    ax_array[0].legend(loc='upper left', shadow=True, fontsize='small')

    pylab.setp(ax_array[1].xaxis.get_majorticklabels(), rotation=20)
    rects = create_bg_rects(nodes,max(prots)*1.1)
    for r in rects:
        ax_array[1].add_patch(r)
    ax_array[1].plot_date(dates,prots,marker='.',linestyle=' ',color='r',label = 'Daily Protein')
    ax_array[1].plot_date(dates,moving_avg(prots,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
    ax_array[1].set_ylim([0,max(prots)*1.1])
    ax_array[1].set_title('Protein')
    ax_array[1].set_ylabel('Protein (g)')
    ax_array[1].legend(loc='upper left', shadow=True, fontsize='small')

    #Note: the first part of this range is invalid due to nonexistent data. Use truncated_tdees; plot against truncated_dates
    truncated_tdees = tdees[460:]
    truncated_dates = dates[460:]
    
    pylab.setp(ax_array[2].xaxis.get_majorticklabels(), rotation=20)
    rects = create_bg_rects(nodes,max(tdees)*1.1)
    for r in rects:
        ax_array[2].add_patch(r)
    ax_array[2].plot_date(truncated_dates,truncated_tdees,marker='.',linestyle=' ',color='r',label = 'Daily TDEE')
    ax_array[2].plot_date(truncated_dates,moving_avg(truncated_tdees,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
    ax_array[2].set_ylim([0,max(tdees)*1.1])
    ax_array[2].set_title('Estimated TDEE (kCal)')
    ax_array[2].set_ylabel('Est. TDEE (kCal)')
    ax_array[2].legend(loc='upper left', shadow=True, fontsize='small')
    #pylab.show()
    
def graph_body(nodes,n=5):
    #Plots a 3 window graph of daily caloric intake (redundant, but useful for side by side comparison), daily weight, and daily bodyfat (TODO)
    dates =[nodes[node].get_date() for node in nodes]
    cals = [nodes[node].get_calorie_intake() for node in nodes]
    tdees = [nodes[node].get_tdee() for node in nodes]
    t_weights = [nodes[node].get_bnode().get_weight() for node in nodes]
    t_bfs = [nodes[node].get_bnode().get_bodyfat() for node in nodes]   
    
    #Hack to get rid of 0's for unrecorded weights
    weights = []
    
    for t in range(len(t_weights)):
        if t_weights[t] == 0:
            if t > (int(len(t_weights)/2)):
                for u in range(t,0,-1):
                    if t_weights[u] != 0:
                        weights.append(t_weights[u])
                        break
            elif t < (int(len(t_weights)/2)):
                for u in range(t,len(t_weights)):
                    if t_weights[u] != 0:
                        weights.append(t_weights[u])
                        break                 
        else:
            weights.append(t_weights[t])

    #End hack
    
    #Hack to get rid of 0's for unrecorded bodyfats
    bodyfats = []
    
    for t in range(len(t_bfs)):
        if t_bfs[t] == 0:
            if t > (int(len(t_bfs)/2)):
                for u in range(t,0,-1):
                    if t_bfs[u] != 0:
                        bodyfats.append(t_bfs[u])
                        break
            elif t < (int(len(t_bfs)/2)):
                for u in range(t,len(t_bfs)):
                    if t_bfs[u] != 0:
                        bodyfats.append(t_bfs[u])
                        break                 
        else:
            bodyfats.append(t_bfs[t])

    #End hack
    if len(dates) != len(weights):
        weights.append(weights[-1]) #HACK
    if len(dates) != len(bodyfats):
        bodyfats.append(bodyfats[-1]) #HACK
    
    net_cis = pylab.subtract(cals,tdees) #Note: the first part of this range is invalid due to nonexistent data. Use truncated_net_cis; plot against truncated_dates
    truncated_net_cis = net_cis[460:]
    truncated_dates = dates[460:]
    
    truncated_bfs = bodyfats[208:] #Note: the first part of this range is invalid due to nonexistent data. Use truncated_bfs; plot against truncated_dates_bf
    truncated_dates_bf = dates[208:]
             

    fig,ax_array = pylab.subplots(4)
    fig.tight_layout()
    fig.canvas.set_window_title('BioData') 
    
    #PLOT CALS - TDEE
    pylab.setp(ax_array[0].xaxis.get_majorticklabels(), rotation=20)
    rects = create_bg_rects(nodes,max(truncated_net_cis)*1.1,min(truncated_net_cis)*1.1)
    for r in rects:
        ax_array[0].add_patch(r)
         
    ax_array[0].plot_date(truncated_dates,truncated_net_cis,marker='.',linestyle=' ',color='r',label = 'Net Caloric Intake')
    ax_array[0].plot_date(truncated_dates,moving_avg(truncated_net_cis,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
    ax_array[0].set_ylim([min(truncated_net_cis)*1.1,max(truncated_net_cis)*1.1])
    ax_array[0].set_title('Net Caloric Intake')
    ax_array[0].set_ylabel('Calories (kCal)')
    ax_array[0].legend(loc='upper left', shadow=True, fontsize='small')
    ax_array[0].axhline(y=0, color='k')
        
    #PLOT WEIGHT
    pylab.setp(ax_array[1].xaxis.get_majorticklabels(), rotation=20)
    rects = create_bg_rects(nodes,110,180) #HACK
    for r in rects:
        ax_array[1].add_patch(r)
    ax_array[1].plot_date(dates,weights,marker='.',linestyle=' ',color='r',label = 'Weight')
    ax_array[1].plot_date(dates,moving_avg(weights,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
    ax_array[1].set_ylim([min(weights) - 5,max(weights) + 5])
    ax_array[1].set_title('Weight')
    ax_array[1].set_ylabel('Weight (lb)')
    ax_array[1].legend(loc='upper left', shadow=True, fontsize='small')
    
    #PLOT BODYFAT
    pylab.setp(ax_array[2].xaxis.get_majorticklabels(), rotation=20)
    rects = create_bg_rects(nodes,6,30) #HACK
    for r in rects:
        ax_array[2].add_patch(r)
    ax_array[2].plot_date(truncated_dates_bf,truncated_bfs,marker='.',linestyle=' ',color='r',label = 'Bodyfat')
    ax_array[2].plot_date(truncated_dates_bf,moving_avg(truncated_bfs,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
    ax_array[2].set_ylim([min(truncated_bfs) - 2,max(truncated_bfs) + 2])
    ax_array[2].set_title('Bodyfat')
    ax_array[2].set_ylabel('Bodyfat (%)')
    ax_array[2].legend(loc='upper left', shadow=True, fontsize='small')
    
    #PLOT COMBO
    
    #Find offsets - normalize to weight
    weight_avg = sum(weights)/len(weights)
    net_cis_avg = sum(truncated_net_cis)/len(truncated_net_cis)
    bodyfat_avg = sum(truncated_bfs)/len(truncated_bfs)
    
    weight_scale = 125.0
    bodyfat_scale = 25.0
    net_cis_scale = 1.0
    
    norm_weights = [weight_scale*(float(w)/weight_avg - 1) for w in weights]
    norm_o_n_c = [net_cis_scale*(float(nc)/abs(net_cis_avg) - 1) for nc in truncated_net_cis]
    norm_bodyfats = [bodyfat_scale*(float(b)/bodyfat_avg - 1) for b in truncated_bfs]
        
    pylab.setp(ax_array[3].xaxis.get_majorticklabels(), rotation=20)
    rects = create_bg_rects(nodes,-10,10) #HACK
    for r in rects:
        ax_array[3].add_patch(r)
    ax_array[3].plot_date(dates,moving_avg(norm_weights,n),marker='',linestyle='-',color='r',label = 'Weight Moving Avg. (' + str(n) + ') taps')
    ax_array[3].plot_date(truncated_dates_bf,moving_avg(norm_bodyfats,n),marker='',linestyle='-',color='g',label = 'BF Moving Avg. (' + str(n) + ') taps')
    ax_array[3].plot_date(truncated_dates,moving_avg(norm_o_n_c,n),marker='',linestyle='-',color='b',label = 'Net CI Moving Avg. (' + str(n) + ') taps')    
    ax_array[3].set_ylim([-7,6])
    ax_array[3].set_title('Comparison')
    ax_array[3].set_ylabel('Normalized Scale')
    ax_array[3].legend(loc='upper left', shadow=True, fontsize='small')
    ax_array[3].axhline(y=0, color='k')
    