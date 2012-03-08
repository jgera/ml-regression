# local
import dataset


###############################################################################


SPAM = 1
NOTSPAM = 0


dataformat = []
#             48 continuous real [0,100] attributes of type word_freq_WORD
dataformat += 48 * [(float, lambda x: 0 <= x <= 100)]
#              6 continuous real [0,100] attributes of type char_freq_CHAR
dataformat +=  6 * [(float, lambda x: 0 <= x <= 100)]
#              1 continuous real [1,...] attribute of type capital_run_length_average
dataformat +=  1 * [(float, lambda x: 0 <= x)]
#              1 continuous integer [1,...] attribute of type capital_run_length_longest
dataformat +=  1 * [(int, lambda x: 0 <= x)]
#              1 continuous integer [1,...] attribute of type capital_run_length_total
dataformat +=  1 * [(int, lambda x: 0 <= x)]
#              1 nominal {0,1} class attribute of type spam
dataformat +=  1 * [(int, lambda x: x == SPAM or x == NOTSPAM)]


data = []


def load():
    data.extend(dataset.loadfile('spambase.data', 4601, dataformat))


###############################################################################
