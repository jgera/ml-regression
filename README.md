# Regression Classifiers

These classifiers were part of a [project](http://www.ccs.neu.edu/home/jaa/CS6140.11F/Homeworks/hw.03.html) for my Fall 2011 [machine learning class](http://www.ccs.neu.edu/home/jaa/CS6140.11F/).

To run, put *spambase.data* from the UCI [spambase dataset](http://archive.ics.uci.edu/ml/datasets/Spambase) into the same directory as *regression.py*.

    $ python2 regression.py

This will train a learner on folds 2..10 of the dataset for each of the four combinations of _regression_ or _logistic regression_ paired with either _stochastic learning_ or _batch learning_. Fold 1 is retained for testing. Each learner will print its root mean squared error after every pass and write a file containing data for a ROC curve.

See [my analysis](https://docs.google.com/document/d/1X-QElILvBe5w8qHwWBecVl-pZCs__s_E3kI3tuK1OLU/edit) for a discussion of the results.

-- [PLR](http://f06mote.com)

---

### Perceptron Classifier

There is also a simple perceptron learner in this project folder. To run, put [perceptronData.txt](http://www.ccs.neu.edu/home/jaa/CS6140.11F/Homeworks/perceptronData.txt) into the same directory as *perceptron.py*.

    $ python2 perceptron.py

This will run a single perceptron learner on the provided linearly-separable dataset until convergence.
