from util import *
from config import *
from mdp import *
import numpy as np
import math

def basicFeatureExtractor(state, action):
  i, n, b, ad, pctr, imps, cost = state
  features = [("pctr-big", pctr > .5)] #list of (key, value) pairs
  features = [("pctr-small", pctr <= .5)] #list of (key, value) pairs
  #features.append( (("budget", math.floor(b/100)*100), 1) )
  #features.append(  (("impressions-left", math.floor(n/100)*100), 1)   )
  #features.append( (("pctr-small", pctr < 0.1 and pctr > 0.0), 1) )
  #features.append( (("pctr-big", pctr >= 0.1), 1) )
  return features

def main():
  mdp  = makeMDP(campaignNum=0, B=1323253)
  explorationProb = 0.2
  qLearner = QLearningAlgorithm(mdp.actions, mdp.discount(), basicFeatureExtractor, explorationProb)
  simulate(mdp, qLearner, numTrials=1000, maxIterations=1000000, verbose=True, sort=False)

if __name__ == '__main__':
  main()