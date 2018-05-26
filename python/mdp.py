from util import *
from config import *
import numpy as np

class BiddingMDP(MDP):
  def __init__(self, N, B, ads, prices, clicks, pctrs, maxBidPrice):
    self.N = N
    self.B = B
    # self.ads = ads
    self.prices = prices
    self.clicks = clicks
    self.pctrs = pctrs
    self.maxBidPrice = 300

  def startState(self):
    #STATE = (#bids so far, #bids remaining, budget remaining, ad features, pctr, #impressions, amount spent)
    return (0, self.N, self.B, self.pctrs[0], 0, 0)


  def actions(self, state):
    i, n, b, pctr, imps, cost = state
    if b < 300:
      return [0]

    return [0, self.maxBidPrice]
    #return [x for x in range(0, min(self.maxBidPrice, b) + 1, 10)]

  def succAndProbReward(self, state, action):
    i, n, b, pctr, imps, cost = state

    if (n == 1) or (b < self.maxBidPrice): # Reached end state    ...  or (b == 0)
      return []

    click = self.clicks[i]
    winprice = self.prices[i]

    # if click:
    #   print "action:", action
    #   print "price: ", winprice
    #   print "pctr:  ", pctr
    #   print "budget:", b
    #   print "iters: ", n

    if action >= winprice: # Won last auction
      # if click != 0:
        # print i, ":", click
      newState = (i+1, n-1, b-winprice, self.pctrs[i+1], imps+1, cost+winprice)
      reward = click - 100 * winprice/float(self.B)
      return[(newState, 1., reward)]
    else: # Lost last auction
      newState = (i+1, n-1, b, self.pctrs[i+1], imps, cost)
      reward = 0#-click
      return[(newState, 1., reward)]

  def discount(self):
    return 1.0

  def getN(self):
    return self.N

def calculateBudget(c0, N, camp):
  #load from somewhere else!
  prices_train = np.load(outPath + camp + "/train/prices.npy")
  m_mean = np.mean(prices_train, axis=None)
  B = m_mean * c0 * N

  return int(B)

def makeMDP(camp, B=-1, N=-1, maxBidPrice=300, c0=1./32):
  dataPath = outPath + camp + "/test/"

  pctr = np.load(dataPath + "pCTR.npy")
  prices = np.load(dataPath + "prices.npy")
  clicks = np.load(dataPath + "clicks.npy")
  ads = np.load(dataPath + "features.npy")

  if N < 0:
    N = len(clicks)

  if B < 0:
    B = calculateBudget(c0, N, camp)

  print "N:", N
  print "B:", B
  print "nClicks:", np.sum(clicks)
  #make MDP
  mdp = BiddingMDP(N=N, B=B, ads=ads, prices=prices, clicks=clicks, \
                  pctrs=pctr, maxBidPrice=maxBidPrice)

  return mdp



class SmallBiddingMDP(MDP):
  def __init__(self, N, B, prices, clicks, pctrs, maxBidPrice):
    self.N = N
    self.B = B
    self.prices = prices
    self.clicks = clicks
    self.pctrs = pctrs
    self.maxBidPrice = 300

  def binPctr(pctr):
    return round(pctr, 2)

  def startState(self):
    #STATE = #trials remaining, budget remaining, pctr
    return (binPctr(self.pctrs[0]))


  def actions(self, state):
    i, n, b, ad, pctr, imps, cost = state
    if b < 300:
      return [0]

    return [0, 300]
    #return [x for x in range(0, min(self.maxBidPrice, b) + 1, 10)]

  def succAndProbReward(self, state, action):
    pctr, imps, cost = state

    if (n == 1): # Reached end state    ...  or (b == 0)
      return []

    click = self.clicks[i]
    winprice = self.prices[i]

    # if click:
    #   print "action:", action
    #   print "price: ", winprice
    #   print

    if action >= winprice: # Won last auction
      # if click != 0:
        # print i, ":", click
      newState = (binPctr(self.pctrs[i+1]))
      reward = click #- winprice/float(self.B)
      return[(newState, 1., reward)]
    else: # Lost last auction
      newState = (binPctr(self.pctrs[i+1]))
      reward = 0#-click
      return[(newState, 1., reward)]

  def discount(self):
    return 1.0

def makeSmallMDP(camp, B, N=-1, maxBidPrice=300):
  dataPath = outPath + camp + "/test/"

  pctr = np.load(dataPath + "pCTR.npy")
  prices = np.load(dataPath + "prices.npy")
  clicks = np.load(dataPath + "clicks.npy")
  ads = np.load(dataPath + "features.npy")

  if N < 0:
    N = len(clicks)

  #make MDP
  mdp = SmallBiddingMDP(N=N, B=B, ads=ads, prices=prices, clicks=clicks, \
                  pctrs=pctr, maxBidPrice=maxBidPrice)

  return mdp