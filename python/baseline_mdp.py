# Given a policy, run the MDP on the policy over a given ad campaign
# Code based off of CMDP paper code

import numpy as np
from config import *
from generate_pdfs import *

def run(auction, N, policy, budget, pctr_pdf, pctr_bins, bid_log, logging=False, verbose=False):
  log = "{:>8}\t{:>10}\t{:>8}\t{:>8}\t{:>10}\t{:>10}\n".format("i","bid_price", "win_price", "click", "budget", "cost")
  if logging:
    bid_log.append(log)
  if verbose:
    print(log)

  b = budget #???
  nImps = 0
  nClicks = 0
  cost = 0

  for i in range(N):
    price = auction["prices"][i]
    click = auction["clicks"][i]
    pctr = auction["pctr"][i]
    index = np.digitize(pctr, pctr_bins) - 1
    a = max(0, min(b, policy[index]))

    if a >= price:
        b -= price #decrement budget
        nImps += 1 #won 1 impression
        nClicks += click #won 0 or 1 clicks
        cost += price #increment cost

    log = "{:>8}\t{:>10}\t{:>8}\t{:>8}\t{:>10}\t{:>10}\n".format(i, a, price, nClicks, b, cost)
    if logging:
      bid_log.append(log)
    if verbose:
      print(log)

  return nImps, nClicks, cost

def medianMarketPricePolicy(m_pdf):
  m, n = m_pdf.shape
  policy = np.zeros((m,))
  for i in range(m):
    cumScore = 0
    for j in range(n):
      cumScore += m_pdf[i, j]
      if cumScore >= 0.5:
        policy[i] = j + 1
        break

  return policy


def calculateBudget(c0, N):
  prices_train = np.load(outPath + camp + "/train/prices.npy")
  m_mean = np.mean(prices_train, axis=None)
  B = m_mean * c0 * N

  return int(B)

if __name__ == '__main__':
  camp = campaigns[0]
  dataPath = outPath + camp + "/test/"

  auction = {}
  auction["pctr"] = np.load(dataPath + "pCTR.npy")
  auction["prices"] = np.load(dataPath + "prices.npy")
  auction["clicks"] = np.load(dataPath + "clicks.npy")

  #calculating distributions of CTR and market price
  bins = makeBins()
  pctr_pdf = get_pctr_pdf(auction["pctr"], bins)

  m_pdf = get_m_pdf(auction["prices"], auction["pctr"], pctr_pdf, bins)

  #create baseline policy
  policy_name = "baseline"
  baseline = medianMarketPricePolicy(m_pdf)

  logging = True

  #calulating budget
  c0_list = ["32", "16", "8", "4"]
  for c0_str in c0_list:
    c0 = 1/float(c0_str)
    N = len(auction["clicks"])
    B = calculateBudget(c0, N)

    #setting up logging
    bid_log = []

    #test baseline policy
    run(auction, N=N, policy=baseline, budget=B, pctr_pdf=pctr_pdf, pctr_bins=bins,
        bid_log=bid_log, logging=logging, verbose=False)

    if logging:
      with open(logPath + camp + "/" + policy_name + "/" + c0_str + ".txt", "w") as f:
        for line in bid_log:
          f.write("{}\n".format(line))
