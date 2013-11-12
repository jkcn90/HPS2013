import random

class Player:
    __paramsNum = 0
    __posScoreNum = 0
    __negScoreNum = 0
    __initNum = 60
    def __init__(self, paramsNum):
        self.__paramsNum = paramsNum

    def getParamsStr(self):
        self.__posScoreNum = int(self.__paramsNum * 0.6)
        self.__negScoreNum = self.__paramsNum - self.__posScoreNum

        posWeights = []
        negWeights = []
        self.__initWeights(self.__posScoreNum, posWeights)
        self.__initWeights(self.__negScoreNum, negWeights)
        
        self.__subtractWeights(posWeights)
        print 'pos weights = ' + str(posWeights)
        total = self.__getSum(posWeights)
        print 'pos sum = ' + str(total)
        self.__subtractWeights(negWeights)
        print 'neg weights = ' + str(negWeights)
        total = self.__getSum(negWeights)
        print 'neg sum = ' + str(total)

        strout = self.__getOutStr(posWeights, False)
        strout += self.__getOutStr(negWeights, True)

        return strout

    def __getOutStr(self, weights, isNegative):
        tmp = ''
        for w in weights:
            if isNegative:
                tmp += '-'
            if w < 10:
                tmp += '0.0'
            else:
                tmp += '0.'
            tmp += str(w)
            tmp += ' '
        return tmp
        
    def __subtractWeights(self, weights):
        tooMuch = True

        while tooMuch:
            for i in range(0, len(weights)):
                rndNum = random.randint(0, self.__initNum - 1)
                if (rndNum < weights[i]):
                    weights[i] -= rndNum
                if (self.__getSum(weights) <= 100):
                    tooMuch = False
                    break

        sumTmp = self.__getSum(weights)
        diff = 100 - sumTmp
        for i in range(0, diff):
            rndNum = random.randint(0, len(weights) - 1)
            weights[rndNum] += 1
                

    def __getSum(self, weights):
        total = 0
        for s in weights:
            total += s
        return total

    def __initWeights(self, weightNum, weights):
        for i in range(0, weightNum):
            weights.append(self.__initNum)
        
if __name__ == '__main__':
    d = Player(10)
    strout = d.getParamsStr()
    print strout
    
