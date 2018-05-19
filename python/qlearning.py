from util import *
from config import *
from mdp import *
import numpy as np
import math

def basicFeatureExtractor(state, action):
  i, n, b, ad, pctr, imps, cost = state
  features = [] #list of (key, value) pairs
  features.append( ( ("avg budget", math.floor(b/(10*n) * 10)), 1) )
  features.append( (("pctr", round(pctr, 2)), 1) )
  return features

def main():
  mdp  = makeMDP(campaignNum=0, B=1323253)
  explorationProb = 0.2
  qLearner = QLearningAlgorithm(mdp.actions, mdp.discount(), basicFeatureExtractor, explorationProb)
  simulate(mdp, qLearner, numTrials=1000, maxIterations=1000000, verbose=True, sort=False)

if __name__ == '__main__':
  main()