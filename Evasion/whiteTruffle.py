import sys
import socket

port = 4567
maxlen = 999999
eom = '\n'
print(sys.argv)
if len(sys.argv) > 2:
  port = int(sys.argv[2])
HP = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', port))

def readSocket(sock, timeout=0):
  inputData = ''
  while True:
    chunk = sock.recv(maxlen)
    if not chunk:
      break
    elif chunk == '':
      raise RuntimeError('socket connection broken')
    inputData = inputData + chunk
    if eom in inputData:
      break
  if inputData == '':
    return eom
  serverSaid(inputData)
  return inputData.strip()

def sendSocket(sock, msg):
  msg += eom
  totalsent = 0
  MSGLEN = len(msg) 
  while totalsent < MSGLEN:
    sent = sock.send(msg[totalsent:])
    if sent == 0:
      raise RuntimeError('socket connection broken')
    totalsent = totalsent + sent
  iSaid(msg)

def parseData(msg, maxNumberOfWalls):
  msgList = msg.split('\n')
  if msgList[0] != 'Walls':
    return msg

  # Parse Walls
  wallOffset = int(msgList[1])
  walls = [parseWallString(wall) for wall in msgList[2:2+wallOffset]]

  # Parse Moves to Next Wall Build
  assert(msgList[2+wallOffset] == 'Moves to Next Wall Build')
  movesToNextWallBuild = int(msgList[3+wallOffset])

  # Parse Hunter and Prey Location
  hunterData = msgList[4+wallOffset]
  hunterDirection = hunterData.split(' ')[1]
  hunterLocation = cleanListString(hunterData.split(' ')[2])

  preyData = msgList[5+wallOffset]
  preyLocation = cleanListString(preyData.split(' ')[1])

  # Parse Remaining Time
  remainingTime = float(msgList[6+wallOffset])
  return (walls, maxNumberOfWalls, movesToNextWallBuild, hunterDirection, hunterLocation, preyLocation, remainingTime)

def parseWallString(wall):
  wall = wall.split(' ')
  wallNumber = int(wall[0])
  wall = cleanListString(wall[1])
  wallStart = wall[0:2]
  wallEnd = wall[2:]
  return (wallNumber, wallStart, wallEnd)

def cleanListString(listString):
  listString = listString.replace('(', '')
  listString = listString.replace(')', '')
  return tuple(int(x) for x in listString.split(','))

def makeMove(socket, direction, wallToCreate, wallToRemove):
  if wallToCreate != []:
    (x1, y1) = wallToCreate[0]
    (x2, y2) = wallToCreate[1]
    sendSocket(socket,'%sw(%d,%d),(%d,%d)'%(direction, x1, y1, x2, y2))
  elif wallToRemove != []:
    sendSocket(socket,'%swx%d'%(direction, wallToRemove))
  else:
    sendSocket(socket,'%s'%(direction))

def serverSaid(msg):
  msg = stripNewLine(msg)
  print('Server: %s'%msg[:80])
def iSaid(msg):
  msg = stripNewLine(msg)
  print('Client: %s'%msg[:80])

def stripNewLine(msg):
  if msg[-1] == '\n':
    return msg[:-1]
  return msg

if __name__=='__main__':
  from hunter import playHunterAlternate
  from prey import playPreyAlternate

  hunterTrigger = True
  try:
    # Return Team Name
    question = readSocket(s, 1)
    assert(question == 'Team Name?')
    sendSocket(s, 'WhiteTruffle')

    # Read N (Time steps to build the next wall)
    #      M (Max number of walls)
    (N, M) = [int(x) for x in readSocket(s).split(' ')] 

    # Play Game
    while True:
      data = ''
      while True:
        dataNew = readSocket(s)
        data += dataNew + '\n'
        if '.' in data:
          break

      if data == '':
        break
      if HP == 'H':
        (direction, wallToCreate, wallToDestroy, hunterTrigger) = playHunterAlternate(hunterTrigger, *parseData(data, M))
      else:
        direction = playPreyAlternate(*parseData(data, M))
        wallToCreate = []
        wallToDestroy = []
      makeMove(s, direction, wallToCreate, wallToDestroy)
  finally:
    print('Close socket')
    s.close()
