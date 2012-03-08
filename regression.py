# stdlib
import random
# local
import progress as pg
import resultset
import spambase
import dataset
import stats


FOLDCOUNT = 10
RANDOMSEED = 1337
INDENT = '  '


###############################################################################


class Regression(object):

    def __init__(self):
        raise NotImplementedError

    @staticmethod
    def model(weights, features):
        '''Calculate regression for features given weights.
        [number] [number] --> number
        '''
        return stats.dotprod(weights, features)

    @staticmethod
    def gradient(model, feature, label):
        '''Calculate regression gradient for a weight.
        number number number --> number
        '''
        return (model - label) * feature

    class LogisticRegression(object):

        def __init__(self):
            raise NotImplementedError

        @staticmethod
        def model(weights, features):
            '''Calculate logistic regression for features given weights.
            [number] [number] --> number
            '''
            return stats.logistic(Regression.model(weights, features))

        @staticmethod
        def gradient(model, feature, label):
            '''Calculate logistic regression gradient for a weight.
            number number number --> number
            '''
            return model * (1 - model) * Regression.gradient(model, feature,
                                                             label)


###############################################################################


class GradientDescent(object):

    def __init__(self):
        raise NotImplementedError

    @staticmethod
    def stochastic(weights, datapoint, score, gradient, learningrate):
        '''Gradient descend new weights from a single datapoint.

        weights      -- list of weights
        datapoint    -- DataPoint instance
        score        -- function [weights features --> score]
        gradient     -- function [score feature label --> gradient]
        learningrate -- learning rate parameter (lambda)

        '''
        s = score(weights, datapoint.features)
        return [w - learningrate * gradient(s, datapoint.features[j],
                                            datapoint.label) \
                for j, w in enumerate(weights)]

    @staticmethod
    def stochastic_pass(weights, datapoints, score, gradient, learningrate):
        '''Gradient descend new weights from a list of datapoints.

        This is a wrapper for stochastic which simply completes a full pass
        through the datapoints before returning.

        weights      -- list of weights
        datapoints   -- list of DataPoint instances
        score        -- function [weights features --> score]
        gradient     -- function [score feature label --> gradient]
        learningrate -- learning rate parameter (lambda)

        '''
        newweights = weights[:]
        for dp in datapoints:
            newweights = GradientDescent.stochastic(newweights, dp, score,
                                                    gradient, learningrate)
        return newweights

    @staticmethod
    def batch(weights, datapoints, score, gradient, learningrate):
        '''Gradient-descend new weights from a list of datapoints.

        weights      -- list of weights
        datapoints   -- list of DataPoint instances
        score        -- function [weights features --> score]
        gradient     -- function [score feature label --> gradient]
        learningrate -- learning rate parameter (lambda)

        '''
        return [w - learningrate * sum([gradient(score(weights, dp.features),
                                                 dp.features[j],
                                                 dp.label) \
                                        for dp in datapoints]) \
                for j, w in enumerate(weights)]

    @staticmethod
    def loop(weights, training, score, gradient, learningrate, reducelr,
             gdfunction, maxratio):
        '''A gradient descent loop for either batch or stochastic_pass.

        weights      -- initial weight vector
        training     -- list of DataPoint instances to train on
        score        -- function [weights features --> score]
        gradient     -- function [score feature label --> gradient]
        learningrate -- learning rate parameter (lambda)
        reducelr     -- function [number --> number] to reduce learning rate
        gdfunction   -- function with a signature like GradientDescent.batch
        maxraio      -- maximum newerror:olderror ratio before stopping

        '''
        INDENT = '  '
        print INDENT * 2 + 'Initial learning rate:', learningrate

        # initialize the error
        error = stats.rmse(
            [score(weights, dp.features) for dp in training],
            [dp.label for dp in training])
        print INDENT * 2 + 'Initial Training RMSE:', error

        # loop
        while True:

            # calculate new weights & error
            newweights = gdfunction(weights, training, score, gradient,
                                    learningrate)
            try:
                newerror = stats.rmse(
                    [score(newweights, dp.features) for dp in training],
                    [dp.label for dp in training])
            except OverflowError:
                newerror = error + 1
                print INDENT * 3 + 'Training RMSE: Overflow'
            else:
                if newerror <= error:
                    print INDENT * 2 + 'Training RMSE: v', newerror
                else:
                    print INDENT * 3 + 'Training RMSE: ^', newerror

            # figure out what to do next
            if newerror <= error:
                ratio = newerror / error
                # error went down; accept error and weights
                error = newerror
                weights = newweights
                # do we stop?
                if ratio > maxratio:
                    print INDENT * 2 + 'Finished learning; error ratio:',
                    print ratio, '>', maxratio
                    break
            else:
                # error went up; retry with a smaller lambda
                learningrate = reducelr(learningrate)
                print INDENT * 3 + 'Retrying with learning rate:', learningrate

        # done
        return weights


