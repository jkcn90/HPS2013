import math

def playPreyAlternate(walls, maxNumberOfWalls, movesToNextWallBuild, hunterDirection, hunterLocation, preyLocation, remainingTime):
  if hunterDirection == 'SE':
    bestMove = 'SW'
  elif hunterDirection == 'NW':
    bestMove = 'NE'
  elif hunterDirection == 'NE':
    bestMove = 'NW'
  else:
    bestMove = 'NE'
  return bestMove

def playPrey(walls, maxNumberOfWalls, movesToNextWallBuild, hunterDirection, hunterLocation, preyLocation, remainingTime):

	possibleMoves = ['NN', 'SS', 'EE', 'WW', 'NE', 'SE', 'NW', 'SW', 'ZZ']
	# because the current compartment should always be a square,
	# all we need to is to specify the N, S, E, W bound 
	#currentCompartment = return CurrentCompartment(walls, preyLocation)
	(hRX, hRY) = getRelativePosition(preyLocation, hunterLocation)
	print 'hunterDirection: ' + hunterDirection
	print 'hRX: ' + str(hRX) + ' hRY: ' + str(hRY)
	print hRX<0
	print hRY<0

	if hunterDirection == 'NW':
		if hRX <= 0 and hRY <= 0:
			bestMove = 'NW'
		elif hRX > 0 and hRY > 0:
			bestMove = 'SE'
		elif hRX <= 0 and hRY > 0:
			bestMove = 'NW'
		elif hRX > 0 and hRY <= 0:
			bestMove = 'NW'
	elif hunterDirection == 'NE':
		if hRX < 0 and hRY <= 0:
			bestMove = 'NE'
		elif hRX >= 0 and hRY > 0:
			bestMove = 'NE'
		elif hRX < 0 and hRY > 0:
			bestMove = 'SW'
		elif hRX >= 0 and hRY <= 0:
			bestMove = 'NE'
	elif hunterDirection == 'SW':
		if hRX <= 0 and hRY < 0:
			bestMove = 'SW'
		elif hRX > 0 and hRY >= 0:
			bestMove = 'SW'
		elif hRX <= 0 and hRY >= 0:
			bestMove = 'SW'
		elif hRX > 0 and hRY < 0:
			bestMove = 'NE'
	elif hunterDirection == 'SE':
		if hRX < 0 and hRY < 0:
			bestMove = 'NW'
		elif hRX >= 0 and hRY >= 0:
			bestMove = 'SE'
		elif hRX < 0 and hRY >= 0:
			bestMove = 'SE'
		elif hRX >= 0 and hRY < 0:
			bestMove = 'SE'
	print 'preybestMove' + bestMove
	return bestMove
	

def getDistance(self, other):
	return math.sqrt( (self[0]-other[0])**2 + (self[1]-other[1])**2 )

# if X Distance < 0 : other is in east of self
#               > 0 : other is in west of self
def getXDistance(self, other):
	print (other[0]-self[0])
	return (other[0]-self[0])

# if Y Distance < 0 : other is in north of self
#               > 0 : other is in south of self 
def getYDistance(self, other):
	print (other[1]-self[1])
	return (other[1]-self[1])

def getRelativePosition(self, other):
	return (getXDistance(self,other), getYDistance(self,other))

def getDiagonalDifference(self, other):
	return (self[0]-self[1])-(other[0]-other[1])

def getCounterDiagonalDifference(self, other):
	return (self[0]+self[1])-(other[0]+other[1])

def CurrentCompartment(walls, preyLocation):
	pass


