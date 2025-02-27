'''
The MIT License (MIT)

Copyright 2019 Dhruvaraj nagarajan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import tensorflow as tf
import numpy as np

raw_data = open ("test_data_udp.txt"). readlines ()
raw_labels = open ("test_label_udp.txt"). readlines ()

x = []
y = []

for _ in raw_data:

	_ = _.split ()
	x.append ([int (_[0]), int (_[1]), int (_[2]), int (_[3])])

for _ in raw_labels:

	y.append ([0, 1])

nodesForLayerInput = 4
nodesForLayer1 = 50
nodesForLayer2 = 50
nodesForLayer3 = 50
nodesForLayerOut = 1

numberOfClassesOut = 2

data = tf.placeholder ('float', shape = [None, 4])
label = tf.placeholder ('float')

layer1 = {
		
	'w' : tf.Variable (tf.zeros ([4, nodesForLayer1])),
	'b' : tf.Variable (tf.zeros ([nodesForLayer1]))
}

layer2 = {
	
	'w' : tf.Variable (tf.zeros ([nodesForLayer1, nodesForLayer2])),
	'b' : tf.Variable (tf.zeros ([nodesForLayer2]))
}

layer3 = {
	
	'w' : tf.Variable (tf.zeros ([nodesForLayer2, nodesForLayer3])),
	'b' : tf.Variable (tf.zeros ([nodesForLayer3]))
}

layerOut = {
	
	'w' : tf.Variable (tf.zeros ([nodesForLayer3, numberOfClassesOut])),
	'b' : tf.Variable (tf.zeros ([numberOfClassesOut]))
}

saver = tf.train.Saver ()

def graph (_data):

	ansLayer1 = tf.nn.relu (tf.add(tf.matmul(_data, layer1['w']), layer1['b']))
	ansLayer2 = tf.nn.relu (tf.add(tf.matmul(ansLayer1, layer2['w']), layer2['b']))
	ansLayer3 = tf.nn.relu (tf.add(tf.matmul(ansLayer2, layer3['w']), layer3['b']))

	ansLayerOut = tf.add(tf.matmul(ansLayer3, layerOut['w']), layerOut['b'])

	return ansLayerOut

def train (_x):

	prediction = graph (_x)

	cost = tf.reduce_mean (tf.nn.softmax_cross_entropy_with_logits (

		_sentinel = None,
		logits = prediction,
		labels = label,
		dim = -1,
		name = None)
	)

	optimiser = tf.train.AdamOptimizer ().minimize (cost)

	nEpochs = 1

	with tf.Session () as sess:

		sess.run (tf.global_variables_initializer ())

		saver.restore (sess, "/dir/model_train.ckpt")

		for epoch in range (nEpochs):

			epoch_loss = 0
			test = 0

			for i in range (100):

				i, c = sess.run ([optimiser, cost], feed_dict = {data : x, label : y})

				epoch_loss += c
				
				print(c)

		correct = tf.equal (tf.argmax (prediction, 1), tf.argmax (label, 1))

		accuracy = tf.reduce_mean (tf.cast (correct, 'float'))

		print ("Accuracy ", accuracy.eval ({data : x, label : y}))

train(data)
