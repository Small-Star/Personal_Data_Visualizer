'''
Created on Jun 6, 2016

'''
import wx
import datetime
import collections

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
        
def lvpan(self,ar=True,af=True):
    #MISC
    self.bold_font = wx.Font(10, wx.MODERN, wx.BOLD, wx.NORMAL, False, u'Consolas')
    self.header_font = wx.Font(11, wx.MODERN, wx.BOLD, wx.NORMAL, False, u'Consolas')
    
    l_vbox_pan = wx.Panel(self)
    l_vbox_pan.SetBackgroundColour('#CEDED7')
    l_vbox_pan.SetMinSize((200,930))

    self.lvp_sizer = wx.BoxSizer(wx.VERTICAL)
    l_vbox_pan.SetSizer(self.lvp_sizer) 
    
    if ar:
        #header_font = wx.Font(11, wx.MODERN, wx.BOLD, wx.NORMAL, False, u'Consolas')
                
        t_adj_range = wx.StaticText(l_vbox_pan, label="ADJUST RANGE")
        t_adj_range.SetFont(self.header_font)
        
        #Date Range Selector
        dp_sizer_beg = wx.BoxSizer(wx.HORIZONTAL)
        self.dp_beg = wx.DatePickerCtrl(l_vbox_pan,-1, pos=(20,15), style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        #self.dp_beg.Bind(wx.EVT_DATE_CHANGED, self.ondatesel)
        t_dp_start = wx.StaticText(l_vbox_pan, label="Start:   ")
        dp_sizer_beg.Add(t_dp_start,0, flag=wx.EXPAND | wx.ALIGN_RIGHT | wx.TOP, border = 10)
        dp_sizer_beg.Add(self.dp_beg,1, flag=wx.EXPAND , border = 10)
     
        dp_sizer_end = wx.BoxSizer(wx.HORIZONTAL)        
        self.dp_end = wx.DatePickerCtrl(l_vbox_pan,-1, pos=(20,15), style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        #self.dp_end.Bind(wx.EVT_DATE_CHANGED, self.ondatesel)
        t_dp_end = wx.StaticText(l_vbox_pan, label="End:     ")
        dp_sizer_end.Add(t_dp_end,0, flag=wx.EXPAND | wx.ALIGN_RIGHT | wx.TOP, border = 10)
        dp_sizer_end.Add(self.dp_end,1, flag=wx.EXPAND , border = 10)
             
        redraw_btn = wx.Button(l_vbox_pan, label='Redraw')
        redraw_btn.Bind(wx.EVT_BUTTON, self.ondatesel)
            
        self.lvp_sizer.Add(t_adj_range,0, flag=wx.EXPAND | wx.TOP | wx.LEFT, border = 10)
        self.lvp_sizer.Add(dp_sizer_beg,0, flag= wx.LEFT | wx.RIGHT | wx.TOP, border = 10) 
        self.lvp_sizer.Add(dp_sizer_end,0, flag= wx.LEFT | wx.RIGHT | wx.BOTTOM, border = 10) 
 
    
    if af == True:
        t_adj_ma = wx.StaticText(l_vbox_pan, label="ADJUST MA FILTER")
        t_adj_ma.SetFont(self.header_font)  

        num_taps_sizer = wx.BoxSizer(wx.HORIZONTAL)
        t_num_taps = wx.StaticText(l_vbox_pan, label="Num. Taps:   ")
        self.spin_taps = wx.SpinCtrl(l_vbox_pan, value='5')
        
        num_taps_sizer.Add(t_num_taps,0, flag=wx.EXPAND | wx.ALIGN_RIGHT | wx.TOP, border = 10)
        num_taps_sizer.Add(self.spin_taps,1, flag=wx.EXPAND , border = 10)
        
        self.lvp_sizer.Add(t_adj_ma,0, flag=wx.EXPAND | wx.TOP | wx.LEFT, border = 10)
        self.lvp_sizer.Add(num_taps_sizer,0, flag= wx.LEFT | wx.RIGHT | wx.TOP, border = 10) 
                  
    if af or ar == True:
        self.lvp_sizer.Add(redraw_btn,0, flag= wx.ALIGN_CENTER | wx.ALL, border = 10)
                
    return l_vbox_pan

def fig_pan(self):
    self.canvas = FigureCanvas(self,-1,self.fig)
    
    r_sizer = wx.BoxSizer(wx.VERTICAL)
    r_sizer.Add(self.canvas, 20, flag=wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, border = 10)
    chart_toolbar = NavigationToolbar2Wx(self.canvas)
    r_sizer.Add(chart_toolbar, 0, flag=wx.ALIGN_CENTER | wx.TOP, border=5)
    
    return r_sizer
    
def subset_nodes(nodelist, beg=datetime.date(1001,1,1), end=datetime.date(3001,1,1), dp=True):
    if dp:
        subset = [k for k,v in nodelist.iteritems() if (v.get_date() < datepicker_to_datetime(end) and v.get_date() >= datepicker_to_datetime(beg))]
    elif dp == False:
        subset = [k for k,v in nodelist.iteritems() if (v.get_date() < end and v.get_date() >= beg)]   
             
    subset_nodelist = {}
    for s in subset:
        subset_nodelist[s] = nodelist[s]
    return subset_nodelist

def datepicker_to_datetime(d):
    return datetime.date(d.GetYear(),d.GetMonth()+1,d.GetDay()) #For whatever reason, there is an off by one error. +1 is a hacky fix.

def sort_nodes(nodes):
    nodes_ = collections.OrderedDict(sorted(nodes.iteritems(), key=lambda x: x[0]))
    return nodes_

