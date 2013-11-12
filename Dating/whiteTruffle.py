import socket
import copy
import sys
eom = '<EOM>\n'

def send(s, msg):
    print("sending")
    print(msg)
    msg += eom
    totalsent = 0
    while totalsent < len(msg):
        sent = s.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

def receive(s, timeout=0):
    msg = ''
    while eom not in msg:
        chunk = s.recv(1024)
        if not chunk:
          break
        if chunk == '':
            raise RuntimeError("socket connection broken")
        msg += chunk
    msg = msg.replace(eom, '')
    return msg

def getPlayerTypeAndNumberOfAttributes(rawData, playerTypeToConfirm = None):
  rawData = rawData.split('\n')

  # Check the header Data
  headerData = rawData[0].split(' ')
  playerType = headerData[0]
  numberOfAttributes = int(headerData[1])

  if playerTypeToConfirm is not None:
    assert(playerType == playerTypeToConfirm)
  return (playerType, numberOfAttributes)

def parseCandidates(rawData, numberOfAttributes):
  rawData = rawData.split('\n')

  # Check if first line is header
  headerRow = rawData[0]
  if headerRow[0] in ('M', 'P'):
    rawData = rawData[1:]

  # Parse Candidates
  candidates = [(
                  [float(attribute)
                   for attribute
                   in attributes.split(' ')[:numberOfAttributes]
                   if attribute != ''
                  ],
                  float(attributes.split(' ')[numberOfAttributes])
                )
                for attributes in rawData
                if attributes != '']
  return candidates

def encodeCandidate(candidate):
  candidate = str(candidate)
  candidate = candidate.replace('[', '')
  candidate = candidate.replace(']', '')
  candidate = candidate.replace(',', '')
  return candidate

if __name__ == '__main__':
  import matchmaker
  from Player import Player
  port = 4567
  print(sys.argv)
  if len(sys.argv) > 1:
    port = int(sys.argv[1])
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('127.0.0.1', port))

  try:
    question = receive(s)

    assert(question == 'Team Name?')
    send(s, 'WhiteTruffle')

    # Read in data
    rawData = receive(s)
    (playerType, numberOfAttributes) = getPlayerTypeAndNumberOfAttributes(rawData)

    if playerType == 'P':
      p = Player(numberOfAttributes)
      playerStr = p.getParamsStr()

    while True:
      if playerType == 'M':
        # Play Matchmaker
        candidates = parseCandidates(rawData, numberOfAttributes)
        #nextCandidate = matchmaker.playRandom(candidates, numberOfAttributes)
        #nextCandidate = matchmaker.playBruteForce(candidates, numberOfAttributes)
        nextCandidate = matchmaker.playSimulatedAnnealing(candidates, numberOfAttributes)
        
        send(s, encodeCandidate(nextCandidate))
      elif playerType == 'P':
        send(s, playerStr)
      else:
        raise Exception('Invalid Player Type')

      rawData = receive(s)
      if 'end' in rawData:
        break
    
  except:
    raise
  finally:
    print('Close socket')
    s.close()
