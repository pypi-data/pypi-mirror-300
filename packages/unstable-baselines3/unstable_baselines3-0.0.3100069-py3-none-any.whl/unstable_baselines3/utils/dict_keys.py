# whether agent is able to be trained/should be trained
DICT_TRAIN = 'train'

# whether an agent should only collect buffer examples, usually implies DICT_TRAIN is false
# If using this, should probably have the following setup:
#   all DICT_TRAIN for a particular agent is false
#   all DICT_COLLECT_ONLY for that agent is true
# this will result in the agent only training in one large batch after each epoch
# this should be done automatically if  coevolver:PettingZooCaptianCoevolution.local_collection_mode
DICT_COLLECT_ONLY = 'collect_only'