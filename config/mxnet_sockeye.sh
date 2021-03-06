#!/usr/bin/env bash

#D_HOME=/home/at15/workspace/src/github.com/at15/snowbot-data/cornell/
D_HOME=/home/at15/workspace/src/github.com/at15/snowbot-data/twitter/
#M_HOME=/home/at15/workspace/src/github.com/at15/snowbot-model/mxnet_sockeye
M_HOME=/home/at15/workspace/src/github.com/at15/snowbot-model/mxnet_sockeye_twitter_1209_01

python -m sockeye.train --source ${D_HOME}src-train.txt \
                       --target ${D_HOME}tgt-train.txt \
                       --validation-source ${D_HOME}src-val.txt \
                       --validation-target ${D_HOME}tgt-val.txt \
                       --rnn-num-hidden 256 \
                       --output ${M_HOME}


# initial version
#python -m sockeye.translate --models /home/at15/workspace/src/github.com/at15/snowbot-model/mxnet_sockeye_1207_01
# initial version, but run until no improvement
#python -m sockeye.translate --models /home/at15/workspace/src/github.com/at15/snowbot-model/mxnet_sockeye_1207_02
# no more i don't know
#python -m sockeye.translate --models /home/at15/workspace/src/github.com/at15/snowbot-model/mxnet_sockeye_1208_01
# python -m sockeye.translate --models /home/at15/workspace/src/github.com/at15/snowbot-model/mxnet_sockeye_twitter_1209_01