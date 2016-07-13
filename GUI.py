import wx
import wxmplot
import numpy
import datetime

from GUI_Tab_Diet import *
from GUI_Tab_Body import *
from GUI_Tab_Lift import *
from GUI_Tab_Goal import *
from GUI_Tab_Mood import *
from GUI_Tab_Book import *

from vis_diet import *
from vis_goals import *
from vis_records import *
from vis_weightlifting import *
from vis_mood import *

class gFrame(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, None, title="PDV", pos=(150,150), size=(350,200))  

        self.InitUI()

         
    def InitUI(self):
        
        #Menu        
        menubar = wx.MenuBar()
        menu_file = wx.Menu()
        menu_notes = wx.Menu()
        menubar.Append(menu_file, '&File')
        menubar.Append(menu_notes, '&Notes')
        
        menu_item_open = menu_file.Append(wx.ID_OPEN, 'Open', 'Open a notebook file')
        self.Bind(wx.EVT_MENU, self.OnOpen, menu_item_open)      
        
        menu_item_quit = menu_file.Append(wx.ID_EXIT, 'Exit', 'Exit PDV')
        self.Bind(wx.EVT_MENU, self.OnQuit, menu_item_quit)
        
        menu_item_workout_note_viewer = menu_notes.Append(1001, 'View Workout Notes')
        self.Bind(wx.EVT_MENU, self.Notes, menu_item_workout_note_viewer)   
        
        self.SetMenuBar(menubar)
        
        self.node_list = self.read_data_wrapper()
                
        #Notebook Setup
        nbk = Nbk(self,self.node_list)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nbk, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)
        
        self.Layout()
        self.Maximize()
        self.Show(True)

    def Notes(self,event):
        pass
        
    def OnQuit(self,event):
        self.Close()
        
    def OnOpen(self,event):
        pass

    def read_data_wrapper(self):
        frd = File_Read_Dlg(None)
        frd.ShowModal()
        self.day_nodes = frd.get_nodes()  
        frd.Destroy()          
        return self.day_nodes

class Nbk(wx.Notebook):
    def __init__(self, parent, nodes):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        bodytab = Tab_Body(self, nodes)
        diettab = Tab_Diet(self, nodes)
        lifttab = Tab_Lift(self, nodes)
        goaltab = Tab_Goal(self, nodes)
        moodtab = Tab_Mood(self, nodes)
        booktab = Tab_Book(self, nodes)
        self.AddPage(bodytab, "Body")
        self.AddPage(diettab, "Diet")
        self.AddPage(lifttab, "Lifts")
        self.AddPage(goaltab, "Goals")
        self.AddPage(moodtab, "Mood")
        self.AddPage(booktab, "Books")
                 
    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print 'OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel)
        event.Skip()
  
    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print 'OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel)
        event.Skip()
        
class Notes_Dlg(wx.Dialog):
    
    def __init__(self, *args, **kw):
        super(File_Read_Dlg, self).__init__(*args, **kw) 
            
        self.InitUI()
        self.SetSize((400, 400))
        self.SetTitle("Notes")
        
        
    def InitUI(self):
        pnl = wx.Panel(self)
        
        cbtn = wx.Button(pnl, label='Close')
        cbtn.Bind(wx.EVT_BUTTON, self.OnClose)
        
    def OnClose(self, e):
        self.Close(True)  
                        
