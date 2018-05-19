from util import *
from config import *
import numpy as np

class BiddingMDP(MDP):
  def __init__(self, N, B, ads, prices, clicks, pctrs, maxBidPrice):
    self.N = N
    self.B = B
    self.ads = ads
    self.prices = prices
    self.clicks = clicks
    self.pctrs = pctrs
    self.maxBidPrice = 300

  def startState(self):
    #STATE = (#bids so far, #bids remaining, budget remaining, ad features, pctr, #impressions, amount spent)
    return (0, self.N, self.B, self.ads[0], self.pctrs[0], 0, 0)


  def actions(self, state):
    i, n, b, ad, pctr, imps, cost = state
    return [x for x in range(0, min(self.maxBidPrice, b) + 1, 10)]

  def succAndProbReward(self, state, action):
    i, n, b, ad, pctr, imps, cost = state

    if (n == 1) or (b == 0): # Reached end state
      return []

    click = self.clicks[i]
    winprice = self.prices[i]

    if action >= winprice: # Won last auction
      # if click != 0:
        # print i, ":", click
      newState = (i+1, n-1, b-winprice, self.ads[i+1], self.pctrs[i+1], imps+1, cost+winprice)
      return[(newState, 1., click)]
    else: # Lost last auction
      newState = (i+1, n-1, b, self.ads[i+1], self.pctrs[i+1], imps, cost)
      return[(newState, 1., 0)]

  def discount(self):
    return 1.0

def makeMDP(campaignNum, B, N=-1, maxBidPrice=300):
  camp = campaigns[campaignNum]
  dataPath = outPath + camp + "/test/"

  pctr = np.load(dataPath + "pCTR.npy")
  prices = np.load(dataPath + "prices.npy")
  clicks = np.load(dataPath + "clicks.npy")
  ads = np.load(dataPath + "features.npy")

  if N < 0:
    N = len(clicks)

  #make MDP
  mdp = BiddingMDP(N=N, B=B, ads=ads, prices=prices, clicks=clicks, \
                  pctrs=pctr, maxBidPrice=maxBidPrice)

  return mdp