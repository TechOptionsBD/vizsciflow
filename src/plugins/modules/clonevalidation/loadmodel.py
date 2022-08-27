import sys
import pickle
import argparse

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Load sims from trained model.')
        parser.add_argument('model', type=str, help='The model path')
        parser.add_argument('simtypes', type=str, nargs='+', help='Type of sims')

        args = parser.parse_args()

        #load the trained Neural Net
        with open(args.model, 'rb') as fileObject:
            loaded_fnn = pickle.load(fileObject)

        network_prediction = loaded_fnn.activate([args.simtypes[0], args.simtypes[1], args.simtypes[2], args.simtypes[3], args.simtypes[4], args.simtypes[5]])

        print(network_prediction[1])

    except Exception as e:
        print >> sys.stderr, 'Error occured while loading sims: ' + str(e)
        sys.exit(1)