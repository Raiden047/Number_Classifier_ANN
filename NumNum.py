#imports
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

import tensorflow as tf

#set parameters
learning_rate = 0.01
training_iteration = 30
batch_size = 100
display_step = 2

#TF graph input
x = tf.placeholder("float", [None, 784])
y = tf.placeholder("float", [None, 10])

#Create Model

#set model weights
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

with tf.name_scope("Wx_b") as scope:
    #construct a linear model
    model = tf.nn.softmax(tf.matmul(x, W) + b)

#Add summary ops to collect data
#w_h = tf.histogram_summary("Weights", W)
#b_h = tf.histogram_summary("biases", b)

#More name scopes will clean up graph representation
with tf.name_scope("cost_function") as scope:
    # Minimize error using cross entropy
    # Cross entropy
    cost_function = -tf.reduce_sum(y*tf.log(model))
    # Create a summary to monitor the cost function
    #tf.scalar_summary("cost_function", cost_function)

with tf.name_scope("train") as scope:
    # Gradient descent
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost_function)

#Initializing the variables
init = tf.global_variables_initializer()

#Merge all summaries into a single operator
#merged_summary_op = tf.merge_all_summaries()

#Launch the graph
with tf.Session() as sess:
    sess.run(init)

    #Set the logs writer to the folder /temp/tensorflow_logs
    #summary_writer = tf.train.SummaryWriter()

    #Trainig Cycle
    for iteration in range(training_iteration):
        avg_cost = 0.
        total_batch = int(mnist.train.num_examples/batch_size)
        #Loop over all batches
        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            #Fit training using batch data
            sess.run(optimizer, feed_dict={x: batch_xs, y: batch_ys})
            #Compute the average loss
            avg_cost += sess.run(cost_function, feed_dict={x: batch_xs, y: batch_ys})/total_batch
            #Write logs for each interation

        #Display logs per interation step
        if iteration % display_step == 0:
            print("Iteration:", '%04d' % (iteration + 1), "cost=", "{:.9f}".format(avg_cost))

    print("Tunning Completed!")

    #Test the model
    predictions = tf.equal(tf.argmax(model, 1), tf.argmax(y, 1))
    #Calculate accuarcy
    accuracy = tf.reduce_mean(tf.cast(predictions, "float"))
    print("Accuarcy:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))


