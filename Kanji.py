import wx, sys, random, copy

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
quizList = []
mistakeList = []

quizQuestionIndex = None

def isQuiz():
	return (quizQuestionIndex != None)

startQuizButton = wx.Button(p, label="Start Quiz", pos=(20,10))
quizProgBar = wx.Gauge(p, size=(200, 20), pos=(120, 10))
quizText = wx.StaticText(p, label="Push button to begin quiz", pos=(20, 50), size=(200,15))
quizText.SetFont(quizFont)
quizText.SetBackgroundColour(('WHITE'))
fixMistakesButton = wx.Button(p, label="Fix Mistakes", pos=(20, 90))

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

def popQuestion():
	q = quizList[quizQuestionIndex]
	quizText.SetLabel(q['meaning'])

def startQuiz():
	global quizQuestionIndex, quizList
	if len(dictList) > 0:
		random.shuffle(quizList)
		quizProgBar.SetRange(len(quizList))
		quizProgBar.SetValue(0)
		quizQuestionIndex = 0
		popQuestion()

def onFixMistakesButton(e):
	global quizList, mistakeList
	quizList = mistakeList
	mistakeList = []
	startQuiz()

def onQuizButton(e):
	global quizList, mistakeList
	quizList = copy.copy(dictList)
	mistakeList = []
	startQuiz()

def advanceToNextQuestion():
	global quizQuestionIndex
	quizProgBar.SetValue(quizQuestionIndex+1)
	if quizQuestionIndex < len(quizList)-1:
		quizQuestionIndex += 1
		popQuestion()
	else:
		quizQuestionIndex = None
		quizText.SetLabel('Mistakes {} of {}'.format(len(mistakeList), len(quizList)))

def onCloseMainWindow(e):
	f = open('Map', 'w') 
	for k in kanjiList:
		f.write("{} {} {}\n".format(k.GetLabelText().encode('utf-8'), k.GetPosition().x, k.GetPosition().y))
	e.Skip()
	
def onPanelMouseDown(e):
	if isQuiz():
		correctAnswer = quizList[quizQuestionIndex]['kanji']
		for w in kanjiList:
			if w.GetLabel() == correctAnswer:
				setHigh(w)
		advanceToNextQuestion()

def onKanjiMouseDown(e):
	if isQuiz():
		k = e.GetEventObject()
		question = quizList[quizQuestionIndex]
		if k.GetLabel() == question['kanji']:
			setHigh(k)
		else:
			mistakeList.append(question)
			for w in kanjiList:
				if w.GetLabel() == question['kanji']:
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
	if not isQuiz():
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
fixMistakesButton.Bind(wx.EVT_BUTTON, onFixMistakesButton)

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
		entry = {'kanji': words[0].decode('utf-8'), 'meaning': words[1].rstrip().decode('utf-8')}
		dictList.append(entry)
	except:
		continue

a.MainLoop()