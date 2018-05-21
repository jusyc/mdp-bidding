from util import *
from config import *
from mdp import *
import numpy as np
import math

def basicFeatureExtractor(state, action):
  i, n, b, ad, pctr, imps, cost = state
  features = []
  budget = math.floor(b/1000)*1000
  num = math.floor(n/1000)*1000
  # features.append((action, 1))
  # features.append((round(pctr, 2), 1))
  features.append((("action-pctr", action, round(pctr, 2)), 1) )
  # features.append((("action-budget", action, budget), 1) )
  # features.append((("action-num", action, num), 1) )
  features.append((("budget-num", budget, num), 1) )
  #features.append(("pctr-big", pctr > .5)) #list of (key, value) pairs
  #features.append(("pctr-small", pctr <= .5)) #list of (key, value) pairs
  #features.append(("action = " + action, 1))
  #features.append( (("budget", math.floor(b/100)*100), 1) )
  #features.append(  (("impressions-left", math.floor(n/100)*100), 1)   )
  #features.append( (("pctr-small", pctr < 0.1 and pctr > 0.0), 1) )
  #features.append( (("pctr-big", pctr >= 0.1), 1) )
  return features

def main():
  camp = campaigns[0]
  resultPath = logPath + str(camp) + "/qlearning/v0-rewards.txt"
  mdp  = makeMDP(camp=camp, B=1323253) #1323253

  vi = ValueIteration();
  vi.solve(mdp)
  print "V: ", vi.V 
if __name__ == '__main__':
  main()
