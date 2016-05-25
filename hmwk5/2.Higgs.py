
# coding: utf-8

# In[1]:

# Name: Alex Egg  
# Email: eggie5@gmail.com
# PID: A53112354

from pyspark import SparkContext
sc = SparkContext()


# In[2]:

from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint

from string import split,strip

from pyspark.mllib.tree import GradientBoostedTrees, GradientBoostedTreesModel
from pyspark.mllib.tree import RandomForest, RandomForestModel

from pyspark.mllib.util import MLUtils


# In[3]:

# Read the file into an RDD
# If doing this on a real cluster, you need the file to be available on all nodes, ideally in HDFS.
path='/HIGGS/HIGGS.csv'
inputRDD=sc.textFile(path)


# In[4]:

# Transform the text RDD into an RDD of LabeledPoints
Data=inputRDD.map(lambda line: [float(strip(x)) for x in line.split(',')]).map(lambda a: LabeledPoint(a[0], a[1:]))


# In[5]:

Data1=Data.sample(False,0.1).cache()
(trainingData,testData)=Data1.randomSplit([0.7,0.3])



# In[7]:

from time import time
errors={}
for depth in [10]:
    start=time()
    model=GradientBoostedTrees.trainClassifier(trainingData, categoricalFeaturesInfo={}, numIterations=10, maxDepth=depth,
        learningRate=0.25, maxBins=35)
    errors[depth]={}
    dataSets={'train':trainingData,'test':testData}
    for name in dataSets.keys():  # Calculate errors on train and test sets
        data=dataSets[name]
        Predicted=model.predict(data.map(lambda x: x.features))

        LabelsAndPredictions = data.map(lambda lp: lp.label).zip(Predicted)
        Err = LabelsAndPredictions.filter(lambda (v,p): v != p).count()/float(data.count())
        errors[depth][name]=Err
    print depth,errors[depth],int(time()-start),'seconds'
# Expected test error <= 27.5%
# Expected running time <= 350 seconds
# 10 {'test': 0.2806224626238058, 'train': 0.26497137638847573} 66 seconds
# 10 {'test': 0.27378476281278563, 'train': 0.24796675763802906} 67 seconds



