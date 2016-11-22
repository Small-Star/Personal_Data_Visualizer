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

class Tab_Mood(wx.Panel):
    
    def __init__(self, parent, nodelist):
                
        self.fig = None
        self.canvas = None
        self.nodelist = nodelist
            
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
                
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        l_vbox_pan = lvpan(self)        
        self.dp_beg.SetValue(wx.DateTimeFromDMY(30,10,2015))
        
        v_line = wx.StaticLine(self, style=wx.LI_VERTICAL)
        h_line = wx.StaticLine(self, style=wx.LI_VERTICAL) 
        
        #LABELS                 
        self.lab_a_a = wx.StaticText(l_vbox_pan, label='Avg. Activation:')
        self.lab_mx_a = wx.StaticText(l_vbox_pan, label='Max. Activation:')
        self.lab_mi_a = wx.StaticText(l_vbox_pan, label='Min. Activation:')
        self.lab_sd_a = wx.StaticText(l_vbox_pan, label='Std. Activation:')
        
        self.lab_a_v = wx.StaticText(l_vbox_pan, label='Avg. Valence:')
        self.lab_mx_v = wx.StaticText(l_vbox_pan, label='Max. Valence:')
        self.lab_mi_v = wx.StaticText(l_vbox_pan, label='Min. Valence:')
        self.lab_sd_v = wx.StaticText(l_vbox_pan, label='Std. Valence:')
        
        self.lab_mc_e = wx.StaticText(l_vbox_pan, label='MOST COMMON STATE')        
        self.lab_mc_e.SetFont(self.bold_font)  
        self.lab_mc_s = wx.StaticText(l_vbox_pan, label='A0:V0') #FINISH
                        
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
        self.lvp_sizer.Add(self.lab_a_a,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mx_a,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mi_a,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_sd_a,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 10) 
        self.lvp_sizer.Add(self.lab_a_v,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mx_v,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mi_v,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_sd_v,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 10)
        self.lvp_sizer.Add(self.lab_mc_e,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 10)
        self.lvp_sizer.Add(self.lab_mc_s,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
    
        #Misc Setup
        self.r_sizer = fig_pan(self)
        self.main_sizer.Add(l_sizer,0,wx.EXPAND | wx.ALIGN_LEFT)
        self.main_sizer.Add(v_line,0,wx.EXPAND | wx.ALL)
        self.main_sizer.Add(self.r_sizer,8,wx.EXPAND | wx.ALL | wx.ALIGN_LEFT)
        
        self.SetSizer(self.main_sizer)
        self.Show(True)
        
    def draw(self, n=5):
        nodes = sort_nodes(self.nodelist) #HACK: FIX (nodes are coming unsorted somewhere, which was causing problems drawing rects
        
        #Don't bother to pass the number of taps, just read it out
        spv = self.spin_taps.GetValue()
        if spv > 1:
            n = spv
            
        dates =[nodes[node].get_date() for node in nodes if nodes[node].get_mood() != (('','',''),('','',''))]
        moods = [nodes[node].get_mood() for node in nodes if nodes[node].get_mood() != (('','',''),('','',''))]
        a_l = [x[0][0] for x in moods]
        a_u = [x[0][1] for x in moods]
        a_s = [x[0][2] for x in moods]
        
        v_l = [x[1][0] for x in moods]
        v_u = [x[1][1] for x in moods]
        v_s = [x[1][2] for x in moods]
        
        a_mid = [sum(x)/2.0 for x in zip(a_l, a_u)]
        v_mid = [sum(x)/2.0 for x in zip(v_l, v_u)]
        
        #UPDATE STATS   
        self.lab_a_a.SetLabel("Avg. Activation: "+ str(round(np.mean(a_mid),2)))
        self.lab_mx_a.SetLabel("Max. Activation: "+ str(max(a_u)))
        self.lab_mi_a.SetLabel("Min. Activation: "+ str(min(a_l)))
        self.lab_sd_a.SetLabel("Std. Activation: "+ str(round(np.std(a_mid),2))) 
        
        self.lab_a_v.SetLabel("Avg. Valence: "+ str(round(np.mean(v_mid),2)))
        self.lab_mx_v.SetLabel("Max. Valence: "+ str(max(v_u)))
        self.lab_mi_v.SetLabel("Min. Valence: "+ str(min(v_l)))
        self.lab_sd_v.SetLabel("Std. Valence: "+ str(round(np.std(v_mid),2)))                   
        
        self.fig,ax_array = pylab.subplots(1)
        self.fig.tight_layout()
        self.fig.canvas.set_window_title('Mood') 
                
        pylab.setp(ax_array.xaxis.get_majorticklabels(), rotation=20)
        
        ax_array.plot_date(dates,a_l,marker='x',linestyle=' ',color='b',label = 'Activation (LB)')
        ax_array.plot_date(dates,moving_avg(a_l,n,True),marker='',linestyle='-', linewidth=3,color='b',label = 'Moving Avg. (' + str(n) + ') taps')
        ax_array.plot_date(dates,a_u,marker='x',linestyle=' ',color='b',label = 'Activation (UB)')
        ax_array.plot_date(dates,moving_avg(a_u,n,True),marker='',linestyle='-', linewidth=3,color='b',label = 'Moving Avg. (' + str(n) + ') taps')

        ax_array.plot_date(dates,v_l,marker='x',linestyle=' ',color='g',label = 'Valence (LB)')
        ax_array.plot_date(dates,moving_avg(v_l,n,True),marker='',linestyle='-', linewidth=3,color='g',label = 'Moving Avg. (' + str(n) + ') taps')
        ax_array.plot_date(dates,v_u,marker='x',linestyle=' ',color='g',label = 'Valence (UB)')
        ax_array.plot_date(dates,moving_avg(v_u,n,True),marker='',linestyle='-', linewidth=3,color='g',label = 'Moving Avg. (' + str(n) + ') taps')
        ax_array.set_ylim([1,9])

        ax_array.set_title('Mood (Circumplex Model)')        
        ax_array.set_ylabel('Intensity')
        ax_array.legend(loc='upper left', shadow=True, fontsize='small')
 

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