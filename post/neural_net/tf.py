import tensorflow as tf

x1 = tf.constant([3])
x2 = tf.constant([5])
result = x1 * x2

print(result)

sess = tf.Session()
print(sess.run(result))
sess.close()