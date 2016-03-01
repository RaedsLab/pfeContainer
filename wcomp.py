# -*- coding: utf-8 -*-

"""
	Authors: L. Capocchi (capocchi@univ-corse.fr), S. Sehili
	Date: 15/10/2014
	Description:
		Plug-in to enabled the "wcomp" submenu of the .amd contextual menu
	Depends: Nothing
"""

import wx
import os
import sys
import zipfile
import zipimport

import pluginmanager
import Editor
import ZipManager
import Menu


ID_WCOMP_SHAPE = wx.NewId()
ID_EXPORT_WCOMP_PY_SHAPE = wx.NewId()
ID_EXPORT_WCOMP_DLL_SHAPE = wx.NewId()

global shape

def OnStrategies(event):
	''' Event Handler for the strategies definition
	'''

	global shape

	#obj = event.GetEventObject()
	#canvas = obj.GetParent()

	### .amd file
	amd = zipfile.ZipFile(shape.model_path, 'a')
	### test if strategies file is zipped
	if 'strategies.py' not in amd.namelist():
		try:
			amd.writestr(zipfile.ZipInfo('strategies.py'), '')
		finally:
			amd.close()
	else:
		amd.close()

	editorFrame = Editor.GetEditor(None, wx.ID_ANY, _('Strategies definition'))
	editorFrame.AddEditPage("Strategies",os.path.join(shape.model_path, 'strategies.py'))
	editorFrame.Show()

def OnExportPy(event):
	""" Export the strategies into a python file.
		unzip the strategies file from .amd
	"""

	global shape

	amd = zipfile.ZipFile(shape.model_path, 'r')

	### if amd contain strategies.py file
	if 'strategies.py' in amd.namelist():
		### ask the output directory
		dlg = wx.DirDialog(None, _("Choose a directory:"),
							style=wx.DD_DEFAULT_STYLE
							#| wx.DD_DIR_MUST_EXIST
							#| wx.DD_CHANGE_DIR
							)

		if dlg.ShowModal() == wx.ID_OK:
			outpath = dlg.GetPath()
			### extract the file from the amd file
			amd.extract("strategies.py", outpath)

			print "strategies.py extracted from %s to %s"%(os.path.basename(shape.model_path), outpath)

		# Only destroy a dialog after you're done with it.
		dlg.Destroy()

	amd.close()

def OnExportDll(event):
	""" Export the strategies into a dll file.
		unzip the strategies file from .amd
	"""
	print "Export into a dll file"

@pluginmanager.register("IMPORT_STRATEGIES")
def scan_strategies_importing(*args, **kwargs):

	fn = kwargs['fn']

	### .amd file
	amd = zipfile.ZipFile(fn, 'r')
	### test if strategies file is zipped
	if 'strategies.py' in amd.namelist():

		amd.close()

		importer = zipimport.zipimporter(fn)

		try:
			module = importer.load_module('strategies')
			new_name = "strategies_of_%s"%os.path.splitext(os.path.basename(fn))[0]
			module.__name__ = new_name
			sys.modules[new_name] = module

		except Exception, info:
			print "plugin generale wcomp.py: %s"%info
	else:
		amd.close()

@pluginmanager.register("ADD_WCOMP_EXPORT_MENU")
def add_wcomp_export_menu(*args, **kwargs):

	global shape

	menu = kwargs['parent']
	shape = kwargs['model']
	export_subMenu = kwargs['submenu']

	exportWCompPy = wx.MenuItem(menu, ID_EXPORT_WCOMP_PY_SHAPE, _("WComp (.py)"), _("Python file for WComp strategies"))
	exportWCompDLL = wx.MenuItem(menu, ID_EXPORT_WCOMP_DLL_SHAPE, _("WComp (.dll)"), _("Python file for WComp strategies"))
	Export_SubMenu1 = export_subMenu.AppendItem(exportWCompPy)
	Export_SubMenu2 = export_subMenu.AppendItem(exportWCompDLL)

	menu.Bind(wx.EVT_MENU, OnExportPy, id=ID_EXPORT_WCOMP_PY_SHAPE)
	menu.Bind(wx.EVT_MENU, OnExportDll, id=ID_EXPORT_WCOMP_DLL_SHAPE)

@pluginmanager.register("ADD_WCOMP_STRATEGY_MENU")
def add_wcomp_strategy_menu(*args, **kwargs):

	global shape

	menu = kwargs['parent']
	shape = kwargs['model']

	strategies = wx.MenuItem(menu, ID_WCOMP_SHAPE, _("Strategies"), _("WCOMP strategies definition"))
	strategies.SetBitmap(wx.Image(os.path.join(ICON_PATH_16_16,'wcomp.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap())

	Strategies_menu = menu.AppendItem(strategies)
	menu.Bind(wx.EVT_MENU, OnStrategies, id=ID_WCOMP_SHAPE)

def Config(parent):
	""" Plug-in settings frame.
	"""
	dlg = wx.MessageDialog(parent, _('No settings available for this plug-in\n'), _('Blink configuration'), wx.OK | wx.ICON_EXCLAMATION)
	dlg.ShowModal()
