from global_var import *
import os
import subprocess
import sys
import time
# import win32com.client
# import win32net
import wx
import threading
from auto_gui import *
from KThread import *
from wx.lib.scrolledpanel import ScrolledPanel
import common
from FindRegression import *

filename = r"C:\logs\nic-diag.log"

class RedirectText:
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

        if not os.path.exists(r"C:\logs"):
            os.mkdir(r"C:\logs")
        self.filename = open(filename, "w")

    def write(self,string):
        wx.CallAfter(self.out.WriteText, string)
        if self.filename.closed:
            pass
        else:
            self.filename.write(string)

    def flush(self):
        pass

class MyForm(wx.Frame):


    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "NVIDIA LTE Throughput Tester",size=(1350,800))

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.pl = wx.Panel(self.panel)
        #self.pl = wx.Pane()
        self.pl.SetBackgroundColour("#d8d8bf")

        self.Font_Result = wx.Font(12,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)

        #self.pl2 = wx.Panel(self, wx.ID_ANY)

        #self.pl = wx.Panel(self, -1)
        #self.pl.SetBackgroundColour("#EFFEFE")

        # TestType Part
        sbTestType = wx.StaticBox(self.pl, -1, 'Test Type', size=(-1, -1))
        #sbTestType.SetForegroundColour(wx.BLUE)
        sbsTestType = wx.StaticBoxSizer(sbTestType, wx.HORIZONTAL)
        #self.stTestType = wx.StaticText(self.pl,-1,'Test Type')
        #sbsTestType.Add(self.stTestType, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)
        bsTestType = wx.BoxSizer ( wx.HORIZONTAL )
        self.rbNotest = wx.RadioButton(self.pl, -1, 'No Test')
        self.Bind(wx.EVT_RADIOBUTTON, self.TestType, id=self.rbNotest.GetId())
        self.rbAuto   = wx.RadioButton(self.pl, -1, 'Auto Test')
        self.Bind(wx.EVT_RADIOBUTTON, self.TestType, id=self.rbAuto.GetId())
        self.rbUnit = wx.RadioButton(self.pl, -1, 'Unit Test')
        self.Bind(wx.EVT_RADIOBUTTON, self.TestType, id=self.rbUnit.GetId())

       # bsTestType.Add(self.stTestType,0, wx.ALL,10)
        bsTestType.Add(self.rbAuto,0, wx.ALL,10)
        bsTestType.Add(self.rbUnit,0, wx.ALL,10)
        bsTestType.Add(self.rbNotest,0, wx.ALL,10)
        sbsTestType.Add(bsTestType, 0, wx.LEFT,10)

        #platform
        #sbPlatformType = wx.StaticBox(self.pl, -1, 'Platform', size=(-1, -1))
        #sbsPlatformType = wx.StaticBoxSizer(sbPlatformType, wx.HORIZONTAL)
        #bsPlatformType = wx.BoxSizer ( wx.HORIZONTAL )
        self.rbplatform = wx.RadioBox(self.pl, -1, "Platform", choices=["Win XP", "WoA"], majorDimension=0, style=wx.RA_SPECIFY_COLS)

        #self.rbWinxp = wx.RadioButton(self.pl, -1, 'Win XP')
        #self.Bind(wx.EVT_RADIOBUTTON, self.PlatformType, id=self.rbWinxp.GetId())
        #self.rbWoA = wx.RadioButton(self.pl, -1, 'WoA')
        #self.Bind(wx.EVT_RADIOBUTTON, self.PlatformType, id=self.rbWoA.GetId())
        #bsPlatformType.Add(self.rbWinxp,0, wx.ALL,10)
        #bsPlatformType.Add(self.rbplatform,0, wx.ALL,10)
        #sbsPlatformType.Add(bsPlatformType, 0, wx.LEFT,10)
        # BranchSelection Part
        sbBranchSelection = wx.StaticBox(self.pl, -1, 'BranchSelection', size=(-1, -1))
        #sbBranchSelection.SetForegroundColour(wx.BLUE)
        sbsBranchSelection = wx.StaticBoxSizer(sbBranchSelection, wx.HORIZONTAL)
        #self.stBranchSelection = wx.StaticText(self.pl,-1,'BranchSelection')
       # sbsBranchSelection.Add(self.stBranchSelection, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)
        bsBranchSelection = wx.BoxSizer ( wx.HORIZONTAL )
        self.mainBr = wx.CheckBox(self.pl, -1 ,'main')
        self.cr3Br = wx.CheckBox(self.pl, -1 ,'cr3')
        self.FTBr = wx.CheckBox(self.pl, -1 ,'Sanity Test')
        bsBranchSelection.Add(self.mainBr,0, wx.ALL,10)
        bsBranchSelection.Add(self.cr3Br,0, wx.ALL,10)
        bsBranchSelection.Add(self.FTBr,0, wx.ALL,10)
        sbsBranchSelection.Add(bsBranchSelection, 0, wx.LEFT,10)


        # SelectScenario Part
        sbSelectScenario = wx.StaticBox(self.pl, -1, 'SelectScenario', size=(-1, -1))
        #sbSelectScenario.SetForegroundColour(wx.BLUE)
        sbsSelectScenario = wx.StaticBoxSizer(sbSelectScenario, wx.VERTICAL)
        #self.stSelectScenario = wx.StaticText(self.pl,-1,'SelectScenario')
       # sbsSelectScenario.Add(self.stSelectScenario, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)
        bsSelectScenario = wx.BoxSizer ( wx.VERTICAL )
        bsSelectScenariox = []
        self.scen = []


        counter = 0
        index = -1
        for i in range(0,len(scenario_implemented)):
            self.scen.append(wx.CheckBox(self.pl, -1 ,scenario_implemented[i]))
            # if re.search('UL',scenario_implemented[i]) and re.search('FTP',scenario_implemented[i]):
                # self.scen[i].SetBackgroundColour("#ff154d")
            # elif re.search('UL',scenario_implemented[i]) and re.search('UDP',scenario_implemented[i]):
                # self.scen[i].SetBackgroundColour("#7fff00")
            # elif re.search('DL',scenario_implemented[i]) and re.search('FTP',scenario_implemented[i]):
                # self.scen[i].SetBackgroundColour("#0000ff")
            # elif re.search('DL',scenario_implemented[i]) and re.search('UDP',scenario_implemented[i]):
                # self.scen[i].SetBackgroundColour("#db7093")
            if re.search('FTP',scenario_implemented[i]) :
                self.scen[i].SetForegroundColour("#0000ff")
            elif re.search('UDP',scenario_implemented[i]):
                self.scen[i].SetForegroundColour("#db7093")
                
            if counter%5 == 0:
                bsSelectScenariox.append(wx.BoxSizer ( wx.HORIZONTAL ))
                index += 1
            bsSelectScenariox[index].Add(self.scen[i],0, wx.ALL,1)
            counter += 1
            
        #self.scen[i].SetFont(font)

        self.Alltest = wx.CheckBox(self.pl, -1 ,"All")
        bsSelectScenariox[index].Add(self.Alltest)

        for i in range(0,len(bsSelectScenariox)):
            bsSelectScenario.Add(bsSelectScenariox[i])

        sbsSelectScenario.Add(bsSelectScenario, 0, wx.LEFT,5)

        # BandSelection Part
        sbBandSelection = wx.StaticBox(self.pl, -1, 'BandSelection', size=(-1, -1))
        #sbBandSelection.SetForegroundColour(wx.BLUE)
        sbsBandSelection = wx.StaticBoxSizer(sbBandSelection, wx.VERTICAL)
        #self.stBandSelection = wx.StaticText(self.pl,-1,'BandSelection')
       # sbsBandSelection.Add(self.stBandSelection, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)
        bsBandSelection = wx.BoxSizer ( wx.HORIZONTAL )
        self.band4 = wx.CheckBox(self.pl, -1 ,'4')
        self.band17 = wx.CheckBox(self.pl, -1 ,'17')
        bsBandSelection.Add(self.band4,0, wx.ALL,10)
        bsBandSelection.Add(self.band17,0, wx.ALL,10)
        sbsBandSelection.Add(bsBandSelection, 0, wx.CENTER,10)
        
        # ProtocolSelection Part
        sbProtocolSelection = wx.StaticBox(self.pl, -1, 'ProtocolSelection', size=(-1, -1))
        #sbProtocolSelection.SetForegroundColour(wx.BLUE)
        sbsProtocolSelection = wx.StaticBoxSizer(sbProtocolSelection, wx.VERTICAL)
        bsProtocolSelection = wx.BoxSizer ( wx.HORIZONTAL )
        self.cftp = wx.CheckBox(self.pl, -1 ,'FTP')
        self.cudp = wx.CheckBox(self.pl, -1 ,'UDP')
        bsProtocolSelection.Add(self.cftp,0, wx.ALL,10)
        bsProtocolSelection.Add(self.cudp,0, wx.ALL,10)
        sbsProtocolSelection.Add(bsProtocolSelection, 0, wx.CENTER,10)

        # AdditionalOption Part
        sbAdditionOption = wx.StaticBox(self.pl, -1, 'AdditionOption', size=(-1, -1))
        #sbAdditionOption.SetForegroundColour(wx.BLUE)
        sbsAdditionOption = wx.StaticBoxSizer(sbAdditionOption, wx.VERTICAL)
        #self.stAdditionOption = wx.StaticText(self.pl,-1,'AdditionOption')
       # sbsAdditionOption.Add(self.stAdditionOption, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)
        bsAdditionOption = wx.BoxSizer ( wx.HORIZONTAL )
        self.stchangelist = wx.StaticText(self.pl,-1,' CL ')

        self.changelist = wx.TextCtrl(self.pl,-1,size=(60,20), value=u"")


        self.resume = wx.CheckBox(self.pl, -1 ,'Resume')
        self.flash = wx.CheckBox(self.pl, -1 ,'Flash')
        #self.graph = wx.CheckBox(self.pl, -1 ,'Graph')
        self.force = wx.CheckBox(self.pl, -1 ,'Force')
        self.cReg = wx.CheckBox(self.pl, -1 ,'Reg')
        #self.cReg.SetValue(True)
        #self.stNbComp = wx.StaticText(self.pl,-1,'Nb.Comparisons')
        #self.tcNbComp = wx.TextCtrl(self.pl,-1,size=(20,20), value=u"")
        bsAdditionOption.Add(self.stchangelist,0, wx.ALL,10)
        bsAdditionOption.Add(self.changelist,0, wx.ALL,10)
        #self.stOk_cl = wx.StaticText(self.pl,-1,'Ref_CL')
        #self.tOk_cl = wx.TextCtrl(self.pl,-1,size=(60,20), value=u"")
        #bsAdditionOption.Add(self.stOk_cl,0, wx.ALL,10)
        #bsAdditionOption.Add(self.tOk_cl,0, wx.ALL,10)
        #self.stKo_cl = wx.StaticText(self.pl,-1,'Reg_CL')
        #self.tKo_cl = wx.TextCtrl(self.pl,-1,size=(60,20), value=u"")
        #bsAdditionOption.Add(self.stKo_cl,0, wx.ALL,10)
       # bsAdditionOption.Add(self.tKo_cl,0, wx.ALL,10)


        bsAdditionOption.Add(self.flash,0, wx.ALL,10)
        #bsAdditionOption.Add(self.graph,0, wx.ALL,10)
        bsAdditionOption.Add(self.force,0, wx.ALL,10)
        bsAdditionOption.Add(self.cReg,0, wx.ALL,10)
        bsAdditionOption.Add(self.resume,0, wx.ALL,10)
        #bsAdditionOption.Add(self.stNbComp,0, wx.ALL,10)
        #bsAdditionOption.Add(self.tcNbComp,0, wx.ALL,10)
        sbsAdditionOption.Add(bsAdditionOption, 0, wx.LEFT,10)

        # StartSection Part
        sbStartSection = wx.StaticBox(self.pl, -1, 'Execution', size=(-1, -1))
        #sbStartSection.SetForegroundColour(wx.BLUE)
        sbsStartSection = wx.StaticBoxSizer(sbStartSection, wx.VERTICAL)
        #self.stStartSection = wx.StaticText(self.pl,-1,'StartSection')
       # sbsStartSection.Add(self.stStartSection, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)
        bsStartSection = wx.BoxSizer ( wx.HORIZONTAL )
        bStart = wx.Button(self.pl,-1,label="Start")
        bStop = wx.Button(self.pl,-1,label="Stop")
        bResult = wx.Button(self.pl,-1,label="Result")
        bReg = wx.Button(self.pl,-1,label="REG")
        bSetting = wx.Button(self.pl,-1,label="Setting")
        bExit = wx.Button(self.pl,-1,label="Exit")
        self.Bind(wx.EVT_BUTTON,self.eExit,bExit)
        self.Bind(wx.EVT_BUTTON, self.onRun, bStart)
        bsStartSection.Add(bStart,0, wx.ALL,10)
        self.Bind(wx.EVT_BUTTON, self.stopThread, bStop)
        bsStartSection.Add(bStop,0, wx.ALL,10)
        self.Bind(wx.EVT_BUTTON, self._onShowResult, bResult)
        bsStartSection.Add(bResult,0, wx.ALL,10)
        self.Bind(wx.EVT_BUTTON, self._onShowOptions, bSetting)
        self.Bind(wx.EVT_BUTTON, self.Regression_Start, bReg)
        bsStartSection.Add(bReg,0, wx.ALL,10)
        bsStartSection.Add(bSetting,0, wx.ALL,10)
        bsStartSection.Add(bExit,0, wx.ALL,10)
        sbsStartSection.Add(bsStartSection, 0, wx.LEFT,10)


        # FlashSection Part
        sbFlashSection = wx.StaticBox(self.pl, -1, 'Flash', size=(-1, -1))
        #sbFlashSection.SetForegroundColour(wx.BLUE)
        sbsFlashSection = wx.StaticBoxSizer(sbFlashSection, wx.VERTICAL)
        #self.stFlashSection = wx.StaticText(self.pl,-1,'FlashSection')
       # sbsFlashSection.Add(self.stFlashSection, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)
        bsFlashSection = wx.BoxSizer ( wx.HORIZONTAL )
        #self.entry = wx.TextCtrl(self.pl,-1,size=(600,20))
        self.entry = wx.TextCtrl(self.pl,-1,r"",wx.Point(20,20), wx.Size(500,20), \
                wx.TE_MULTILINE | wx.TE_RICH2)

        self.Bind(wx.EVT_TEXT_ENTER, self.OnPressEnter, self.entry)
        bFile = wx.Button(self.pl,-1,label="File")
        self.Bind(wx.EVT_BUTTON, self.OnOpenScen, bFile)
        bFlash = wx.Button(self.pl,-1,label="Flash")
        self.Bind(wx.EVT_BUTTON,self.flash_only,bFlash)

        bsFlashSection.Add(self.entry,0, wx.ALL,10)
        bsFlashSection.Add(bFile,0, wx.ALL,10)
        bsFlashSection.Add(bFlash,0, wx.ALL,10)
        sbsFlashSection.Add(bsFlashSection, 0, wx.LEFT,10)

        # LogSection Part
        sbLogSection = wx.StaticBox(self.pl, -1, 'LogSection', size=(-1, -1))
        #sbLogSection.SetForegroundColour(wx.BLUE)
        sbsLogSection = wx.StaticBoxSizer(sbLogSection, wx.VERTICAL)
        #self.stLogSection = wx.StaticText(self.pl,-1,'LogSection')
       # sbsLogSection.Add(self.stLogSection, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)
        bsLogSection = wx.BoxSizer ( wx.HORIZONTAL )
        self.log = wx.TextCtrl(self.pl, wx.ID_ANY, size=(700,300),style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        self.log.SetBackgroundColour("#000000")
        self.log.SetForegroundColour('#ffffff')
        bsLogSection.Add(self.log,1,wx.LEFT,10)


        #Callbox Options
        bsCallbox = wx.BoxSizer(wx.VERTICAL)
        bsDirection = wx.BoxSizer(wx.HORIZONTAL)
        bsTBRB = wx.BoxSizer(wx.HORIZONTAL)
        bsMode = wx.BoxSizer(wx.HORIZONTAL)


        self.rbCustom = wx.CheckBox(self.pl, -1 ,'Custom')
        stdir = wx.StaticText(self.pl,-1,' (DL/UL/COMB)')
        self.tcDirection =  wx.TextCtrl(self.pl,-1,size=(30,20), value=u"")
        stdlsize = wx.StaticText(self.pl,-1,' DL Size(Mb)')
        self.tcDownlik_size = wx.TextCtrl(self.pl,-1,size=(30,20), value=u"")
        stulsize = wx.StaticText(self.pl,-1,' UL Size(Mb)')
        self.tcUplink_size = wx.TextCtrl(self.pl,-1,size=(30,20), value=u"")
        stdlrb = wx.StaticText(self.pl,-1,' DL RB')
        self.tcdlrb = wx.TextCtrl(self.pl,-1,size=(30,20), value=u"")
        stdltb = wx.StaticText(self.pl,-1,' DL TBS')
        self.tcdltb = wx.TextCtrl(self.pl,-1,size=(30,20), value=u"")
        stulrb = wx.StaticText(self.pl,-1,' UL RB')
        self.tculrb = wx.TextCtrl(self.pl,-1,size=(30,20), value=u"")
        stultb = wx.StaticText(self.pl,-1,' UL TBS')
        self.tcultb = wx.TextCtrl(self.pl,-1,size=(30,20), value=u"")
        strlc = wx.StaticText(self.pl,-1,' RLC(AM/UM)')
        self.tcrlc = wx.TextCtrl(self.pl,-1,size=(30,20), value=u"")
        stmode = wx.StaticText(self.pl,-1,' MODE(SISO=1/MIMO=3)')
        self.tcmode = wx.TextCtrl(self.pl,-1,size=(30,20), value=u"")

        bsDirection.Add(self.rbCustom,1,wx.LEFT,10)
        bsDirection.Add(stdir,1,wx.LEFT,10)
        bsDirection.Add(self.tcDirection,1,wx.LEFT,10)
        bsDirection.Add(stdlsize,1,wx.LEFT,10)
        bsDirection.Add(self.tcDownlik_size,1,wx.LEFT,10)
        bsDirection.Add(stulsize,1,wx.LEFT,10)
        bsDirection.Add(self.tcUplink_size,1,wx.LEFT,10)

        bsTBRB.Add(stdlrb,1,wx.LEFT,10)
        bsTBRB.Add(self.tcdlrb,1,wx.LEFT,10)
        bsTBRB.Add(stdltb,1,wx.LEFT,10)
        bsTBRB.Add(self.tcdltb,1,wx.LEFT,10)
        bsTBRB.Add(stulrb,1,wx.LEFT,10)
        bsTBRB.Add(self.tculrb,1,wx.LEFT,10)
        bsTBRB.Add(stultb,1,wx.LEFT,10)
        bsTBRB.Add(self.tcultb,1,wx.LEFT,10)

        bsMode.Add(strlc,1,wx.LEFT,10)
        bsMode.Add(self.tcrlc,1,wx.LEFT,10)
        bsMode.Add(stmode,1,wx.LEFT,10)
        bsMode.Add(self.tcmode,1,wx.LEFT,10)

        bsCallbox.Add(bsDirection,1,wx.LEFT,10)
        bsCallbox.Add(bsTBRB,1,wx.LEFT,10)
        bsCallbox.Add(bsMode,1,wx.LEFT,10)

        sbCallbox = wx.StaticBox(self.pl, -1, 'Callbox Config', size=(-1, -1))
        sbsCallbox = wx.StaticBoxSizer(sbCallbox, wx.VERTICAL)
        sbsCallbox.Add(bsCallbox, 0,wx.LEFT,10)

        bsMsg = wx.BoxSizer ( wx.HORIZONTAL )
        self.msg = wx.TextCtrl(self.pl, wx.ID_ANY, size=(550,200),style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        #self.msg.SetBackgroundColour("#000000")
        #self.msg.SetForegroundColour('#ffffff')
        bsMsg.Add(self.msg,1,wx.LEFT,10)
        #self.asrt = wx.TextCtrl(self.pl, wx.ID_ANY, size=(550,150),style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        #self.msg.SetBackgroundColour("#000000")
        #self.msg.SetForegroundColour('#ffffff')
        #bsAssert = wx.BoxSizer ( wx.HORIZONTAL )
        #bsAssert.Add(self.asrt,1,wx.LEFT,10)
        bsAsset_Msg = wx.BoxSizer ( wx.VERTICAL )
        bsAsset_Msg.Add(sbsCallbox, 0, wx.EXPAND)
        bsAsset_Msg.Add(bsMsg, 0, wx.EXPAND)

        bsLGMSG = wx.BoxSizer ( wx.HORIZONTAL)
        bsLGMSG.Add(bsLogSection, 0, wx.EXPAND)
        bsLGMSG.Add(bsAsset_Msg, 0, wx.EXPAND)
        #sbsLogSection.Add(bsLogSection, 0, wx.LEFT,10)
        sbsLogSection.Add(bsLGMSG, 0, wx.LEFT,10)


        #TEST TYPE BRANCH BAND JOINING
        bsTTBS = wx.BoxSizer ( wx.HORIZONTAL)
        bsTTBS.Add(sbsTestType, 0, wx.EXPAND)
        bsTTBS.Add(sbsBranchSelection, 0, wx.EXPAND)
        bsTTBS.Add(sbsBandSelection, 0, wx.EXPAND)
        bsTTBS.Add(sbsProtocolSelection, 0, wx.EXPAND)
        bsTTBS.Add(sbsAdditionOption, 0, wx.EXPAND)
        #bsTTBS.Add(sbsPlatformType, 0, wx.EXPAND)
        bsTTBS.Add(self.rbplatform, 0, wx.EXPAND)

        #StartSection and Flash Joining
        bsSSFS = wx.BoxSizer ( wx.HORIZONTAL)
        bsSSFS.Add(sbsStartSection, 0, wx.EXPAND)
        bsSSFS.Add(sbsFlashSection, 0, wx.EXPAND)


        # Fill the Frame
        self.sizer = wx.BoxSizer ( wx.VERTICAL)
        self.sizer.Add(bsTTBS, 0, wx.EXPAND)
        # sizer.Add(sbsTestType, 0, wx.EXPAND)
        # sizer.Add(sbsBranchSelection, 0, wx.EXPAND)
        self.sizer.Add(sbsSelectScenario, 0, wx.EXPAND)
        #sizer.Add(sbsBandSelection, 0, wx.EXPAND)
        #sizer.Add(sbsAdditionOption, 0, wx.EXPAND)
        self.sizer.Add(bsSSFS,0,wx.EXPAND)
        #self.sizer.Add(sbsStartSection, 0, wx.EXPAND)
        self.sizer.Add(sbsLogSection, 0, wx.EXPAND)

        self.addProgress()
        self.pl.SetSizer(self.sizer)
        self.Center()
        self.Show(True)

        self._resultPanel()
        self.Rsizer.Layout()
        self._Additional_options()
        self.Osizer.Layout()
        self.optionPanel.SetSize(self.GetClientSizeTuple())
        self.resultPanel.SetSize(self.GetClientSizeTuple())
        self.pl.SetSize(self.GetClientSizeTuple())

        #self._onShowMain(None)

        self.redir=RedirectText(self.log)
        sys.stdout=self.redir
        sys.stderr=self.redir


        #image_file = 'test.jpeg'
        #bmp1 = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #self.bitmap1 = wx.StaticBitmap(self, -1, bmp1, (0, 0))

        #self.Refresh_Frame()

        self.flash_list = []

    def _resultPanel(self):

        #RESULT PANEL
        #self.resultPanel = wx.Panel(self.panel)
        self.resultPanel = ScrolledPanel(self.panel)
        self.resultPanel.SetupScrolling()

        # TestType Part
        sbTestType = wx.StaticBox(self.resultPanel, -1, 'Test Type', size=(-1, -1))
        #sbTestType.SetForegroundColour(wx.BLUE)
        sbsTestType = wx.StaticBoxSizer(sbTestType, wx.HORIZONTAL)
        #self.stTestType = wx.StaticText(self.resultPanel,-1,'Test Type')
        #sbsTestType.Add(self.stTestType, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)
        bsTestType = wx.BoxSizer ( wx.HORIZONTAL )
        self.rbMainR = wx.RadioButton(self.resultPanel, -1, 'Main')
        self.Bind(wx.EVT_RADIOBUTTON, self.TestType, id=self.rbMainR.GetId())
        self.rbCr3R   = wx.RadioButton(self.resultPanel, -1, 'Cr3')
        self.Bind(wx.EVT_RADIOBUTTON, self.TestType, id=self.rbCr3R.GetId())
        self.rbStR = wx.RadioButton(self.resultPanel, -1, 'ST')
        self.Bind(wx.EVT_RADIOBUTTON, self.TestType, id=self.rbStR.GetId())


       # bsTestType.Add(self.stTestType,0, wx.ALL,10)
        bsTestType.Add(self.rbCr3R,0, wx.ALL,10)
        bsTestType.Add(self.rbStR,0, wx.ALL,10)
        bsTestType.Add(self.rbMainR,0, wx.ALL,10)
        sbsTestType.Add(bsTestType, 0, wx.LEFT,10)

        # SelectScenario Part
        sbSelectScenario = wx.StaticBox(self.resultPanel, -1, 'SelectScenario', size=(-1, -1))
        #sbSelectScenario.SetForegroundColour(wx.BLUE)
        sbsSelectScenario = wx.StaticBoxSizer(sbSelectScenario, wx.VERTICAL)
        #self.stSelectScenario = wx.StaticText(self.resultPanel,-1,'SelectScenario')
       # sbsSelectScenario.Add(self.stSelectScenario, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)


        bsSelectScenario = wx.BoxSizer ( wx.VERTICAL )
        bsSelectScenariox = []
        #bsSelectScenariox.append(wx.BoxSizer ( wx.HORIZONTAL ))
        #bsSelectScenariox.append(wx.BoxSizer ( wx.HORIZONTAL ))
        self.scenR = []
        counter = 0
        index = -1
        font = wx.Font(7,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_LIGHT)

        for i in range(0,len(scenario_implemented)):
            self.scenR.append(wx.CheckBox(self.resultPanel, -1 ,scenario_implemented[i]))
            if re.search('FTP',scenario_implemented[i]) :
                self.scenR[i].SetForegroundColour("#0000ff")
            elif re.search('UDP',scenario_implemented[i]):
                self.scenR[i].SetForegroundColour("#db7093")
            if counter%5 == 0:
                bsSelectScenariox.append(wx.BoxSizer ( wx.HORIZONTAL ))
                index += 1
            bsSelectScenariox[index].Add(self.scenR[i],0, wx.ALL,1)
            counter += 1
        self.AlltestR = wx.CheckBox(self.resultPanel, -1 ,"All")
        bsSelectScenariox[1].Add(self.AlltestR)

        for i in range(0,len(bsSelectScenariox)):
            bsSelectScenario.Add(bsSelectScenariox[i])

        sbsSelectScenario.Add(bsSelectScenario, 0, wx.LEFT,5)







##        bsSelectScenario = wx.BoxSizer ( wx.HORIZONTAL )
##        self.scenR = []
##        for i in range(0,len(scenario_implemented)):
##            self.scenR.append(wx.CheckBox(self.resultPanel, -1 ,scenario_implemented[i]))
##            bsSelectScenario.Add(self.scenR[i],0, wx.ALL,1)
##        sbsSelectScenario.Add(bsSelectScenario, 0, wx.LEFT,5)

        # BandSelection Part
        sbBandSelection = wx.StaticBox(self.resultPanel, -1, 'BandSelection', size=(-1, -1))
        #sbBandSelection.SetForegroundColour(wx.BLUE)
        sbsBandSelection = wx.StaticBoxSizer(sbBandSelection, wx.VERTICAL)
        #self.stBandSelection = wx.StaticText(self.resultPanel,-1,'BandSelection')
       # sbsBandSelection.Add(self.stBandSelection, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)
        bsBandSelection = wx.BoxSizer ( wx.HORIZONTAL )
        self.band4R = wx.CheckBox(self.resultPanel, -1 ,'4')
        self.band17R = wx.CheckBox(self.resultPanel, -1 ,'17')
        bsBandSelection.Add(self.band4R,0, wx.ALL,10)
        bsBandSelection.Add(self.band17R,0, wx.ALL,10)
        sbsBandSelection.Add(bsBandSelection, 0, wx.CENTER,10)

        # GraphOption Part
        sbAdditionOption = wx.StaticBox(self.resultPanel, -1, 'GraphOption', size=(-1, -1))
        #sbAdditionOption.SetForegroundColour(wx.BLUE)
        sbsAdditionOption = wx.StaticBoxSizer(sbAdditionOption, wx.VERTICAL)
        #self.stAdditionOption = wx.StaticText(self.resultPanel,-1,'AdditionOption')
       # sbsAdditionOption.Add(self.stAdditionOption, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)
        bsAdditionOption = wx.BoxSizer ( wx.HORIZONTAL )
        self.stchangelistR = wx.StaticText(self.resultPanel,-1,' CL ')
        self.forceGraph = wx.CheckBox(self.resultPanel, -1 ,'Force')

        self.changelistR = wx.TextCtrl(self.resultPanel,-1,size=(60,20), value=u"")
        #self.Bind(wx.EVT_TEXT_ENTER, self.OnPressEnter, self.changelistR)
        self.stNbCompR = wx.StaticText(self.resultPanel,-1,'Nb.Comparisons')
        self.tcNbCompR = wx.TextCtrl(self.resultPanel,-1,size=(20,20), value=u"")
        bsAdditionOption.Add(self.stchangelistR,0, wx.ALL,10)
        bsAdditionOption.Add(self.changelistR,0, wx.ALL,10)
        bsAdditionOption.Add(self.stNbCompR,0, wx.ALL,10)
        bsAdditionOption.Add(self.tcNbCompR,0, wx.ALL,10)
        bsAdditionOption.Add(self.forceGraph,0, wx.ALL,10)

        sbsAdditionOption.Add(bsAdditionOption, 0, wx.LEFT,10)

        # StartSection Part
        sbStartSection = wx.StaticBox(self.resultPanel, -1, '', size=(-1, -1))
        #sbStartSection.SetForegroundColour(wx.BLUE)
        sbsStartSection = wx.StaticBoxSizer(sbStartSection, wx.VERTICAL)
        #self.stStartSection = wx.StaticText(self.resultPanel,-1,'StartSection')
       # sbsStartSection.Add(self.stStartSection, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)
        bsStartSection = wx.BoxSizer ( wx.HORIZONTAL )
        bStart = wx.Button(self.resultPanel,-1,label="Generate")
        bStop = wx.Button(self.resultPanel,-1,label="Clear")
        bResult = wx.Button(self.resultPanel,-1,label="Main Window")
        self.Bind(wx.EVT_BUTTON, self._updateResultPanel, bStart)
        bsStartSection.Add(bStart,0, wx.ALL,10)
        self.Bind(wx.EVT_BUTTON, self._cleanResultPanel, bStop)
        bsStartSection.Add(bStop,0, wx.ALL,10)
        self.Bind(wx.EVT_BUTTON, self._onShowMain, bResult)
        bsStartSection.Add(bResult,0, wx.ALL,10)
        sbsStartSection.Add(bsStartSection, 0, wx.CENTER,10)

        #TEST TYPE BRANCH BAND JOINING
        bsTTBS = wx.BoxSizer ( wx.HORIZONTAL)
        bsTTBS.Add(sbsTestType, 0, wx.EXPAND)
        bsTTBS.Add(sbsBandSelection, 0, wx.EXPAND)
        bsTTBS.Add(sbsAdditionOption, 0, wx.EXPAND)

        #IMAGE
##        self.img = []
##        self.caption = []
##        gridSizer = wx.GridSizer(rows=20, cols=1)
##
##        InsideBoxer =[]
##        #self.stcHelp = wx.StaticText(self.resultPanel, label="help help help\n"*8)
##        #btn = wx.Button(self.resultPanel, label="close[x]")
##        #btn.Bind(wx.EVT_BUTTON, self._onShowMain)
##        sizer2 = wx.BoxSizer(wx.VERTICAL)
##        sizer2.Add((20,20),proportion=1)
##       # sizer2.Add(self.stcHelp)
##        for i in range(0,len(BAND_TANGO_ALLOWED)):
##            for j in range(0,len(scenario_implemented)):
##                InsideBoxer.append(wx.BoxSizer(wx.VERTICAL))
##                self.caption.append(wx.StaticText(self.resultPanel,-1," "))
##                self.img.append(wx.StaticBitmap(self.resultPanel, wx.ID_ANY, wx.BitmapFromImage(wx.EmptyImage(240,240))))
##                InsideBoxer[i*len(scenario_implemented)+j].Add(self.caption[i*len(scenario_implemented)+j],-1,wx.ALL|wx.ALIGN_CENTER_VERTICAL,10)
##
##                InsideBoxer[i*len(scenario_implemented)+j].Add(self.img[i*len(scenario_implemented)+j])
##                gridSizer.Add(InsideBoxer[i*len(scenario_implemented)+j])

        #gridSizer.Add(btn)

        #gridSizer.Add(sizer2, 0, wx.ALIGN_RIGHT)

        # Fill the Frame
        self.Rsizer = wx.BoxSizer ( wx.VERTICAL)
        self.Rsizer.Add(bsTTBS, 0, wx.EXPAND)
        self.Rsizer.Add(sbsSelectScenario, 0, wx.EXPAND)
        self.Rsizer.Add(sbsStartSection, 0, wx.EXPAND)
        #self.Rsizer.Add((5,5), proportion=1)
       # self.Rsizer.Add(gridSizer, 0, wx.EXPAND)

        self.resultPanel.SetSizer(self.Rsizer)
        self.resultPanel.Hide()
        self.resultPanel.Raise()
        #self.resultPanel.SetBackgroundColour((240,250,240))
        self.Bind(wx.EVT_SIZE, self._onSize)

    def _Additional_options(self):
        self.optionPanel = ScrolledPanel(self.panel)
        self.optionPanel.SetupScrolling()

        # Options Part
        sboptions = wx.StaticBox(self.optionPanel, -1, 'Options', size=(-1, -1))
        sbsoptions = wx.StaticBoxSizer(sboptions, wx.HORIZONTAL)
        bsoptions = wx.BoxSizer ( wx.HORIZONTAL )

        #AT PORT
        satport = wx.StaticText(self.optionPanel,-1,'AT PORT')
        bsoptions.Add(satport,0, wx.ALL,10)
        self.atport = wx.TextCtrl(self.optionPanel,-1,size=(60,20), value=u"")
        bsoptions.Add(self.atport,0, wx.ALL,10)
        #self.Bind(wx.EVT_RADIOBUTTON, self.options, id=self.rbStR.GetId())

        #MODEM PORT
        smodemport = wx.StaticText(self.optionPanel,-1,'MODEM PORT')
        bsoptions.Add(smodemport,0, wx.ALL,10)
        self.modemport = wx.TextCtrl(self.optionPanel,-1,size=(60,20), value=u"")
        bsoptions.Add(self.modemport,0, wx.ALL,10)

        #VID
        svid = wx.StaticText(self.optionPanel,-1,'VID ')
        bsoptions.Add(svid,0, wx.ALL,10)
        self.vid_no = wx.TextCtrl(self.optionPanel,-1,size=(60,20), value=u"")
        bsoptions.Add(self.vid_no,0, wx.ALL,10)
        #NEXT WIDGET

        #END

        sbsoptions.Add(bsoptions, 0, wx.LEFT,10)
        #Return
        sbreturn = wx.StaticBox(self.optionPanel, -1, '', size=(-1, -1))
        sbsreturn = wx.StaticBoxSizer(sbreturn, wx.HORIZONTAL)
        bsreturn = wx.BoxSizer ( wx.HORIZONTAL )
        bReturn = wx.Button(self.optionPanel,-1,label="Return")
        self.Bind(wx.EVT_BUTTON, self._onShowMain, bReturn)
        bsreturn.Add(bReturn,0, wx.ALL,10)
        sbsreturn.Add(bsreturn,0,wx.CENTER,10)

        self.Osizer = wx.BoxSizer ( wx.VERTICAL)
        self.Osizer.Add(sbsoptions, 0, wx.EXPAND)
        self.Osizer.Add(sbsreturn, 0, wx.EXPAND)
        self.optionPanel.SetSizer(self.Osizer)
        self.optionPanel.Hide()
        self.optionPanel.Raise()
        self.Bind(wx.EVT_SIZE, self._onSize)

    def eExit(self,event):
        os._exit(1)
            
    def _onShowMain(self, event):
        self.pl.SetPosition((0,0))
        self.resultPanel.Hide()
        self.optionPanel.Hide()
        self.pl.Show()
        self.Refresh_Frame()

    def _onShowResult(self, event):
        self.resultPanel.SetPosition((0,0))
        self.resultPanel.Show()
        self.pl.Hide()
        self.optionPanel.Hide()
        self.resultPanel.Refresh()
        self.Refresh_Frame()

    def _onShowOptions(self, event):
        self.optionPanel.SetPosition((0,0))
        self.optionPanel.Show()
        self.pl.Hide()
        self.resultPanel.Hide()
        self.optionPanel.Refresh()
        self.Refresh_Frame()

    def GetResultPanelOption(self):
        if (self.rbMainR.GetValue()):
            self.branch_selected = "main"
            self.branch_idx = 0
        elif (self.rbCr3R.GetValue()):
            self.branch_selected = "cr3"
            self.branch_idx = 1
        else :
            self.branch_selected = "ST"
            self.branch_idx = 2

        self.band_4graph =[]
        if self.band4R.IsChecked():
           self.band_4graph.append(4)
        if self.band17R.IsChecked():
            self.band_4graph.append(17)

        self.scenario_4graph = []
        if self.AlltestR.IsChecked():
            self.scenario_4graph = scenario_implemented
        else :
            for i in range(0,len(scenario_implemented)):
                if self.scenR[i].IsChecked() :
                    self.scenario_4graph.append(scenario_implemented[i])

        try:
            self.clR = int(self.changelistR.GetValue())
        except:
            self.clR = 0

        try:
            self.nbcmpR = int(self.tcNbCompR.GetValue())
        except:
            self.nbcmpR = 5

        self.image_3d()

    def init_2d(self,foo,x,y):
        return [[foo for i in range(x)] for j in range(y)]

    def image_3d(self):

        #cdir ='\\\serv2.icerasemi.com\home\gcflab\workspace\callbox-test_cr3\swtools\main.br\\auto_regression\callbox\chart\\'
        #cdir = '\\\\'+CHART_LOC+'\\'
        cdir = 'chart\\'
        self.image_list =[]
        for i in range(0,len(BRANCH_ALLOWED)):
            self.image_list.append(" ")
            self.image_list[i] = self.init_2d("x",len(scenario_implemented),len(BAND_TANGO_ALLOWED))


        for i in range(0,len(BRANCH_ALLOWED)):
            for j in range(0,len(BAND_TANGO_ALLOWED)):
                for k in range(0,len(scenario_implemented)):
                    file = scenario_implemented[k]+"_"+"Band"+str(BAND_TANGO_ALLOWED[j])+"_"+BRANCH_ALLOWED[i]+".jpeg"
                    self.image_list[i][j][k] = cdir+file



    def _updateResultPanel(self,event):

        self.GetResultPanelOption()
        self._cleanResultPanel()
        self.img = []
        self.caption = []
        size = len(self.band_4graph) * len(self.scenario_4graph)
        self.gridSizer = wx.GridSizer(rows=size, cols=1)
        InsideBoxer =[]
        if self.forceGraph.IsChecked() or self.clR !=0 :
            for i in self.band_4graph:
                for j in self.scenario_4graph:
                    Chart().chart_scenario(int(i),self.clR,self.nbcmpR,j,self.branch_selected)


        for j in range(0,len(self.band_4graph)):
            for k in range(0,len(self.scenario_4graph)):
                self.caption.append(wx.StaticText(self.resultPanel,-1,"BAND "+str(self.band_4graph[j])+" "+self.scenario_4graph[k]))
                self.caption[j*len(self.scenario_4graph)+k].SetFont(self.Font_Result)
                self.img.append(wx.StaticBitmap(self.resultPanel, wx.ID_ANY, wx.BitmapFromImage(wx.Image(self.image_list[self.branch_idx][self.find_index(BAND_TANGO_ALLOWED,self.band_4graph[j])][self.find_index(scenario_implemented,self.scenario_4graph[k])],wx.BITMAP_TYPE_ANY))))
                #print "img loc",self.image_list[self.branch_idx][l][self.find_index(scenario_implemented,self.scenario_4graph[k])]
                InsideBoxer.append(wx.BoxSizer(wx.VERTICAL))
                InsideBoxer[j*len(self.scenario_4graph)+k].Add(self.caption[j*len(self.scenario_4graph)+k])
                InsideBoxer[j*len(self.scenario_4graph)+k].Add(wx.StaticText(self.resultPanel,-1,""))
                InsideBoxer[j*len(self.scenario_4graph)+k].Add(self.img[j*len(self.scenario_4graph)+k])

                self.gridSizer.Add(InsideBoxer[j*len(self.scenario_4graph)+k])

                #self.img[j*len(self.scenario_4graph)+k].SetBitmap(wx.BitmapFromImage( wx.Image(self.image_list[self.branch_idx][j][k],wx.BITMAP_TYPE_ANY)))

                #self.caption[j*len(self.scenario_4graph)+k].SetLabel("Band "+str(self.band_4graph[j])+"  "+self.scenario_4graph[k])
                #self.img[j*len(self.scenario_4graph)+k].SetBitmap(wx.BitmapFromImage( wx.Image(self.image_list[self.branch_idx][j][k],wx.BITMAP_TYPE_ANY)))


        self.Rsizer.Add(self.gridSizer, 0, wx.EXPAND)
        self.Refresh_Frame()

    def _cleanResultPanel(self,event=0):
        try:
            self.Rsizer.Hide(self.gridSizer)
            self.Rsizer.Remove(self.gridSizer)
        except:
            pass
            #print "Already Empty"
        self.gridSizer = []
        self.Refresh_Frame()

    def _onSize(self, event):
        event.Skip()
        self.resultPanel.SetSize(self.GetClientSizeTuple())
        self.pl.SetSize(self.GetClientSizeTuple())

    def ParseArgs(self):
        self.branch_4test =[]
        if self.mainBr.IsChecked():
            self.branch_4test.append('main')
        if self.cr3Br.IsChecked():
            self.branch_4test.append('cr3')
        if self.FTBr.IsChecked():
            self.branch_4test.append('ST')

        self.band_4test =[]
        if self.band4.IsChecked():
           self.band_4test.append(4)
        if self.band17.IsChecked():
            self.band_4test.append(17)
            
        self.protocol_4test =[]
        if self.cftp.IsChecked():
           self.protocol_4test.append("FTP")
        if self.cudp.IsChecked():
            self.protocol_4test.append("UDP")
            
        #BAND_TANGO_ALLOWED = band_4test

        self.scenario_4test = []
        if self.Alltest.IsChecked():
            self.scenario_4test = scenario_implemented

        else :
            for i in range(0,len(scenario_implemented)):
                if self.scen[i].IsChecked() :
                    self.scenario_4test.append(scenario_implemented[i])

        try:
            if self.rbCustom.IsChecked():
                self.scenario_4test.append("CUSTOM")
        except:
            pass

        #print self.scenario_4test

        try:
            self.cl = int(self.changelist.GetValue())
        except:
            self.cl = 0

        try:
            self.nbcmp = int(self.tcNbComp.GetValue())
        except:
            self.nbcmp = 0

        #Option Panel
        if (str(self.atport.GetValue()) != "") :
            common.PORT_COM_TANGO = str(self.atport.GetValue())
            #print "AT Port to use",common.PORT_COM_TANGO

        if(str(self.modemport.GetValue()) != ""):
            common.MODEM_PORT = str(self.modemport.GetValue())
            #print "Modem Port to use",common.MODEM_PORT

        if(str(self.vid_no.GetValue()) != ""):
            common.VID = str(self.vid_no.GetValue())
            #print "VID number to use",common.VID

        try:
            if self.rbplatform.GetSelection() == 0:
                common.CARDHU = False
            if self.rbplatform.GetSelection() == 1:
                common.CARDHU = True
                common.MODEM_PORT = common.CARDHU_MODEM_TCP
        except:
            common.CARDHU = False

        try:
            if self.rbCustom.IsChecked():
                print "Setting default values for custom config"

                if self.tcDirection.GetValue() == "":
                    self.tcDirection.SetValue("DL")

                if self.tcrlc.GetValue() == "":
                    self.tcrlc.SetValue("AM")

                if self.tcdlrb.GetValue() == "":
                    self.tcdlrb.SetValue(str(RB_START))
                if self.tcdltb.GetValue() == "":
                    self.tcdltb.SetValue(str(TBSIDX_START))
                if self.tculrb.GetValue() == "":
                    self.tculrb.SetValue(str(10))
                if self.tcultb.GetValue() == "":
                    self.tcultb.SetValue(str(10))
                if self.tcDownlik_size.GetValue() == "":
                    self.tcDownlik_size.SetValue(str(1000))
                #self.tcDownlik_size.SetValue(str(1000))
                if self.tcUplink_size.GetValue() == "":
                    self.tcUplink_size.SetValue(str(500))
                if self.tcmode.GetValue() == "":
                    self.tcmode.SetValue(str(1))
        except:
            pass

    def Refresh_Progress(self):
        self.sizer.Layout()
        self.pl.Layout()

    def Refresh_Frame(self):
        #self.log.Clear()
        self.sizer.Layout()
        self.Rsizer.Layout()
        self.Osizer.Layout()
        self.panel.Refresh()
        self.pl.Refresh()
        self.resultPanel.Refresh()
        self.SendSizeEvent()
        self.resultPanel.SetupScrolling()
        self.resultPanel.Layout()
        self.optionPanel.Layout()
        self.pl.Layout()
        self.panel.Layout()

        self.log.Refresh()
        self.redir=RedirectText(self.log)
        sys.stdout=self.redir
        sys.stderr=self.redir

    def onRun(self, event):

        self.cleanProgress()
        self.ParseArgs()
        self.InitupdateProgress()

        self.t1 = KThread(target=self.Start_Test)
        self.t1.start()

        self.t2 = KThread(target=self.updateProgress)
        self.t2.start()

    def stopThread(self,event):
        #print "Number of Active Threads",threading.activeCount()
        if threading.activeCount()>1:
            self.t1.kill() # Autocallbox Thread
            self.t2.kill() # Read_Status Thread
            print "Number of Active Threads",threading.activeCount()
        #print "Number of Active Threads",threading.activeCount()
        #self.cleanProgress()

    def addProgress(self):

        #ProgressSection
        self.cl_run = "       "
        self.branch_run = "     "
        self.band_run = "  "
        self.scen_run = "               "
        self.scenario_4test = ""
        #current Run
        sbCurrentRun = wx.StaticBox(self.pl, -1, 'Current Test', size=(-1, -1))
        #sbCurrentRun.SetForegroundColour(wx.GREEN)
        sbsCurrentRun = wx.StaticBoxSizer(sbCurrentRun, wx.VERTICAL)
        bsCurrentRun = wx.BoxSizer ( wx.HORIZONTAL )
        self.stCL = wx.StaticText(self.pl,-1,self.cl_run)
        self.stBranch = wx.StaticText(self.pl,-1,self.branch_run)
        self.stBand = wx.StaticText(self.pl,-1,self.band_run)
        self.stScen = wx.StaticText(self.pl,-1,self.scen_run)
        bsCurrentRun.Add(wx.StaticText(self.pl,-1,"CL : "))
        bsCurrentRun.Add(self.stCL,1,wx.ALL|wx.EXPAND,10)
        bsCurrentRun.Add(wx.StaticText(self.pl,-1,"BRANCH : "))
        bsCurrentRun.Add(self.stBranch,1,wx.ALL|wx.EXPAND,10)
        bsCurrentRun.Add(wx.StaticText(self.pl,-1,"BAND : "))
        bsCurrentRun.Add(self.stBand,1,wx.ALL|wx.EXPAND,10)
        bsCurrentRun.Add(wx.StaticText(self.pl,-1,"SCENARIO : "))
        bsCurrentRun.Add(self.stScen,1,wx.ALL|wx.EXPAND,10)
        sbsCurrentRun.Add(bsCurrentRun, 0, wx.LEFT,10)

        #Band4
        sbBand4Prog = wx.StaticBox(self.pl, -1, 'Band 4 Progress', size=(-1, -1))
        #sbBand4Prog.SetForegroundColour(wx.BLUE)
        sbsBand4Prog = wx.StaticBoxSizer(sbBand4Prog, wx.VERTICAL)
        bsBand4Prog = wx.BoxSizer ( wx.HORIZONTAL )
        self.stscen_4 = []
        for i in range(0,len(scenario_implemented)):
            self.stscen_4.append(wx.StaticText(self.pl, -1 ,""))
            bsBand4Prog.Add(self.stscen_4[i],0, wx.ALL,10)
        sbsBand4Prog.Add(bsBand4Prog, 0, wx.LEFT,10)

        #Band17
        sbBand17Prog = wx.StaticBox(self.pl, -1, 'Band 17 Progress', size=(-1, -1))
        #sbBand17Prog.SetForegroundColour(wx.BLUE)
        sbsBand17Prog = wx.StaticBoxSizer(sbBand17Prog, wx.VERTICAL)
        bsBand17Prog = wx.BoxSizer ( wx.HORIZONTAL )
        self.stscen_17 = []
        for i in range(0,len(scenario_implemented)):
            self.stscen_17.append(wx.StaticText(self.pl, -1 ,""))
            bsBand17Prog.Add(self.stscen_17[i],0, wx.ALL,10)
        sbsBand17Prog.Add(bsBand17Prog, 0, wx.LEFT,10)

        #PROGRESS SECTION JOIN
        self.bsPRG = wx.BoxSizer ( wx.VERTICAL)
        self.bsPRG.Add(sbsCurrentRun, 0, wx.EXPAND)
        self.bsPRG.Add(sbsBand4Prog, 0, wx.EXPAND)
        self.bsPRG.Add(sbsBand17Prog, 0, wx.EXPAND)

        self.sizer.Add(self.bsPRG,0,wx.EXPAND)

        #self.pl.Refresh()

        #self.Refresh_Frame()
    def InitupdateProgress(self):
        self.stCL.SetLabel(self.cl_run)
        self.stBranch.SetLabel(self.branch_run)
        self.stBand.SetLabel(self.band_run)
        self.stScen.SetLabel(self.scen_run)

        if self.band4.IsChecked():
            for i in range(0,len(self.scenario_4test)):
                self.stscen_4[i].SetLabel(self.scenario_4test[i])


        if self.band17.IsChecked():
            for i in range(0,len(self.scenario_4test)):
                self.stscen_17[i].SetLabel(self.scenario_4test[i])

        self.Refresh_Frame()

    def updateProgress(self):

        self.scen_list_4x = []
        self.scen_list_17x = []
        for scen in self.scenario_4test:
            self.scen_list_4x.append(scen)
            self.scen_list_17x.append(scen)

        while threading.activeCount()>1:
        #while self.t1.isAlive() or self.t4.isAlive():
            time.sleep(5)
            self.Read_Status_Msg()
            time.sleep(5)
            Read = self.Read_Status()
            if Read == True :
                self.stCL.SetLabel(self.cl_run)
                self.stBranch.SetLabel(self.branch_run)
                self.stBand.SetLabel(self.band_run)
                self.stScen.SetLabel(self.scen_run)

                for i in range(0,len(self.scenario_4test)):
                    if self.band4.IsChecked():
                        if self.scen_list_4x[i] == STATUS_OK:
                            self.stscen_4[i].SetBackgroundColour("#1ad821") # GREEN
                        elif self.scen_list_4x[i] == STATUS_REGRESSION:
                            self.stscen_4[i].SetBackgroundColour("#ddff0f") # Orange
                        elif self.scen_list_4x[i] == STATUS_ASSERT:
                            self.stscen_4[i].SetBackgroundColour("#ff1515") # Red
                        elif self.scen_list_4x[i] != self.scenario_4test[i]:
                            self.stscen_4[i].SetBackgroundColour("#0000ff") # Blue

                    if self.band17.IsChecked():
                        if self.scen_list_17x[i] == STATUS_OK:
                            self.stscen_17[i].SetBackgroundColour("#1ad821") # GREEN
                        elif self.scen_list_17x[i] == STATUS_REGRESSION:
                            self.stscen_17[i].SetBackgroundColour("#ddff0f") # Orange
                        elif self.scen_list_17x[i] == STATUS_ASSERT:
                            self.stscen_17[i].SetBackgroundColour("#ff1515") # Red
                        elif self.scen_list_17x[i] != self.scenario_4test[i]:
                            self.stscen_17[i].SetBackgroundColour("#0000ff") # Blue

                self.Refresh_Progress()
                #self.pl.Refresh()
                # self.panel.Fit()
                # self.SendSizeEvent()
                # #self._onSize(wxFrame::SendSizeEvent)

    def cleanProgress(self):
        self.cl_run = ""
        self.branch_run = ""
        self.band_run = ""
        self.scen_run = ""
        self.scenario_4test = ""

        self.stCL.SetLabel(self.cl_run)
        self.stBranch.SetLabel(self.branch_run)
        self.stBand.SetLabel(self.band_run)
        self.stScen.SetLabel(self.scen_run)

        for i in range(0,len(scenario_implemented)):
            self.stscen_4[i].SetLabel("")
            self.stscen_4[i].SetBackgroundColour("#bfbfbf")

        for i in range(0,len(scenario_implemented)):
            self.stscen_17[i].SetLabel("")
            self.stscen_17[i].SetBackgroundColour("#bfbfbf")

        self.Refresh_Frame()

    def mainThread(self):
        self.kill_thread = False
        self.t1 = threading.Thread(target=self.Start_Test)
        self.t1.start()

        while True:
            if self.kill_thread == True :
                #self.t1.join()
                #print "Killing Thread"
                sys.exit(1)


    def ResultWindow(self, event):
        print "Result Window"

    def TestType(self, event):
        if (self.rbAuto.GetValue()):
            self.testchoice = 0;
        elif (self.rbUnit.GetValue()):
            self.testchoice = 1
        else:
            self.testchoice = 2

    def PlatformType(self, event):
        if (self.rbWinxp.GetValue()):
            self.platformchoice = 0;
        elif (self.rbWoA.GetValue()):
            self.platformchoice = 1

    def Start_Test(self):
        iCT = CallboxTest()
        iCT.Init_Auto(self.branch_4test,self.band_4test,self.scenario_4test)
        if self.rbCustom.IsChecked():
            iCT.custom_config(rlc=self.tcrlc.GetValue(),dl_rb=int(self.tcdlrb.GetValue()),dl_tb=int(self.tcdltb.GetValue()),ul_rb=int(self.tculrb.GetValue()),ul_tb=int(self.tcultb.GetValue()),dl_size=int(self.tcDownlik_size.GetValue()),ul_size=int(self.tcUplink_size.GetValue()),tm=int(self.tcmode.GetValue()),dir=self.tcDirection.GetValue())

        if self.testchoice == 0:
            #print "Call Auto scheduler"
            iCT.start(Res=self.resume.IsChecked())
        elif self.testchoice == 1:
            if self.flash.IsChecked() == True and self.entry.GetLabel() != "":
                #print "Run Test with Flashing"
                Untar().main(self.entry.GetLabel(),self.branch_4test[0])
                Flash().flash_modem(99999,self.branch_4test[0])
                #shutil.copy2(BINARY_LIB+'99999.zlib.wrapped',BINARY_LIB+str(self.cl)+self.branch_4test[0]+'.zlib.wrapped')
                if int(self.cl) !=0 and not os.path.exist(BINARY_LIB+str(self.cl)+self.branch_4test[0]+'.zlib.wrapped'):
                    shutil.copy2(BINARY_LIB+'99999.zlib.wrapped',BINARY_LIB+str(self.cl)+self.branch_4test[0]+'.zlib.wrapped')
                iCT.Init_Auto(self.branch_4test,self.band_4test,self.scenario_4test)
                iCT.Run_Branch_Test(Forced=self.force.IsChecked(),flash=False,Reg=self.cReg.IsChecked(),CL=self.cl,Resume=self.resume.IsChecked())
                #print "Run Test Finished"
            else:
                #print "Run Test without Flashing"
                iCT.Run_Branch_Test(Forced=self.force.IsChecked(),flash=self.flash.IsChecked(),Reg=self.cReg.IsChecked(),CL=self.cl,Resume=self.resume.IsChecked())
                #print "Run Test Finished"

        elif self.testchoice == 2:
           print "No Test"


    def find_index(self,lst,item):
        for i in range(0,len(lst)):
            if(lst[i]==item):
                return i
        return 0

    def Read_Status(self):
        file = 'status.txt'
        self.scen_list_4 =[]
        self.status_list_4 = []
        self.scen_list_17 =[]
        self.status_list_17 = []

        latest_CL = 0
        latest_br = ""
        CURRENT_SCEN = ""
        if os.path.exists(file):
            FILE_OK = open(file,'r')
            for line in (FILE_OK.readlines()):#reversed
                try:
                    band_run = re.search(re.compile(r"Band:(\S+)"),line).group(1)
                    scen = re.search(re.compile(r"Test:(\S+)"), line).group(1)
                    Status = re.search(re.compile(r"Status:(\S+)(])"), line).group(1)
                    if int(band_run) == 4 :
                        self.scen_list_4x[self.find_index(self.scenario_4test,scen)] = Status
                    elif int(band_run) == 17 :
                        self.scen_list_17x[self.find_index(self.scenario_4test,scen)] = Status
                except:
                    pass

            self.cl_run = re.search(re.compile(r"CL([0-9]+)"),line).group(1)
            self.branch_run = re.search(re.compile(r"Branch:(\S+)"),line).group(1)
            self.scen_run  = re.search(re.compile(r"Test:(\S+)"), line).group(1)
            self.band_run = re.search(re.compile(r"Band:(\S+)"),line).group(1)

            FILE_OK.close()
            return True
        else:
            return False

    def OnPressEnter(self,event):
        x = 1
        #self.stInfo.SetLabel( self.entry.GetValue())

    def OnOpenScen(self,event):
        wildcard = " (*.tar,*.gz,*.wrapped,*.rar)|*.tar;*.gz;*.wrapped;*.rar"
        dialog = wx.FileDialog(None, "Choose a file",os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            self.entry.AppendText(filename)
            self.flash_list.append(filename)
        dialog.Destroy()

    def flash_only(self,event):
        self.t3 = KThread(target=self.flash_thread)
        self.t3.start()

    def flash_thread(self):
        if self.entry.GetLabel() != "" :
            Untar().main(self.entry.GetLabel(),self.branch_4test[0])
            Flash().flash_modem(99999,self.branch_4test[0])
        else:
            print "Please select a binary to flash"


    def Regression_Start(self,event):
        #self.Read_Status_Msg()
        #return

        self.cleanProgress()
        self.ParseArgs()
        self.InitupdateProgress()
        self.t4 = KThread(target=self.regression_thread)
        self.t4.start()
        self.t2 = KThread(target=self.updateProgress)
        self.t2.start()


    def Already_Written(self,cl,branch,band,scen,status):
        try:
            out = self.msg.GetValue()
            Flag = False
            result = out.split('\n')
            #print "Result",result
            #print "len",len(result)
            for i in range(0,(len(result)-1)):
                #print "i",i
                #print "inside"
                #print "Line",line
                #print "result[i]",result[i]
                grp = re.search('CL:([0-9]+) Branch:(\S+) Band:(\S+) SCENARIO:(\S+) STATUS:(\S+)',result[i])
                #print "written",grp.group(1) #print grp.group(2), grp.group(3), grp.group(4) , grp.group(5)
                #print "Next",str(cl),branch,band,scen,status
                if grp.group(1) == str(cl) and grp.group(2) == branch and grp.group(3) == band and grp.group(4) == scen and grp.group(5) == status :
                   #print "True"
                   Flag =  True

            return Flag
        except:
            return False
            pass
            #return False

    def assert_info(self,cl,branch,band,scen,Status):
        file = 'assert\\ASSERT_%s_CL%d.txt'%(scen,int(cl))
        #print file
        if os.path.exists(file):    
            FILE_OK = open(file,'r')
            #print "Path exists"
            NB_LINES = 0
            #self.msg.WriteText('CL:%d\tBranch:%s\tBand:%s\tSCENARIO:%s\tSTATUS:%s\n'%(int(cl),branch,band,scen,Status))
            for line in (FILE_OK.readlines()):#reversed
                #print "line",line
                try:
                    if re.search('DXP0 Crash Report',line) or re.search('DXP1 Crash Report',line):
                        self.msg.WriteText('\n')
                        NB_LINES = 8
                    if NB_LINES > 0:
                        if line != "":
                            NB_LINES -= 1
                            self.msg.WriteText(line)
                except:
                    pass
            FILE_OK.close()
            try:
                shutil.copy2(file,'assert\\ASSERT_%s_CL%d_x.txt'%(scen,int(cl)))
                os.remove(file)
            except:
                pass

    def Read_Status_Msg(self):
        try:
            file = 'status.txt'
            FILE_OK = open(file,'r')
            for line in (FILE_OK.readlines()):#reversed
                #print "line",line
                try:
                    Status = re.search(re.compile(r"Status:(\S+)(])"), line).group(1)
                    if Status in [STATUS_REGRESSION,STATUS_ASSERT,STATUS_ERROR]:
                        cl = re.search(re.compile(r"CL([0-9]+)"),line).group(1)
                        branch = re.search(re.compile(r"Branch:(\S+)"),line).group(1)
                        scen = re.search(re.compile(r"Test:(\S+)"), line).group(1)
                        band = re.search(re.compile(r"Band:(\S+)"),line).group(1)
                        #print "band"
                        if not self.Already_Written(int(cl),branch,band,scen,Status):
                            #print "write Text"
                            self.msg.WriteText('CL:%d Branch:%s Band:%s SCENARIO:%s STATUS:%s\n'%(int(cl),branch,band,scen,Status))
                            if Status == STATUS_ASSERT:
                                pass
                                #self.assert_info(int(cl),branch,band,scen,Status)
                except:
                    pass


            FILE_OK.close()
        except:
            pass

    def regression_thread(self):
        cl = int(self.changelist.GetValue())
        if cl != 0 :
            Regression()._run(self.branch_4test,self.band_4test,self.scenario_4test,cl)
            return

class Test_Thread(threading.Thread):
    def run(self):

        iCT = CallboxTest()
        iCT.Init_Auto(self.branch_4test,self.band_4test,self.scenario_4test)
        if self.testchoice == 0:
            print "Call Auto scheduler"
            iCT.start()
        elif self.testchoice == 1:
            iCT.Run_Branch_Test(Forced=self.force.IsChecked(),flash=self.flash.IsChecked(),Build=False,CL=self.cl)
            print "Run Test"
        elif self.testchoice == 2:
           print "No Test"



if __name__ == "__main__":
    app = wx.PySimpleApp()
    #app = wx.App()
    frame = MyForm().Show()
    app.MainLoop()