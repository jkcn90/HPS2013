import operator
from random import randint, shuffle, choice
from itertools import combinations_with_replacement, ifilter, permutations, islice, combinations

def playRandom(candidates, numberOfAttributes):
  nextCandidate = [randint(0,1) for r in range(0, numberOfAttributes)]
  return nextCandidate

def playBruteForce(candidates, numberOfAttributes):
  possibleCombinationOfWeights = list(getIfilter(numberOfAttributes))
  possibleWeights = getPermutationOfWeights(possibleCombinationOfWeights)

  (bestWeights, _) = getBestWeights(candidates, possibleWeights)
  possibleCandidates = getFilteredCandidateList(candidates, bestWeights)
  nextCandidate = list(possibleCandidates[0])
  return nextCandidate

def playSimulatedAnnealing(candidates, numberOfAttributes):
  #if randint(0, 1) == 1:
  #  nextCandidate = playRandom(candidates, numberOfAttributes)
  #  return
  singleCandidateParsing(candidates, numberOfAttributes)
  (bestWeights, cumulativeDifferences) = getBestWeights(candidates, [getRandomWeightSelection(numberOfAttributes)])

  maxTemperature = 250
  for k in range(maxTemperature):
    temperature = (k/float(maxTemperature)) * 100
    if randint(0, 100) > temperature:
      weightSelection = [getRandomWeightSelection(numberOfAttributes) for _ in range(maxTemperature-k)]
    else:
      if cumulativeDifferences[0] > 1.1:
        minRotated = rotateMin(candidates, bestWeights, cumulativeDifferences)
        shakenWeights = shakeZeros(candidates, minRotated, cumulativeDifferences)
      else:
        shakenWeights = shakeZeros(candidates, bestWeights, cumulativeDifferences)
      #shakenWeights = shakeZeros(candidates, bestWeights, cumulativeDifferences)
      swappedWeights = swapPositiveNegative(candidates, shakenWeights, cumulativeDifferences)
      #weightSelection = getNeighborWeightSelecion(swappedWeights)
      weightSelection = swappedWeights

    #weightSelection = list(set(getPermutationOfWeights(randomWeightSelection)))
    (thisBestWeights, thisCumulativeDifferences) = getBestWeights(candidates, weightSelection)
    #print(thisCumulativeDifferences)

    if (cumulativeDifferences[0] > thisCumulativeDifferences[0] and
        (cumulativeDifferences[1] > thisCumulativeDifferences[1] or
         cumulativeDifferences[2] < thisCumulativeDifferences[2])):
      bestWeights = thisBestWeights
      cumulativeDifferences = thisCumulativeDifferences
      print(bestWeights)
      print(cumulativeDifferences)

    if cumulativeDifferences[0] < 0.05:
      possibleCandidates = getFilteredCandidateList(candidates, bestWeights)
      if len(possibleCandidates) > 0:
        break

  possibleCandidates = getFilteredCandidateList(candidates, bestWeights)
  if len(possibleCandidates) < 1:
    nextCandidate = playRandom(candidates, numberOfAttributes)
  else:
    nextCandidate = list(possibleCandidates[0])
  return nextCandidate

def rotateMin(candidates, bestWeights, cumulativeDifferences):
  bestWeights = bestWeights[0]
  minIndicies = [i for (i,w) in enumerate(bestWeights) if abs(min(bestWeights)-w) < 0.01]

  rotatedMin = []
  for i in minIndicies:
    for k in range(-10, 10):
      rotated = list(bestWeights)
      rotated[i] = k * 0.1
      rotatedMin += [tuple(rotated)]
  (thisBestWeights, thisCumulativeDifferences) = getBestWeights(candidates, rotatedMin)
  if cumulativeDifferences[0] > thisCumulativeDifferences[0]:
    return thisBestWeights
  return [bestWeights]

def shakeZeros(candidates, bestWeights, cumulativeDifferences):
  bestWeights = bestWeights[0]
  zerosWeightsIndex = [i for (i,w) in enumerate(bestWeights) if abs(w) < 0.5]

  shakenWeights = []
  for i in zerosWeightsIndex:
    shaken1 = list(bestWeights)
    shaken2 = list(bestWeights)
    shaken1[i] = randint(80, 110) / float(100)
    shaken2[i] = -randint(80, 110) / float(100)
    shakenWeights += [tuple(shaken1)]
    shakenWeights += [tuple(shaken2)]
  (thisBestWeights, thisCumulativeDifferences) = getBestWeights(candidates, shakenWeights)
  if cumulativeDifferences[0] > thisCumulativeDifferences[0]:
    return thisBestWeights
  return [bestWeights]

def swapPositiveNegative(candidates, bestWeights, cumulativeDifferences):
  bestWeights = tuple(bestWeights[0])
  positiveWeightsIndex = [i for (i,w) in enumerate(bestWeights) if w > 0]
  negativeWeightsIndex = [i for (i,w) in enumerate(bestWeights) if w < 0]

  swappedWeights = []
  for i in positiveWeightsIndex:
    for j in negativeWeightsIndex:
      swapped = list(bestWeights)
      swapped[i], swapped[j] = 0.5 * swapped[j], swapped[i]
      swappedWeights += [tuple(swapped)]
  (thisBestWeights, thisCumulativeDifferences) = getBestWeights(candidates, swappedWeights)
  if cumulativeDifferences[0] > thisCumulativeDifferences[0]:
    return thisBestWeights
  return [bestWeights]

