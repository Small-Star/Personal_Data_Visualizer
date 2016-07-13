'''
Created on Jun 6, 2016

'''

import wx

from GUI_lib import *

class Tab_Book(wx.Panel):
    #IMPROVEMENT - Add autoupdating script when time
    def __init__(self, parent, nodelist):       
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        im = self.draw()
        imageCtrl = wx.StaticBitmap(self, -1, im)
        main_sizer.Add(imageCtrl,1,wx.EXPAND | wx.ALL | wx.ALIGN_LEFT)
        self.Refresh()

        self.SetSizer(main_sizer)
        self.Show(True)
        
    def draw(self, fname="/home/u_delta/projects/bookcover_collage/collage.jpg"):
        try:
            img = wx.Image(fname, wx.BITMAP_TYPE_ANY)
            img = img.Scale(1900, 950, wx.IMAGE_QUALITY_HIGH)
            #IMPROVEMENT - Add dynamic resizing when time
            result = wx.BitmapFromImage(img)
            return result
        
        except IOError:
            print "Image file %s not found" % fname
            raise SystemExit

        