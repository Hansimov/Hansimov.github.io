# ---------------- QuadRemesher plugin for Cinema4D --------------------
# Author : Maxime Rouca

import c4d
import os
import time
import subprocess
import webbrowser
import platform
import shutil
import zipfile
import tempfile

from c4d import gui, plugins, bitmaps

# the unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1053320

__QR_plugin_version__ = "1.0.1"

g_logDebugInfo = False
g_logCrashInTextFile = False
g_enableCompare = False

g_newGUIID_index = 10000

g_QRPluginFolder = ""
g_QRExportFolder = ""
g_enginePath = ""

# to make it pre R20 compatible (by Tom Chen)
C4D_RELEASE = int(c4d.GetC4DVersion() / 1000)


def resetGUIID(startIndex):
	global g_newGUIID_index
	g_newGUIID_index = startIndex

def newGUIID() :
	global g_newGUIID_index
	g_newGUIID_index = g_newGUIID_index+1
	return g_newGUIID_index

# ---- folders ----
def unixifyPath(path):
	path = path.replace('\\', '/')
	return path

def getQRPluginFolder():
	global g_QRPluginFolder
	if (g_QRPluginFolder == ""):
		g_QRPluginFolder = os.path.dirname(os.path.realpath(__file__))
		g_QRPluginFolder = unixifyPath(g_QRPluginFolder)
		# ?? os.path.join(c4d.storage.GeGetStartupWritePath(), "plugins")
	return g_QRPluginFolder

def getQRExportFolder():
	global g_QRExportFolder
	if (g_QRExportFolder == ""):
		isMacOSX = (platform.system()=="Darwin") or (platform.system()=="macosx")
		if isMacOSX:
			QRTempFolder = "/var/tmp/Exoside"
		else:
			QRTempFolder = os.path.join(tempfile.gettempdir(), "Exoside")
		g_QRExportFolder = os.path.join(QRTempFolder, "QuadRemesher/Cinema4D")
		g_QRExportFolder = unixifyPath(g_QRExportFolder)
	return g_QRExportFolder

def getEnginePath():
	global g_enginePath
	if g_enginePath=="":
		isMacOSX = (platform.system()=="Darwin") or (platform.system()=="macosx")
		script_folder = os.path.dirname(os.path.realpath(__file__))
		if isMacOSX :
			g_enginePath = script_folder+"/QuadRemesherEngine/xremesh"
		else:
			g_enginePath = script_folder+"/QuadRemesherEngine/xremesh.exe"
	return g_enginePath


# --------- Save Load permanent string values ------------
def saveStringValue(token, value):
	#if g_logDebugInfo: print "saving "+token+"="+value
	pluginFolder = getQRPluginFolder()
	filepath = os.path.join(pluginFolder, "_"+token+".txt")
	text_file = open(filepath, "w")
	text_file.write(value)
	text_file.close()

def loadStringValue(token, errorValue=""):
	pluginFolder = getQRPluginFolder()
	filepath = os.path.join(pluginFolder, "_"+token+".txt")
	if os.path.exists(filepath):
		tmp = open(filepath, "r").read()
		#if g_logDebugInfo: print "loading "+token+ "="+tmp
		return tmp
	#if g_logDebugInfo: print "loading "+token+ ": NOT FOUND!"
	return errorValue

def saveIntValue(token, value):
	#if g_logDebugInfo: print "saving int "+token
	pluginFolder = getQRPluginFolder()
	filepath = os.path.join(pluginFolder, "_"+token+".txt")
	text_file = open(filepath, "w")
	text_file.write("%d"%value)
	text_file.close()

def loadIntValue(token, errorValue=0):
	#if g_logDebugInfo: print "loading int "+token
	pluginFolder = getQRPluginFolder()
	filepath = os.path.join(pluginFolder, "_"+token+".txt")
	if os.path.exists(filepath):
		try:
			return int(open(filepath, "r").read())
		except:
			return errorValue
	return errorValue

def saveFloatValue(token, value):
	#if g_logDebugInfo: print "saving int "+token
	pluginFolder = getQRPluginFolder()
	filepath = os.path.join(pluginFolder, "_"+token+".txt")
	text_file = open(filepath, "w")
	text_file.write("%f"%value)
	text_file.close()

def loadFloatValue(token, errorValue=0):
	#if g_logDebugInfo: print "loading int "+token
	pluginFolder = getQRPluginFolder()
	filepath = os.path.join(pluginFolder, "_"+token+".txt")
	if os.path.exists(filepath):
		try:
			return float(open(filepath, "r").read())
		except:
			return errorValue
	return errorValue




def saveAndChangeOption(previousValues, options, key, val):
	try:
		prevVal = options[key]
		if prevVal != None:
			options[key] = val
			previousValues[key] = prevVal
	except Exception:
		print(' WARNING : '+str(key)+' does not exists!')

def restoreAllSavedOptions(previousValues, options):
	for key, value in previousValues.iteritems():
		try:
			options[key] = value
		except Exception:
			print(' WARNING : '+str(key)+' does not exists! (restore)')

def cleanExportFolder(_ExportFolder):
	#return True
	#gui.MessageDialog("cleanExportFolder.....", c4d.GEMB_OK)
	for the_file in os.listdir(_ExportFolder):
		file_path = os.path.join(_ExportFolder, the_file)
		#gui.MessageDialog(file_path, c4d.GEMB_OK)
		try:
			if os.path.isfile(file_path):
				#if g_logDebugInfo: print "remove : "+file_path
				os.remove(file_path)
			# else : shutil.rmtree(file_path)
		except Exception, e:
			if g_logDebugInfo: print e

	#gui.MessageDialog("cleanExportFolder Done!", c4d.GEMB_OK)
	return True


def createExportFolder(_ExportFolder):
	try:
		if os.path.exists(_ExportFolder) == False:
			os.makedirs(_ExportFolder)
	except:
		if g_logDebugInfo: print "Can't create export folder : "+_ExportFolder
		gui.MessageDialog("Error : Can't create export folder!", c4d.GEMB_OK)
		return False

	return True


#--- Log Crash ---
def clearCrashTextFile():
	global g_logCrashInTextFile
	if g_logCrashInTextFile:
		logFilePath = os.path.join(c4d.storage.GeGetStartupWritePath(), "library/scripts/crashLog.txt")
		myfile = open(logFilePath, "w")
		myfile.close()

def logCrashTextFile(text):
	global g_logCrashInTextFile
	if g_logCrashInTextFile:
		logFilePath = os.path.join(c4d.storage.GeGetStartupWritePath(), "library/scripts/crashLog.txt")
		myfile = open(logFilePath, "a")
		myfile.write(text)
		myfile.close()