class File_Read_Dlg(wx.Dialog):
    
    def __init__(self, *args, **kw):
        super(File_Read_Dlg, self).__init__(*args, **kw) 
            
        self.InitUI()
        self.SetSize((300, 230))
        self.SetTitle("File Read Status")
        
    def InitUI(self):
        pnl = wx.Panel(self)
        
        self.nodes = {}
        
        self.bold_font = wx.Font(10, wx.MODERN, wx.BOLD, wx.NORMAL, False, u'Consolas')

        t_status = wx.StaticText(pnl, label="STATUS:")
        t_status.SetFont(self.bold_font)
                
        self.lab_d_read = wx.StaticText(pnl, label='Diet Info: NOT READ                                ')
        self.lab_g_read = wx.StaticText(pnl, label='Goal Info: NOT READ                                ')
        self.lab_r_read = wx.StaticText(pnl, label='Records Info: NOT READ                                ')
        self.lab_w_read = wx.StaticText(pnl, label='Weightlifting Info: NOT READ                                ')
        self.lab_m_read = wx.StaticText(pnl, label='Mood Info: NOT READ                               ')
        
        self.lab_status = wx.StaticText(pnl, label='Status: Active                         ')
        self.lab_status.SetFont(self.bold_font)
        
        cbtn = wx.Button(pnl, label='Close')
        cbtn.Bind(wx.EVT_BUTTON, self.OnClose)
        
        sb = wx.StaticBox(pnl)
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)  
        sbs.Add(t_status, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=20)       
        sbs.Add(self.lab_d_read, flag=wx.LEFT | wx.RIGHT, border=30)        
        sbs.Add(self.lab_g_read, flag=wx.LEFT | wx.RIGHT, border=30)
        sbs.Add(self.lab_r_read, flag=wx.LEFT | wx.RIGHT, border=30)  
        sbs.Add(self.lab_w_read, flag=wx.LEFT | wx.RIGHT, border=30)  
        sbs.Add(self.lab_m_read, flag=wx.LEFT | wx.RIGHT, border=30)
        #sbs.Add(h_line,0,wx.EXPAND | wx.ALL | wx.RIGHT, border = 10)
        sbs.Add(self.lab_status, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM, border=30)  
        sbs.Add(cbtn, flag=wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, border=30)  
        pnl.SetSizer(sbs)
        self.Show(True)
        self.Bind(wx.EVT_ACTIVATE, self.read_data) 
        
    def OnClose(self, e):
        self.Close(True)  
                        
    def read_data(self,e):        
        print "Init"
        self.lab_d_read.SetLabel('Diet Info: NOT READ                                ')
        self.lab_g_read.SetLabel('Goal Info: NOT READ                                ')
        self.lab_r_read.SetLabel('Records Info: NOT READ                                ')
        self.lab_w_read.SetLabel('Weightlifting Info: NOT READ                                ')
        self.lab_m_read.SetLabel('Mood Info: NOT READ                                ')
        
        self.lab_status.SetLabel("Status: Init")
        day_nodes = {}
        print "Reading diet info..."
        self.lab_status.SetLabel("Status: Reading diet info...")
        self.lab_status.Show(False)
        self.lab_status.Show(True)
        day_nodes = read_data_diet(day_nodes)
        self.lab_d_read.SetLabel("Diet Info: SUCCESSFULLY READ")
        print "Reading goals info..."
        self.lab_d_read.Update()
        self.lab_status.SetLabel("Status: Reading goals info...")
        self.lab_status.Update()
        day_nodes = read_data_goals(day_nodes = day_nodes)
        self.lab_g_read.SetLabel("Goal Info: SUCCESSFULLY READ")
        self.lab_g_read.Update()
        print "Reading records info..."
        self.lab_status.SetLabel("Status: Reading records info...")
        self.lab_status.Update()
        day_nodes = read_data_records(day_nodes = day_nodes)
        self.lab_r_read.SetLabel("Records Info: SUCCESSFULLY READ")
        self.lab_r_read.Update()
        print "Reading weightlifting info..."
        self.lab_status.SetLabel("Status: Reading weightlifting info...")
        self.lab_status.Update()
        day_nodes = read_weightlifting_records(day_nodes = day_nodes)
        self.lab_w_read.SetLabel("Weightlifting Info: SUCCESSFULLY READ")
        self.lab_w_read.Update()
        print "Reading mood info..."
        self.lab_status.SetLabel("Status: Reading mood info...")
        self.lab_status.Update()
        day_nodes = read_data_mood(day_nodes = day_nodes)
        self.lab_m_read.SetLabel("Mood Info: SUCCESSFULLY READ")
        self.lab_m_read.Update()
        self.lab_status.SetLabel("Status: FINISHED")

        self.nodes = day_nodes
    
    def get_nodes(self):
        return self.nodes
        
if __name__ == '__main__':
    gui = wx.App()
    gframe = gFrame()
    gui.MainLoop()