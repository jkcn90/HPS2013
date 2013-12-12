from time import sleep

class auctionLazy:

  def __init__(self, itemListString):
    itemList = map(int, itemListString.split(' '))
    self.playerId = itemList[0]
    self.numberOfPlayers = itemList[1]
    self.numberOfTypes = itemList[2]
    self.goal = itemList[3]
    self.itemList = itemList[4:]
    self.budget = 100
    self.bidResults = {playerNumber:() for playerNumber in range(self.numberOfPlayers)}
    self.turn = 0

  def getStrategyStr(self):
    item = self.itemList[0]
    # Determine which items are possible to yield an early win
    itemCloseness = getNthIndexOfItem(self.numberOfTypes, item, self.itemList)
    if itemCloseness > self.budget:
      return '0'

    # Check who is closest to winning
    maxMinPrice = 1
    for playerNumber in range(self.numberOfPlayers):
      playerHistory = self.bidResults[playerNumber]
      playerBudget = 100 - sum([x for (_, x) in playerHistory])
      numberOfThisItem = sum([1 for (x, _) in playerHistory if x == item])

      if playerNumber == self.playerId:
        myNumberOfThisItem = numberOfThisItem
        continue

      minPriceList = [y for (x, y) in playerHistory if x == item]
      if len(minPriceList) > 0:
        minPrice = min(minPriceList)
        if maxMinPrice < minPrice:
          maxMinPrice = minPrice

      if numberOfThisItem == self.goal:
        sleep(8)
        if self.budget > playerBudget:
          price = playerBudget+1
        else:
          price = 0
        return str(price)

    if myNumberOfThisItem == self.goal-1:
      return str(self.budget)

    #if myNumberOfThisItem > (3.0 * self.goal)/ 4:
    #  if maxMinPrice < self.budget:
    #    return str(maxMinPrice)

    # Default to 1
    price = 1
    return str(price)

  def setAuctionResult(self, resultString):
    results = map(int, resultString.split(' '))
    player = results[0]
    pricePaid = results[1]
    self.budget = results[2]
    
    # Add new bid to history
    previousHistory = self.bidResults[player]

    item = self.itemList.pop(0)
    newHistory = previousHistory + ((item, pricePaid),)
    
    self.bidResults.update({player:newHistory})

    # Update turn
    self.turn += 1

def getNthIndexOfItem(N, item, list_):
  i = -1
  for x in xrange(N):
    i = list_.index(item, i+1)
  return i
