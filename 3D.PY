import wx
import vtk
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
import os
import Tkinter
 
class p1(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
         
        #to interact with the scene using the mouse use an instance of vtkRenderWindowInteractor. 
        self.widget = wxVTKRenderWindowInteractor(self, -1)
        self.widget.Enable(1)
        self.widget.AddObserver("ExitEvent", lambda o,e,f=self: f.Close())
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.widget, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Layout()
        self.ren = vtk.vtkRenderer()
        self.filename=""
        self.isploted = False
            
    def renderthis(self):
            # open a window and create a renderer            
            self.widget.GetRenderWindow().AddRenderer(self.ren)
   
           # open file             
            openFileDialog = wx.FileDialog(self, "Open STL file", "", self.filename,
                                       "*.stl", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
             
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.filename = openFileDialog.GetPath()
            # render the data
            reader = vtk.vtkSTLReader()
            reader.SetFileName(self.filename)
   
            # To take the polygonal data from the vtkConeSource and
            # create a rendering for the renderer.
            coneMapper = vtk.vtkPolyDataMapper()
            coneMapper.SetInputConnection(reader.GetOutputPort())
 
            # create an actor for our scene
            if self.isploted:
                coneActor=self.ren.GetActors().GetLastActor()
                self.ren.RemoveActor(coneActor)
                 
            coneActor = vtk.vtkActor()
            coneActor.SetMapper(coneMapper)
            # Add actor
            self.ren.AddActor(coneActor)
           # print self.ren.GetActors().GetNumberOfItems()
 
            if not self.isploted:
                axes = vtk.vtkAxesActor()
                self.marker = vtk.vtkOrientationMarkerWidget()
                self.marker.SetInteractor( self.widget._Iren )
                self.marker.SetOrientationMarker( axes )
                self.marker.SetViewport(0.75,0,1,0.25)
                self.marker.SetEnabled(1)
 
            self.ren.ResetCamera()
            self.ren.ResetCameraClippingRange()
            cam = self.ren.GetActiveCamera()
            cam.Elevation(10)
            cam.Azimuth(70)
            self.isploted = True
            self.ren.Render()

 
class VTKFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(1000,550))
        self.sp = wx.SplitterWindow(self)
        self.p1 = p1(self.sp)
        self.p2 = wx.Panel(self.sp,style=wx.SUNKEN_BORDER)
        self.sp.SplitHorizontally(self.p2,self.p1,40)
        
        self.InitUI()         
        self.butt()
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("STL File Viewer")


    def butt(self):
        #New
        iconnew = wx.Image("/home/yatheesh/Documents/E-F-icons/file new.ico", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.btnew = wx.BitmapButton(self.p2, id=-1, bitmap=iconnew,
        pos=(0, 0), size = (30, 30))
        self.btnew.SetToolTip(wx.ToolTip("New"))

        #Save
        iconsave = wx.Image("/home/yatheesh/Documents/Q-R-S-icons/save.ico", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.btsave = wx.BitmapButton(self.p2, id=-1, bitmap=iconsave,
        pos=(30, 0), size = (30, 30))
        self.btsave.SetToolTip(wx.ToolTip("Save"))
        self.btsave.Bind(wx.EVT_BUTTON,self.saveFile)
       

        #Open
        iconopen = wx.Image("/home/yatheesh/Documents/Q-R-S-icons/open.jpeg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.btopen = wx.BitmapButton(self.p2, id=-1, bitmap=iconopen,
        pos=(60, 0), size = (30, 30))
        self.btopen.SetToolTip(wx.ToolTip("Open"))
        self.btopen.Bind(wx.EVT_BUTTON,self.plot)
                
 
    def plot(self,event):
        self.p1.renderthis()
        self.SetTitle("STL File Viewer: "+self.p1.filename)
      
        
    def InitUI(self):    

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        editMenu = wx.Menu()
        viewMenu = wx.Menu()  #create a menu for view
        helpMenu = wx.Menu()  #create a menu for help

        #MENUBAR
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu,"&File") # Adding the "filemenu" to the MenuBar
        menuBar.Append(editMenu,"&Edit")
        menuBar.Append(viewMenu, "&View")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

 
        #FILE MENU
        menuNew  = fileMenu.Append(wx.ID_NEW, "&New"," Create a new file")  #add to create New File
        menuOpen = fileMenu.Append(wx.ID_OPEN, "&Open..."," Open a file to edit")  #add open to File
        menuSave  = fileMenu.Append(wx.ID_SAVE, "&Save") 
        menuSaveAs  = fileMenu.Append(wx.ID_SAVEAS, "&Save As...")  
        fileMenu.AppendSeparator()
        menuExit = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')

        #EDIT MENU
        menuCopy = editMenu.Append(wx.ID_COPY)
        menuCut = editMenu.Append(wx.ID_CUT)
        menuPaste = editMenu.Append(wx.ID_PASTE)
        
        #VIEW MENU
        menuView = viewMenu.Append(wx.ID_ANY, "TODO:", "Still to do")

        #HELP MENU
        menuAbout = helpMenu.Append(wx.ID_ABOUT, "&About", "About this program")  #add about menu item
        
        #MENU EVENTS
        wx.EVT_MENU(self, wx.ID_NEW, self.OnNew);
        wx.EVT_MENU(self, wx.ID_OPEN, self.OnOpen);
        wx.EVT_MENU(self, wx.ID_SAVE, self.saveFile);
        wx.EVT_MENU(self, wx.ID_SAVEAS, self.OnSaveAs);
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnExit);
        #wx.EVT_MENU(self, wx.ID_, self.OnAbout);

            
        
    def OnAbout(self,e):
        openFileDialog = wx.MessageDialog(self, "A small STL File editor", "My 3D editor", wx.OK)  #create a dialog (dlg) box to display the     message, and ok button
        openFileDialog.ShowModal()  #show the dialog box, modal means cannot do anything on the program until clicks ok or cancel
        openFileDialog.Destroy()  #destroy the dialog box when its not needed

    def OnExit(self,e):
        self.Close(True)  #on menu item select, close the app frame.

    def OnNew(self,e):
        homedir = os.environ['HOME']
        if not os.path.exists(homedir):
            if getpass.getuser():
                homedir = "C:/Users/" + getpass.getuser() + "/"
            else:
                homedir = "C:/"
        newFileDialog = wx.FileDialog(self, "New Operation File", homedir, "",
            "Operation Files (*.fwr)|*.fwr|All Files|(*.*)|*.*", wx.FD_CREATE|wx.OVERWRITE_PROMPT)

    def OnOpen(self,e):
        self.p1.renderthis()
        self.SetTitle("STL File Viewer: "+self.p1.filename)      

      
    def saveFile(self, e):
        self.dirname = ""
        saveFileDialog = wx.FileDialog(self, "Save Operation File", self.dirname, "",
                 "Operation Files (*.stl)|*.str|All Files (*.*)|*.*", wx.SAVE|wx.OVERWRITE_PROMPT)
        if saveFileDialog.ShowModal() == wx.ID_OK:
            contents = self.control.GetValue()
            self.filename = saveFileDialog.GetFilename()
            self.dirname = saveFileDialog.GetDirectory()
            filehandle = open(os.path.join(self.dirname, self.filename), 'w')
            filehandle.write(contents)
            filehandle.close()
        else:
           sys.exit(1)
        saveFileDialog.Destroy()

    def OnSaveAs(self, e):
       self.dirname = "";

       saveAsFileDialog = wx.FileDialog(self, "Save Operation File As", self.dirname, "",
        "Operation Files (*.stl)|*.stl|All Files (*.*)|*.*", 
        wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

       if saveAsFileDialog.ShowModal() == wx.ID_OK:
        contents = self.control.GetValue()
        self.filename = saveFileDialog.GetFilename()
        self.dirname = saveFileDialog.GetDirectory()
        filehandle = open(os.path.join(self.dirname, self.filename), 'w')
        filehandle.write(contents)
        filehandle.close()
       else:
        sys.exit(1)
       saveFileDialog.Destroy()

      # save current contents in the file
      # use wxPython output streams
      #output_stream = wx.FileOutputStream(saveFileDialog.GetPath())

      #if not output_stream.IsOk():    
      #    wx.LogError("Cannot save contents of Operations File '%s'" % saveFileDialog.GetPath())
      #    return  

    
         
app = wx.App(redirect=False)
frame = VTKFrame(None,"STL File Viewer")
frame.Show()
app.MainLoop()
