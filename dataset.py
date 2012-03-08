# local
import progress as pg


###############################################################################


class DataPoint(object):

    def __init__(self, feature_value_vector, label_value):
        self.features = feature_value_vector # data
        self.label = label_value # actual label

    def __str__(self):
        return '{} labeled {}'.format(self.features, self.label)

    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__, self.features,
                                   self.label)


###############################################################################


def loadfeature(s, f):
    '''Load a single feature value from a string.'''
    changetype, checkvalue = f
    d = changetype(s)
    if checkvalue(d):
        return d
    else:
        raise ValueError(d + ' fails value check in ' + f)


def loadfile(dfile, linect, dformat):
    '''Load linect lines from labeled data in dfile according to dformat.
    Return a list of DataPoint instances.

    dfile   -- file name
                -- one data point per line
                -- values are separated by commas
                -- final value is the label

    dformat -- data format list
                -- tuples with a function to coerce the vaulue and a function
                   which returns false if the value is invalid
                   eg:
                   >>> fmt = 48 * [(float, lambda x: 0 <= x <= 100   )] + \
                              6 * [(int,   lambda x: 0 < x           )] + \
                              1 * [(int,   lambda x: x == 1 or x == 0)]

    '''
    print 'Loading "{}"'.format(dfile)
    data = []
    with open(dfile, mode='rb') as fd:
        with pg.Progress(linect, 2, pg.bar('Lines', 32)) as pr:
            for line in fd:
                # clean the data & create the datapoint
                cleandata = [loadfeature(raw.strip(), fmt) \
                             for raw, fmt in zip(line.split(','), dformat)]
                data += [DataPoint(cleandata[:-1], cleandata[-1])]
                # indicate progress
                try:
                    pr.next()
                except TypeError:
                    break
    return data


###############################################################################


def applykernel(data, kernel):
    '''Apply a function to each vector of feature values *IN PLACE*.
    Return a list of DataPoint instances.

    data -- list of DataPoint instances

    kn   -- function [[number] --> [number]]
         -- transform a single feature for all datapoints

    NOTE: Transformation is not performed in place, but resultant data is
    stored in place.

    '''
    # rotate to a list of feature vectors
    lofv = zip(*[dp.features for dp in data])
    # transform each vector
    lov = [kernel(f) for f in lofv]
    # rotate back into data points
    for dp, features in zip(data, zip(*lov)):
        dp.features = features


###############################################################################