# --------------------------- Progress Bar Dialog -------------
class QRProgressDialog(c4d.gui.GeDialog):
	PROGRESSBAR_ID = 1010
	PROGRESSTEXT_ID = 1011
	BTN_Abort = 1012


	def __init__(self):
		#print "  --- ProgressDialog CTor ..."
		self.theMainWindow = None
		self.ProgressValue = 0
		self.ProgressText = ""
		return

	def __del__(self):
		#print "  ... ProgressDialog DTor ---"
		return

	# GeDialog interface:
	def CreateLayout(self):
		#print "ProgressDialog: CreateLayout ..."

		self.GroupBegin(id=1000, flags=c4d.BFH_SCALEFIT, cols=2)
		self.AddCustomGui(self.PROGRESSBAR_ID, c4d.CUSTOMGUI_PROGRESSBAR, "", c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, 0, 0)
		self.AddStaticText(self.PROGRESSTEXT_ID, flags=c4d.BFH_RIGHT, name="00.0%%")
		self.GroupEnd()

		self.AddButton(self.BTN_Abort, flags=c4d.BFH_SCALEFIT, name="中止生成网格")
		return True

	# GeDialog interface: Called when the dialog is initialized by the GUI.
	def InitValues(self):
		#print "ProgressDialog: InitValues"
		self.SetTitle("生成网格中....")
		self.SetTimer(300)
		self.__TestCounter = 0
		return True

	def stopProgress(self):
		self.SetTimer(0)

		progressMsg = c4d.BaseContainer(c4d.BFM_SETSTATUSBAR)
		progressMsg[c4d.BFM_STATUSBAR_PROGRESSON] = False
		progressMsg[c4d.BFM_STATUSBAR_PROGRESS] = 1
		self.SendMessage(self.PROGRESSBAR_ID, progressMsg)


	# GeDialog interface:
	def Timer(self, msg):
		try:
			#print("Timer called... Count=", self.__TestCounter)
			# avoid infinite loop...
			#self.__TestCounter = self.__TestCounter+1
			#if (self.__TestCounter >= 20):
			#	print "Count > 20 -> Close !!!!!!!!!!"
			#	self.Close()

			self.ProgressValue, self.ProgressText = self.theMainWindow.getRemeshingProgress()

			# Error ?
			if (self.ProgressValue < 0):
				#print "Timer: progressValue<0 -> Close()"
				self.Close()
				if (self.ProgressValue != -2):
					if self.ProgressText != None and len(self.ProgressText) > 0:
						gui.MessageDialog(self.ProgressText, c4d.GEMB_OK)
					else:
						gui.MessageDialog("An error has occured during remeshing!", c4d.GEMB_OK)
				return


			# Success ?
			if (self.ProgressValue == 2.0):
				#print "Timer: progressValue==2.0 -> RemeshIt_Finish() + Close()"
				self.theMainWindow.RemeshIt_Finish()
				self.stopProgress()
				self.Close()
				return

			# Remeshing...:
			newPBarValue = self.ProgressValue # in [0, 1]
			progressMsg = c4d.BaseContainer(c4d.BFM_SETSTATUSBAR)
			progressMsg[c4d.BFM_STATUSBAR_PROGRESSON] = True
			progressMsg[c4d.BFM_STATUSBAR_PROGRESS] = newPBarValue
			#progressMsg[c4d.BFM_STATUSBAR_TINT_COLOR] = newPBarValue
			self.SendMessage(self.PROGRESSBAR_ID, progressMsg)

			self.SetString(self.PROGRESSTEXT_ID, '%.1f %%' % (100.0*newPBarValue))

		except Exception:
			import traceback
			print("Execute Timer ERROR: " + str(traceback.format_exc()) + "\n")
			self.Close()


	# GeDialog interface:
	'''
	def Message(self, msg, result):
		if msg.GetId() == c4d.BFM_TIMER_MESSAGE:
			print "TimerMessage..."

		return gui.GeDialog.Message(self, msg, result)
		'''

	# GeDialog interface: (AskClose is called before closing, not only by user click (Window[X]+AbortButton), but also by python .Close())
	def AskClose(self):
		#print("ProgressDialog: AskClose called! (-> doAbort)")
		try:
			self.stopProgress()
			if self.ProgressValue != 2.0:				# do not call doAbort in case of RemeshingSuccess
				self.doAbort()
		except Exception:
			import traceback
			print("AskClose ERROR: " + str(traceback.format_exc()) + "\n")

		return False  # means 'OK, can be closed'


	# GeDialog interface: (DestroyWindow is called when the dialog is about to be closed temporarily, for example for layout switching.)
	#def DestroyWindow(self):
	#	print("ProgressDialog: DestroyWindow called!")

	# GeDialog interface:
	def Command(self, id, msg):
		#print("ProgressDialog: Command called id=", id)
		if id == self.BTN_Abort:
			#print("ProgressDialog: AbortButton -> Close()")
			self.Close()
			return True
		else:
			return False

	def doAbort(self):
		#print("ProgressDialog: doAbort called")
		try:
			# -- kill the remeshing process:
			if (self.theMainWindow.remeshProcess != None):
				if (self.theMainWindow.remeshProcess.poll() == None): # poll -> one means that the process has not yet terminated
					#print "Kill the remeshProcess!"
					self.theMainWindow.remeshProcess.kill()
		except Exception:
			import traceback
			print("AskClose ERROR: " + str(traceback.format_exc()) + "\n")





