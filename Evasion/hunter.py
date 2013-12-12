import math
import operator
import copy

def playHunterAlternate(trigger, walls, maxNumberOfWalls, movesToNextWallBuild, hunterDirection, hunterLocation, preyLocation, remainingTime):
  direction = hunterDirection
  if direction != 'SE':
    trigger = False
  relativeLocationOfPrey = getRelativeLocation(hunterLocation, preyLocation)
  wallToCreate = []
  wallToDestroy = []
  tolerance = range(1, 15)
  minorTolerance = range(1, 2)
  minorToleranceY = range(2, 5)
  if preyLocation[1] > 460 and hunterLocation[1] > 460 and movesToNextWallBuild < 1:
    wallsToDestroy = [wallNumber
                      for (wallNumber, (x, _), (xAlt, _)) in walls
                      if x == xAlt
                      and (
                           (hunterDirection in {'NW', 'SW'}
                            and x > preyLocation[0]
                            and x < hunterLocation[0])
                           or
                           (hunterDirection in {'NE', 'SE'}
                            and x < preyLocation[0]
                            and x > hunterLocation[0])
                          )]
    if wallsToDestroy != []:
      wallToDestroy = wallsToDestroy[0]
      wallToCreate = []

    if wallToDestroy != []:
      if hunterDirection in {'SE', 'SW'} and relativeLocationOfPrey in {'SE', 'SW', 'S'}:
        wallToCreate = createHorizontalWall(hunterLocation, walls)
      elif hunterDirection in {'NE', 'NW'} and relativeLocationOfPrey in {'NE', 'NW', 'N'}:
        wallToCreate = createHorizontalWall(hunterLocation, walls)
    return (direction, wallToCreate, wallToDestroy, trigger)

  if getYDistance(hunterLocation, preyLocation) in minorToleranceY and hunterLocation[1] < 400:
    if hunterDirection in {'SE', 'SW'} and relativeLocationOfPrey in {'SE', 'SW'}:
      wallToCreate = createHorizontalWall(hunterLocation, walls, 1)
    elif hunterDirection in {'NE', 'NW'} and relativeLocationOfPrey in {'NE', 'NW'}:
      wallToCreate = createHorizontalWall(hunterLocation, walls, 1)

  if hunterDirection == 'SE' and trigger:
    if getXDistance(hunterLocation, preyLocation) in tolerance:
      wallToCreate = createVerticalWall(hunterLocation, walls)
  else:
    if getXDistance(hunterLocation, preyLocation) in minorTolerance:
      if hunterDirection in {'SW', 'NW'} and relativeLocationOfPrey in {'SW', 'NW', 'W'}:
        wallToCreate = createVerticalWall(hunterLocation, walls)

  if getYDistance(hunterLocation, preyLocation) in minorToleranceY and hunterLocation[1] < 400:
    if hunterDirection in {'SE', 'SW'} and relativeLocationOfPrey in {'SE', 'SW'}:
      wallToCreate = createHorizontalWall(hunterLocation, walls, 1)
    elif hunterDirection in {'NE', 'NW'} and relativeLocationOfPrey in {'NE', 'NW'}:
      wallToCreate = createHorizontalWall(hunterLocation, walls, 1)

  if len(walls) > 3 or wallToCreate == []:
    wallsToDestroy = [wallNumber
                      for (wallNumber, (x, _), (xAlt, _)) in walls
                      if getXDistance(hunterLocation, (x,)) == 3
                      and x == xAlt
                      and (
                           (hunterDirection in {'NW', 'SW'}
                            and x > preyLocation[0]
                            and x < hunterLocation[0])
                           or
                           (hunterDirection in {'NE', 'SE'}
                            and x < preyLocation[0]
                            and x > hunterLocation[0])
                          )]
    if wallsToDestroy != []:
      wallToDestroy = wallsToDestroy[0]
      wallToCreate = []
    else:
      yWalls = [y
                for (_, (_, y), (_, yAlt)) in walls
                if y == yAlt
                and y > hunterLocation[1]]

      if yWalls != []:
        wallsToDestroy = [wallNumber
                          for (wallNumber, (_, y), (_, yAlt)) in walls
                          if y == yAlt
                          and y > min(yWalls)]
      else:
        wallsToDestroy = []
      if wallsToDestroy != []:
        wallToDestroy = wallsToDestroy[0]
      else:
        yWalls = [y
                  for (_, (_, y), (_, yAlt)) in walls
                  if y == yAlt
                  and y < hunterLocation[1]]

        if yWalls != []:
          wallsToDestroy = [wallNumber
                            for (wallNumber, (_, y), (_, yAlt)) in walls
                            if y == yAlt
                            and y < max(yWalls)]
        else:
          wallsToDestroy = []
        if wallsToDestroy != []:
          wallToDestroy = wallsToDestroy[0]
        else:
          xWalls = [x
                    for (_, (x, _), (xAlt, _)) in walls
                    if x == xAlt
                    and x > preyLocation[0]
                    and x > hunterLocation[0]]

          if xWalls != []:
            wallsToDestroy = [wallNumber
                              for (wallNumber, (x, _), (xAlt, _)) in walls
                              if x == xAlt
                              and x > min(xWalls)]
          else:
            wallsToDestroy = []
          if wallsToDestroy != []:
            wallToDestroy = wallsToDestroy[0]
          else:
            xWalls = [x
                      for (_, (x, _), (xAlt, _)) in walls
                      if x == xAlt
                      and x < preyLocation[0]
                      and x < hunterLocation[0]]

            if xWalls != []:
              wallsToDestroy = [wallNumber
                                for (wallNumber, (x, _), (xAlt, _)) in walls
                                if x == xAlt
                                and x < max(xWalls)]
            else:
              wallsToDestroy = []
            if wallsToDestroy != []:
              wallToDestroy = wallsToDestroy[0]
            else:
              xWalls = [x
                        for (_, (x, _), (xAlt, _)) in walls
                        if x == xAlt
                        and x > preyLocation[0]
                        and x < hunterLocation[0]]

              if xWalls != []:
                wallsToDestroy = [wallNumber
                                  for (wallNumber, (x, _), (xAlt, _)) in walls
                                  if x == xAlt
                                  and x > min(xWalls)]
              else:
                wallsToDestroy = []
              if wallsToDestroy != []:
                wallToDestroy = wallsToDestroy[0]
              elif trigger:
                xWalls = [x
                          for (_, (x, _), (xAlt, _)) in walls
                          if x == xAlt
                          and x < preyLocation[0]
                          and x > hunterLocation[0]]

                if xWalls != []:
                  wallsToDestroy = [wallNumber
                                    for (wallNumber, (x, _), (xAlt, _)) in walls
                                    if x == xAlt
                                    and x < max(xWalls)]
                else:
                  wallsToDestroy = []
                if wallsToDestroy != []:
                  wallToDestroy = wallsToDestroy[0]

  return (direction, wallToCreate, wallToDestroy, trigger)

