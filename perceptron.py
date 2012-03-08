# local
import stats


if __name__ == '__main__':

    # load from file
    data = []
    with open('perceptronData.txt', mode='rb') as fd:
        for line in fd:
            data.append([float(field.strip()) for field in line.split('\t')])
    count = len(data)

    # add phantom feature
    for d in data:
        d.insert(0, 1.0)

    # split into positive and negative sets
    pos = [d[:-1] for d in data if d[-1] ==  1.0]
    neg = [d[:-1] for d in data if d[-1] == -1.0]
    assert len(pos) + len(neg) == count
    del data

    # invert negative examples; put them in positive set
    for d in neg:
        pos.append([-f for f in d])
    assert len(pos) == count
    del neg

    # initialize the weight vector
    weights = len(pos) * [0.0]

    # iterate
    iteration = 0
    mistakes = 1
    while mistakes: # should be while iteration < (m * |v|^2) / (d^2)
        iteration += 1
        mistakes = 0
        for d in pos:
            if stats.dotprod(weights, d) > 0:
                pass # good!
            else:
                weights = [w + f for w, f in zip(weights, d)]
                mistakes += 1
        print 'Iteration {}, total mistakes {}'.format(iteration, mistakes)

    print 'Classifier weights: {}'.format(
        ' '.join([str(w) for w in weights]))

    print 'Normalized with threshold: {}'.format(
        ' '.join([str(w/weights[0]) for w in weights[1:]]))
