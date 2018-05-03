def log(msg):
  if isLogging:
    print(msg)

def loadData(filename):
  log("Loading data...")
  with open(inName) as f:
    lines = f.readlines()
  #data in format:
  #click(0,1) winning_price(int) features(featindex1:1 featindex2:1 featindex3:1 ...)
  log("Reformatting data...")
  d = [(arr[0], arr[1], {int(k):int(v) for k,v in (x.split(":") for x in arr[2:])})
        for arr in (line.split(" ") for line in lines)]

  return d

#Setting up variables
inPath = "../../make-ipinyou-data/"
outPath = "../data/"
campaigns = ["1458", "2261", "2997", "3386", "3476", "2259", "2821", "3358", "3427"]

camp = campaigns[0]

inTrainName = inPath + camp + "/" +  "train.yzx.txt"
outTrainPath = outPath + camp + "/" + "train.theta.txt"

inTrainName = inPath + camp + "/" + "test.yzx.txt"
outTrainPath = outPath + camp + "/" + "test.theta.txt"

isLogging = True

#Loading data
d_train = loadData(inTrainName)

#Training logistic regression model on train data
#Input: features
#Output: P(click)

#Using model to evaluate predicted click through rate (pCTR) on train and test datasets

print(d[0])