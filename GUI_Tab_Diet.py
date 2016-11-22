'''
Created on Jun 5, 2016

'''

from constants import *

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

import vis_diet
from GUI_lib import *

class Tab_Diet(wx.Panel):
    
    def __init__(self, parent, nodelist):
                
        self.fig = None
        self.canvas = None
        self.nodelist = nodelist
            
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
                
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        l_vbox_pan = lvpan(self)        
        self.dp_beg.SetValue(wx.DateTimeFromDMY(1,0,2014))
        
        v_line = wx.StaticLine(self, style=wx.LI_VERTICAL)
        h_line = wx.StaticLine(self, style=wx.LI_VERTICAL) 
        
        #LABELS                 
        self.lab_a_kc = wx.StaticText(l_vbox_pan, label='Avg. Intake (kCal):')
        self.lab_mx_kc = wx.StaticText(l_vbox_pan, label='Max. Intake (kCal):')
        self.lab_sd_kc = wx.StaticText(l_vbox_pan, label='Std. Intake (kCal):')
        
        self.lab_a_p = wx.StaticText(l_vbox_pan, label='Avg. Protein (g):')
        self.lab_mi_p = wx.StaticText(l_vbox_pan, label='Min. Protein (g):')
        self.lab_sd_p = wx.StaticText(l_vbox_pan, label='Std. Protein (g):')
        
        self.lab_a_t = wx.StaticText(l_vbox_pan, label='Avg. TDEE (kCal):')
        self.lab_mi_t = wx.StaticText(l_vbox_pan, label='Max. TDEE (kCal):')
        self.lab_mx_t = wx.StaticText(l_vbox_pan, label='Min. TDEE (kCal):')
        self.lab_sd_t = wx.StaticText(l_vbox_pan, label='Std. TDEE (kCal):')
        
        self.lab_a_n = wx.StaticText(l_vbox_pan, label='Avg. Net CI (kCal):')
        self.lab_mi_n = wx.StaticText(l_vbox_pan, label='Max. Net CI (kCal):')
        self.lab_mx_n = wx.StaticText(l_vbox_pan, label='Min. Net CI (kCal):')
        self.lab_sd_n = wx.StaticText(l_vbox_pan, label='Std. Net CI (kCal):')
        
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
        self.lvp_sizer.Add(self.lab_a_kc,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mx_kc,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_sd_kc,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 10) 
        self.lvp_sizer.Add(self.lab_a_p,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mi_p,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_sd_p,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 10) 
        self.lvp_sizer.Add(self.lab_a_t,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mi_t,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mx_t,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_sd_t,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 10) 
        self.lvp_sizer.Add(self.lab_a_n,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mi_n,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mx_n,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_sd_n,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
    
        #Misc Setup
        self.r_sizer = fig_pan(self)
        self.main_sizer.Add(l_sizer,0,wx.EXPAND | wx.ALIGN_LEFT)
        self.main_sizer.Add(v_line,0,wx.EXPAND | wx.ALL)
        self.main_sizer.Add(self.r_sizer,8,wx.EXPAND | wx.ALL | wx.ALIGN_LEFT)
        
        self.SetSizer(self.main_sizer)
        self.Show(True)
        
    def draw(self,n=5):
        nodes = sort_nodes(self.nodelist) #HACK: FIX (nodes are coming unsorted somewhere, which was causing problems drawing rects
        
        #Don't bother to pass the number of taps, just read it out
        spv = self.spin_taps.GetValue()
        if spv > 1:
            n = spv
            
        #Plots a 3 window graph of daily caloric intake, daily protein intake, and daily TDEE
        dates =[nodes[node].get_date() for node in nodes]
        cals = [nodes[node].get_calorie_intake() for node in nodes]
        prots = [nodes[node].get_protein_intake() for node in nodes]    
        tdees = [nodes[node].get_tdee() for node in nodes]
        #fics = [nodes[node].get_fic() for node in nodes]
        
        #Provide an offset for static values; this allows for adjusted ranges
        date_offset = dates[0] - BEG_DATE
        
        net_cis = pylab.subtract(cals,tdees) #Note: the first part of this range is invalid due to nonexistent data. Use truncated_net_cis; plot against truncated_dates
        truncated_net_cis = net_cis[max(TDEE_OFFSET - date_offset.days,0):]
        
        #Note: the first part of this range is invalid due to nonexistent data. Use truncated_tdees; plot against truncated_dates
        truncated_tdees = tdees[max(TDEE_OFFSET - date_offset.days,0):]
        truncated_dates = dates[max(TDEE_OFFSET - date_offset.days,0):]
         
        #UPDATE STATS
        self.lab_a_kc.SetLabel("Avg. Intake (kCal): " + str(round(sum(cals)/float(len(cals)),2)))  
        self.lab_mx_kc.SetLabel("Max. Intake (kCal): " + str(max(cals))) 
        self.lab_sd_kc.SetLabel("Std. Intake (kCal): " + str(round(numpy.std((cals)),2))) 

        self.lab_a_p.SetLabel("Avg. Protein (g): " + str(round(sum(prots)/float(len(prots)),2)))  
        self.lab_mi_p.SetLabel("Min. Protein (g): " + str(min(prots))) 
        self.lab_sd_p.SetLabel("Std. Protein (g): " + str(round(numpy.std((prots)),2))) 
                
        self.lab_a_t.SetLabel("Avg. TDEE (kCal): " + str(round(sum(truncated_tdees)/float(len(truncated_tdees)),2)))  
        self.lab_mx_t.SetLabel("Max. TDEE (kCal): " + str(max(truncated_tdees)))
        self.lab_mi_t.SetLabel("Min. TDEE (kCal): " + str(min(truncated_tdees))) 
        self.lab_sd_t.SetLabel("Std. TDEE (kCal): " + str(round(numpy.std((truncated_tdees)),2)))   
        
        self.lab_a_n.SetLabel("Avg. Net CI (kCal): " + str(round(sum(truncated_net_cis)/float(len(truncated_net_cis)),2)))  
        self.lab_mx_n.SetLabel("Max. Net CI (kCal): " + str(max(truncated_net_cis)))
        self.lab_mi_n.SetLabel("Min. Net CI (kCal): " + str(min(truncated_net_cis))) 
        self.lab_sd_n.SetLabel("Std. Net CI (kCal): " + str(round(numpy.std((truncated_net_cis)),2)))  
         
        #PLOT  
        self.fig,ax_array = pylab.subplots(4)
        self.fig.tight_layout()
        self.fig.subplots_adjust(hspace=.15)
        self.fig.canvas.set_window_title('Nutrient Intake') 
         
        #Plot Calorie Intake       
        pylab.setp(ax_array[0].get_xticklabels(), visible=False)
        rects = create_bg_rects(nodes,max(cals)*1.1)
        for r in rects:
            ax_array[0].add_patch(r)
        ax_array[0].plot_date(dates,cals,marker='.',linestyle=' ',color='r',label = 'Daily Calories')
        ax_array[0].plot_date(dates,moving_avg(cals,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
        ax_array[0].set_ylim([0,max(cals)*1.1])
        ax_array[0].set_title('Calorie Intake')
        ax_array[0].set_ylabel('Calories (kCal)')
        ax_array[0].legend(loc='upper left', shadow=True, fontsize='small')
        
        #Plot Protein Intake
        pylab.setp(ax_array[1].get_xticklabels(), visible=False)
        rects = create_bg_rects(nodes,max(prots)*1.1)
        for r in rects:
            ax_array[1].add_patch(r)
        ax_array[1].plot_date(dates,prots,marker='.',linestyle=' ',color='r',label = 'Daily Protein')
        ax_array[1].plot_date(dates,moving_avg(prots,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
        ax_array[1].set_ylim([0,max(prots)*1.1])
        ax_array[1].set_title('Protein')
        ax_array[1].set_ylabel('Protein (g)')
        ax_array[1].legend(loc='upper left', shadow=True, fontsize='small')
        
        #Plot Estimated TDEE
        pylab.setp(ax_array[2].get_xticklabels(), visible=False)
        rects = create_bg_rects(nodes,max(tdees)*1.1)
        for r in rects:
            ax_array[2].add_patch(r)
        ax_array[2].plot_date(truncated_dates,truncated_tdees,marker='.',linestyle=' ',color='r',label = 'Daily TDEE')
        ax_array[2].plot_date(truncated_dates,moving_avg(truncated_tdees,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
        ax_array[2].set_ylim([0,max(tdees)*1.1])
        ax_array[2].set_title('Estimated TDEE (kCal)')
        ax_array[2].set_ylabel('Est. TDEE (kCal)')
        ax_array[2].legend(loc='upper left', shadow=True, fontsize='small')
    
        #Plot Cals - TDEE
        pylab.setp(ax_array[3].xaxis.get_majorticklabels(), rotation=20)
        rects = create_bg_rects(nodes,max(truncated_net_cis)*1.1,min(truncated_net_cis)*1.1)
        for r in rects:
            ax_array[3].add_patch(r)
        ax_array[3].plot_date(truncated_dates,truncated_net_cis,marker='.',linestyle=' ',color='r',label = 'Net Caloric Intake')
        ax_array[3].plot_date(truncated_dates,moving_avg(truncated_net_cis,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
        ax_array[3].set_ylim([min(truncated_net_cis)*1.1,max(truncated_net_cis)*1.1])
        ax_array[3].set_title('Net Caloric Intake')
        ax_array[3].set_ylabel('Calories (kCal)')
        ax_array[3].legend(loc='upper left', shadow=True, fontsize='small')
        ax_array[3].axhline(y=0, color='k')       
                 
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
    