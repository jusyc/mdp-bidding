# Given a policy, run the MDP on the policy over a given ad campaign
# Code based off of CMDP paper code, Q-Learning code from class

import mdp
import numpy as np
from config import *
from generate_pdfs import *

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
  policy_name = "qlearning"
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

    #make MDP
    mdp = BiddingMDP(N=N, B=)

    #test baseline policy
    run(auction, N=N, policy=baseline, budget=B, pctr_pdf=pctr_pdf, pctr_bins=bins,
        bid_log=bid_log, logging=logging, verbose=False)

    if logging:
      with open(logPath + camp + "/" + policy_name + "/" + c0_str + ".txt", "w") as f:
        for line in bid_log:
          f.write("{}\n".format(line))


