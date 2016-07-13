'''
Created on Jun 6, 2016

'''

from constants import *

import wx
import wxmplot
import numpy
import pylab
import copy

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from vis_graphs_lib import *
from vis_diet import *
from vis_goals import *
from vis_records import *
from vis_weightlifting import *

from GUI_lib import *

class Tab_Lift(wx.Panel):
    
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
        self.lab_s_mw = wx.StaticText(l_vbox_pan, label='Starting Max (lbs):')
        self.lab_pr_mw = wx.StaticText(l_vbox_pan, label='PR Max (lbs):')
        self.lab_i_mw = wx.StaticText(l_vbox_pan,label='Improvement:')
        
        self.lab_s_vs = wx.StaticText(l_vbox_pan, label='Starting V/S (lbs):')
        self.lab_pr_vs = wx.StaticText(l_vbox_pan, label='PR V/S (lbs):')
        self.lab_i_vs = wx.StaticText(l_vbox_pan,label='Improvement:')
        
        self.lab_t_vol = wx.StaticText(l_vbox_pan, label='Total Vol (lbs):') 
        
        self.lab_i_mw.SetFont(self.bold_font)
        self.lab_i_vs.SetFont(self.bold_font)
        self.lab_t_vol.SetFont(self.bold_font)
                 
        #STATIC TXTS
        t_lift_select = wx.StaticText(l_vbox_pan, label="SELECT LIFT")
        t_lift_select.SetFont(self.header_font)
                
        t_stats = wx.StaticText(l_vbox_pan, label="STATS")
        t_stats.SetFont(self.header_font)   
                      
        #DRAW 
        self.draw(DEFAULT_LIFT,5)

        #LEFT PANEL SETUP
        l_sizer = wx.BoxSizer(wx.VERTICAL)

        l_vbox_pan.SetSizer(self.lvp_sizer)
        l_sizer.Add(l_vbox_pan, 0, flag=wx.EXPAND | wx.ALL, border = 10)
                
        #Lift Select ComboBox
        self.cb_lift = wx.ComboBox(l_vbox_pan, value=DEFAULT_LIFT,choices=self.get_lift_list(), style=wx.CB_READONLY)
        self.cb_lift.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        
        #Culling Checkbox
        self.cb_cull = wx.CheckBox(l_vbox_pan, label='Cull Non-Work Sets?', pos=(20, 20))
        self.cb_cull.SetValue(False)
        self.cb_cull.Bind(wx.EVT_CHECKBOX, self.Culling)
         
        #Add Elements to Sizer
        self.lvp_sizer.Add(t_lift_select,0, flag=wx.EXPAND | wx.TOP | wx.LEFT, border = 10)
        self.lvp_sizer.Add(self.cb_lift,0, flag=wx.EXPAND | wx.ALL, border = 10) 
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 5) 
        self.lvp_sizer.Add(self.cb_cull,0, flag=wx.EXPAND | wx.ALL, border = 10) 
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 10) 
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 10) 
        self.lvp_sizer.Add(t_stats,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 10) 
        self.lvp_sizer.Add(self.lab_s_mw,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_pr_mw,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25) 
        self.lvp_sizer.Add(self.lab_i_mw,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)  
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 10)  
        self.lvp_sizer.Add(self.lab_s_vs,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
        self.lvp_sizer.Add(self.lab_pr_vs,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25) 
        self.lvp_sizer.Add(self.lab_i_vs,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25) 
        self.lvp_sizer.Add(h_line,0,wx.EXPAND | wx.ALL, border = 10)           
        self.lvp_sizer.Add(self.lab_t_vol,0,wx.EXPAND | wx.LEFT | wx.ALIGN_LEFT, border = 25)
              
        #MAIN SIZER SETUP  
        self.r_sizer = fig_pan(self)
        self.main_sizer.Add(l_sizer,0,wx.EXPAND | wx.ALIGN_LEFT)
        self.main_sizer.Add(v_line,0,wx.EXPAND | wx.ALL)
        self.main_sizer.Add(self.r_sizer,8,wx.EXPAND | wx.ALL | wx.ALIGN_LEFT)
        self.SetSizer(self.main_sizer)
        
        self.Show(True)
        
    def Culling(self,e): 
        sender = e.GetEventObject()
        isChecked = sender.GetValue()

        self.main_sizer.Remove(self.r_sizer)
        
        self.draw(lift=self.cb_lift.GetValue(),cull=isChecked)   

        self.r_sizer = fig_pan(self)
 
        self.main_sizer.Add(self.r_sizer,8,wx.EXPAND | wx.ALL | wx.ALIGN_LEFT)
        self.SetSize(self.GetSize())        #Hack to get around refresh issues
 
        self.Show(True)
    
    def ondatesel(self,e):  
        old_nl = self.nodelist   
        self.nodelist = subset_nodes(self.nodelist,self.dp_beg.GetValue(),self.dp_end.GetValue())
        
        self.main_sizer.Remove(self.r_sizer)
        self.draw(lift=self.cb_lift.GetValue())   
        
        self.nodelist = old_nl  #Hacky, fix when possible 
        self.r_sizer = fig_pan(self)
 
        self.main_sizer.Add(self.r_sizer,8,wx.EXPAND | wx.ALL | wx.ALIGN_LEFT)
        self.SetSize(self.GetSize())        #Hack to get around refresh issues
 
        self.Show(True)
    
    def get_lift_list(self):
        nodes = self.nodelist
        
        ls = [nodes[node].get_bnode().get_workout().get_lifts() for node in nodes if nodes[node].get_bnode().worked_out() == True]
        pruned_ls = [x[y][0][0] for x in ls if x != [] for y in range(len(x))]
        lifts = []
        
        for l in pruned_ls:
            if l not in lifts:
                lifts.append(l)
        return sorted(lifts)
        
    def OnSelect(self, e):
        i = e.GetString()
        self.main_sizer.Remove(self.r_sizer)
        self.draw(i)    
        self.r_sizer = fig_pan(self)

        self.main_sizer.Add(self.r_sizer,8,wx.EXPAND | wx.ALL | wx.ALIGN_LEFT)
        self.SetSize(self.GetSize())        #Hack to get around refresh issues

        self.Show(True)
        
    def draw(self, lift='Bench Press', n=5,cull=False):
        nodes=self.nodelist
        
        #Don't bother to pass the number of taps, just read it out
        spv = self.spin_taps.GetValue()
        if spv > 1:
            n = spv
                    
        dates = [nodes[node].get_date() for node in nodes]
        lifts = [(nodes[node].get_bnode().get_workout().get_lift(lift),nodes[node].get_date()) if nodes[node].get_bnode().worked_out() == True else ([],nodes[node].get_date()) for node in nodes ]   
        
        #CALCULATE
        
        #Figure out if lift is isometric or not based on presence of seconds indicator
        for l in range(len(lifts)):
            if lifts[l][0] != []:
                if lifts[l][0][0][0][1] != []:
                    #print str(lifts[l][0][0][0][1].split('x')[1])[-1]
                    if str(lifts[l][0][0][0][1].split('x')[1])[-1] == 's':
                        is_isometric = True
                    else:
                        is_isometric = False
                    break

        raw_nums = []
        max_weight = []
        total_vol = []
        max_vol_per_set = []
        
        #Run through all returned lifts              
        for r1 in range(len(lifts)):
            if lifts[r1][0] == []:
                max_weight.append(-1) #FIX these
                total_vol.append(-1)
                max_vol_per_set.append(-1)
                continue
            #date = lifts[r1][1]
            m_w = 0
            m_w_t = 0
            t_v = 0
            m_v_p_s = 0
            #print lifts[r1][0][0][0][1].split('x')[0][-1]
            
            lift_day = lifts[r1][0][0]
            
            if cull == True:
                for r2 in range(len(lift_day)):
                    w_str = lift_day[r2][1].split('x')[0]
                    if w_str != 'BW':
                        w = int(w_str)
                    elif w_str == 'BW':
                        w = 150     #FIX: This is just a standin for actual bodyweight on that day     
                    if w > m_w_t:
                        m_w_t = w
                       
            for r3 in range(len(lift_day)):
                w_str = lift_day[r3][1].split('x')[0]
                if w_str != 'BW':
                    w = int(w_str)
                elif w_str == 'BW':
                    w = 150     #FIX: This is just a standin for actual bodyweight on that day
                r = int(lift_day[r3][1].split('x')[1].strip('IFs '))    #Stripping indicator of isometric; also ignoring failure/injury indicator ***FIX THIS***
                
                #Culling
                if cull == True:
                    if w <= m_w_t*(100-CULL_PERCENTAGE)/100:
                        #Skip lift if not greater than CULL_PERCENTAGE away from max
                        continue
                raw_nums.append((w,r))
                
                if w > m_w:
                        m_w = w
                        
                t_v += w*r
                    
                if w*r > m_v_p_s:
                    m_v_p_s = w*r
            
            #Update lists for each lift
            max_weight.append(m_w)
            total_vol.append(t_v)
            max_vol_per_set.append(m_v_p_s)  

        #Interpolate nonexistent data
        d_ord_p = [lifts[d][1].toordinal() for d in range(len(lifts)) if max_weight[d] != -1] #Dates that have lifts present
        #d_ord_np = [lifts[d][1].toordinal() for d in range(len(lifts)) if max_weight[d] == -1] #Dates that do not have lifts present
        d_ord_total = [lifts[d][1].toordinal() for d in range(len(lifts))]

        #Filter out filler data
        f_max_weight = [max_weight[x] for x in range(len(max_weight)) if max_weight[x] != -1]
        f_total_vol = [total_vol[x] for x in range(len(total_vol)) if total_vol[x] != -1]
        f_max_vol_per_set = [max_vol_per_set[x] for x in range(len(max_vol_per_set)) if max_vol_per_set[x] != -1]      
        
        #Perform interpolation  
        i_max_weight = np.interp(d_ord_total,d_ord_p,f_max_weight)  
        i_total_vol = np.interp(d_ord_total,d_ord_p,f_total_vol)  
        i_max_vol_per_set = np.interp(d_ord_total,d_ord_p,f_max_vol_per_set)                 
        
        #UPDATE STATS
        s_mw = max_weight[max_weight.index(filter(lambda x: x>0, max_weight)[0])]
        pr_mw = max(max_weight)
        
        s_vs = max_vol_per_set[max_vol_per_set.index(filter(lambda x: x>0, max_vol_per_set)[0])]
        pr_vs = max(max_vol_per_set)
        
        if is_isometric == False:
            self.lab_s_mw.SetLabel("Starting Max (lbs): " + str(s_mw))        
            self.lab_pr_mw.SetLabel("PR Max (lbs): " + str(pr_mw))
            self.lab_i_mw.SetLabel("Improvement: " + str(pr_mw - s_mw)) 
            self.lab_s_vs.SetLabel("Starting V/S (lbs): " + str(s_vs))
            self.lab_pr_vs.SetLabel("PR V/S (lbs): " + str(pr_vs))
            self.lab_i_vs.SetLabel("Improvement: " + str(pr_vs - s_vs))
            self.lab_t_vol.SetLabel('Total Vol (lbs): ' + str(sum(total_vol))) 
        
        elif is_isometric == True:      
            self.lab_s_mw.SetLabel("Starting Max (lbs): n/a")        
            self.lab_pr_mw.SetLabel("PR Max (lbs): n/a")
            self.lab_i_mw.SetLabel("Improvement: n/a") 
            self.lab_s_vs.SetLabel("Starting V/S (lb-sec): " + str(s_vs))
            self.lab_pr_vs.SetLabel("PR V/S (lb-sec): " + str(pr_vs))
            self.lab_i_vs.SetLabel("Improvement: " + str(pr_vs - s_vs))
            self.lab_t_vol.SetLabel('Total Vol (lb-sec): ' + str(sum(total_vol))) 
            
        #PLOT
        self.fig,ax_array = pylab.subplots(3)
        self.fig.tight_layout()
        self.fig.canvas.set_window_title(lift + ' Lift Numbers') 
        
        #Plot Vol/Set
        pylab.setp(ax_array[0].xaxis.get_majorticklabels(), rotation=20)
        rects = create_bg_rects(nodes,max(max_vol_per_set)*1.1)
        for r in rects:
            ax_array[0].add_patch(r)
        if is_isometric == False:
            ax_array[0].plot_date(dates,max_vol_per_set,marker='.',linestyle=' ',color='r',label = 'Max Volume/Set (lbs)')
            ax_array[0].plot_date(dates,moving_avg(i_max_vol_per_set,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
            ax_array[0].set_ylim([min([m for m in max_vol_per_set if m > 0])*0.9,max(max_vol_per_set)*1.1])
            ax_array[0].set_title(lift + ' - Max Volume/Set')
            ax_array[0].set_ylabel('Weight (lbs)')
            ax_array[0].legend(loc='upper left', shadow=True, fontsize='small')  
                  
        elif is_isometric == True:
            ax_array[0].plot_date(dates,max_vol_per_set,marker='.',linestyle=' ',color='r',label = 'Max Volume/Set (lb-sec)')
            ax_array[0].plot_date(dates,moving_avg(i_max_vol_per_set,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
            ax_array[0].set_ylim([min([m for m in max_vol_per_set if m > 0])*0.9,max(max_vol_per_set)*1.1])
            ax_array[0].set_title(lift + ' - Max Volume/Set')
            ax_array[0].set_ylabel('Weight*Time (lb-sec)')
            ax_array[0].legend(loc='upper left', shadow=True, fontsize='small')
        
        #Plot Total Volume
        pylab.setp(ax_array[1].xaxis.get_majorticklabels(), rotation=20)
        rects = create_bg_rects(nodes,max(total_vol)*1.1)
        for r in rects:
            ax_array[1].add_patch(r)
        if is_isometric == False:
            ax_array[1].plot_date(dates,total_vol,marker='.',linestyle=' ',color='r',label = 'Total Volume (lbs)')
            ax_array[1].plot_date(dates,moving_avg(i_total_vol,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
            ax_array[1].set_ylim([min([m for m in total_vol if m > 0])*0.9,max(total_vol)*1.1])
            ax_array[1].set_title(lift + ' - Total Volume')
            ax_array[1].set_ylabel('Weight (lbs)')
            ax_array[1].legend(loc='upper left', shadow=True, fontsize='small')
            
        elif is_isometric == True:
            ax_array[1].plot_date(dates,total_vol,marker='.',linestyle=' ',color='r',label = 'Total Volume (lb-sec)')
            ax_array[1].plot_date(dates,moving_avg(i_total_vol,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
            ax_array[1].set_ylim([min([m for m in total_vol if m > 0])*0.9,max(total_vol)*1.1])
            ax_array[1].set_title(lift + ' - Total Volume')
            ax_array[1].set_ylabel('Weight*Time (lb-sec)')
            ax_array[1].legend(loc='upper left', shadow=True, fontsize='small')
        
        #Plot Max Weight
        pylab.setp(ax_array[2].xaxis.get_majorticklabels(), rotation=20)
        rects = create_bg_rects(nodes,max(max_weight)*1.1)
        for r in rects:
            ax_array[2].add_patch(r)
        ax_array[2].plot_date(dates,max_weight,marker='.',linestyle=' ',color='r',label = 'Max Weight (lbs)')
        ax_array[2].plot_date(dates,moving_avg(i_max_weight,n),marker='',linestyle='-',color='r',label = 'Moving Avg. (' + str(n) + ') taps')
        ax_array[2].set_ylim([min([m for m in max_weight if m > 0])*0.9,max(max_weight)*1.1])
        ax_array[2].set_title(lift + ' - Max Weight')
        ax_array[2].set_ylabel('Weight (lbs)')
        ax_array[2].legend(loc='upper left', shadow=True, fontsize='small')
