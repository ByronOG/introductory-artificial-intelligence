# ----------------------------------------------------------------------
# Name:        classify
# Purpose:     Homework 9
#
# Author:      Rula Khayrallah
#
# Copyright ©  Rula Khayrallah
# ----------------------------------------------------------------------
"""
A machine learning classifier

usage:
classify.py [-h] [{perceptron,knn}] [{digits,iris}] [hyperparameter]

positional arguments:
  {perceptron,knn}  Which classification algorithm?
  {digits,iris}     Which dataset?
  hyperparameter    How many iterations?/ What value of k?

optional arguments:
  -h, --help        show this help message and exit
"""
import argparse
import classifiers
import digits
import iris

def compute_accuracy(predictions, data):
    """
    Compute the accuracy as the percentage of correct prediction over
    the total number of examples processed
    :param predictions: A list of the predicted labels
    :param data: A list of the example objects
    """
    total = len(data)
    correct = [predictions[i] == data[i].label
               for i in range(total)].count(True)
    return correct / total * 100

def report(filename, predictions, data, phase):
    """
    Write the predictions to the specified file and print the accuracy.
    :param filename (string): name of the output file
    :param predictions: list of predicted labels
    """
    with open(filename, 'w', encoding='utf-8') as outfile:
        for p in predictions:
            outfile.write(f'{p}\n')
    accuracy = compute_accuracy(predictions, data)
    print(f'{phase} accuracy: {accuracy:.2f}%')


def get_data(dataset, phase):
    """
    Get the training/validation/test data from the files.
    :param dataset: (string) digits or iris
    :param phase: train, validation or test
    :return: a list of Example objects representing the data for the
    given dataset.
    """
    if dataset == "digits":
        data = digits.read(f'{dataset}/{phase}images.txt',
                           f'{dataset}/{phase}labels.txt')
    elif dataset == "iris":
        data = iris.read(f'{dataset}/{phase}.csv')
    return data

def perceptron(dataset, iterations):
    """
    Train, validate and test a Perceptron classifier on the given
    dataset.
    The validation output is saved in 'dataset_Validation_output.txt'
    The test output is saved in 'dataset_Test_output.txt'
    :param dataset: (string) digits or iris
    :param iterations: integer - number of iteration to use when
    training the perceptron.
    """
    print('Training...')
    data = get_data( dataset, "train")
    all_labels = tuple(sorted({example.label for example in data}))
    p = classifiers.Perceptron(all_labels, iterations)
    p.train(data)

    for phase in ("Validation", "Test"):
        print(f'{phase} in progress...')
        data = get_data(dataset, phase)
        predictions = [p.predict(f) for f in data]
        report(f'{dataset}_{phase}_output.txt', predictions, data, phase)


def knn(dataset, k):
    """
    Classify data based on the nearest k neighbors.
    :param dataset: (string) digits or iris
    :param k: number of neighbors
    :return:
    """
    training_data = get_data( dataset, "train")
    for phase in ("Validation", "Test"):
        print(f'{phase} in progress...')
        data = get_data(dataset, phase)
        predictions = [classifiers.predict_knn(training_data, example, k)
                       for example in data]
        report(f'{dataset}_{phase}_output.txt', predictions, data, phase)


def get_arguments():
    """
    Parse and validate the command line arguments
    :return: (tuple containing the various arguments specified
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('classifier',
                        help='Which classification algorithm?',
                        nargs='?',
                        choices=['perceptron', 'knn'],
                        default='perceptron')
    parser.add_argument('dataset',
                        help='Which dataset?',
                        nargs='?',
                        choices=['digits', 'iris'],
                        default='digits')
    parser.add_argument('hyperparameter',
                        help='How many iterations?/ What value of k?',
                        nargs = '?',
                        type=int,
                        default=1)
    arguments = parser.parse_args()
    dataset = arguments.dataset
    classifier = arguments.classifier
    hyperparameter = arguments.hyperparameter
    return dataset, classifier, hyperparameter


def main():
    dataset, classifier, hyperparameter = get_arguments()
    classification_algorithm = globals()[classifier]
    classification_algorithm(dataset, hyperparameter)

if __name__ == '__main__':
    main()
