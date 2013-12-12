import sys
import socket
import numpy as np
from exceptions import ZeroDivisionError

port = 4567
eom = "<EOM>"
maxlen = 999999
boardSize = 1000
print(sys.argv)
if len(sys.argv) > 1:
  port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', port))

def readSocket(sock, timeout=0):
  inpData=''
  while True:
    chunk = sock.recv(maxlen)
    if not chunk:
      break
    elif chunk == '':
      raise RuntimeError("socket connection broken")
    inpData = inpData + chunk
    if eom in inpData:
      break
  inpData=inpData.strip()[:-len(eom)]
  serverSaid(inpData.replace('\n', ' [N] ')[:90])
  return inpData.strip()

def sendSocket(sock, msg):
  msg += eom
  totalsent = 0
  MSGLEN = len(msg) 
  while totalsent < MSGLEN:
    sent = sock.send(msg[totalsent:])
    if sent == 0:
      raise RuntimeError("socket connection broken")
    totalsent = totalsent + sent
  #iSaid(msg)

def makeMove(socket, pid, x, y):
  sendSocket(socket,"(%d,%d,%d)"%(pid, x, y))

def serverSaid(msg):
  print("Server: %s"%msg[:80])
def iSaid(msg):
  print("Client: %s"%msg[:80])

class State:
  def __init__(self, numberOfPlayers, numberOfStones, playerId, boardSize):
    self.playerId = playerId
    self.numberOfStones = numberOfStones
    self.numberOfPlayers = numberOfPlayers
    self.boardSize = boardSize

    self.nextPlayer = 0
    self.timeLeft = -1.00
    self.moves = []
    self.areas = []

  def parseState(self, gameState):
    # 1. Player ID, Remaining Time
    # 2. Moves Played
    # 3. Area Captured so far
    state = gameState.split('\n')

    line1 = state[0].split(',')
    self.nextPlayer = int(line1[0])
    if self.nextPlayer == self.playerId:
      self.timeLeft = float(line1[1])

    self.parseMoves(state[1])
    self.parseAreas(state[2])

  def parseMoves(self, movestr):
    self.moves=[[] for i in range(0,self.numberOfPlayers+1)]
    if len(movestr) == 0: return # no moves yet
    movelist=movestr.split('),(')
    movelist[0] = movelist[0][1:]
    movelist[-1] = movelist[-1][:-1]
    for m in movelist:
      m=m.split(',')
      mid=int(m[0])
      x =int(m[1])
      y =int(m[2])
      self.moves[mid].append((x,y))

  def parseAreas(self, areastr):
    self.areas = [0] # dummy 0-index
    alist = areastr.split('),(')
    alist[0] = alist[0][1:]
    alist[-1] = alist[-1][:-1]
    for astr in alist:
      (aid, area) = astr.split(',')
      print("Player %s area: %s" % (aid, area))
      self.areas.append(int(area))
      assert(len(self.areas) == int(aid)+1)

if __name__=="__main__":
  from circleStrategy import playMove

  print("Get question from socket")
  try:
    # Process Protocol 2: Return Team Name
    question = readSocket(s, 1)
    assert(question == 'Team Name?')
    sendSocket(s, "WhiteTruffle")

    # Process Protocol 3: Read and Parse Game Initialization Parameters
    params = readSocket(s)
    params = params.split(',')
    numberOfPlayers = int(params[0])
    numberOfStones = int(params[1])
    assert(int(params[2]) == boardSize)
    pid = int(params[3])
    state = State(numberOfPlayers, numberOfStones, pid, boardSize)

    # Process Protocol 4: Play Game
    for turn in range(numberOfStones):
      for player in range(1, numberOfPlayers+1):
        gameState = readSocket(s)
        state.parseState(gameState)

        # assert(player == state.nextPlayer)
        if player == pid:
          (x, y) = playMove(state)
          makeMove(s, pid, x, y)

    # Read Game Result
    state.parseState(readSocket(s))
    if np.argmax(state.areas) == state.playerId:
      print("I won! with %.2f percent area"%(100*float(state.areas[state.playerId])/boardSize**2))
    else:
      print("I lost from player %d! with %.2f percent area"%(np.argmax(state.areas),100*float(state.areas[state.playerId])/boardSize**2))
  finally:
    print("Close socket")
    s.close()
