#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chainer
import chainer.functions as F
import chainer.links as L


class VGG19(chainer.Chain):

    def __init__(self):
        super(VGG19, self).__init__(
            conv1_1=L.Convolution2D(3, 64, 3, pad=1),
            bn1_1=L.BatchNormalization(64),
            conv1_2=L.Convolution2D(64, 64, 3, pad=1),
            bn1_2=L.BatchNormalization(64),

            conv2_1=L.Convolution2D(64, 128, 3, pad=1),
            bn2_1=L.BatchNormalization(128),
            conv2_2=L.Convolution2D(128, 128, 3, pad=1),
            bn2_2=L.BatchNormalization(128),

            conv3_1=L.Convolution2D(128, 256, 3, pad=1),
            bn3_1=L.BatchNormalization(256),
            conv3_2=L.Convolution2D(256, 256, 3, pad=1),
            bn3_2=L.BatchNormalization(256),
            conv3_3=L.Convolution2D(256, 256, 3, pad=1),
            bn3_3=L.BatchNormalization(256),
            conv3_4=L.Convolution2D(256, 256, 3, pad=1),
            bn3_4=L.BatchNormalization(256),

            conv4_1=L.Convolution2D(256, 512, 3, pad=1),
            bn4_1=L.BatchNormalization(512),
            conv4_2=L.Convolution2D(512, 512, 3, pad=1),
            bn4_2=L.BatchNormalization(512),
            conv4_3=L.Convolution2D(512, 512, 3, pad=1),
            bn4_3=L.BatchNormalization(512),
            conv4_4=L.Convolution2D(512, 512, 3, pad=1),
            bn4_4=L.BatchNormalization(512),

            conv5_1=L.Convolution2D(512, 512, 3, pad=1),
            bn5_1=L.BatchNormalization(512),
            conv5_2=L.Convolution2D(512, 512, 3, pad=1),
            bn5_2=L.BatchNormalization(512),
            conv5_3=L.Convolution2D(512, 512, 3, pad=1),
            bn5_3=L.BatchNormalization(512),
            conv5_4=L.Convolution2D(512, 512, 3, pad=1),
            bn5_4=L.BatchNormalization(512),

            fc4=L.Linear(512, 1024),
            fc5=L.Linear(1024, 1024),
            fc6=L.Linear(1024, 10),
        )
        self.train = True

    def __call__(self, x, t):
        h = F.relu(self.bn1_1(self.conv1_1(x), test=not self.train))
        h = F.relu(self.bn1_2(self.conv1_2(h), test=not self.train))
        h = F.max_pooling_2d(h, 2, 2)
        h = F.dropout(h, ratio=0.25, train=self.train)

        h = F.relu(self.bn2_1(self.conv2_1(h), test=not self.train))
        h = F.relu(self.bn2_2(self.conv2_2(h), test=not self.train))
        h = F.max_pooling_2d(h, 2, 2)
        h = F.dropout(h, ratio=0.25, train=self.train)

        h = F.relu(self.bn3_1(self.conv3_1(h), test=not self.train))
        h = F.relu(self.bn3_2(self.conv3_2(h), test=not self.train))
        h = F.relu(self.bn3_3(self.conv3_3(h), test=not self.train))
        h = F.relu(self.bn3_4(self.conv3_4(h), test=not self.train))
        h = F.max_pooling_2d(h, 2, 2)
        h = F.dropout(h, ratio=0.25, train=self.train)

        h = F.relu(self.bn4_1(self.conv4_1(h), test=not self.train))
        h = F.relu(self.bn4_2(self.conv4_2(h), test=not self.train))
        h = F.relu(self.bn4_3(self.conv4_3(h), test=not self.train))
        h = F.relu(self.bn4_4(self.conv4_4(h), test=not self.train))
        h = F.max_pooling_2d(h, 2, 2)
        h = F.dropout(h, ratio=0.25, train=self.train)

        h = F.relu(self.bn5_1(self.conv5_1(h), test=not self.train))
        h = F.relu(self.bn5_2(self.conv5_2(h), test=not self.train))
        h = F.relu(self.bn5_3(self.conv5_3(h), test=not self.train))
        h = F.relu(self.bn5_4(self.conv5_4(h), test=not self.train))
        h = F.max_pooling_2d(h, 2, 2)
        h = F.dropout(h, ratio=0.25, train=self.train)

        h = F.dropout(F.relu(self.fc4(h)), ratio=0.5, train=self.train)
        h = F.dropout(F.relu(self.fc5(h)), ratio=0.5, train=self.train)
        h = self.fc6(h)

        self.pred = F.softmax(h)
        self.loss = F.softmax_cross_entropy(h, t)
        self.accuracy = F.accuracy(self.pred, t)

        if self.train:
            return self.loss
        else:
            return self.pred

model = VGG19()