###############################################################################


def main2(gdname, gdfunction, training, regression, learningrate):
    '''Perform gradient descent with a learner and analyze the results.'''

    # learning rate
    try:
        initiallr, reducelr = learningrate
        suffix = 'dynamic' + str(initiallr)
    except TypeError:
        initiallr = learningrate
        reducelr = lambda x: x
        suffix = initiallr

    # learn
    weights = GradientDescent.loop(
        len(training[0].features) * [0.0],
        training,
        regression.model,
        regression.gradient,
        initiallr,
        reducelr,
        gdfunction,
        0.99)

    # test
    terror = stats.rmse(
        [regression.model(weights, dp.features) for dp in testing],
        [dp.label for dp in testing])
    print INDENT * 2 + 'Testing RMSE:', terror

    ## produce a result set
    results = [resultset.DataResult(dp.label,
                                    regression.model(weights, dp.features)) \
               for dp in testing]

##    ## find a good operating point
##    op = resultset.minerrop(results)
##    print INDENT * 2 + 'Operating Point:', op

##    ## assign predictions
##    results = resultset.applyop(op, results)

    ## output roc data
    roc = resultset.rocdata(results)
    auc = resultset.auc(roc)
    with open('{}-{}_lambda={}_auc={}'.format(regression.__name__, gdname,
                                       suffix, auc).lower(),
              mode='wb') as fd:
        for fpr, tpr in roc:
            fd.write('{}, {}\n'.format(fpr, tpr))


###############################################################################


if __name__ == '__main__':
    print

    # load from file
    spambase.load()
    d = spambase.data

    # zscore feature values
    def pre(lon):
        mu = stats.mean(lon)
        sd = stats.stddev(stats.mvue(lon, mu))
        return stats.zscore(lon, mu, sd)
    dataset.applykernel(d, pre)

    # insert phantom features
    for dp in d:
        dp.features = [1.0] + list(dp.features)

    # roll into folds
    folds = [[] for i in xrange(FOLDCOUNT)]
    k = 0 # kurrent fold
    for dp in d:
        # add to the current fold & switch to the next fold
        folds[k].append(dp)
        k = (k + 1) % FOLDCOUNT

    # unroll to testing & training
    testing = folds[0]
    training = []
    [training.extend(f) for f in folds[1:]]
    del folds

    # randomize testing
    random.seed(RANDOMSEED) # make shuffle the same each time
    random.shuffle(training)

    print 'Testing count:', len(testing)
    print 'Training count:', len(training)

    # do the four learners
    rates = [0.0001,
             (1.0, lambda lr: lr/10),
             0.1,
             0.01]
    for reg in (Regression, Regression.LogisticRegression):
        print '== {} =='.format(reg.__name__)
        for gdfunc in (GradientDescent.stochastic_pass, GradientDescent.batch):
            print INDENT * 1 + '== {} Gradient Descent =='.format(
                gdfunc.__name__.capitalize())
            lr = rates.pop(0)
            main2(gdfunc.__name__, gdfunc, training, reg, lr)


###############################################################################
