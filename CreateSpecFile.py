#!/usr/bin/env python
#----------------------------------------------------------------------------
# Name:              CreateSpecFile.py
# version:           1.0.7
# last updated:      06/20/2019 GES
# Purpose:           Convert .#### data to file that can be read by pymca
#
# Author:            George Sterbinsky
# Acknowledgments:   Several functions are based on Plot_4idc_data.py by Yong Choi             
#
# Created:           2015
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# ***import packages***
import wx            #wxPython GUI package
import os
import glob
import datetime
import math
import time
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# ***Create GUI***

# Create a new frame class, derived from the wxPython Frame.
class MyFrame(wx.Frame):
    
    
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)
            #, size=(500, 200))
        
        self.InitUI()
        self.Centre()
        self.Show()


    def InitUI(self):
        panel = wx.Panel(self)       
        
        #Sizers
        vbox = wx.BoxSizer(wx.VERTICAL)   # one sizer to hold them all
        sb = wx.StaticBox(panel, label='Create pymca readable file from .#### files')  #decorative box with title for panel
        titlefgs = wx.StaticBoxSizer(sb, wx.VERTICAL)   # put sb in sizer
        fgs = wx.FlexGridSizer(3, 3, 5, 5)              # sizer for file info and controls
        #timerfgs = wx.FlexGridSizer(1, 4, 5, 5)         # sizer for auto update options
        timerfgs = wx.BoxSizer(wx.HORIZONTAL)         # sizer for auto update options
        
        # static text widgets
        readlabel  = wx.StaticText(panel, label="Read from:")
        writelabel = wx.StaticText(panel, label="Write to:")
        namelabel  = wx.StaticText(panel, label="File name:")
        
        # strings
        self.path0=os.getcwd()   # remembers current directory
        self.path1=os.getcwd()   # remembers current directory
        self.specfilename = 'AllData.spec'

        # lists
        self.newdatalist = glob.glob(self.path0+'/*.[0-9][0-9][0-9][0-9]')
        self.olddatalist = glob.glob(self.path0+'/*.[0-9][0-9][0-9][0-9]')
        
        # text controls
        self.readtc  = wx.TextCtrl(panel, wx.ID_ANY, self.path0)
        self.writetc = wx.TextCtrl(panel, wx.ID_ANY, self.path1)
        self.nametc  = wx.TextCtrl(panel, wx.ID_ANY, self.specfilename)
        
        # button widgets
        readbutton   = wx.Button(panel, wx.ID_ANY, label='choose')
        writebutton  = wx.Button(panel, wx.ID_ANY, label='choose')
        createbutton = wx.Button(panel, wx.ID_ANY, label='create file')
        createbutton.SetBackgroundColour(wx.Colour(0, 255, 0))
        
        #checkbox
        self.readandwritecb = wx.CheckBox(panel, wx.ID_ANY, label='read and write in same directory'
            +'                       ') #-controls width of window
           #+'123456789a123456789b123')-23
        
        #widgets for auto update
        timeunitlabel = wx.StaticText(panel, label='sec')#+'                                                          ') #label string length controls default width of GUI
        self.timer = wx.Timer(self)
        self.defautltime = '10' 
        self.autocb = wx.CheckBox(panel,  wx.ID_ANY, label='auto update every')
        self.timetc  = wx.TextCtrl(panel, wx.ID_ANY, self.defautltime, size=(55,-1))
        
        #Add widgets to sizers
        #Format: sizer.Add(wx.Window window, integer proportion=0, integer flag = 0, integer border = 0)
        #add widgets for autoupdate to sizer
        timerfgs.Add(self.readandwritecb, 1, wx.RIGHT|wx.EXPAND, 3)
        timerfgs.Add(self.autocb, 0, wx.RIGHT|wx.EXPAND, 3)
        timerfgs.Add(self.timetc, 0, wx.RIGHT|wx.EXPAND, 3)
        timerfgs.Add(timeunitlabel, 0, wx.EXPAND)        
        
        #add widgets for read dir
        fgs.Add(readlabel, 0, wx.EXPAND)
        fgs.Add(self.readtc, 1, wx.EXPAND)
        fgs.Add(readbutton, 0, wx.EXPAND)
        
        #add widgets for write dir
        fgs.Add(writelabel, 0, wx.EXPAND)
        fgs.Add(self.writetc, 1, wx.EXPAND)
        fgs.Add(writebutton, 0, wx.EXPAND)
        
        #add widgets for name and create
        fgs.Add(namelabel, 0, wx.EXPAND)
        fgs.Add(self.nametc, 1, wx.EXPAND)
        fgs.Add(createbutton, 0, wx.EXPAND)
        
        #allow text controls to expand
        fgs.AddGrowableCol(1, 1)
        
        #add widgets to sizer for label
        titlefgs.Add(fgs, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=5)
        titlefgs.Add(timerfgs, proportion=0, flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, border=5)
        
        #add sizer for label to sizer for boarder and fit
        vbox.Add(titlefgs, proportion=0, flag=wx.ALL|wx.EXPAND, border=10)
        panel.SetSizerAndFit(vbox)
        self.Fit()
        
        #bind widgets with functions
        self.Bind(wx.EVT_BUTTON,   self.OnFindDir0, readbutton)
        self.Bind(wx.EVT_BUTTON,   self.OnFindDir1, writebutton)
        self.Bind(wx.EVT_BUTTON,   self.OnCreateFile, createbutton)
        self.Bind(wx.EVT_CHECKBOX, self.StartAutoUpdate, self.autocb)
        self.Bind(wx.EVT_TIMER,    self.OnUpdate, self.timer)
        self.Bind(wx.EVT_CHECKBOX, self.ReadWriteSame, self.readandwritecb)
    
    
    def ReadWriteSame(self, event):
        sender = event.GetEventObject()
        isChecked = sender.GetValue()
        if isChecked:
            dir0 = self.readtc.GetValue()
            self.writetc.SetValue(dir0)##
            
            
    def CheckForNewFiles(self):
        dir0 = self.readtc.GetValue()
        self.olddatalist = self.newdatalist
        self.newdatalist = glob.glob(dir0+'/*.[0-9][0-9][0-9][0-9]')
        if self.olddatalist != self.newdatalist:
            dir1 = self.writetc.GetValue()
            fname = str(self.nametc.GetValue())
            CreateSpecFile(dir0,dir1,fname)
    
    
    def StartAutoUpdate(self, event):
        sender = event.GetEventObject()
        isChecked = sender.GetValue()
        self.timer.Stop()
        if isChecked:
            str1 = self.timetc.GetValue()
            var1 = float(str1)*1000      # in msec
            self.timer.Start(var1)       # in msec
            print('auto update on')
            self.CheckForNewFiles()
        else:
            print('auto update off')            


    def OnUpdate(self, event):
        self.CheckForNewFiles()
    
    
    def OnFindDir0(self, event):
        dir0 = ''
        default0 = self.readtc.GetValue()
        if default0 == '':
            default0 = self.path0
        dlg = wx.DirDialog(
            self, message = 'Choose data directory',
            defaultPath = default0,
            #style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR) #for old versions of wx
            style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dir0 = dlg.GetPath()
        dlg.Destroy()
        print('data directory: ', dir0)
        self.readtc.SetValue(dir0)##
        isChecked = self.readandwritecb.GetValue()
        if isChecked: self.writetc.SetValue(dir0)##
        
        
    def OnFindDir1(self, event):
        dir1 = ''
        default1 = self.writetc.GetValue()
        if default1 == '':
            default1 = self.path1
        dlg = wx.DirDialog(
            self, message = 'Choose data directory',
            defaultPath = default1,
            #style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR) #for old versions of wx
            style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dir1 = dlg.GetPath()
        dlg.Destroy()
        print('data directory: ', dir1)
        self.writetc.SetValue(dir1)##
        isChecked = self.readandwritecb.GetValue()
        if isChecked: self.readtc.SetValue(dir1)##


    def OnCreateFile(self, event):
        dir0 = self.readtc.GetValue()
        dir1 = self.writetc.GetValue()
        fname = str(self.nametc.GetValue())
        CreateSpecFile(dir0,dir1,fname)
        #self.olddatalist = glob.glob(dir0+'/*.[0-9][0-9][0-9][0-9]')
        self.newdatalist = glob.glob(dir0+'/*.[0-9][0-9][0-9][0-9]')
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# ***Functions for creating spec file***

#Creates a list of data column headers from colum header string in 9BM data files
def CreateHeaderList(strng):
    newstrng = ''
    ctr = 0
    for i in range(len(strng)):
        if strng[i]==' ' and strng[i-1]!=' ' and strng[i+1]!=' ':
            newstrng += '_'
            ctr += 1
        elif strng[i]==' ':
            newstrng += strng[i]
            ctr = 0
        else:
            newstrng += strng[i]
            ctr+=1
        if ctr == 21:
            newstrng += '   '
            ctr = 0
    return newstrng.split()
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------    
#gets date and time from 4idc data file
def Get4idcDateTime(datafilename):
    f = open(str(datafilename), 'r') #open jth file in list
    for line in f:                   # loop over lines in file
        if 'Scan time =' in line:
            line = line.replace('\r','')
            dtl = line.replace(',',' ')
            dtl = dtl.split('=')
            dtl = dtl[1].split()
            d = ['','','']
            if   dtl[0] == 'JAN': d[0] = 1
            elif dtl[0] == 'FEB': d[0] = 2
            elif dtl[0] == 'MAR': d[0] = 3
            elif dtl[0] == 'APR': d[0] = 4
            elif dtl[0] == 'MAY': d[0] = 5
            elif dtl[0] == 'JUN': d[0] = 6
            elif dtl[0] == 'JUL': d[0] = 7
            elif dtl[0] == 'AUG': d[0] = 8
            elif dtl[0] == 'SEP': d[0] = 9
            elif dtl[0] == 'OCT': d[0] = 10
            elif dtl[0] == 'NOV': d[0] = 11
            elif dtl[0] == 'DEC': d[0] = 12
            d[1] = int(dtl[1])
            d[2] = int(dtl[2])
            t = dtl[3].split('.') 
            t = t[0].split(':')   #convert time string to h:m:s list
            for i in range(len(t)): t[i] = int(t[i]) #convert string to nums
            dt = datetime.datetime(d[2],d[0],d[1],t[0],t[1],t[2])
            break
    f.close()
    return dt
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
#gets date and time from 9bm or 20bm data file
def Get9bmDateTime(datafilename):
    f = open(str(datafilename), 'r') #open file
    firstLine = f.readline() #read first line of jth file
    firstLine = firstLine.replace('\r','')
    firstLine = firstLine.split() #create list of words in string firstline
    
    for words in firstLine:  #loop over words in list
        if '/' in words:     #if the word contains a '/'
            d = words        # save the word to 'd', it is the date
        if ':' in words:     # if the word contains a ':'
            t = words        # save it to 't', it is the time
        if words=='AM' or words=='AM;' or words=='PM' or words=='PM;':
            ampm = words     # save AM or PM to ampm
    
    d = d.split('/') #convert date string to m:d:y list
    for i in range(len(d)): d[i] = int(d[i]) #convert string to nums
    
    t = t.split(':') #convert time string to h:m:s list
    for i in range(len(t)): t[i] = int(t[i]) #convert string to nums
    
    #convert 12 hr time to 24 hr time 
    if 'P' in ampm: t[0] += 12
    if t[0] == 12:  t[0] = 0
    if t[0] == 24:  t[0] = 12
    
    #convert date and time lists into a datetime obj (dt) for sorting
    dt = datetime.datetime(d[2],d[0],d[1],t[0],t[1],t[2])
    
    f.close()
    return dt
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# gets names of data coulmns from 4IDC data file and returns them in a list
def Get4idcColNames(datafilename):
    f = open(str(datafilename), 'r') #open file
    list_ColName=[]   #create empty list
    for line in f:
        if line.startswith('#'):
            line = line.replace('\r','')
            words=line.split()
            try:
                int(words[1])
            except ValueError:
                pass
            else:
                words = line.split(',')
                if len(words) > 1:
                    ColName = words[1]
                    if ColName == ' ':
                        words = words[0].split()
                        ColName = words[-1]
                    if ColName.startswith(' '):
                        ColName = ColName[1:]
                    ColName = ColName.replace(' ','_') #remove spaces from column names
                else:
                    ColName = 'Index'
                #i=0
                #while ColName in list_ColName:
                #    if i>0: ColName = ColName[:-len(str(i))]
                #    ColName += str(i+1)
                #    i+=1
                list_ColName.append(ColName)
    f.close()
    return list_ColName
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# gets type of scan from list of data columns in 4IDC data file
def Get4idcScanType(list_ColName):
    scanType = 'motorScan'
    if list_ColName[1] == 'SGM1:Energy':
        scanType = 'energyScan'
        if (list_ColName[3] == 'i0_A'):
            scanType = 'XMCDvsE'
    if (list_ColName[1]=='Hys Control') or (list_ColName[1]=='Field program string'):
        #if (list_ColName[2] == 'i0') and (list_ColName[6] == 'i0'):
        scanType = 'XMCDvsH'
    return scanType
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# gets string containg modified column labels from a list column labels
# in a 4IDC data file
def Get4idcHeaderString(scanType,list_ColName):
    if scanType == 'motorScan':
        headString = 'I0   TEY/I0   FY/I0   reflectivity/I0   '
    elif scanType == 'energyScan':
        headString = 'I0   TEY/I0   FY/I0   reflectivity/I0   reference/I0   '
    else:
        headString = 'Sum_reflectivity   XMCD_reflectivity   Sum_TEY   XMCD_TEY   Sum_FY   XMCD_FY   reference   '
    #headString = '#L   '   #+list_ColName[1]+'   '
    for i,item in enumerate(list_ColName):
        j=0
        while item in headString.split():
            if j>0: item = item[:-len(str(j))]
            item += str(j+1)
            j+=1
        if i > 1:
            headString += item+'   '
        elif i==1:
            headString = '#L   '+list_ColName[i]+'   '+headString
        else:
            firstToLast = list_ColName[i]
    #headString = headString[0:-3] + '\n'
    headString += firstToLast+'\n'
    return headString
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# gets string containg modified row of data values from a list of data values
# in a 4IDC data file
def Get4idcDataLine(scanType,dataList):
    dataString = dataList[1]+'   '

    if scanType == 'motorScan':
        #headString += 'I0   reflectivity   TEY   FY   '
        i0p = float(dataList[2])
        REFp = float(dataList[3])
        TEYp = float(dataList[4])
        TFYp = float(dataList[5])
    elif scanType == 'energyScan':
        #headString += 'I0   reflectivity   TEY   FY   reference   '
        i0p = float(dataList[3])
        REFp = float(dataList[4])
        TEYp = float(dataList[5])
        TFYp = float(dataList[6])
        refer = float(dataList[7])
    elif scanType == 'XMCDvsE':
        #headString += 'Sum_reflectivity   XMCD_reflectivity   Sum_TEY   XMCD_TEY   Sum_FY   XMCD_FY   reference   '
        i0p = float(dataList[3])
        TEYp = float(dataList[4])
        TFYp = float(dataList[5])
        REFp = float(dataList[6])
        i0n = float(dataList[7])
        TEYn = float(dataList[8])
        TFYn = float(dataList[9])
        REFn = float(dataList[10])
        refer = float(dataList[17])
    elif scanType == 'XMCDvsH':
        #headString += 'Sum_reflectivity   XMCD_reflectivity   Sum_TEY   XMCD_TEY   Sum_FY   XMCD_FY   reference   '
        i0p = float(dataList[2])
        TEYp = float(dataList[3])
        TFYp = float(dataList[4])
        REFp = float(dataList[5])
        i0n = float(dataList[6])
        TEYn = float(dataList[7])
        TFYn = float(dataList[8])
        REFn = float(dataList[9])
        refer = float(dataList[16])
    
    if (scanType=='motorScan') or (scanType=='energyScan'):
        if (i0p > 0) and (TEYp > 0):
            Sum_TEY = TEYp/i0p
        else:
            Sum_TEY = 0
        if (i0p > 0) and (TFYp > 0):
            Sum_TFY = TFYp/i0p
        else:
            Sum_TFY = 0
        if (i0p > 0) and (REFp > 0):
            Sum_REF = REFp/i0p
        else:
            Sum_REF = 0
        dataString += str(i0p)+'   '+str(Sum_TEY)+'   '+str(Sum_TFY)+'   '+str(Sum_REF)+'   '
        if scanType == 'energyScan':
            if (i0p > 0) and (refer > 0):
                Sum_refer = refer/i0p
            else:
                Sum_refer = 0
            dataString += str(Sum_refer)+'   '
    
    elif (scanType=='XMCDvsE') or (scanType=='XMCDvsH'):
        if (i0p > 0) and (i0n > 0) and (TEYp > 0) and (TEYn > 0):
            Sum_TEY = TEYp/i0p + TEYn/i0n
            XMCD_TEY = TEYp/i0p - TEYn/i0n
        else:
            Sum_TEY = 0
            XMCD_TEY = 0
        if (i0p > 0) and (i0n > 0) and (TFYp > 0) and (TFYn > 0):
            Sum_TFY = TFYp/i0p + TFYn/i0n
            XMCD_TFY = TFYp/i0p - TFYn/i0n
        else:
            Sum_TFY = 0
            XMCD_TFY = 0
        if (i0p > 0) and (i0n > 0) and (REFp > 0) and (REFn > 0):
            Sum_REF = REFp/i0p + REFn/i0n
            XMCD_REF = REFp/i0p - REFn/i0n
        else:
            Sum_REF = 0
            XMCD_REF = 0
        dataString += str(Sum_REF)+'   '+str(XMCD_REF)+'   '
        dataString += str(Sum_TEY)+'   '+str(XMCD_TEY)+'   '
        dataString += str(Sum_TFY)+'   '+str(XMCD_TFY)+'   '
        dataString += str(refer)+'   '
    
    i = 0
    for item in dataList:
        if i > 1: dataString += item+'   '
        i += 1
    dataString += dataList[0]+'   '+'\n' #= dataString[0:3] + '\n'    
    return dataString
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
def Get4idcShortHeaderList(datafilename):
    PVlistMain = [
        'CPU mode',
        'CPU H',
        'CPU V',
        'SGM Energy',
        '8-pole sample',
        '8-pole Axis 1 Field',
        '8-pole Axis 2 Field',
        '8-pole Axis 3 Field',
        '8-pole Axis 4 Field',
        'Front T',
        '7T Sample',
        '7T Z',
        '7T T',
        '7T field']
    PVlistBeam = ['CPU mode','CPU H','CPU V','SGM Energy']
    PVlist7T = ['7T Sample','7T Z','7T T','7T field']
    
    f = open(str(datafilename), 'r') #open file
    headerBeam = '##########\n# beamline info:\n'
    shortHeader = '##########\n# Octopolar chamber info:\n'
    header7T = '##########\n# 7T chamber info:\n'
    for line in f:
        if line.startswith('# Extra'):
            line = line.replace('\r','')
            for expInfo in PVlistMain:
                if expInfo in line:
                    words=line.split(',')
                    PVdesc=words[1]
                    PVvalue=words[2]
                    if len(words) > 3: PVunit=words[3]
                    else: PVunit=''
                    PVunit  = PVunit.replace('"','')   # remove quotation mark
                    PVunit  = PVunit.replace(' ','')   # remove extra space before unit
                    PVunit  = PVunit.replace('\n','')  # remove newline
                    PVvalue = PVvalue.replace('"','')  # remove quotation mark
                    PVvalue = PVvalue.replace(' ','')  # remove spaces
                    PVvalue = PVvalue.replace('\n','') # remove newline
                    headline = '# '+PVdesc+'\t'+PVvalue+' '+PVunit+'\n'
                    if expInfo in PVlistBeam: headerBeam += headline
                    elif expInfo in PVlist7T: header7T += headline
                    else: shortHeader += headline
                    break
    f.close()
    shortHeader = headerBeam+shortHeader+header7T+'##########\n'
    return shortHeader
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
#Creates spec file from .#### files       
def CreateSpecFile(DataPath,WritePath,newFileName):
    
    #make a list of file in current dir with .#### extension
    ScanList = glob.glob(DataPath+'/*.[0-9][0-9][0-9][0-9]') 
    # make a nother list with same length as ScanList
    TimeList = list(range(len(ScanList)))
    
    #get date and time from file headers
    for j in range(len(ScanList)): #loop over all files in ScanList
        data4idc = 0
        f = open(str(ScanList[j]), 'r') #open jth file in list
        firstLine = f.readline() #read first line of jth file
        firstLine = firstLine.replace('\r','')
        f.close()
        if 'mda2ascii' in firstLine: 
            data4idc = 1
            dt = Get4idcDateTime(str(ScanList[j]))
        else:
            dt = Get9bmDateTime(str(ScanList[j]))
        TimeList[j] = dt  # place dt in list
        
    #create a tuple with file name and timestamp 
    fl = [(ScanList[j], TimeList[j]) for j in range(len(ScanList))]
    
    # sort the tuple by date and time    
    fl.sort(key=lambda xy: xy[1])
    
    # create .spec file and write file header to it
    Newfile = str(WritePath)+'/'+str(newFileName) #Newfile = DataPath+'/AllData.spec'
    #nf = open(str(Newfile), 'wb') #recall that 'wb' was necessary for windows, needs testing
    nf = open(str(Newfile), 'w') #changed to 'w' to correct python 3 error
    nf.write('#F '+str(newFileName)+'\n')
    nf.write('#E '+str(time.time())+'\n')
    nf.write('#D '+datetime.datetime.now().ctime()+'\n')
    nf.write('#C This Spec File created by CreateSpecFile.py'+'\n')
    nf.write('#C CreateSpecFile.py written by George Sterbinsky, 2015'+'\n')
    nf.write('\n')
    
    # write contents of .#### files to .spec file and format to be read by pymca
    for j in range(len(ScanList)):  #loop over all files in ScanList
        wrtHead = 0                 #variable to track if column labels and data have been written
        wrtHead4 = 0                #variable to track if 4IDC column labels and data have been written
        fname = str(fl[j][0]).split('/')       #split full path into list of dirs and file name
        if len(fname) < 2: fname = str(fl[j][0]).split('\\')      # previous split didn't work, try again
        nf.write('#S '+str(j+1)+' ')#+fname[-1])# +'\n')          # write scan number
        
        if data4idc:
            ColNameList4 = Get4idcColNames(str(fl[j][0]))
            ScanType4 = Get4idcScanType(ColNameList4)
            nf.write(ScanType4+'   ')                             # write scan type
        
        nf.write(fname[-1] + '\n')                                # write file name
        nf.write('#D '+fl[j][1].ctime()+'\n')                     # write time stamp
        
        if data4idc:
            headLines4 = Get4idcShortHeaderList(str(fl[j][0]))
            nf.write(headLines4)
        
        f = open(str(fl[j][0]), 'r')            # open .#### file
        for line in f:                          # loop over lines in file
            line = line.replace('\r','')
            
            if wrtHead == 1:     #if true write col labels
                cols = line.replace('*',' ')[1:] 
                cols = CreateHeaderList(cols)       #create list of column headings in string
                nf.write('#L ')
                I0 = -1
                IT = -1
                Iref = -1
                for i,words in enumerate(cols):             #loop over column labels
                    if words == 'I0' or 'I0-' in words:
                        I0 = i
                    if words == 'IT' or words == 'It' or 'It-' in words:
                        IT = i
                    if words == 'Iref' or 'Iref-' in words:
                        Iref = i
                    if i > 0: nf.write('   ')
                    nf.write(words)
                if I0 > 0 and IT > 0:
                    nf.write('   ln(I0/IT)')
                if IT > 0 and Iref > 0:
                    nf.write('   ln(IT/Iref)')
                nf.write('\n')
                wrtHead = 2                  # next line is data
            
            elif wrtHead == 2:               # if true write data
                if line == '\n':             # if blank line end of data reached
                     nf.write(line)          # write line
                     wrtHead = 0             # reset variable to track header (may not be necessary)
                elif line[0] != '*':
                    cols = line.split()      #create list of words in string line
                    if data4idc:
                        if wrtHead4:         # if true write 4IDC col labels
                            nf.write(str(Get4idcHeaderString(ScanType4,ColNameList4)))
                            wrtHead4 = 0
                        nf.write(str(Get4idcDataLine(ScanType4,cols)))
                    else:
                        for words in cols: nf.write(words+'   ')
                        if I0 > 0 and IT > 0:
                            if float(cols[I0])<=0 or float(cols[IT])<=0:
                                lnI0IT = 0
                            else:
                                lnI0IT = math.log(float(cols[I0])/float(cols[IT]))
                            nf.write(str(lnI0IT)+'   ')
                        if IT > 0 and Iref > 0:
                            if float(cols[IT])<=0 or float(cols[Iref])<=0:
                                lnITIref = 0
                            else:
                                lnITIref = math.log(float(cols[IT])/abs(float(cols[Iref])))
                            nf.write(str(lnITIref))
                        nf.write('\n')
            
            else:                              # line in header, write as is
                nf.write(line)            
            if '# Column Headings:' in line:   # next line is col labels
                wrtHead = 1  
            if '# 1-D Scan Values' in line:    # next line is data
                wrtHead = 2
                wrtHead4 = 1
        nf.write('\n')
        f.close()
    nf.close()
    print('created spec file')
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App()    # Create an instance of the application class
    MyFrame(None, title='Create spec file (GES)')
    app.MainLoop()    # Tell it to start processing events