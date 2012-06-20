import wx


a = wx.App()
f = wx.Frame(None, -1, 'Kanji Canvas')
f.SetSize((500,500))
p = wx.Panel(f)

kanjiFont = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

dragWindow = None
inputBox = None

kanjiList = []

def onCloseMainWindow(e):
	f = open('Map', 'w') 
	for k in kanjiList:
		f.write("{} {} {}\n".format(k.GetLabelText().encode('utf-8'), k.GetPosition().x, k.GetPosition().y))
	e.Skip()

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
	global kanjiFont, p, kanjiList
	t = wx.StaticText(p, label=text, pos=point)
	t.SetBackgroundColour(('WHITE'))
	t.SetFont(kanjiFont)
	t.Bind(wx.EVT_LEFT_UP, onMouseUp)
	t.Bind(wx.EVT_LEFT_DOWN, onMouseDown)
	t.Bind(wx.EVT_MOTION, onMouseMove)
	kanjiList.append(t)

p.Bind(wx.EVT_LEFT_UP, onMouseUp)
p.Bind(wx.EVT_MOTION, onMouseMove)
p.Bind(wx.EVT_LEFT_DCLICK, onDoubleClick)
f.Bind(wx.EVT_CLOSE, onCloseMainWindow)

f.Show()

mapFile = open('Map', 'r')
for line in mapFile:
	words = line.split()
	try:
		putKanji(words[0].decode('utf-8'), wx.Point(int(words[1]), int(words[2])))
	except:
		continue

a.MainLoop()