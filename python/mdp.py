import util
import numpy as np

class BiddingMDP(util.MDP):
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
    # n, b, ad, pctr, imps, clicks, cost = state
    return [x for x in range(min(maxBidPrice, self.B) + 1)]

  def succAndProbReward(self, state, action):
    i, n, b, ad, pctr, imps, cost = state

    if (n == 0) or (b == 0): # Reached end state
      return []

    click = self.clicks[i]
    winprice = self.clicks[i]

    if action >= winprice: # Won last auction
      newState = (i+1, n-1, b-winprice, ads[i+1], pctrs[i+1], imps+1, cost+winprice)
      return[(newState, 1., click)]
    else: # Lost last auction
      newState = (i+1, n-1, b, ads[i+1], pctrs[i+1], imps, cost)
      return[(newState, 1., 0)]

  def discount(self):
    return 1.0
