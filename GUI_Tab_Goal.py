'''
Created on Jun 6, 2016

'''

import wx
import wxmplot
import numpy
import pylab

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from vis_graphs_lib import *
from vis_diet import *
from vis_goals import *
from vis_records import *
from vis_weightlifting import *

from GUI_lib import *

class Tab_Goal(wx.Panel):
    
    def __init__(self, parent, nodelist):
                
        self.fig = None
        self.canvas = None
        self.nodelist = nodelist
            
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
                
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        l_vbox_pan = lvpan(self)        
        self.dp_beg.SetValue(wx.DateTimeFromDMY(22,2,2014))
        
        v_line = wx.StaticLine(self, style=wx.LI_VERTICAL)
        h_line = wx.StaticLine(self, style=wx.LI_VERTICAL) 
        
        #LABELS                 
        self.lab_a_t = wx.StaticText(l_vbox_pan, label='Avg. Tasks/Day')
        self.lab_a_c = wx.StaticText(l_vbox_pan, label='Avg. Completion (%):')
        self.lab_t_d = wx.StaticText(l_vbox_pan, label='Tasks Done:')
        self.lab_t_d.SetFont(self.header_font)
        
        #STATIC TXTS    
        t_stats = wx.StaticText(l_vbox_pan, label="STATS")
        t_stats.SetFont(self.header_font)   
                     
        #DRAW   
        self.draw(5)
        
        #LEFT PANEL SETUP
        l_sizer = wx.BoxSizer(wx.VERTICAL)
        l_vbox_pan.SetSizer(self.lvp_sizer)
        l_sizer.Add(l_vbox_pan, 0, flag=wx.EXPAND | wx.ALL, border = 10)
        
        #Add Elements to Sizer
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 10) 
        self.lvp_sizer.Add(t_stats,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 10) 
        self.lvp_sizer.Add(self.lab_a_t,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_a_c,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_t_d,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        
        #Misc Setup
        self.r_sizer = fig_pan(self)
        self.main_sizer.Add(l_sizer,0,wx.EXPAND | wx.ALIGN_LEFT)
        self.main_sizer.Add(v_line,0,wx.EXPAND | wx.ALL)
        self.main_sizer.Add(self.r_sizer,8,wx.EXPAND | wx.ALL | wx.ALIGN_LEFT)
        
        self.SetSizer(self.main_sizer)
        self.Show(True)
        
    def draw(self, n=5):
        nodes_ = sort_nodes(self.nodelist) #HACK: FIX (nodes are coming unsorted somewhere, which was causing problems drawing rects
        '''Takes in a list of goals, plots the statuses as a stacked time series'''
        #subset_nodes(self.nodelist, beg=datetime.date(2014,2,22),dp=False)
        #Don't bother to pass the number of taps, just read it out
        spv = self.spin_taps.GetValue()
        if spv > 1:
            n = spv        
                    
        #Get a list of the active dates
        nodes = subset_nodes(nodes_, beg=datetime.date(2014,3,22), dp=False)
        dates =[nodes[node].get_date() for node in nodes]
                
        #Make 4 dicts, each representing the normalized value of the number of goals per day with the particular status description
        done_percentage =[len(nodes[node].get_goals_of_status('DONE'))/(nodes[node].get_num_goals() + .0000001)*100 for node in nodes] #Added in the tiny fraction to prevent DBZ errors
        not_done_percentage =[len(nodes[node].get_goals_of_status('NOT DONE'))/(nodes[node].get_num_goals() + .0000001)*100 for node in nodes] #Added in the tiny fraction to prevent DBZ errors
        not_done_nf_percentage =[len(nodes[node].get_goals_of_status('NOT DONE NF'))/(nodes[node].get_num_goals() + .0000001)*100 for node in nodes] #Added in the tiny fraction to prevent DBZ errors
        partially_done_percentage =[len(nodes[node].get_goals_of_status('PARTIALLY DONE'))/(nodes[node].get_num_goals() + .0000001)*100 for node in nodes] #Added in the tiny fraction to prevent DBZ errors
        
        #Make another dict for plotting the total number of goals per day
        num_goals = [nodes[node].get_num_goals() for node in nodes]
    
        #Setup for the whole fig
        self.fig,ax_array = pylab.subplots(2)
        self.fig.tight_layout()
        self.fig.canvas.set_window_title('Goal Completion') 
        
        #Stick together some of the serieses so that everything can stack properly (using the bottom = ...)
        qualified_done_percentage = map(add,done_percentage, partially_done_percentage)
        qualified_done_percentage = map(add,qualified_done_percentage, not_done_nf_percentage)
        
        #Top plot is the qualified done plot, plots the combination of done, partially done, and not done no fault
        pylab.setp(ax_array[0].xaxis.get_majorticklabels(), rotation=20)
            #Plots the bars
        ax_array[0].bar(dates, not_done_percentage, 1,align='center',linewidth=0,color='red',label='Not Done')
        ax_array[0].bar(dates, qualified_done_percentage, 1,bottom=not_done_percentage,align='center',linewidth=0,color='green',label='Done (or Qualified)')
            #Second axis is for the number of goals and the MA
        ax_0_2 = self.fig.add_axes(ax_array[0].get_position(), frameon=False)
        ax_0_2.yaxis.tick_right()
        ax_0_2.plot_date(dates,num_goals,marker='',linestyle=':',linewidth=1,color='black',label='Num Tasks')
        ax_0_2.plot_date(dates,moving_avg(num_goals,n,True),marker='',linestyle='-',color='black',label = 'Moving Avg. (' + str(n) + ') taps')
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
        ax_1_2 = self.fig.add_axes(ax_array[1].get_position(), frameon=False)
        ax_1_2.yaxis.tick_right()
        ax_1_2.plot_date(dates,num_goals,marker='',linestyle=':',linewidth=1,color='black',label='Num Tasks')
        ax_1_2.plot_date(dates,moving_avg(num_goals,n,True),marker='',linestyle='-',color='black',label = 'Moving Avg. (' + str(n) + ') taps')
        pylab.setp(ax_1_2.get_xticklabels(), visible=False)
        ax_array[1].legend(loc='upper left', shadow=True, fontsize='small')
        ax_1_2.legend(loc='upper right', shadow=True, fontsize='small')
        ax_array[1].set_title('Task Completion (Fully Enumerated)')
        ax_1_2.set_ylabel('Number of Tasks')
        ax_array[1].set_ylabel('Task Completion (Percentage)')
        ax_1_2.yaxis.set_label_position("right")
        ax_array[1].xaxis_date()
        
        #Update Stats
        self.lab_a_t.SetLabel("Avg. Tasks/Day: " + str(round(sum(num_goals)/float(len(num_goals)),2)))
#         nt = [num_goals[i] - int(num_goals[i]*not_done_nf_percentage[i]/100) for i in range(len(num_goals))]
#         tc = [int(num_goals[i]*done_percentage[i]/100) + int((partially_done_percentage[i]/100)/2) for i in range(len(num_goals))]
#         atc = [tc[i]/(nt[i] + .00001) for i in range(len(num_goals))]
#         tcp = sum(atc)
        #FIX DBZ SHIT
        self.lab_a_c.SetLabel("Avg. Completion (%): " + str(round(100*sum(done_percentage)/(sum(done_percentage) + sum(not_done_percentage)),2)))
        self.lab_t_d.SetLabel("Tasks Done: " + str(sum([int(done_percentage[i]*num_goals[i]/100) for i in range(len(num_goals))])))
        
        
    def ondatesel(self,e):  
        old_nl = self.nodelist   
        self.nodelist = subset_nodes(self.nodelist,self.dp_beg.GetValue(),self.dp_end.GetValue())
        
        self.main_sizer.Remove(self.r_sizer)
        self.draw(5)   
        
        self.nodelist = old_nl  #Hacky, fix when possible 
        self.r_sizer = fig_pan(self)
 
        self.main_sizer.Add(self.r_sizer,8,wx.EXPAND | wx.ALL | wx.ALIGN_LEFT)
        self.SetSize(self.GetSize())        #Hack to get around refresh issues
 
        self.Show(True)