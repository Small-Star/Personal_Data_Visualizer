'''
Created on Jun 6, 2016

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

from GUI_lib import *

class Tab_Body(wx.Panel):
    
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
        self.lab_a_w = wx.StaticText(l_vbox_pan, label='Avg. Weight (lbs):')
        self.lab_mx_w = wx.StaticText(l_vbox_pan, label='Max. Weight (lbs):')
        self.lab_mi_w = wx.StaticText(l_vbox_pan, label='Min. Weight (lbs):')
        self.lab_sd_w = wx.StaticText(l_vbox_pan, label='Std. Weight (lbs):')
        
        self.lab_a_bf = wx.StaticText(l_vbox_pan, label='Avg. Bodyfat (%):')
        self.lab_mx_bf = wx.StaticText(l_vbox_pan, label='Max. Bodyfat (%):')
        self.lab_mi_bf = wx.StaticText(l_vbox_pan, label='Min. Bodyfat (%):')
        self.lab_sd_bf = wx.StaticText(l_vbox_pan, label='Std. Bodyfat (%):')
        
        self.lab_a_n = wx.StaticText(l_vbox_pan, label='Avg. Net CI (kCal):')
        
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
        self.lvp_sizer.Add(self.lab_a_w,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mx_w,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mi_w,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_sd_w,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 10)
        self.lvp_sizer.Add(self.lab_a_bf,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mx_bf,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_mi_bf,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_sd_bf,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 10)
        self.lvp_sizer.Add(self.lab_a_n,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
                        
        #Misc Setup
        self.r_sizer = fig_pan(self)
        self.main_sizer.Add(l_sizer,0,wx.EXPAND | wx.ALIGN_LEFT)
        self.main_sizer.Add(v_line,0,wx.EXPAND | wx.ALL)
        self.main_sizer.Add(self.r_sizer,8,wx.EXPAND | wx.ALL | wx.ALIGN_LEFT)
        
        self.SetSizer(self.main_sizer)
        self.Show(True)
        
    def draw(self, n=5):
        nodes = self.nodelist
        
        #Don't bother to pass the number of taps, just read it out
        spv = self.spin_taps.GetValue()
        if spv > 1:
            n = spv
            
        #Plots a 3 window graph of daily caloric intake (redundant, but useful for side by side comparison), daily weight, and daily bodyfat (TODO)
        dates =[nodes[node].get_date() for node in nodes]
        cals = [nodes[node].get_calorie_intake() for node in nodes]
        tdees = [nodes[node].get_tdee() for node in nodes]
        t_weights = [nodes[node].get_bnode().get_weight() for node in nodes]
        t_bfs = [nodes[node].get_bnode().get_bodyfat() for node in nodes]   
        
        #CALCULATION
        
        #Several messy things done to get rid of 0's for nonexistent numbers; FIX
        weights = []
        
        #Getting rid of 0's for nonexistent weights by using nearest neighbor - change to np.interp
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

        #Getting rid of 0's for nonexistent bfs by using nearest neighbor - change to np.interp
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
    
        if len(dates) != len(weights):
            weights.append(weights[-1]) #Jiggle by one hack
        if len(dates) != len(bodyfats):
            bodyfats.append(bodyfats[-1]) #Jiggle by one hack
        
        #Provide an offset for static values; this allows for adjusted ranges
        date_offset = dates[0] - BEG_DATE
        
        net_cis = pylab.subtract(cals,tdees) #Note: the first part of this range is invalid due to nonexistent data. Use truncated_net_cis; plot against truncated_dates
        truncated_net_cis = net_cis[max(TDEE_OFFSET - date_offset.days,0):]
        truncated_dates = dates[max(TDEE_OFFSET - date_offset.days,0):]
        
        truncated_bfs = bodyfats[max(BF_OFFSET - date_offset.days,0):] #Note: the first part of this range is invalid due to nonexistent data. Use truncated_bfs; plot against truncated_dates_bf
        truncated_dates_bf = dates[max(BF_OFFSET - date_offset.days,0):]

        #Update Stats
        self.lab_a_w.SetLabel("Avg. Weight (lbs): " + str(round(sum(weights)/float(len(weights)),2)))  
        self.lab_mx_w.SetLabel("Max. Weight (lbs): " + str(max(weights)))
        self.lab_mi_w.SetLabel("Min. Weight (lbs): " + str(min(weights))) 
        self.lab_sd_w.SetLabel("Std. Weight (lbs): " + str(round(numpy.std((weights)),2)))     
        
        self.lab_a_bf.SetLabel("Avg. Bodyfat (%): " + str(round(sum(truncated_bfs)/float(len(truncated_bfs)),2)))  
        self.lab_mx_bf.SetLabel("Max. Bodyfat (%): " + str(max(truncated_bfs)))
        self.lab_mi_bf.SetLabel("Min. Bodyfat (%): " + str(min(truncated_bfs))) 
        self.lab_sd_bf.SetLabel("Std. Bodyfat (%): " + str(round(numpy.std((truncated_bfs)),2)))      
        
        self.lab_a_n.SetLabel("Avg. Net CI (kCal): " + str(round(sum(truncated_net_cis)/float(len(truncated_net_cis)),2)))  
                         
        #PLOT
        self.fig,ax_array = pylab.subplots(4)
        self.fig.tight_layout()
        self.fig.subplots_adjust(hspace=.15)
        self.fig.canvas.set_window_title('BioData') 
            
        #Plot Weight
        pylab.setp(ax_array[0].get_xticklabels(), visible=False)
        rects = create_bg_rects(nodes,110,180) #HACK
        for r in rects:
            ax_array[0].add_patch(r)
        ax_array[0].plot_date(dates,weights,marker='.',linestyle=' ',color='r',label = 'Weight')
        ax_array[0].plot_date(dates,moving_avg(weights,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
        ax_array[0].set_ylim([min(weights) - 5,max(weights) + 5])
        ax_array[0].set_title('Weight')
        ax_array[0].set_ylabel('Weight (lb)')
        ax_array[0].legend(loc='upper left', shadow=True, fontsize='small')
        
        #Plot Bodyfat
        pylab.setp(ax_array[1].get_xticklabels(), visible=False)
        rects = create_bg_rects(nodes,6,30) #HACK
        for r in rects:
            ax_array[1].add_patch(r)
        ax_array[1].plot_date(truncated_dates_bf,truncated_bfs,marker='.',linestyle=' ',color='r',label = 'Bodyfat')
        ax_array[1].plot_date(truncated_dates_bf,moving_avg(truncated_bfs,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
        ax_array[1].set_ylim([min(truncated_bfs) - 2,max(truncated_bfs) + 2])
        ax_array[1].set_title('Bodyfat')
        ax_array[1].set_ylabel('Bodyfat (%)')
        ax_array[1].legend(loc='upper left', shadow=True, fontsize='small')
        
        #Plot Cals - TDEE
        pylab.setp(ax_array[2].get_xticklabels(), visible=False)
        rects = create_bg_rects(nodes,max(truncated_net_cis)*1.1,min(truncated_net_cis)*1.1)
        for r in rects:
            ax_array[2].add_patch(r)
             
        ax_array[2].plot_date(truncated_dates,truncated_net_cis,marker='.',linestyle=' ',color='r',label = 'Net Caloric Intake')
        ax_array[2].plot_date(truncated_dates,moving_avg(truncated_net_cis,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
        ax_array[2].set_ylim([min(truncated_net_cis)*1.1,max(truncated_net_cis)*1.1])
        ax_array[2].set_title('Net Caloric Intake')
        ax_array[2].set_ylabel('Calories (kCal)')
        ax_array[2].legend(loc='upper left', shadow=True, fontsize='small')
        ax_array[2].axhline(y=0, color='k')
        
        #Plot Combo
        
        #Find offsets - normalize to weight
        #FIX - normalize properly
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
    