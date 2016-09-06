import numpy as np

class KNearestNeighbor(object):
  """ a kNN classifier with L2 distance """

  def __init__(self):
    pass

  def train(self, X, y):
    """
    Train the classifier. For k-nearest neighbors this is just 
    memorizing the training data.

    Inputs:
    - X: A numpy array of shape (num_train, D) containing the training data
      consisting of num_train samples each of dimension D.
    - y: A numpy array of shape (N,) containing the training labels, where
         y[i] is the label for X[i].
    """
    self.X_train = X
    self.y_train = y
    
  def predict(self, X, k=1, num_loops=0):
    """
    Predict labels for test data using this classifier.

    Inputs:
    - X: A numpy array of shape (num_test, D) containing test data consisting
         of num_test samples each of dimension D.
    - k: The number of nearest neighbors that vote for the predicted labels.
    - num_loops: Determines which implementation to use to compute distances
      between training points and testing points.

    Returns:
    - y: A numpy array of shape (num_test,) containing predicted labels for the
      test data, where y[i] is the predicted label for the test point X[i].  
    """
    if num_loops == 0:
      dists = self.compute_distances_no_loops(X)
    elif num_loops == 1:
      dists = self.compute_distances_one_loop(X)
    elif num_loops == 2:
      dists = self.compute_distances_two_loops(X)
    else:
      raise ValueError('Invalid value %d for num_loops' % num_loops)

    return self.predict_labels(dists, k=k)

  def compute_distances_two_loops(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using a nested loop over both the training data and the 
    test data.

    Inputs:
    - X: A numpy array of shape (num_test, D) containing test data.

    Returns:
    - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
      is the Euclidean distance between the ith test point and the jth training
      point.
    """
    num_test = X.shape[0]
    num_train = self.X_train.shape[0]
    dists = np.zeros((num_test, num_train))
    for i in xrange(num_test):
      for j in xrange(num_train):
        #####################################################################
        # TODO:                                                             #
        # Compute the l2 distance between the ith test point and the jth    #
        # training point, and store the result in dists[i, j]. You should   #
        # not use a loop over dimension.                                    #
        #####################################################################
        # print "Hi"
        # print X.shape
        # print self.X_train.shape

        tmp =  np.power(self.X_train[j, :] - X[i, :], 2)
        # print "Hi"
        # print tmp.shape
        # if (i % 50 and j == 1):
        #   print ((float(i) / num_test) * 100), ' % done'

        dists[i, j] = np.sum(tmp)
        #####################################################################
        #                       END OF YOUR CODE                            #
        #####################################################################
    return dists

  def compute_distances_one_loop(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using a single loop over the test data.

    Input / Output: Same as compute_distances_two_loops
    """
    num_test = X.shape[0]
    num_train = self.X_train.shape[0]
    dists = np.zeros((num_test, num_train))
    for i in xrange(num_test):
      #######################################################################
      # TODO:                                                               #
      # Compute the l2 distance between the ith test point and all training #
      # points, and store the result in dists[i, :].                        #
      #######################################################################
      dists[i, :] = np.sum(np.power(self.X_train - X[i,:], 2), axis = 1)
      #######################################################################
      #                         END OF YOUR CODE                            #
      #######################################################################
    return dists

  def compute_distances_no_loops(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using no explicit loops.

    Input / Output: Same as compute_distances_two_loops
    """
    #There seems to be a bug in this function... However the distance between the other two (correct) functions seems to be correct
    #Hmmm, strange... That means all these algorithms are incorrect? Time for another debugging session
    num_test = X.shape[0]
    num_train = self.X_train.shape[0]
    dists = np.zeros((num_test, num_train)) 
    #########################################################################
    # TODO:                                                                 #
    # Compute the l2 distance between all test points and all training      #
    # points without using any explicit loops, and store the result in      #
    # dists.                                                                #
    #                                                                       #
    # You should implement this function using only basic array operations; #
    # in particular you should not use functions from scipy.                #
    #                                                                       #
    # HINT: Try to formulate the l2 distance using matrix multiplication    #
    #       and two broadcast sums.                                         #
    #########################################################################


    # print 'HEY!', X.shape
    # print self.X_train.shape
    # #using binomial 'expansion'
    # #sigma(A - B)^2 = sigma(A^2 - 2*A*B + B^2)
    A = np.sum( np.square(X), axis=1)
    # print "A", A.shape
    B = np.sum( np.square(self.X_train), axis = 1).T
    # print "B", B.shape
    #B = np.tile( B,(500,5000) )
    AB = np.dot(X, self.X_train.T)
    # print "AB", AB.shape
    dists = -2 * AB
    # print "inner", dists.shape
    dists += B
    # print "inner1", dists.shape
    dists += np.matrix(A).T
    # print "inner2", dists.shape       #Want to add this to every sample, so equivalent to matrix addition


    # A = np.sum(np.square(X), axis=1)
    # B = np.sum(np.square(self.X_train), axis=1)
    # print 'A', A.shape
    # print 'B', B.shape
    # C = -2 * np.dot(X, self.X_train.T)
    #
    # print 'C', C.shape
    # dists = np.sum(A + B.T - AB, axis=1)

    # X_tmp = np.reshape(X, (num_test, -1))
    # X_tmp = np.repeat(X_tmp, 10, axis=0)
    # X_train_tmp = np.repeat(self.X_train, )
    # X_train_tmp = np.reshape(self.X_train, (num_train, -1))
    # dists = np.sum(np.power(X_train_tmp - X_tmp, 2), axis=0)
    #########################################################################
    #                         END OF YOUR CODE                              #
    #########################################################################
    return dists

  def predict_labels(self, dists, k=1):
    """
    Given a matrix of distances between test points and training points,
    predict a label for each test point.

    Inputs:
    - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
      gives the distance betwen the ith test point and the jth training point.

    Returns:
    - y: A numpy array of shape (num_test,) containing predicted labels for the
      test data, where y[i] is the predicted label for the test point X[i].  
    """
    num_test = dists.shape[0]
    y_pred = np.zeros(num_test)
    for i in xrange(num_test):
      # A list of length k storing the labels of the k nearest neighbors to
      # the ith test point.
      # closest_y = []
      # print self.y_train
      # print max(self.y_train)
      closest_y = np.zeros((10, 1))
      # print 'Closest_y', closest_y.shape
      #########################################################################
      # TODO:                                                                 #
      # Use the distance matrix to find the k nearest neighbors of the ith    #
      # testing point, and use self.y_train to find the labels of these       #
      # neighbors. Store these labels in closest_y.                           #
      # Hint: Look up the function numpy.argsort.                             #
      #########################################################################

      #sort smallest k distances in ascending order
      index_of_smallest_k = self.y_train[dists[i,:].argsort()[:k]]
      # print index_of_smallest_k
      # print 'IOSK', index_of_smallest_k.shape

      closest_y[index_of_smallest_k] += 1

      # for i in xrange(k):     #xrange was without k itself, right?
      #   # print i
      #   closest_y[index_of_smallest_k[i]] += 1  #add to the index of the predicted label
      # print closest_y

      #########################################################################
      # TODO:                                                                 #
      # Now that you have found the labels of the k nearest neighbors, you    #
      # need to find the most common label in the list closest_y of labels.   #
      # Store this label in y_pred[i]. Break ties by choosing the smaller     #
      # label.                                                                #
      #########################################################################

      y_pred[i] = np.argmax(closest_y)

      #########################################################################
      #                           END OF YOUR CODE                            # 
      #########################################################################

    return y_pred

