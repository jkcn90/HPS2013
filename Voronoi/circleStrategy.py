import random
import math
import copy
import itertools
import subprocess
from operator import itemgetter

def playMove(state):
  alreadyPlayedMoves = list(itertools.chain.from_iterable(state.moves))

  midpoint = state.boardSize / 2
  center = (midpoint, midpoint)

  if state.numberOfPlayers == 2:
    radius = midpoint * 0.8
    points = getPointsOnCircle(center, radius, state.boardSize, alreadyPlayedMoves)
    points += getPointsOnCircle(center, 0, state.boardSize, alreadyPlayedMoves)
  else:
    radius = midpoint * 0.8
    radius2 = midpoint * 0.1

    points = getPointsOnCircle(center, radius, state.boardSize, alreadyPlayedMoves)
    points += getPointsOnCircle(center, radius2, state.boardSize, alreadyPlayedMoves)
    points += getPointsOnCircle(center, 0, state.boardSize, alreadyPlayedMoves)

  if state.timeLeft < 18 and state.numberOfStones != 10:
    (x, y) = random.choice(points)
    return (x, y)

  nextMoves = getBestMove(state.moves, points, state.playerId, state.numberOfPlayers, state.numberOfStones)

  #maxAreaPlayer = max(enumerate(state.areas), key=itemgetter(1))[0]
  #if maxAreaPlayer == state.playerId:
  #  (x, y) = max(nextMoves, key=itemgetter(state.playerId+1))[0:2]
  #else:
  #  sortedNextMoves = sorted(nextMoves, key=itemgetter(state.playerId+1), reverse=True)
  #  sortedNextMoves = sorted(nextMoves, key=itemgetter(maxAreaPlayer+1))
  #  (x, y) = sortedNextMoves[0][0:2]
  (x, y) = max(nextMoves, key=itemgetter(state.playerId+1))[0:2]
  return (x, y)

def getBestMove(previousMoves, points, playerId, numberOfPlayers, numberOfStones):
  points = str(points)
  points = points.replace('(', '')
  points = points.replace(')', '')
  points = points.replace(' ', '')
  points = points.replace(']', '')
  points = points.replace('[', '')

  points = points + '\n' + str(numberOfPlayers) + ',' + str(playerId) + ',' + str(numberOfStones)
  playerMoves = ''

  for playerNumber in range (1, numberOfPlayers+1):
    thisPlayerMoves = str(previousMoves[playerNumber])
    thisPlayerMoves = thisPlayerMoves.replace('(', str(playerNumber) + ',')
    thisPlayerMoves = thisPlayerMoves.replace(')', '')
    thisPlayerMoves = thisPlayerMoves.replace('[', '')
    thisPlayerMoves = thisPlayerMoves.replace(']', '')
    thisPlayerMoves = thisPlayerMoves.replace(' ', '')
    if thisPlayerMoves != '':
      thisPlayerMoves = ',' + thisPlayerMoves

    playerMoves += thisPlayerMoves
    
  input_ = points + playerMoves
  p = subprocess.Popen(["./Voronoi"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  output = p.communicate(input_)[0]

  output = [int(x) for x in output.split(',')]

  outputs = []
  tupleLength = numberOfPlayers+2
  for i in range(0, tupleLength):
    outputs += [output[i:]]

  output = zip(*outputs)[::tupleLength]
  return output

def getPointsOnCircle(center, radius, boardSize, excludeMoves = []):
  return [(x, y)
          for x in range(0, boardSize)
          for y in range(0, boardSize)
          if abs(getDistance(center, (x, y)) - radius) == 0
          if (x,y) not in excludeMoves]

def getDistance((x1, y1), (x2, y2)):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def calibrateRadis():
  pass

if __name__ == '__main__':
  points = getPointsOnCircle((500, 500), 100, 1000)
  print(points)
