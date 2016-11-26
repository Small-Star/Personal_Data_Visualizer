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
 
        
        #self.lab_po_a = wx.StaticText(l_vbox_pan, label='Plot Activation')
        #self.lab_po_v = wx.StaticText(l_vbox_pan, label='Plot Valence')
              
        self.lab_a_a = wx.StaticText(l_vbox_pan, label='Avg. Activation:')
        self.lab_mx_a = wx.StaticText(l_vbox_pan, label='Max. Activation:')
        self.lab_mi_a = wx.StaticText(l_vbox_pan, label='Min. Activation:')
        self.lab_sd_a = wx.StaticText(l_vbox_pan, label='Std. Activation:')
        
        self.lab_a_v = wx.StaticText(l_vbox_pan, label='Avg. Valence:')
        self.lab_mx_v = wx.StaticText(l_vbox_pan, label='Max. Valence:')
        self.lab_mi_v = wx.StaticText(l_vbox_pan, label='Min. Valence:')
        self.lab_sd_v = wx.StaticText(l_vbox_pan, label='Std. Valence:')
        
        self.lab_mc_s = wx.StaticText(l_vbox_pan, label='A0:V0') #FINISH
                        
        #STATIC TXTS    
        self.t_po = wx.StaticText(l_vbox_pan, label='PLOTTING OPTIONS') 
        self.t_po.SetFont(self.bold_font)  
        t_stats = wx.StaticText(l_vbox_pan, label="STATS")
        t_stats.SetFont(self.header_font)   
        self.t_mc_e = wx.StaticText(l_vbox_pan, label='MOST COMMON STATE')        
        self.t_mc_e.SetFont(self.header_font)  
                     
        #DRAW   
        self.draw(5)
        
        #LEFT PANEL SETUP
        l_sizer = wx.BoxSizer(wx.VERTICAL)
        l_vbox_pan.SetSizer(self.lvp_sizer)
        l_sizer.Add(l_vbox_pan, 0, flag=wx.EXPAND | wx.ALL, border = 10)
        
        #Plotting Control Checkboxes
        self.cb_a = wx.CheckBox(l_vbox_pan, label='Activation', pos=(20, 20))
        self.cb_a.SetValue(True)
        self.cb_a.Bind(wx.EVT_CHECKBOX, self.PlotOpts)
        
        self.cb_v = wx.CheckBox(l_vbox_pan, label='Valence', pos=(20, 20))
        self.cb_v.SetValue(True)
        self.cb_v.Bind(wx.EVT_CHECKBOX, self.PlotOpts)
        
        self.cb_bars = wx.CheckBox(l_vbox_pan, label='Show Bars', pos=(20, 20))
        self.cb_bars.SetValue(False)
        self.cb_bars.Bind(wx.EVT_CHECKBOX, self.PlotOpts)
        
        self.cb_rep_bars = wx.CheckBox(l_vbox_pan, label='Representative Bars Only', pos=(20, 20))
        self.cb_rep_bars.SetValue(False)
        self.cb_rep_bars.Bind(wx.EVT_CHECKBOX, self.PlotOpts)
        
        #Add Elements to Sizer
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 10) 
        self.lvp_sizer.Add(self.t_po,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 10) 
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 5) 
        self.lvp_sizer.Add(self.cb_a,0, flag=wx.EXPAND | wx.ALL, border = 5) 
        self.lvp_sizer.Add(self.cb_v,0, flag=wx.EXPAND | wx.ALL, border = 5) 
        self.lvp_sizer.Add(self.cb_bars,0, flag=wx.EXPAND | wx.ALL, border = 5)
        self.lvp_sizer.Add(self.cb_rep_bars,0, flag=wx.EXPAND | wx.ALL, border = 5)
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
        self.lvp_sizer.Add(self.t_mc_e,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 10)
        self.lvp_sizer.Add(self.lab_mc_s,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
    
        #Misc Setup
        self.r_sizer = fig_pan(self)
        self.main_sizer.Add(l_sizer,0,wx.EXPAND | wx.ALIGN_LEFT)
        self.main_sizer.Add(v_line,0,wx.EXPAND | wx.ALL)
        self.main_sizer.Add(self.r_sizer,8,wx.EXPAND | wx.ALL | wx.ALIGN_LEFT)
        
        self.SetSizer(self.main_sizer)
        self.Show(True)
        
    def PlotOpts(self,e): 
        self.main_sizer.Remove(self.r_sizer)
        
        self.draw(plot_activation=self.cb_a.GetValue(),plot_valence=self.cb_v.GetValue(),plot_bars=self.cb_bars.GetValue(),plot_rep_bars=self.cb_rep_bars.GetValue())   

        self.r_sizer = fig_pan(self)
 
        self.main_sizer.Add(self.r_sizer,8,wx.EXPAND | wx.ALL | wx.ALIGN_LEFT)
        self.SetSize(self.GetSize())        #Hack to get around refresh issues
 
        self.Show(True)
    
    def draw(self, n=5, plot_activation=True,plot_valence=True, plot_bars=True, plot_rep_bars=False):
        nodes = sort_nodes(self.nodelist) #HACK: FIX (nodes are coming unsorted somewhere, which was causing problems drawing rects
        
        color_activation = '#99423f'
        color_valence = '#54675c'
        
        #Don't bother to pass the number of taps, just read it out
        spv = self.spin_taps.GetValue()
        if spv > 1:
            n = spv
            
        dates = [nodes[node].get_date() for node in nodes if nodes[node].get_mood() != (('','',''),('','',''))]
        moods = [nodes[node].get_mood() for node in nodes if nodes[node].get_mood() != (('','',''),('','',''))]
        
        if plot_activation:
            a_l = [x[0][0] for x in moods]
            a_u = [x[0][1] for x in moods]
            a_s = [x[0][2] for x in moods]
        
        if plot_valence:
            v_l = [x[1][0] for x in moods]
            v_u = [x[1][1] for x in moods]
            v_s = [x[1][2] for x in moods]

        if plot_activation:        
            a_mid = [sum(x)/2.0 for x in zip(a_l, a_u)]
        if plot_valence:
            v_mid = [sum(x)/2.0 for x in zip(v_l, v_u)]
        
        #UPDATE STATS   
        
        if plot_activation:
            self.lab_a_a.SetLabel("Avg. Activation: "+ str(round(np.mean(a_mid),2)))
            self.lab_mx_a.SetLabel("Max. Activation: "+ str(max(a_u)))
            self.lab_mi_a.SetLabel("Min. Activation: "+ str(min(a_l)))
            self.lab_sd_a.SetLabel("Std. Activation: "+ str(round(np.std(a_mid),2))) 
        
        if plot_valence:
            self.lab_a_v.SetLabel("Avg. Valence: "+ str(round(np.mean(v_mid),2)))
            self.lab_mx_v.SetLabel("Max. Valence: "+ str(max(v_u)))
            self.lab_mi_v.SetLabel("Min. Valence: "+ str(min(v_l)))
            self.lab_sd_v.SetLabel("Std. Valence: "+ str(round(np.std(v_mid),2)))                   
            
        self.fig,ax_array = pylab.subplots(1)
        self.fig.tight_layout()
        self.fig.canvas.set_window_title('Mood') 
                
        pylab.setp(ax_array.xaxis.get_majorticklabels(), rotation=20)
        
        #Don't show rects if plotting both datasets, it's too busy
        if plot_bars and plot_activation and not plot_valence:
                rects = create_mood_rects(dates,a_u,a_l,a_s,'activation',plot_rep_bars)            
        if plot_bars and plot_valence and not plot_activation:
                rects = create_mood_rects(dates,v_u,v_l,v_s,'valence',plot_rep_bars)
        
        if plot_bars and (plot_activation ^ plot_valence):
            for r in rects:
                ax_array.add_patch(r)
        
        if plot_activation:
            ax_array.plot_date(dates,a_l,marker='x',linestyle=' ',color=color_activation,label = 'Activation (LB)')
            ax_array.plot_date(dates,moving_avg(a_l,n,True),marker='',linestyle='-', linewidth=3,color=color_activation,label = 'Moving Avg. (' + str(n) + ') taps')
            ax_array.plot_date(dates,a_u,marker='x',linestyle=' ',color=color_activation,label = 'Activation (UB)')
            ax_array.plot_date(dates,moving_avg(a_u,n,True),marker='',linestyle='-', linewidth=3,color=color_activation,label = 'Moving Avg. (' + str(n) + ') taps')

        if plot_valence:
            ax_array.plot_date(dates,v_l,marker='x',linestyle=' ',color=color_valence,label = 'Valence (LB)')
            ax_array.plot_date(dates,moving_avg(v_l,n,True),marker='',linestyle='-', linewidth=3,color=color_valence,label = 'Moving Avg. (' + str(n) + ') taps')
            ax_array.plot_date(dates,v_u,marker='x',linestyle=' ',color=color_valence,label = 'Valence (UB)')
            ax_array.plot_date(dates,moving_avg(v_u,n,True),marker='',linestyle='-', linewidth=3,color=color_valence,label = 'Moving Avg. (' + str(n) + ') taps')
        ax_array.set_ylim([1,9])

        ax_array.set_title('Mood (Circumplex Model)')        
        ax_array.set_ylabel('Intensity')
        ax_array.legend(loc='upper left', shadow=True, fontsize='small')
 
    def ondatesel(self,e):    
        old_nl = self.nodelist   
        self.nodelist = subset_nodes(self.nodelist,self.dp_beg.GetValue(),self.dp_end.GetValue())
        
        self.main_sizer.Remove(self.r_sizer)
        self.draw(n=self.spin_taps.GetValue(),plot_activation=self.cb_a.GetValue(),plot_valence=self.cb_v.GetValue(),plot_bars=self.cb_bars.GetValue(),plot_rep_bars=self.cb_rep_bars.GetValue()) 
        
        self.nodelist = old_nl  #Hacky, fix when possible 
        self.r_sizer = fig_pan(self)
 
        self.main_sizer.Add(self.r_sizer,8,wx.EXPAND | wx.ALL | wx.ALIGN_LEFT)
        self.SetSize(self.GetSize())        #Hack to get around refresh issues
 
        self.Show(True)