# --------------------------------------------------------- Main Dialog	 ----------------------------------------------
class QuadRemesherDialog(c4d.gui.GeDialog):

	BTN_LicenseManager_ID = 10050
	BTN_WebDoc_ID = 10051
	BTN_ResetOptions_ID = 10052
	BTN_RemeshIt_ID = 10053
	BTN_SetDensityColoring_ID = 10054
	BTN_DebugCompare_ID = 10056

	_UseStatusBar = False     # Use StatusBar or specific Dialog
	
	def __init__(self):
		#print "--- QRDialog CTor ..............."
		self._pluginFolder = getQRPluginFolder()

		# check installation
		if os.path.exists( self._pluginFolder ) == False:
			gui.MessageDialog("Warning: the following folder does not exist!\n"+self._pluginFolder+"\n QuadRemesher plugin may not be installed properly. \nPlease check the documentation and re-install it!", c4d.GEMB_OK)

		self._ExportFolder = getQRExportFolder()

		if self._UseStatusBar == False:
			self.progressDialog = QRProgressDialog()
			self.progressDialog.theMainWindow = self


	#def __del__(self):
	#	print "............. QRDialog DTor ---"

	# GeDialog interface:
	def CreateLayout(self):
		#print "QRDialog: createLayout..."
		#logCrashTextFile("CreateLayout 1\n");
		self.SetTitle("Quad Remesher "+__QR_plugin_version__)

		LeftColWidth = 200
		groupIndex = 11000

		resetGUIID(10000)
		self.INPUT_TargetQuadCount_StaticTextID = newGUIID()
		self.INPUT_TargetQuadCount_ID = newGUIID()
		self.INPUT_AdaptiveSize_StaticTextID = newGUIID()
		self.INPUT_AdaptiveSize_ID = newGUIID()
		self.INPUT_AdaptiveQuadCount_StaticTextID = newGUIID()
		self.INPUT_AdaptiveQuadCount_ID = newGUIID()
		self.INPUT_UseVertexColor_ID = newGUIID()
		self.INPUT_PaintedDensityCoef_StaticTextID = newGUIID()
		self.INPUT_PaintedDensityCoef_ID = newGUIID()

		self.INPUT_UseMaterials_ID = newGUIID()
		self.INPUT_UseNormals_ID = newGUIID()
		self.INPUT_DetectHardEdges_ID = newGUIID()

		self.INPUT_Symmetry_StaticTextID = newGUIID()
		self.INPUT_SymmetryX_ID = newGUIID()
		self.INPUT_SymmetryY_ID = newGUIID()
		self.INPUT_SymmetryZ_ID = newGUIID()

		self.INPUT_HideInput_ID = newGUIID()

		self.GroupBorderSpace(8, 8, 8, 8)

		groupIndex=groupIndex+1
		self.GroupBegin(groupIndex, flags=c4d.BFH_FIT, cols=2)
		self.AddStaticText(self.INPUT_TargetQuadCount_StaticTextID, flags=c4d.BFH_LEFT, initw=LeftColWidth, name="目标四边形数量")
		self.AddEditNumberArrows(self.INPUT_TargetQuadCount_ID, flags=c4d.BFH_SCALEFIT)

		self.GroupEnd()

		self.GroupSpace(20, 8)

		# ---- Quad Size Settings ----
		#self.AddSeparatorH(inith=20, flags=c4d.BFH_FIT)
		groupIndex=groupIndex+1
		self.GroupBegin(groupIndex, flags=c4d.BFH_FIT, title="四边形大小", groupflags=c4d.BFV_BORDERGROUP_FOLD2|c4d.BFV_BORDERGROUP_FOLD_OPEN, rows=4)
		self.GroupBorder(c4d.BORDER_WITH_TITLE_BOLD | c4d.BORDER_IN | c4d.BORDER_ROUND)
		self.GroupBorderSpace(8, 8, 8, 8)

		groupIndex=groupIndex+1
		self.GroupBegin(groupIndex, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, cols=2, rows=1)
		self.AddStaticText(self.INPUT_AdaptiveSize_StaticTextID, flags=c4d.BFH_LEFT, initw=LeftColWidth, name="自适应大小")
		self.AddEditSlider(self.INPUT_AdaptiveSize_ID, flags=c4d.BFH_SCALEFIT)
		self.GroupEnd()

		self.AddCheckbox(self.INPUT_AdaptiveQuadCount_ID, flags=c4d.BFH_SCALEFIT, initw=0, inith=0, name="自适应四边形数量")
		if C4D_RELEASE >= 18:  # to make it pre R18 compatible (by Tom Chen)
			self.AddCheckbox(self.INPUT_UseVertexColor_ID, flags=c4d.BFH_SCALEFIT, initw=0, inith=0, name="使用顶点颜色")

		groupIndex=groupIndex+1
		self.GroupBegin(groupIndex, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, cols=3, rows=1, title="title2")
		self.AddStaticText(self.INPUT_PaintedDensityCoef_StaticTextID, flags=c4d.BFH_LEFT, initw=LeftColWidth, name="四边形密度(绘制)")
		self.AddEditSlider(self.INPUT_PaintedDensityCoef_ID, flags=c4d.BFH_SCALEFIT)
		self.AddButton(self.BTN_SetDensityColoring_ID, flags=c4d.BFH_FIT|c4d.BFH_RIGHT, name="P")
		self.GroupEnd()

		self.GroupEnd() # quads sizing

		# ---- Edge Loops Control ----
		groupIndex=groupIndex+1
		self.GroupBegin(groupIndex, flags=c4d.BFH_FIT, title="循环边控制", groupflags=c4d.BFV_BORDERGROUP_FOLD2|c4d.BFV_BORDERGROUP_FOLD_OPEN, rows=3)
		self.GroupBorder(c4d.BORDER_WITH_TITLE_BOLD | c4d.BORDER_IN | c4d.BORDER_ROUND)
		self.GroupBorderSpace(8, 8, 8, 8)

		self.AddCheckbox(self.INPUT_UseMaterials_ID, c4d.BFH_SCALEFIT, 0, 0, "使用材质")

		self.AddCheckbox(self.INPUT_UseNormals_ID, c4d.BFH_SCALEFIT, 0, 0, "使用法线分割/切断")

		self.AddCheckbox(self.INPUT_DetectHardEdges_ID, c4d.BFH_SCALEFIT, 0, 0, "角度检测硬边")

		self.GroupEnd() # edge loops control

		# ---- Misc ----
		groupIndex=groupIndex+1
		self.GroupBegin(groupIndex, flags=c4d.BFH_SCALEFIT, title="其他", groupflags=c4d.BFV_BORDERGROUP_FOLD2|c4d.BFV_BORDERGROUP_FOLD_OPEN, rows=3)
		self.GroupBorder(c4d.BORDER_WITH_TITLE_BOLD | c4d.BORDER_IN | c4d.BORDER_ROUND)
		self.GroupBorderSpace(8, 8, 8, 8)

		groupIndex=groupIndex+1
		self.GroupBegin(groupIndex, flags=c4d.BFH_SCALEFIT, cols=4)
		self.AddStaticText(self.INPUT_Symmetry_StaticTextID, flags=c4d.BFH_LEFT, initw=LeftColWidth, name="对称")
		self.AddCheckbox(self.INPUT_SymmetryX_ID, flags=c4d.BFH_SCALEFIT, initw=0, inith=0, name="X")
		self.AddCheckbox(self.INPUT_SymmetryY_ID, flags=c4d.BFH_SCALEFIT, initw=0, inith=0, name="Y")
		self.AddCheckbox(self.INPUT_SymmetryZ_ID, flags=c4d.BFH_SCALEFIT, initw=0, inith=0, name="Z")
		self.GroupEnd()
		
		self.AddCheckbox(self.INPUT_HideInput_ID, c4d.BFH_SCALEFIT, 0, 0, "隐藏源始对象")

		#self.AddSeparatorH(inith=5)

		groupIndex=groupIndex+1
		self.GroupBegin(groupIndex, flags=c4d.BFH_SCALEFIT, cols=3)
		self.AddButton(self.BTN_LicenseManager_ID, flags=c4d.BFH_SCALEFIT, name="许可证管理器")
		self.AddButton(self.BTN_WebDoc_ID, flags=c4d.BFH_SCALEFIT, name="C4D中文站")
		self.AddButton(self.BTN_ResetOptions_ID, flags=c4d.BFH_SCALEFIT, name="重置选项")
		self.GroupEnd()

		self.GroupEnd() # misc

		# --- Remesh It Button---
		self.GroupSpace(20, 8)

		self.AddButton(self.BTN_RemeshIt_ID, flags=c4d.BFH_SCALEFIT, inith=20, name="<<   开始拓补   >>")

		global g_enableCompare
		if g_enableCompare:
			self.AddButton(self.BTN_DebugCompare_ID, flags=c4d.BFH_SCALEFIT, inith=20, name="Compare")
		
		# set default values
		self.resetTempValues()
		
		# load previously saved options
		self.loadAllTempValuesFromDisk()
		
		# setup all optiosn (using TempValues)
		self.setupAllOptions(True)
		

		return True

	# GeDialog interface: (DestroyWindow is called when the dialog is about to be closed temporarily, for example for layout switching.)
	#def DestroyWindow(self):
	#	print("QRDialog: DestroyWindow called!")


	def doDebugCompare(self):
		import subprocess
		script_folder = os.path.dirname(os.path.realpath(__file__))
		doc = c4d.documents.GetActiveDocument()

		initialObj = doc.GetActiveObject()
		c4d.CallCommand(100004820) # Copy
		c4d.CallCommand(100004821) # Paste
	    
		subprocess.call([script_folder+'/__SwitchToOld.bat'])
		print("Before Remesh OLD : ActiveObj="+doc.GetActiveObject().GetName())
		self.RemeshIt()
		print("After Remesh OLD : ActiveObj="+doc.GetActiveObject().GetName())
		oldRetopo = doc.GetActiveObject()
		doc.GetActiveObject().SetName("OLD_Retopo")
		
		subprocess.call([script_folder+'/__SwitchToNew.bat'])
		doc.SetActiveObject(initialObj)
		print("Before Remesh NEW : ActiveObj="+doc.GetActiveObject().GetName())
		self.RemeshIt()
		print("After Remesh NEW : ActiveObj="+doc.GetActiveObject().GetName())
		newRetopo = doc.GetActiveObject()
		doc.GetActiveObject().SetName("NEW_Retopo")
		
		# Hide New Retopo + make an offset clone
		newRetopoCopy = newRetopo.GetClone()
		#doc.InsertObject(newRetopoCopy)
		newRetopoCopy.InsertAfter(newRetopo)
		newRetopoCopy.SetName("OFFSET_"+newRetopo.GetName())

		#newRetopo[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1   # green=0  red=1   gray=2
		#newRetopo[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1
					
		relPos = newRetopoCopy.GetRelPos()
		print("Offset : x=%f"%(relPos[0]))
		relPos = relPos + c4d.Vector(newRetopoCopy.GetRad()[0] * 2.2, 0, 0)
		print(" ->  %f   rad=%f"%(relPos[0], newRetopoCopy.GetRad()[0]))
		newRetopoCopy.SetRelPos(relPos)
		
		# select both retopo
		doc.SetActiveObject(oldRetopo)
		doc.SetActiveObject(newRetopoCopy, c4d.SELECTION_ADD)
		doc.SetActiveObject(newRetopo, c4d.SELECTION_ADD)
		# show edges : 
		c4d.CallCommand(16351) # Edges
		


	# ------------------ main REMESH IT func ------------
	def RemeshIt(self) :
		
		self.saveAllOptionsToDisk()
		
		#logCrashTextFile("RemeshIt\n");
		if g_logDebugInfo: print "RemeshIt..."
		doc = c4d.documents.GetActiveDocument()

		# ---- save things for next usage --- TODO...

		# set paths :
		export_path = getQRExportFolder()
		settingsFilename = os.path.join(export_path, 'RetopoSettings.txt')
		inputFilename = os.path.join(export_path, 'inputMesh.fbx')
		self.retopoFilename = os.path.join(export_path, 'retopo.fbx')
		self.progressFilename = os.path.join(export_path, 'progress.txt')


		# ---- create folders ----
		if createExportFolder(self._ExportFolder) == False:
			gui.MessageDialog("Error: Cannot create 'Export' Folder!", c4d.GEMB_OK)
			return False
		if cleanExportFolder(self._ExportFolder) == False:
			gui.MessageDialog("Error: Cannot clean 'Export' Folder!", c4d.GEMB_OK)
			return False

		# --- check selection ---
		if (len(doc.GetActiveObjects(0)) > 1):
			gui.MessageDialog("错误: 只能选择一个需要拓补的对象!", c4d.GEMB_OK)
			return False
		if (len(doc.GetActiveObjects(0)) == 0):
			gui.MessageDialog("错误: 必须选择一个需要拓补的对象!", c4d.GEMB_OK)
			return False

		# ---- save in FBX file ----
		# https://developers.maxon.net/docs/Cinema4DCPPSDK/html/group___s_a_v_e_d_o_c_u_m_e_n_t_f_l_a_g_s.html

		# Retrieves FBX exporter plugin, 1026370
		fbxExportId = 1026370
		plug = c4d.plugins.FindPlugin(fbxExportId, c4d.PLUGINTYPE_SCENESAVER)
		if plug is None:
			return False

		data = dict()
		# Sends MSG_RETRIEVEPRIVATEDATA to fbx export plugin
		if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data):
			return False

		# BaseList2D object stored in "imexporter" key hold the settings
		fbxExport = data.get("imexporter", None)
		if fbxExport is None:
			return False

		# Defines FBX export settings (see: https://developers.maxon.net/docs/Cinema4DCPPSDK/html/_ffbxexport_8h.html)
		previousValues = {}
		if c4d.GetC4DVersion() >= 17048:  # to make it pre R17.048 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_FBX_VERSION, c4d.FBX_EXPORTVERSION_7_4_0 )
		elif C4D_RELEASE >= 15:  # to make it pre R15 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_FBX_VERSION, c4d.FBX_EXPORTVERSION_7_3_0 )
		else:  # to make it pre R15 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_FBX_VERSION, c4d.FBX_EXPORTVERSION_NATIVE )
		saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_ASCII, False)

		# general
		if C4D_RELEASE >= 19:  # to make it pre R19 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_SELECTION_ONLY, True)
		saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_SCALE, 1.0)
		if C4D_RELEASE >= 16:  # to make it pre R16 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_LIGHTS, False)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_CAMERAS, False)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_SPLINES, False)
		if C4D_RELEASE >= 19:  # to make it pre R19 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_GLOBAL_MATRIX, False)  # Important !!! (see Remove+InsertAfter below)
		# geometry
		saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_SAVE_NORMALS, True)
		if C4D_RELEASE >= 18:  # to make it pre R18 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_SAVE_VERTEX_COLORS, True)
		if C4D_RELEASE >= 16:  # to make it pre R16 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_SAVE_VERTEX_MAPS_AS_COLORS, False)
		if C4D_RELEASE >= 19:  # to make it pre R19 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_LOD_SUFFIX, False)
		if C4D_RELEASE >= 16:  # to make it pre R16 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_TRIANGULATE, False)
		# animation
		if C4D_RELEASE >= 16:  # to make it pre R16 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_TRACKS, False)
		saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_BAKE_ALL_FRAMES, False)
		saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_PLA_TO_VERTEXCACHE, False)
		# additional
		saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_TEXTURES, True)  # == Materials ??
		saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_EMBED_TEXTURES, False)
		if C4D_RELEASE >= 20:  # to make it pre R20 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_FLIP_Z_AXIS, False)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_UP_AXIS, c4d.FBXEXPORT_UP_AXIS_Y)
		if C4D_RELEASE >= 18:  # to make it pre R18 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_SUBSTANCES, False)
		# others...
		saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_GROUP, False)
		if C4D_RELEASE >= 16:  # to make it pre R16 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_GRP_GENERAL, False)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_GRP_TEXTURES, False)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_GRP_DEBUG, False)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_GRP_GEOMETRY, False)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_GRP_ANIMATION, False)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_GRP_ADDITIONAL, False)
		saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_CLONE_OBJECTS, False)
		if C4D_RELEASE >= 20:  # to make it pre R20 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_INSTANCES, False)
		if C4D_RELEASE >= 18:  # to make it pre R18 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_SDS, False)  # ?????? a tester ca exporte la control cage ???
		if C4D_RELEASE >= 16:  # to make it pre R16 compatible (by Tom Chen)
			saveAndChangeOption(previousValues, fbxExport, c4d.FBXEXPORT_SDS_SUBDIVISION, False)


		# Finally export the document
		workOnClone = True   # Work On clone because FBXEXPORT_SELECTION_ONLY was not available before R19
		if workOnClone:
			tmpDoc = c4d.documents.BaseDocument()
			inputObj = doc.GetActiveObject()
			tmpDoc.InsertObject(inputObj.GetClone())
			exportOK = c4d.documents.SaveDocument(tmpDoc, inputFilename, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, fbxExportId)
			tmpDoc = None
		else:
			exportOK = c4d.documents.SaveDocument(doc, inputFilename, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, fbxExportId)

		# restore exportOptions
		restoreAllSavedOptions(previousValues, fbxExport)

		if not exportOK:
			gui.MessageDialog("Error: Cannot export the selected mesh as FBX file!", c4d.GEMB_OK)
			return False

		# ----- write settings file ----
		settingsFilename = os.path.join(self._ExportFolder, "RemeshSettings.txt")
		settingsFilename = unixifyPath(settingsFilename)
		settings_file = open(settingsFilename, "w")
		settings_file.write('HostApp=Cinema4D\n')
		settings_file.write('FileIn="%s"\n' % inputFilename)
		settings_file.write('FileOut="%s"\n' % self.retopoFilename)
		settings_file.write('ProgressFile="%s"\n' % self.progressFilename)

		if C4D_RELEASE >= 15:  # to make it pre R15 compatible (by Tom Chen)
			settings_file.write("TargetQuadCount=%d\n" % int(self.GetFloat(self.INPUT_TargetQuadCount_ID)))
			settings_file.write("CurvatureAdaptivness=%f\n" % (100.0 * self.GetFloat(self.INPUT_AdaptiveSize_ID)))
		else:
			settings_file.write("TargetQuadCount=%d\n" % int(self.GetReal(self.INPUT_TargetQuadCount_ID)))
			settings_file.write("CurvatureAdaptivness=%f\n" % (100.0 * self.GetReal(self.INPUT_AdaptiveSize_ID)))
		settings_file.write("ExactQuadCount=%d\n" % (not self.GetBool(self.INPUT_AdaptiveQuadCount_ID)))

		settings_file.write("UseVertexColorMap=%d\n" % self.GetBool(self.INPUT_UseVertexColor_ID))

		#settings_file.write("UsePolygonGroups=%d\n" % self.GetBool(self.???))  # Polygon Group and PolygonSelTag are not exported
		#settings_file.write("UseHardEdgeFlags=%d\n" % self.GetBool(self.???))  # not exported in FBX
		settings_file.write("UseMaterialIds=%d\n" % self.GetBool(self.INPUT_UseMaterials_ID))
		settings_file.write("UseIndexedNormals=%d\n" % self.GetBool(self.INPUT_UseNormals_ID))
		settings_file.write("AutoDetectHardEdges=%d\n" % self.GetBool(self.INPUT_DetectHardEdges_ID))

		symAxisText = ''
		if self.GetBool(self.INPUT_SymmetryX_ID): symAxisText = symAxisText + 'X'
		if self.GetBool(self.INPUT_SymmetryY_ID): symAxisText = symAxisText + 'Y'
		if self.GetBool(self.INPUT_SymmetryZ_ID): symAxisText = symAxisText + 'Z'
		if symAxisText != '':
			settings_file.write('SymAxis=%s\n' % symAxisText)
			settings_file.write("SymLocal=1\n")

		settings_file.close()

		# ----- start remesher engine -----
		try:
			if (os.path.isfile(self.retopoFilename)):
				os.remove(self.retopoFilename)
			if (os.path.isfile(self.progressFilename)):
				os.remove(self.progressFilename)

			enginePath = getEnginePath()
			self.remeshProcess = subprocess.Popen([enginePath, "-s", settingsFilename])   #NB: Popen automatically add quotes around parameters when there are SPACES inside

		except Exception:
			import traceback
			print("Execute remesher ERROR: " + str(traceback.format_exc()) + "\n")
			return

		# --- start progress window ---
		self.StartRemeshingTime = time.time()
 		if self._UseStatusBar:
 			c4d.StatusClear()
 			c4d.StatusSetText("Remeshing...")
 			c4d.StatusSetBar(0)

			self.RemeshIt_UpdateProgressLoop()
			
 		else:
			#self.progressDialog = QRProgressDialog()
			#self.progressDialog.theMainWindow = self
			#self.progressDialog.Open(dlgtype=c4d.DLG_TYPE_MODAL, pluginid=PLUGIN_ID, xpos=-2, ypos=-2)
			self.progressDialog.Open(dlgtype=c4d.DLG_TYPE_MODAL, pluginid=0, xpos=-2, ypos=-2) # il ne faut surtout pas mettre pluginid!!!
			# (-2 means center of screen)
			
			
	def EscapePressed(self):
		bc = c4d.BaseContainer()
		rs = c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
		if rs and bc[c4d.BFM_INPUT_VALUE]:
			return True
		return False
	
	def RemeshIt_UpdateProgressLoop(self):
		sleepTime = 0.35
		try:
			while True:
				
				time.sleep(sleepTime)  # time in seconds
			
				ProgressValue, ProgressText = self.getRemeshingProgress()

				# Error ?
				if (ProgressValue < 0):
					if (ProgressText != None and len(ProgressText)>0):
						gui.MessageDialog(ProgressText, c4d.GEMB_OK)
					else:
						gui.MessageDialog("An error has occured during remeshing!", c4d.GEMB_OK)
					c4d.StatusClear()
					return ProgressValue

				# Success ?
				if (ProgressValue == 2.0):
					self.RemeshIt_Finish()
					c4d.StatusClear()
					return 2

				# Abort ?
				if self.EscapePressed():
					c4d.StatusClear()
					return -10

				# Remeshing...:
