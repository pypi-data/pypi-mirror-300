import argparse
from guryansh_topsis import topsis
import sys

def main():
    if len(sys.argv) != 5:
        print("Error: Incorrect number of parameters.")
        print("Usage: guryansh_topsis <inputFileName> <Weights> <Impacts> <resultFileName>")
    else:
        inputFileName = sys.argv[1]
        weights = sys.argv[2]
        impacts = sys.argv[3]
        resultFileName = sys.argv[4]
        topsis(inputFileName, weights, impacts, resultFileName)


if __name__ == "__main__":
    main()
