from numpy import matrix
import tensorflow  as tf
from tensorflow.python.keras.backend import relu
import pandas
import numpy as np
from tensorflow.keras.layers import Dense, Flatten, Conv1D
from tensorflow.keras import Model
from tensorflow.python.keras.backend import conv2d
from tensorflow.python.keras.layers.core import Activation, Dropout
from tensorflow.python.keras.metrics import accuracy
from tensorflow.python.training import optimizer


# Load data 
train_set = pandas.read_csv('train_14d.csv')
print(train_set)
# key_list = list(train_set.keys())
# x_train = np.array(train_set)[:,2:]
x_train = np.delete(np.array(train_set),1,1)
x_train = x_train[:,:2]
print(x_train)

x_train = x_train[..., tf.newaxis].astype('float32')
print(x_train.shape)
y_train = np.array(train_set)[:,1]

print(y_train.shape)

test_set = pandas.read_csv('test_14d.csv')

x_test = np.delete(np.array(test_set),1,1)
x_test = x_test[:,:2]


x_test = x_test[..., tf.newaxis].astype('float32')
y_test = np.array(test_set)[:,1]
print(y_test.shape)

# set batch 
train_ds = tf.data.Dataset.from_tensor_slices((x_train,y_train)).batch(32)

test_ds = tf.data.Dataset.from_tensor_slices((x_test,y_test)).batch(32)



# mnist = tf.keras.datasets.mnist
# # x is question/training data   y is ans/label
# (x_train,y_train),(x_test,y_test) = mnist.load_data()
# x_train,x_test = x_train/255.0,x_test/255.0

# model
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape = (28,28)),
    tf.keras.layers.Dense(128,activation=relu),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10)# classifier 10 class (y ans)
]
)


# Model
class myModel(Model):
    def __init__(self):
        super(myModel,self).__init__()
        self.conv1 = Conv1D(12,2)
        self.flatten = Flatten()
        self.d1 = Dense(36)
        self.dropout = Dropout(0.6)
        #self.d_fit = Dense(34,activation='softmax')
        self.d2 = Dense(2)
    
    def call(self,x):
        # x = self.conv1(x)
        x = self.flatten(x)
        x = self.d1(x)
        
        # x = self.d_fit(x)
        # x = self.dropout(x)
        return self.d2(x)

# Create an instance of the model
model = myModel()

# Optimizer and Loss Func
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
opt = tf.keras.optimizers.Adam()

# Set loss and Accuracy
train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')

# Training Model
@tf.function
def train_step(x,labels):
    with tf.GradientTape() as tape:
        # training=True is only needed if there are layers with different
        # behavior during training versus inference (e.g. Dropout).
        predictions = model(x, training=True)
        loss = loss_object(labels, predictions)
    gradients = tape.gradient(loss,model.trainable_variables)
    opt.apply_gradients(zip(gradients,model.trainable_variables))

    train_loss(loss)
    train_accuracy(labels,predictions)

# Test Model
@tf.function
def test_step(x,labels):
    # training=False is only needed if there are layers with different
    # behavior during training versus inference (e.g. Dropout).
    predictions = model(x, training=False)
    t_loss = loss_object(labels, predictions)

    test_loss(t_loss)
    test_accuracy(labels, predictions)


# Start training
epochs = 20

for epoch in range(epochs):
    # reset the metrices at the start of the next epoch
    train_loss.reset_states()
    train_accuracy.reset_states()
    test_loss.reset_states()
    test_accuracy.reset_states()

    for x, labels in train_ds:
        train_step(x,labels)
    for test_x, test_labels in test_ds:
        test_step(test_x,test_labels)

    print(
    f'Epoch {epoch + 1}, '
    f'Loss: {train_loss.result()}, '
    f'Accuracy: {train_accuracy.result() * 100}, '
    f'Test Loss: {test_loss.result()}, '
    f'Test Accuracy: {test_accuracy.result() * 100}'
     )