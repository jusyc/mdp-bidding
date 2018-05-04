
# Generating probability distribution functions for click through rate and market price
# Code based off of CMDP paper code

import numpy as np
from config import *

def makeBins():
  pctr_init = [0]
  bins = [10**(-7), 10**(-6), 10**(-5), 10**(-4), 10**(-3), 10**(-2), 10**(-1)]
  zip_bin = zip(bins, bins[1:])
  for i, j in zip_bin:
    pctr_bins = np. linspace(i, j, num=20)
    pctr_init = np.append(pctr_init, pctr_bins[:-1])
  pctr_bins2 = np.linspace(0.1, 1, num=10)
  pctr_bins = np.append(pctr_init, pctr_bins2)
  nbins = len(pctr_bins)-1
  return pctr_bins, nbins

def get_pctr_pdf(pctr, bins):
  freq, __ = np.histogram(pctr, bins)
  pctr_pdf = freq/(np.sum(freq))

  return pctr_pdf

def get_m_pdf(prices, pctr, pctr_pdf):
  price_bins = [i for i in range(max_bid+2)]
  freq, __ = np.histogram(prices, price_bins)
  m_pdf = freq/(np.sum(freq)) #Add laplace smoothing??

  joint_pdf, __, __ = np.histogram2d(pctr, prices, bins=[pctr_bins, price_bins])
  joint_pdf = joint_pdf/(np.sum(joint_pdf, axis=None))

  m_cond_pdf = np.zeros_like(joint_pdf)

  for i in range(nbins):
    if pctr_pdf[i] == 0:
      m_cond_pdf[i][:] = m_pdf
    else:
      m_cond_pdf[i][:] = joint_pdf[i][:] / pctr_pdf[i]

  assert np.any(np.sum(m_cond_pdf, axis=1) == 1)

  return m_cond_pdf


if __name__ == "__main__":
  camp = campaigns[0]

  dataPath = outPath + camp + "/test/"

  pctr = np.load(dataPath + "pCTR.npy")
  prices = np.load(dataPath + "prices.npy")

  pctr_bins, nbins = makeBins()

  pctr_pdf = get_pctr_pdf(pctr, pctr_bins)

  m_pdf = get_m_pdf(prices, pctr, pctr_pdf)
