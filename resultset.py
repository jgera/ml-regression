

###############################################################################


class DataResult(object):

    def __init__(self, label_value, learner_value, predicted_label=None):
        self.label = label_value # actual label
        self.score = learner_value # what the learner produced
        self.prediction = predicted_label # according to some operating point

    def __str__(self):
        return 'label: {}, score: {}, prediction: {}'.format(self.label,
                                                             self.score,
                                                             self.prediction)

    def __repr__(self):
        return '{}({}, {}, {})'.format(self.__class__.__name__, self.label,
                                       self.score, self.prediction)


###############################################################################


def applyop(operating_point, results):
    '''Return a new list of DataResults with updated predictions.'''
    return [DataResult(dr.label, dr.score, int(dr.score > operating_point)) \
            for dr in results]


def analyze(results):
    '''Produce a confusion matrix and error-tables data for DataResults.'''

    # initialize
    cmet = {'tp':0.0,
            'fn':0.0,
            'fp':0.0,
            'tn':0.0}

    # categorize each result
    for dr in results:
        cmet['tp'] += dr.label == 1 and dr.prediction == 1
        cmet['fn'] += dr.label == 1 and dr.prediction == 0
        cmet['fp'] += dr.label == 0 and dr.prediction == 1
        cmet['tn'] += dr.label == 0 and dr.prediction == 0

    # false positive rate (false alarms)
    # fraction of negatives which are misclassified as positive
    # fraction of ALL legit emails which are in the spam folder
    cmet['fpr'] = cmet['fp'] / (cmet['fp'] + cmet['tn'])

    # false negative rate (missed spams)
    # fraction of positives which are misclassified as negative
    # fraction of the ALL spam emails which are in the inbox
    cmet['fnr'] = cmet['fn'] / (cmet['tp'] + cmet['fn'])

    # true positive rate (detections)
    # fraction of positives which are classified as positive
    # fraction of the ALL spam emails which are in the spam box
    cmet['tpr'] = cmet['tp'] / (cmet['fn'] + cmet['tp'])

    # overall error rate (mistakes)
    # fraction of all data points which are misclassified
    # fraction of ALL emails which are someplace they aren't supposed to be
    cmet['oer'] = (cmet['fp'] + cmet['fn']) / len(results)
    #
    return cmet


def minerrop(results):
    '''Return the operating point which minimizes overall error.'''
    op = 0.0
    et = analyze(applyop(op, results))
    direction = 0.1 * (1 if et['fpr'] > et['fnr'] else -1)
    preverr = et['oer']
    while True:
        op += direction
        et = analyze(applyop(op, results))
        if et['oer'] > preverr:
            return op - direction
        else:
            preverr = et['oer']


def rocdata(results):
    '''Return all (tp rate, fp rate) pairs accross all operating points.'''
    results = results[:]
    # sort data points by score
    results.sort(key=lambda dr: dr.score)
    # make first pair such that, for all dr, prediction is +
    cmet = analyze(applyop(results[0].score - 1, results))
    pairs = [(cmet['fpr'], cmet['tpr'])]
    # make the rest such that on the final one, for all dr, prediction is -
    for dr in results:
        cmet = analyze(applyop(dr.score, results))
        pairs.append((cmet['fpr'], cmet['tpr']))
    return pairs


def auc(rocdata):
    r = rocdata[:]
    r.reverse()
    return 0.5 * sum([(x1 - x0) * (y1 + y0) \
                      for (x0, y0), (x1, y1) in zip(r, r[1:])])


###############################################################################
