import wx



a = wx.App()
f = wx.Frame(None, -1, 'Kanji Canvas')
f.SetSize((500,500))
p = wx.Panel(f)

kanjiFont = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

dragWindow = None
inputBox = None

def onMouseDown(e):
	global dragWindow, dragWindowStartPos, dragMouseStartPos
	dragWindow = e.GetEventObject()
	dragWindowStartPos = dragWindow.GetPosition()
	dragMouseStartPos = e.GetEventObject().ClientToScreen(e.GetPosition())

def onMouseUp(e):
	global dragWindow
	dragWindow = None

def onMouseMove(e):
	global dragWindow, dragWindowStartPos, dragMouseStartPos
	if dragWindow:
		sPos = e.GetEventObject().ClientToScreen(e.GetPosition())
		if e.LeftIsDown():
			dragWindow.Move(dragWindowStartPos - dragMouseStartPos + sPos)

def onKey(e):
	#print 'onKey', e.GetKeyCode()
	global inputBox
	if e.GetKeyCode() == wx.WXK_ESCAPE:
		inputBox.Destroy()
		inputBox = None
		return
	if e.GetKeyCode() == wx.WXK_RETURN:
		if not inputBox.IsEmpty():
			putKanji(inputBox.GetValue(), inputBox.GetPosition())
			#inputBox.GetValue()
		inputBox.Destroy()
		inputBox = None
		return
	e.Skip()

def onDoubleClick(e):
	global inputBox, kanjiFont
	if inputBox:
		inputBox.Destroy()
		inputBox = None
	inputBox = wx.TextCtrl(e.GetEventObject(), pos=e.GetPosition(), style=wx.TE_PROCESS_ENTER)
	inputBox.SetFont(kanjiFont)
	inputBox.SetSize(inputBox.GetBestSize())
	inputBox.SetBackgroundColour(('WHITE'))
	inputBox.SetFocus()
	inputBox.Bind(wx.EVT_CHAR, onKey)

def putKanji(text, point):
	global kanjiFont, p
	t = wx.StaticText(p, label=text, pos=point)
	t.SetBackgroundColour(('WHITE'))
	t.SetFont(kanjiFont)
	t.Bind(wx.EVT_LEFT_UP, onMouseUp)
	t.Bind(wx.EVT_LEFT_DOWN, onMouseDown)
	t.Bind(wx.EVT_MOTION, onMouseMove)

p.Bind(wx.EVT_LEFT_UP, onMouseUp)
p.Bind(wx.EVT_MOTION, onMouseMove)
p.Bind(wx.EVT_LEFT_DCLICK, onDoubleClick)

f.Show()

putKanji(u'\u5590', (100, 50))
putKanji(u'\u4f50', (50, 100))

a.MainLoop()