def playHunter(walls, maxNumberOfWalls, movesToNextWallBuild, hunterDirection, hunterLocation, preyLocation, remainingTime):
  direction = hunterDirection
  relativeLocationOfPrey = getRelativeLocation(hunterLocation, preyLocation)
  tolerance = [2]

  wallToCreate = []
  wallToDestroy = []
  if getXDistance(hunterLocation, preyLocation) in tolerance:
    if hunterDirection == 'SE' and relativeLocationOfPrey == 'NE':
      wallToCreate = createVerticalWall(hunterLocation, walls)
    elif hunterDirection == 'SE' and relativeLocationOfPrey == 'SW':
      wallToCreate = createHorizontalWall(hunterLocation, walls)
    elif hunterDirection == 'SW' and relativeLocationOfPrey == 'NW':
      wallToCreate = createVerticalWall(hunterLocation, walls)
    elif hunterDirection == 'SW' and relativeLocationOfPrey == 'SE':
      wallToCreate = createHorizontalWall(hunterLocation, walls)

  if getYDistance(hunterLocation, preyLocation) in tolerance:
    if hunterDirection == 'NE' and relativeLocationOfPrey == 'NW':
      wallToCreate = createHorizontalWall(hunterLocation, walls)
    elif hunterDirection == 'NE' and relativeLocationOfPrey == 'SW':
      wallToCreate = createVerticalWall(hunterLocation, walls)
    elif hunterDirection == 'NW' and relativeLocationOfPrey == 'NE':
      wallToCreate = createHorizontalWall(hunterLocation, walls)
    elif hunterDirection == 'NW' and relativeLocationOfPrey == 'SW':
      wallToCreate = createVerticalWall(hunterLocation, walls)

  if getYDistance(hunterLocation, preyLocation) in tolerance or getYDistance(hunterLocation, preyLocation) in tolerance:
    if hunterDirection == 'NE' and relativeLocationOfPrey == 'NE':
      wallToCreate = getWallThatMinimizesArea(hunterLocation, preyLocation, walls)
    elif hunterDirection == 'SE' and relativeLocationOfPrey == 'SE':
      wallToCreate = getWallThatMinimizesArea(hunterLocation, preyLocation, walls)
    elif hunterDirection == 'SW' and relativeLocationOfPrey == 'SW':
      wallToCreate = getWallThatMinimizesArea(hunterLocation, preyLocation, walls)
    elif hunterDirection == 'NW' and relativeLocationOfPrey == 'NW':
      wallToCreate = getWallThatMinimizesArea(hunterLocation, preyLocation, walls)

  #if wallToCreate != []:
  #  beforeArea = getPreyArea(preyLocation, walls)
  #  afterArea = getPreyArea(preyLocation, walls, wallToCreate)
  #  if abs(beforeArea-afterArea)/float(beforeArea) < 0:
  #    wallToCreate = []
  return (direction, wallToCreate, wallToDestroy)

