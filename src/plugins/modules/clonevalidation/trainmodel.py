import argparse
import scipy
#from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
import pandas as pd
import numpy as np


import pybrain
from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer


def load_training_dataSet(fileName):
    data = pd.read_csv(fileName, sep=',', header=None)
    #data.columns = ["state", "outcome"]
    return data


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Load sims from trained model.')
    parser.add_argument('data', type=str, help='The training dataset path.')
    parser.add_argument('output', type=str, help='The output path.')

    args = parser.parse_args()
    myclones_data = load_training_dataSet(arguments['data'])
    myclones_data = myclones_data.values
    inputDim = 8

    means = [(-1, 0), (2, 4), (3, 1)]
    cov = [diag([1, 1]), diag([0.5, 1.2]), diag([1.5, 0.7])]
    alldata = ClassificationDataSet(inputDim, 1, nb_classes=2)

    #input = np.array([ myclones_data[n][16], myclones_data[n][17], myclones_data[n][18], myclones_data[n][15],myclones_data[n][11],myclones_data[n][12],   myclones_data[n][26], myclones_data[n][27]] )

    for n in xrange(len(myclones_data)):
        # for klass in range(3):
        input = np.array(
            [myclones_data[n][16], myclones_data[n][17], myclones_data[n][18], myclones_data[n][15], myclones_data[n][11],
             myclones_data[n][12], myclones_data[n][26], myclones_data[n][27]])
        print(n, "-->", input)
        alldata.addSample(input, int(myclones_data[n][35]))

        tstdata, trndata = alldata.splitWithProportion(0.25)

        print(tstdata)

        tstdata_new = ClassificationDataSet(inputDim, 1, nb_classes=2)
        for n in xrange(0, tstdata.getLength()):
            tstdata_new.addSample(tstdata.getSample(
                n)[0], tstdata.getSample(n)[1])

        trndata_new = ClassificationDataSet(inputDim, 1, nb_classes=2)
        for n in xrange(0, trndata.getLength()):
            trndata_new.addSample(trndata.getSample(
                n)[0], trndata.getSample(n)[1])

        trndata = trndata_new
        tstdata = tstdata_new

        #print("Before --> ", trndata)

        trndata._convertToOneOfMany()
        tstdata._convertToOneOfMany()

        #print("After --> ", trndata)

        print("Number of training patterns: {0}".format(len(trndata)))
        print("Input and output dimensions: {0}, {1}".format(
            trndata.indim, trndata.outdim))
        print("First sample (input, target, class): {0}, {1}, {2}".format(
            trndata['input'][0], trndata['target'][0], trndata['class'][0]))

        fnn = buildNetwork(trndata.indim, 107,
                           trndata.outdim, outclass=SoftmaxLayer)
        trainer = BackpropTrainer(
            fnn, dataset=trndata, momentum=0.1, learningrate=0.05, verbose=True, weightdecay=0.001)

        """
	ticks = arange(-3.,6.,0.2)
	X, Y = meshgrid(ticks, ticks)
	# need column vectors in dataset, not arrays
	griddata = ClassificationDataSet(7,1, nb_classes=2)
	for i in xrange(X.size):
		griddata.addSample([X.ravel()[i],Y.ravel()[i]], [0])
	griddata._convertToOneOfMany()  # this is still needed to make the fnn feel comfy

	"""
        # trainer.trainEpochs(1)
        # trainer.testOnData(verbose=True)
        #print(np.array([fnn.activate(x) for x, _ in tstdata]))

        for i in range(20):
            trainer.trainEpochs(10)
            trnresult = percentError(
                trainer.testOnClassData(), trndata['class'])
            tstresult = percentError(trainer.testOnClassData(
                dataset=tstdata), tstdata['class'])

            print("epoch: %4d" % trainer.totalepochs, "  train error: %5.2f%%" %
                  trnresult, "  test error: %5.2f%%" % tstresult)

            #out = fnn.activateOnDataset(griddata)
            # out = out.argmax(axis=1)  # the highest output activation gives the class
            #out = out.reshape(X.shape)

        import pickle

        with open(out, 'w') as fileObject:
            pickle.dump(fnn, fileObject)

        """

		figure(1)
		ioff()  # interactive graphics off
		clf()  # clear the plot
		hold(True)  # overplot on
		for c in [0, 1, 2]:
			here, _ = where(tstdata['class'] == c)
			plot(tstdata['input'][here, 0], tstdata['input'][here, 1], 'o')
		if out.max() != out.min():  # safety check against flat field
			contourf(X, Y, out)  # plot the contour
		ion()  # interactive graphics on
		draw()  # update the plot

	ioff()
	show()
	"""