#				print("StatusSetBar(%f)" % (100.0*ProgressValue))
				c4d.StatusSetText('Remeshing... (%.1f %%)' % (100.0*ProgressValue))
				c4d.StatusSetBar(100.0*ProgressValue)
				
		except Exception:
			import traceback
			print("exception in RemeshIt_UpdateProgressLoop: " + str(traceback.format_exc()) + "\n")
			gui.MessageDialog("An exception has occured during remeshing!", c4d.GEMB_OK)
			
		return -20


	# returns (progressValue, progressMsg)
	def getRemeshingProgress(self):

		# ---- Wait for result ----
		CurTimeFromStart = time.time() - self.StartRemeshingTime

		# -- read progress file:
		progressLines=[]
		try:
			pf = open(self.progressFilename, "r")
			progressLines = pf.read().splitlines()
			pf.close()
		except Exception:
			if CurTimeFromStart>2 :  # after 2 seconds without progressFile...
				print(' WARNING : no progressFile....')
				return 0, ""
			if CurTimeFromStart>40 :  # after 40 seconds without progressFile...
				print(' ERROR : no progressFile after 40 sec....')
				return -10, ""

		if len(progressLines)>=1:
			try:
				ProgressValueFloat = float(progressLines[0])
			except Exception:
				print(' error in progressbar... line[0]='+str(progressLines[0]))
				return 0, ""

			ProgressText = ""
			try:
				if len(progressLines)>=2:
					ProgressText = progressLines[1]
			except Exception:
				print(' warning in progressbar...')

			if ProgressValueFloat != None:
				# -- error ?
				if (ProgressValueFloat < 0):
					return ProgressValueFloat, ProgressText

				# -- Succeded ?
				if ProgressValueFloat == 2:
					return ProgressValueFloat, ProgressText

				# -- currently remeshing
				if (ProgressValueFloat >= 0 and ProgressValueFloat <= 1.0):
					# update sleepTime
					#if CurTimeFromStart >= 1 and ProgressValueFloat < 0.6:  # in middle of long process... check less often
					#	sleepTime = 0.4
					#if ProgressValueFloat > 0.7 and CurTimeFromStart < 15:  # approaching end of Progress... check more often
					#	sleepTime = 0.1

					return ProgressValueFloat, ProgressText


		# check process is running: if not and noProgressFile, this means that the process has crashed
		# NB: poll -> None means that the process hasn't terminated yet.
		if (self.remeshProcess.poll() != None):
			return -3, "Remeshing Failed! (-3)"

		print "strange case..."
		return 0, ""

	# After retopo success : Finish = import the retopo
	def RemeshIt_Finish(self):
		try:
			doc = c4d.documents.GetActiveDocument()

			# - get the importer
			plug = plugins.FindPlugin(1026369, c4d.PLUGINTYPE_SCENELOADER)
			if plug is None:
				return False
			op = {}
			if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, op):
				return False
			fbximport = op["imexporter"]
			if fbximport is None:
				return False

			# check retopoFile exists
			if os.path.exists(self.retopoFilename) == False:
				return False
		except Exception:
			import traceback
			print("exception in RemeshIt_Finish_A: " + str(traceback.format_exc()) + "\n")
			return False

		# ---- now we can apply changes in the scene
		try:
			doc.StartUndo()

			# - make input invisible -
			inputObj = doc.GetActiveObject()
			if self.GetBool(self.INPUT_HideInput_ID):
				if inputObj:
					#doc.AddUndo(c4d.UNDOTYPE_BITS, inputObj)
					doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, inputObj)

					inputObj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1   # green=0  red=1   gray=2
					inputObj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1

			# ---- import retopo ----
			# - Define the import settings (see https://developers.maxon.net/docs/Cinema4DCPPSDK/html/_ffbximport_8h.html)
			previousValues = {}

			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_GROUP, False)
			if C4D_RELEASE >= 16:  # to make it pre R16 compatible (by Tom Chen)
				saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_GRP_GENERAL, False)		# ??
				saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_GRP_ADDITIONAL, False)		# ??

			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_SCALE, 1.0)
			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_GEOMETRY, True)

			if C4D_RELEASE >= 16:  # to make it pre R16 compatible (by Tom Chen)
				saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_GRP_GEOMETRY, True)
			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_CAMERAS, False)
			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_LIGHTS, False)
			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_MARKERS, False)
			if C4D_RELEASE >= 16:  # to make it pre R16 compatible (by Tom Chen)
				saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_TRACKS, False)
			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_TEXTURES, False)
			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_SHAPES, True)
			if C4D_RELEASE >= 16:  # to make it pre R16 compatible (by Tom Chen)
				saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_CURVES, False)
			if C4D_RELEASE >= 18:  # to make it pre R18 compatible (by Tom Chen)
				saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_COLORS, False)  # A voir...
				saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_SDS, False)
				saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_SUBSTANCES, False)
			if C4D_RELEASE >= 20:  # to make it pre R20 compatible (by Tom Chen)
				saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_INSTANCES, False)

			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_NORMALS, False)  # A VOIR ....
			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_ACTIVATE_JOINTS, True)
			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_KEEP_JOINT_REST_POSE, True)
			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_USE_CURRENT_POSE, True)
			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_CLEAN_TRACKS, True)
			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_CONVERT_TO_PHONGTAG, True)
			saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_VERTEXCACHE_TO_PLA, True)
			if C4D_RELEASE >= 16:  # to make it pre R16 compatible (by Tom Chen)
				saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_SINGLE_MAT_SELECTIONTAGS, True)
				saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_GRP_ANIMATION, True)

			if C4D_RELEASE >= 20:  # to make it pre R20 compatible (by Tom Chen)
				saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_FLIP_Z_AXIS, False)
				saveAndChangeOption(previousValues, fbximport, c4d.FBXIMPORT_UP_AXIS, c4d.FBXIMPORT_UP_AXIS_Y)

			# - import	(retopo will be selected automatically)
			c4d.documents.MergeDocument(doc, self.retopoFilename, c4d.SCENEFILTER_OBJECTS, None)
			retopoObj = doc.GetActiveObject()

			#restore fbx import options:
			restoreAllSavedOptions(previousValues, fbximport)

			doc.AddUndo(c4d.UNDOTYPE_NEW, retopoObj)
			
			# place the retopo in the inputObject's parent just after the inputObject
			# NB: it seems that these operations do not need specific AddUndo... 
			if inputObj.GetNext() != retopoObj:
				# NB: as Remove+Insert will not do any specific operations on the matrices, it's important to have FBXEXPORT_GLOBAL_MATRIX=False
				retopoObj.Remove()
				retopoObj.InsertAfter(inputObj)
			
			doc.EndUndo()

			if c4d.GetC4DVersion() >= 17032:  # to make it pre R17.032 compatible (by Tom Chen)
				c4d.EventAdd(flags=c4d.EVENT_ENQUEUE_REDRAW)
			else:
				c4d.EventAdd()

		except Exception:
			doc.EndUndo()
			import traceback
			print("exception in RemeshIt_Finish: " + str(traceback.format_exc()) + "\n")
			return False

		return True
		
	def saveAllOptionsToVars(self) :
		try:
			if C4D_RELEASE >= 15:
				self._TargetQuadCount = self.GetFloat(self.INPUT_TargetQuadCount_ID)
				self._AdaptiveSize = self.GetFloat(self.INPUT_AdaptiveSize_ID)
				print("saveAllOptionsToVars : _AdaptiveSize = %f"%(self._AdaptiveSize))
				self._PaintedDensityCoef = self.GetFloat(self.INPUT_PaintedDensityCoef_ID)
			else:
				self._TargetQuadCount = self.GetReal(self.INPUT_TargetQuadCount_ID)
				self._AdaptiveSize = self.GetReal(self.INPUT_AdaptiveSize_ID)
				self._PaintedDensityCoef = self.GetReal(self.INPUT_PaintedDensityCoef_ID)
			
			self._AdaptiveQuadCount = self.GetBool(self.INPUT_AdaptiveQuadCount_ID)
			self._UseVertexColor = self.GetBool(self.INPUT_UseVertexColor_ID)
			
			self._UseMaterials = self.GetBool(self.INPUT_UseMaterials_ID)
			self._UseNormals = self.GetBool(self.INPUT_UseNormals_ID)
			self._DetectHardEdges = self.GetBool(self.INPUT_DetectHardEdges_ID)
			
			self._SymmetryX = self.GetBool(self.INPUT_SymmetryX_ID)
			self._SymmetryY = self.GetBool(self.INPUT_SymmetryY_ID)
			self._SymmetryZ = self.GetBool(self.INPUT_SymmetryZ_ID)

			self._HideInput = self.GetBool(self.INPUT_HideInput_ID)

		except Exception:
			print("Warning : exception in saveAllOptionsToVars")
			return


	def saveIntOptionFromID(self, id):
		try:
			guiId = getattr(self, 'INPUT_'+id+'_ID')
			if C4D_RELEASE >= 15:
				val = self.GetFloat(guiId)
			else:
				val = self.GetReal(guiId)
			saveIntValue(id, val)
		except Exception:
			print("Warning : exception in saveIntOptionFromID "+id)

	def saveFloatOptionFromID(self, id):
		try:
			guiId = getattr(self, 'INPUT_'+id+'_ID')
			if C4D_RELEASE >= 15:
				val = self.GetFloat(guiId)
			else:
				val = self.GetReal(guiId)
			saveFloatValue(id, val)
		except Exception:
			print("Warning : exception in saveFloatOptionFromID "+id)

	def loadIntValueFromID(self, id):
		try:
			varname = '_'+id
			prevValue = getattr(self, varname)
			newValue = loadIntValue(id, prevValue)
			setattr(self, varname, newValue)
		except Exception:
			print("Warning : exception in loadIntValueFromID "+id)
			#import traceback
			#print(str(traceback.format_exc()) + "\n")

	def loadFloatValueFromID(self, id):
		try:
			varname = '_'+id
			prevValue = getattr(self, varname)
			newValue = loadFloatValue(id, prevValue)
			#print("loadFloatValueFromID : %s -> %f   prev=%f"%(id, newValue, prevValue))
			setattr(self, varname, newValue)
		except Exception:
			print("Warning : exception in loadFloatValueFromID "+id)
			#import traceback
			#print(str(traceback.format_exc()) + "\n")

	def saveAllOptionsToDisk(self):
		try:
			self.saveIntOptionFromID('TargetQuadCount')
			self.saveFloatOptionFromID('AdaptiveSize')
			self.saveIntOptionFromID('AdaptiveQuadCount')
			self.saveIntOptionFromID('UseVertexColor')
			self.saveFloatOptionFromID('PaintedDensityCoef')

			self.saveIntOptionFromID('UseMaterials')
			self.saveIntOptionFromID('UseNormals')
			self.saveIntOptionFromID('DetectHardEdges')

			self.saveIntOptionFromID('SymmetryX')
			self.saveIntOptionFromID('SymmetryY')
			self.saveIntOptionFromID('SymmetryZ')

			self.saveIntOptionFromID('HideInput')
		
		except Exception:
			print("Warning : exception in saveAllOptionsToDisk")
			#import traceback
			#print(str(traceback.format_exc()) + "\n")
			return

	def loadAllTempValuesFromDisk(self) :
		try:
			self.loadIntValueFromID('TargetQuadCount')
			self.loadFloatValueFromID('AdaptiveSize')
			self.loadIntValueFromID('AdaptiveQuadCount')
			self.loadIntValueFromID('UseVertexColor')
			self.loadFloatValueFromID('PaintedDensityCoef')

			self.loadIntValueFromID('UseMaterials')
			self.loadIntValueFromID('UseNormals')
			self.loadIntValueFromID('DetectHardEdges')

			self.loadIntValueFromID('SymmetryX')
			self.loadIntValueFromID('SymmetryY')
			self.loadIntValueFromID('SymmetryZ')

			self.loadIntValueFromID('HideInput')
			
		except Exception:
			print("Warning : exception in loadAllTempValuesFromDisk")
			#import traceback
			#print(str(traceback.format_exc()) + "\n")
			return


	def doWebDoc(self) :
		try:
			webbrowser.open('http://www.c4dcn.cn/')
		except Exception:
			retYesNo = gui.MessageDialog("Error : cannot open web page!", c4d.GEMB_OK)

	# NB: temp value : { either set to default, or read from disk } -> used to init all UI settings
	def resetTempValues(self):
		self._TargetQuadCount = 5000
		self._AdaptiveSize = 0.5
		self._PaintedDensityCoef = 1.0
		self._AdaptiveQuadCount = False
		self._UseVertexColor = False
		self._UseMaterials = False
		self._UseNormals = False
		self._DetectHardEdges = True
		self._SymmetryX = False
		self._SymmetryY = False
		self._SymmetryZ = False
		
		self._HideInput = True

	# Init all options: min, max.. + using TempValues
	def setupAllOptions(self, silentError) :
		try:
			# NB: TAKE CARE
			#  self.SetFloat(id=XXX_ID, value=50.0, min=0, max=100)
			#  self.SetFloat(id=XXX_ID, value=51) -> this will reset the min and max !!!!!

			if c4d.GetC4DVersion() >= 15037:  # to make it pre R15.037 compatible (by Tom Chen)
				self.SetFloat(id=self.INPUT_TargetQuadCount_ID, value=self._TargetQuadCount, min=6, max=1000000, step=20, format=c4d.FORMAT_INT, quadscale=True)
				self.SetFloat(id=self.INPUT_AdaptiveSize_ID, value=self._AdaptiveSize, min=0.0, max=1.0, step=0.01, format=c4d.FORMAT_PERCENT)
				self.SetFloat(id=self.INPUT_PaintedDensityCoef_ID, value=self._PaintedDensityCoef, min=0.25, max=4.0, step=0.01, format=c4d.FORMAT_FLOAT, quadscale=True)
			else:
				# to make it pre R15.037 compatible (by Tom Chen)
				self.SetReal(id=self.INPUT_TargetQuadCount_ID, value=5000, min=6, max=1000000, step=20, format=c4d.FORMAT_LONG, quadscale=True)
				self.SetReal(id=self.INPUT_AdaptiveSize_ID, value=0.5, min=0.0, max=1.0, step=0.01, format=c4d.FORMAT_PERCENT)
				self.SetReal(id=self.INPUT_PaintedDensityCoef_ID, value=1.0, min=0.25, max=4.0, step=0.01, format=c4d.FORMAT_REAL, quadscale=True)

			self.SetBool(id=self.INPUT_AdaptiveQuadCount_ID, value=self._AdaptiveQuadCount)
			self.SetBool(id=self.INPUT_UseVertexColor_ID, value=self._UseVertexColor)
			self.SetBool(id=self.INPUT_UseMaterials_ID, value=self._UseMaterials)
			self.SetBool(id=self.INPUT_UseNormals_ID, value=self._UseNormals)
			self.SetBool(id=self.INPUT_DetectHardEdges_ID, value=self._DetectHardEdges)
			self.SetBool(id=self.INPUT_SymmetryX_ID, value=self._SymmetryX)
			self.SetBool(id=self.INPUT_SymmetryY_ID, value=self._SymmetryY)
			self.SetBool(id=self.INPUT_SymmetryZ_ID, value=self._SymmetryZ)
			self.SetBool(id=self.INPUT_HideInput_ID, value=self._HideInput)
			
		except Exception:
			if silentError==False:
				retYesNo = gui.MessageDialog("Error : cannot reset options!", c4d.GEMB_OK)
			import traceback
			print(str(traceback.format_exc()) + "\n")

	def doResetOptions(self) :
		self.resetTempValues()
		self.setupAllOptions(False)
		self.saveAllOptionsToDisk()
		

	def doLicMgr(self):
		try:
			script_folder = os.path.dirname(os.path.realpath(__file__))
			isMacOSX = (platform.system()=="Darwin") or (platform.system()=="macosx")
			if isMacOSX :
				licenseManagerPath = script_folder+"/QuadRemesherEngine/xrLicenseManager.app/Contents/MacOS/xrLicenseManager"
			else:
				licenseManagerPath = script_folder+"/QuadRemesherEngine/xrLicenseManager.exe"
			licenseManagerPath = unixifyPath(licenseManagerPath)
		except Exception:
			gui.MessageDialog("Error while setting LicenseManager path!", c4d.GEMB_OK)
			return

		# 2 - launch licenseManager
		try:
			subprocess.Popen([licenseManagerPath, "-hostApp", "Cinema4D"])
		except Exception:
			gui.MessageDialog("Exception: while launching LicenseManager.... (" + str(licenseManagerPath) + ")", c4d.GEMB_OK)
			return

	def getColorFromDensityCoef(self, vertexColorSliderValue):
		color = c4d.Vector()
		try:
			maxSliderValue = 4
			minSliderValue = 0.25
			normalizedValue = 0.0
			if vertexColorSliderValue > 1.0:
				normalizedValue = (vertexColorSliderValue - 1.0) / (maxSliderValue - 1.0)
			elif vertexColorSliderValue < 1.0:
				normalizedValue =  - ((1.0/vertexColorSliderValue) - 1.0) / ((1.0/minSliderValue) - 1.0)

			if (normalizedValue > 1):
				normalizedValue = 1
			if (normalizedValue < -1):
				normalizedValue = -1

			# -- normalizedValue to color
			r = 1.0
			g = 1.0
			b = 1.0
			if normalizedValue > 0.0:
				r = 1
				g = 1-normalizedValue
				b = 1-normalizedValue
			elif normalizedValue < 0.0:
				r = 1+normalizedValue
				g = 1
				b = 1
			color.x = r
			color.y = g
			color.z = b
		except Exception:
			return color
		return color

	def setDensityColoring(self):
		def tool():
			doc = c4d.documents.GetActiveDocument()
			return c4d.plugins.FindPlugin(doc.GetAction(), c4d.PLUGINTYPE_TOOL)

		doc = c4d.documents.GetActiveDocument()

		# init the VertexColor Map in white if none.
		# BaseTag : https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d/C4DAtom/GeListNode/BaseList2D/BaseTag/index.html#c4d.BaseTag
		# VertexColorTag : https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d/C4DAtom/GeListNode/BaseList2D/BaseTag/VariableTag/VertexColorTag/index.html
		# GetPointCount work only on EditableMeshs ... not on base Sphere,Cylinder....
		# To be able to paint on object -> must do 'Make Editable'
		obj = doc.GetActiveObject()
		if obj == None:
			return False

		vct = obj.GetTag(c4d.Tvertexcolor)   # find existing vertex color map
		if vct == None:
			try:
				# Enter Paint Tool:
				c4d.CallCommand(1021286, 1021286) # enter Paint Tool
				tool()[c4d.ID_CA_PAINT_TOOL_MAINMODE] = 1  # Set Paint Mode = Vertex Color

				polycount = obj.GetPolygonCount()
				pointcount = obj.GetPointCount()
				vct = c4d.VertexColorTag(pointcount)
				vct.SetPerPointMode(True)

				# init with white
				#data = vct.GetDataAddressW()
				#white = c4d.Vector4d(1.0, 1.0, 1.0, 1.0)
				#for i in xrange(pointcount):
				#  c4d.VertexColorTag.SetPoint(data, None, None, i, white)
				obj.InsertTag(vct)
				doc.SetActiveTag(vct)

				# init with white
				defColor = c4d.Vector(1,1,1)
				tool()[c4d.ID_CA_PAINT_TOOL_VERTEXCOLOR] = defColor
				c4d.CallButton(tool(), c4d.ID_CA_PAINT_TOOL_APPLY_ALL)

			except Exception:
				import traceback
				print("exception in setDensityColoring: " + str(traceback.format_exc()) + "\n")
				retYesNo = gui.MessageDialog("Error : cannot create VertexColor Tag!\n (Maybe need to convert to Editable)", c4d.GEMB_OK)
				return False
		else:
			doc.SetActiveTag(vct) # select this vertex color tag so that the Paint tool will paint in it.

			# Enter Paint Tool:
			c4d.CallCommand(1021286, 1021286) # enter Paint Tool
			tool()[c4d.ID_CA_PAINT_TOOL_MAINMODE] = 1  # Set Paint Mode = Vertex Color

		# set appropriate color
		try:
			if C4D_RELEASE >= 15:  # to make it pre R15 compatible (by Tom Chen)
				newColor = self.getColorFromDensityCoef(self.GetFloat(self.INPUT_PaintedDensityCoef_ID))
			else:
				# to make it pre R15 compatible (by Tom Chen)
				newColor = self.getColorFromDensityCoef(self.GetReal(self.INPUT_PaintedDensityCoef_ID))
			tool()[c4d.ID_CA_PAINT_TOOL_VERTEXCOLOR] = newColor
		except Exception:
			retYesNo = gui.MessageDialog("Error : cannot assign color.", c4d.GEMB_OK)
			return False

		if c4d.GetC4DVersion() >= 17032:  # to make it pre R17.032 compatible (by Tom Chen)
			c4d.EventAdd(flags=c4d.EVENT_ENQUEUE_REDRAW)
		else:
			# to make it pre R17.032 compatible (by Tom Chen)
			c4d.EventAdd(flags=c4d.EVENT_FORCEREDRAW)

		return True



	# ------ Button commands -----
	def Command(self, id, msg):
		#logCrashTextFile("Command 1 id=%d\n"%id);
		if g_logDebugInfo: print "Command id=%d"%id
		#print "Command id=%d"%id
		#print "msg="+str(msg)

		if id == self.BTN_RemeshIt_ID:
			self.RemeshIt()
			return True

		elif id == self.BTN_LicenseManager_ID:
			self.doLicMgr()
			return True

		elif id == self.BTN_WebDoc_ID:
			self.doWebDoc()

		elif id == self.BTN_ResetOptions_ID:
			self.doResetOptions()

		elif id == self.BTN_SetDensityColoring_ID:
			self.setDensityColoring()

		elif id == self.BTN_DebugCompare_ID:
			self.doDebugCompare()
			return True



		return True


# The Command Plugin (the item in the menu)
class QuadRemesherData(c4d.plugins.CommandData):
	dialog = None

	def Execute(self, doc):
		if self.dialog is None:
			self.dialog = QuadRemesherDialog()

		return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaultw=350, defaulth=200)

	def RestoreLayout(self, sec_ref):
		if self.dialog is None:
			self.dialog = QuadRemesherDialog()

		return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)


if __name__ == "__main__":
	#print " "
	# The plugin can run from R14.041 upwards (by Tom Chen)
	if c4d.GetC4DVersion() >= 14041:
		#print(" ---  QuadRemesher plugin for Cinema 4D by Maxime Rouca 2019 --- ")
		# Get the current path of the file
		dir, file = os.path.split(__file__)

		# Load the icon
		icon = bitmaps.BaseBitmap()
		icon.InitWith(os.path.join(dir, "res", "QuadRemesher_Icon_32.png"))

		plugins.RegisterCommandPlugin(id=PLUGIN_ID, str="Quad Remesher",
									help="QuadRemesher - Automatic retopology", info=0,
									dat=QuadRemesherData(), icon=icon)

	else:
		print "###  QuadRemesher is not suitable for this Cinema 4D release!  ###"
	#print " "

