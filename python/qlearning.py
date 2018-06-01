from util import *
from config import *
from mdp import *
import numpy as np
import math

def getPctrBucket(pctr, numBuckets):
  if pctr == 0:
    return numBuckets
  pwr2 = min(math.log(pctr)/math.log(1./2), numBuckets)
  string = "1/2^" + str(pwr2)
  return string

def basicFeatureExtractor(state, action):
  i, n, b, pctr, imps, cost = state
  features = []
  budget = math.floor(b/100000)*100000
  num = math.floor(n/1000)*1000
  # features.append((action, 1))
  # features.append((round(pctr, 2), 1))
  features.append((("action-pctr", action, getPctrBucket(pctr, 10)), 1) )
  # features.append((("action-pctr-budget", action, getPctrBucket(pctr, 10), budget), 1))
  # features.append((("action-budget", action, budget), 1) )
  # features.append((("action-num", action, num), 1) )
  # features.append((("budget-num", budget, num), 1) )
  #features.append(("pctr-big", pctr > .5)) #list of (key, value) pairs
  #features.append(("pctr-small", pctr <= .5)) #list of (key, value) pairs
  #features.append(("action = " + action, 1))
  #features.append( (("budget", math.floor(b/100)*100), 1) )
  #features.append(  (("impressions-left", math.floor(n/100)*100), 1)   )
  #features.append( (("pctr-small", pctr < 0.1 and pctr > 0.0), 1) )
  #features.append( (("pctr-big", pctr >= 0.1), 1) )
  return features

def main():
  camp = campaigns[8]
  resultPath = logPath + str(camp) + "/qlearning/v0-rewards.txt"
  mdp = makeMDP(camp=camp, c0=1./32) #1323253
  explorationProb = 0.01
  qLearner = QLearningAlgorithm(mdp.actions, mdp.discount(), basicFeatureExtractor, explorationProb)
  simulate(mdp, qLearner, numTrials=1000, maxIterations=1000000, verbose=True, sort=False, resultPath=resultPath, calculateLoss=False)

if __name__ == '__main__':
  main()