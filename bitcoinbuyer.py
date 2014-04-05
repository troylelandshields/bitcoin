"""
Bitcoin Buyer.

-p = Buy and sell perfectly according to whether or not the price of bitcoin will go up or down tomorrow.

-r = Buy randomly!

-l = Buy according to the logReg

-c = Buy according to the CART

-t = Always buy bitcoin

-b = Only buy if both cart and logreg recommend buying

"""

import sys
import getopt
import csv
import random
import math
import locale
locale.setlocale( locale.LC_ALL, '' )

perf = False
rand = False
logReg = False
cart = False
logAndCart = False
alwaysTrue = False
money = 1000
bitcoin = 0
cutoff = 0.5


def buyBitcoin(price):
  global money, bitcoin
  if money >= 100:
    money -= 100
    bitcoin += (100/price)
  else:
    bitcoin+=money/price
    money=0


def sellBitcoin(price):
  global money, bitcoin
  bitcoinToSell = 100/price
  if bitcoin > bitcoinToSell:
    money+=bitcoinToSell*price
    bitcoin -= bitcoinToSell
  else:
    money+=bitcoin*price
    bitcoin = 0

def runTest(filePath):
  global money, bitcoin, rand, perf, logReg, cart, alwaysTrue, cartAndLog

  bought = 0
  sold = 0
  endValue = 0
  with open(filePath, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
          if perf:
            recommendation = "TRUE" == row[12]
          elif rand:
            recommendation = random.choice([True, False])
          elif logReg:
            recommendation = getRecommendation(float(row[2]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11]))
          elif cart:
            recommendation = getCart(float(row[2]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11]))
          elif alwaysTrue:
            recommendation = True
          elif cartAndLog:
            t1 = getRecommendation(float(row[2]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11]))
            t2 = getCart(float(row[2]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11]))
            recommendation = t1 and t2

          if recommendation:
            #print "Buying bitcoin"
            bought+=1
            buyBitcoin(float(row[0]))
          else:
            #print "Selling bitcoin"
            sold+=1
            sellBitcoin(float(row[0]))
          t = money+(bitcoin * float(row[0]))
          endValue = t
          #print "Cash       : \t\t\t $", locale.currency(money, grouping=True)
          #print "Bitcoin    : \t\t\t $", bitcoin
          #print
          #print "Total value: \t\t\t $", t
          #print
        except Exception as e:
          pass
          #print e
  print
  print "Final value: \t\t\t$", locale.currency(endValue, grouping=True)
  print
  print "Days bought bitcoin:", bought
  print "Days sold bitcoin:  ", sold


const = 3555.745605
b1 = -0.03341673
b2 = -151.0948181
b3 = -181.1034241
b4 = -2402.593262
b5 = -1595.167358
b6 = 238.4460754
b7 = 123.7716751
b8 = 162.3624268
b9 = 185.761734


def getRecommendation(costPrctTrxn, Can_conv_rate, Can_rec_rate, Euro_conv_rate, Euro_rec_rate,GBP_conv_rate, GBP_rec_rate, USD_conv_rate, USD_rec_rate):
  global const, b1, b2, b3, b4, b5, b6, b7, b8, b9, cutoff
  p = (math.e ** (const + (b1 * costPrctTrxn) + (b2 * Can_conv_rate) + (b3 * Can_rec_rate)
  + (b4 * Euro_conv_rate) + (b5 * Euro_rec_rate) + (b6 * GBP_conv_rate) + (b7 * GBP_rec_rate)
  + (b8 * USD_conv_rate) + (b9 * USD_rec_rate)))/(1+(math.e ** (const + (b1 * costPrctTrxn) + (b2 * Can_conv_rate) + (b3 * Can_rec_rate)
  + (b4 * Euro_conv_rate) + (b5 * Euro_rec_rate) + (b6 * GBP_conv_rate) + (b7 * GBP_rec_rate)
  + (b8 * USD_conv_rate) + (b9 * USD_rec_rate))))

  if(p > cutoff):
    return True
  else:
    return False

s1 = 5.2507
s2 = 2.4825
s3 = 0.8173
s4 = 1.0821
s5 = 1.5418
s6 = 1.0742

def getCart(costPrctTrxn, Can_conv_rate, Can_rec_rate, Euro_conv_rate, Euro_rec_rate,GBP_conv_rate, GBP_rec_rate, USD_conv_rate, USD_rec_rate):
  if(costPrctTrxn < s1):
    if(costPrctTrxn < s2):
      if(Euro_conv_rate < s3):
        if(costPrctTrxn < s5):
          return True
        else:
          return False
    else:
      if(USD_conv_rate < s4):
        if(Can_conv_rate < s6):
          return True
        else:
          return True
      else:
        return True
  else:
    return False
  return True


def main():
  global perf,rand,logReg,cart,alwaysTrue,cartAndLog
  # parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hprlctb", ["help"])

  except getopt.error, msg:
    print msg
    print "for help use --help"
    sys.exit(2)

  # process options
  for o, a in opts:
    if o in ("-h", "--help"):
      print __doc__
      sys.exit(0)
    if o in ("-p"):
      perf = True
      print "Running Perfect"
    if o in ("-r"):
      rand = True
      print "Running Random"
    if o in ("-l"):
      logReg = True
      print "Running LogReg"
    if o in ("-c"):
      cart = True
      print "Running Cart"
    if o in ("-t"):
      alwaysTrue = True
      print "Always Buying bitcoin"
    if o in ("-b"):
      cartAndLog = True
      print "Using both CART and LogReg"


  # process arguments
  for arg in args:
    process(arg)

def process(arg):
  runTest(arg)

if __name__ == "__main__":
  main()