def getWallThatMinimizesArea(hunterLocation, preyLocation, walls):
  verticalWall = createVerticalWall(hunterLocation, walls)
  horizontalWall = createHorizontalWall(hunterLocation, walls)
  areaAddVertical = getPreyArea(preyLocation, walls, verticalWall)
  areaAddHorizontal = getPreyArea(preyLocation, walls, horizontalWall)
  if areaAddVertical < areaAddHorizontal:
    return verticalWall
  else:
    return horizontalWall

def getPreyArea(preyLocation, walls, newWall = []):
  walls = copy.deepcopy(walls)
  if newWall != []:
    walls += [(-1, newWall[0], newWall[1])]
  (xPrey, yPrey) = preyLocation
  left = [x1
          for (_, (x1, y1), (x2, y2)) in walls
          if yPrey in range(y1, y2+1)
          if xPrey > x1]
  left = max(left+[0])

  right = [x1
           for (_, (x1, y1), (x2, y2)) in walls
           if yPrey in range(y1, y2+1)
           if xPrey < x1]
  right = min(right+[499])

  up = [y1
        for (_, (x1, y1), (x2, y2)) in walls
        if xPrey in range(x1, x2+1)
        if yPrey > y1]
  up = max(up+[0])

  down = [y1
          for (_, (x1, y1), (x2, y2)) in walls
          if xPrey in range(x1, x2+1)
          if yPrey < y1]
  down = min(down+[499])
  area = abs(up-down+1) * abs(left-right+1)
  return area

def getDistance(first, second):
  return math.sqrt((first[0]-second[0])**2 + (first[1]-second[1])**2)

def getXDistance(first, second):
  return abs(first[0]-second[0])

def getYDistance(first, second):
  return abs(first[1]-second[1])

def getRelativeLocation(center, reference):
  # Quadrents are defined as follows:
  # 2 | 1
  # 3 | 4
  (xCenter, yCenter) = center
  (xReference, yReference) = reference

  if xCenter < xReference and yCenter > yReference:
    return 'NE'
  elif xCenter > xReference and yCenter > yReference:
    return 'NW'
  elif xCenter > xReference and yCenter < yReference:
    return 'SW'
  elif xCenter < xReference and yCenter < yReference:
    return 'SE'
  elif xCenter < xReference and yCenter == yReference:
    return 'E'
  elif xCenter > xReference and yCenter == yReference:
    return 'W'
  elif xCenter == xReference and yCenter < yReference:
    return 'S'
  elif xCenter == xReference and yCenter > yReference:
    return 'N'
  else:
    return 'Else'

def createVerticalWall(hunterLocation, walls):
  x = hunterLocation[0]
  minY = getWallCoordinate(hunterLocation, walls, 'min', 'y')
  maxY = getWallCoordinate(hunterLocation, walls, 'max', 'y')
  return [(x, minY), (x, maxY)]

def createHorizontalWall(hunterLocation, walls, gap = 0):
  y = hunterLocation[1]
  minX = getWallCoordinate(hunterLocation, walls, 'min', 'x')
  maxX = getWallCoordinate(hunterLocation, walls, 'max', 'x')
  return [(minX+gap, y), (maxX, y)]

def getWallCoordinate(hunterLocation, walls, minMax, xY):
  (xHunter, yHunter) = hunterLocation
  if minMax == 'min':
    if xY == 'x':
      possibleX = [x1+1
                   for (_, (x1, y1), (x2, y2)) in walls
                   if yHunter in range(y1, y2+1)
                   if xHunter > x1]
      return max(possibleX+[0])
    elif xY == 'y':
      possibleY = [y1+1
                   for (_, (x1, y1), (x2, y2)) in walls
                   if xHunter in range(x1, x2+1)
                   if yHunter > y1]
      return max(possibleY+[0])
  elif minMax == 'max':
    if xY == 'x':
      possibleX = [x1-1
                   for (_, (x1, y1), (x2, y2)) in walls
                   if yHunter in range(y1, y2+1)
                   if xHunter < x1]
      return min(possibleX+[499])
    elif xY == 'y':
      possibleY = [y1-1
                   for (_, (x1, y1), (x2, y2)) in walls
                   if xHunter in range(x1, x2+1)
                   if yHunter < y1]
      return min(possibleY+[499])
