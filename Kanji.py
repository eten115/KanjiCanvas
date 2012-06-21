import wx, sys


a = wx.App(redirect=True, filename='error.txt')
f = wx.Frame(None, -1, 'Kanji Canvas')
f.SetSize((500,500))
p = wx.Panel(f)

kanjiFont = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD)
kanjiFont.SetFaceName("MS Mincho")
quizFont = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)

dragWindow = None
inputBox = None

kanjiList = []
dictList = []

quizQuestionIndex = None
correctAnswerCount = 0

def isQuiz():
	return (quizQuestionIndex != None)

startQuizButton = wx.Button(p, label="Start Quiz", pos=(20,10))
quizProgBar = wx.Gauge(p, size=(200, 20), pos=(120, 10))
quizText = wx.StaticText(p, label="Push button to begin quiz", pos=(20, 50), size=(200,20))
quizText.SetFont(quizFont)

lastHigh = None

def setHigh(w):
	global lastHigh
	if not lastHigh is w:
		if lastHigh:
			lastHigh.SetBackgroundColour(wx.NullColour)
			lastHigh.Show(False)
			lastHigh.Show(True)
		if w:
			w.SetBackgroundColour(('WHITE'))
			w.Show(False)
			w.Show(True)
		lastHigh = w

def findKanjiInDict(kanji):
	for entry in dictList:
		if entry['kanji'] == kanji:
			return entry
	return None

def popQuestion():
	q = dictList[quizQuestionIndex]
	quizText.SetLabel(q['meaning'])

def startQuiz():
	global quizQuestionIndex
	if len(dictList) > 0:
		quizProgBar.SetRange(len(dictList))
		quizProgBar.SetValue(0)
		quizQuestionIndex = 0
		correctAnswerCount = 0
		popQuestion()

def onQuizButton(e):
	startQuiz()
	
def advanceToNextQuestion():
	global quizQuestionIndex
	quizProgBar.SetValue(quizQuestionIndex+1)
	if quizQuestionIndex < len(dictList)-1:
		quizQuestionIndex += 1
		popQuestion()
	else:
		quizQuestionIndex = None
		quizText.SetLabel('Correct {} of {}'.format(correctAnswerCount, len(dictList)))

def onCloseMainWindow(e):
	f = open('Map', 'w') 
	for k in kanjiList:
		f.write("{} {} {}\n".format(k.GetLabelText().encode('utf-8'), k.GetPosition().x, k.GetPosition().y))
	e.Skip()
	
def onPanelMouseDown(e):
	if isQuiz():
		correctAnswer = dictList[quizQuestionIndex]['kanji']
		for w in kanjiList:
			if w.GetLabel() == correctAnswer:
				setHigh(w)
		advanceToNextQuestion()

def onKanjiMouseDown(e):
	if isQuiz():
		global correctAnswerCount
		k = e.GetEventObject()
		correctAnswer = dictList[quizQuestionIndex]['kanji']
		if k.GetLabel() == correctAnswer:
			correctAnswerCount += 1
			setHigh(k)
		else:
			for w in kanjiList:
				if w.GetLabel() == correctAnswer:
					setHigh(w)
		advanceToNextQuestion()
	else:
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

def onInputBoxKey(e):
	global inputBox
	if e.GetKeyCode() == wx.WXK_ESCAPE:
		inputBox.Destroy()
		inputBox = None
		return
	if e.GetKeyCode() == wx.WXK_RETURN:
		if not inputBox.IsEmpty():
			putKanji(inputBox.GetValue(), inputBox.GetPosition())
		inputBox.Destroy()
		inputBox = None
		return
	e.Skip()

def onDoubleClick(e):
	if not inQuiz():
		global inputBox, kanjiFont
		if inputBox:
			inputBox.Destroy()
			inputBox = None
		inputBox = wx.TextCtrl(e.GetEventObject(), pos=e.GetPosition(), style=wx.TE_PROCESS_ENTER)
		inputBox.SetFont(kanjiFont)
		inputBox.SetSize(inputBox.GetBestSize())
		inputBox.SetFocus()
		inputBox.Bind(wx.EVT_CHAR, onInputBoxKey)

def putKanji(text, point):
	global kanjiFont, p, kanjiList
	t = wx.StaticText(p, label=text, pos=point)
	t.SetFont(kanjiFont)
	t.Bind(wx.EVT_LEFT_UP, onMouseUp)
	t.Bind(wx.EVT_LEFT_DOWN, onKanjiMouseDown)
	t.Bind(wx.EVT_MOTION, onMouseMove)
	kanjiList.append(t)

p.Bind(wx.EVT_LEFT_UP, onMouseUp)
p.Bind(wx.EVT_MOTION, onMouseMove)
p.Bind(wx.EVT_LEFT_DCLICK, onDoubleClick)
p.Bind(wx.EVT_LEFT_DOWN, onPanelMouseDown)
f.Bind(wx.EVT_CLOSE, onCloseMainWindow)
startQuizButton.Bind(wx.EVT_BUTTON, onQuizButton)

f.Show()

mapFile = open('Map', 'r')
for line in mapFile:
	try:
		words = line.split()
		pos = wx.Point(int(words[1]), int(words[2]))
		putKanji(words[0].decode('utf-8'), pos)
	except:
		continue

dictFile = open('Dict.txt', 'r')
for line in dictFile:
	try:
		words = line.split('\t')
		entry = {'kanji': words[0].decode('utf-8'), 'meaning': words[1].decode('utf-8')}
		dictList.append(entry)
	except:
		continue

a.MainLoop()