def singleCandidateParsing(candidates, numberOfAttributes):
  for i in range(numberOfAttributes):
    singleCandidate = tuple([100 if i == k else 0 for k in range(numberOfAttributes)])
    test = getBestWeights(candidates, [singleCandidate])

def getNeighborWeightSelecion(weightSelection):
  weightSelection = weightSelection[0]
  positiveWeightsIndex = tuple([i for (i,w) in enumerate(weightSelection) if w > 0])
  negativeWeightsIndex = tuple([i for (i,w) in enumerate(weightSelection) if w < 0])
  
  usedIndex = []
  weights = []
  negativeIndexSwaps = []
  positiveIndexSwaps = []
  if len(positiveWeightsIndex) > 1:
    positiveIndexSwaps = list(combinations(positiveWeightsIndex, 2))
  elif len(negativeWeightsIndex) > 1:
    negativeIndexSwaps = list(combinations(negativeIndexSwaps, 2))

  for (index1, index2) in positiveIndexSwaps+negativeIndexSwaps:
    newWeight = getModifiedWeight(weightSelection, index1, index2)
    weights += newWeight
    usedIndex += [index1, index2]
    positiveWeightsIndex = tuple([i for i in positiveWeightsIndex if i not in usedIndex])
    negativeWeightsIndex = tuple([i for i in negativeWeightsIndex if i not in usedIndex])
  return weights

def getModifiedWeight(weight, index1, index2):
  weight = list(weight)
  weight[index1] += 0.01
  weight[index2] -= 0.1
  return [tuple(weight)]

def getRandomWeightSelection(numberOfAttributes):
  numberOfNegativeWeights = randint(1, numberOfAttributes-1)
  numberOfPositiveWeights = numberOfAttributes-numberOfNegativeWeights

  negativeWeights = getRandomWeightSelection_(numberOfNegativeWeights, numberOfAttributes, True)
  positiveWeights = getRandomWeightSelection_(numberOfPositiveWeights, numberOfAttributes, False)
  weights = positiveWeights+negativeWeights
  shuffle(weights)
  weights = tuple(weights)
  return weights

def getRandomWeightSelection_(numberOfWeights, numberOfAttributes, isNegative):
  weights = []
  for i in range(numberOfWeights):
    currentSum = sum(weights)
    maxAdd = (100-currentSum)
    if i == numberOfWeights-1:
      weight = maxAdd
    else:
      weight = randint(0, maxAdd)
    weights += [weight]

  if isNegative:
    weights = map(operator.mul, weights, [-1 for r in range(len(weights))])
  return weights

def getPermutationOfWeights(unpermutedList):
  permutedListOfList = [list(permutations(x)) for x in unpermutedList]
  permutedList = [x for permutedList in permutedListOfList for x in permutedList]
  return permutedList


def sliceIfilter(ifilterObject, startIndex, endIndex):
  slicedIfilterObject = list(islice(ifilterObject, startIndex, endIndex))
  slicedList = getPermutationOfWeights(slicedIfilterObject)
  return slicedList

def getIfilter(numberOfAttributes):
  return ifilter(sumToPositiveAndNegativeValue,
                 combinations_with_replacement(range(-100, 101),
                 numberOfAttributes)
                )

def getFilteredCandidateList(candidates, weightEstimates):
  candidatesList = [tuple(candidate[0]) for candidate in candidates]
  possibleCandidates = list(
                            set(
                                [tuple([1 if value > 0 else 0 for value in weightEstimate])
                                 for weightEstimate in weightEstimates]
                               )
                           )
  filteredPossibleCandidates = [possibleCandidate for possibleCandidate in possibleCandidates if possibleCandidate not in candidatesList]
  return filteredPossibleCandidates

def getBestWeights(candidates, possibleWeights):
  bestCumulativeDifference = tuple([float('Inf') for r in range(3)])
  bestWeightEstimates = []
  
  for testWeight in possibleWeights:
    testWeight = map(operator.mul, testWeight, [0.01 for r in range(len(testWeight))])
    cumulativeDifference = getCumulativeDifference(candidates, testWeight)
    if bestCumulativeDifference[0] > cumulativeDifference[0]:
      bestCumulativeDifference = cumulativeDifference
      bestWeightEstimates = [testWeight]

  return (bestWeightEstimates, bestCumulativeDifference)

def getCumulativeDifference(candidates, testWeight):
  difference = [dotProduct(testWeight, candidate[0]) - candidate[1]
                for candidate
                in candidates]
  cumulativeDifference = sum(map(abs, difference))
  positiveCumulativeDifference = sum([x for x in difference if x > 0])
  negativeCumulativeDifference = sum([x for x in difference if x < 0])
  #positiveCumulativeDifference = [x for (i,x) in enumerate(difference) if x > 0]
  #negativeCumulativeDifference = [x for (i,x) in enumerate(difference) if x < 0]
  return (cumulativeDifference, positiveCumulativeDifference, negativeCumulativeDifference)

def dotProduct(vector1, vector2):
  return sum(map(operator.mul, vector1, vector2))

def sumToPositiveAndNegativeValue(values, targetValue=100):
  positiveSublist = [value for value in values if value > 0]
  negativeSublist = [value for value in values if value < 0]
  if sum(positiveSublist) == targetValue and sum(negativeSublist) == -targetValue:
    return True
  return False

