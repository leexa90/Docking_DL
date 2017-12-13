import tensorflow as tf
batch_size = 1
with tf.name_scope('inputs') as scope:
    receptor = tf.placeholder(tf.float32,[batch_size,96,96,96,3],name='receptor') #10 by 10 by 10 angstrom box
    ligand = tf.placeholder(tf.float32,[batch_size,96,96,96,3],name='ligand')
    
with tf.name_scope('embedding') as scope:
#    atom_embeddings = tf.get_variable('atom_embeddings',[5, 3])
#    embedded_atom_ids = tf.gather(atom_embeddings,range(0,20))
    layer0 = tf.concat([receptor],-1)#tf.nn.embedding_lookup(atom_embeddings,receptor,name='lookup')

    
with tf.name_scope('layers') as scope:
    #layer1_norm = batch_normalization(layer0,'BN_layer0',feature_norm = True)
    layer1a = tf.layers.conv3d(layer0,16,(3,3,3),padding='same',activation=tf.nn.relu,name='layer1a')
    layer1b = tf.layers.average_pooling3d(layer1a,(3,3,3),(2,2,2),name='layer1b',padding='same')
    layer2a = tf.layers.conv3d(layer1b,32,(3,3,3),padding='same',activation=tf.nn.relu,name='layer2a')
    layer2b = tf.layers.average_pooling3d(layer2a,(3,3,3),(2,2,2),name='layer2b',padding='same')
    layer3a = tf.layers.conv3d(layer2b,64,(3,3,3),padding='same',activation=tf.nn.relu,name='layer3a')
    layer3b = tf.layers.average_pooling3d(layer3a,(3,3,3),(2,2,2),name='layer3c',padding='same')
    layer4a = tf.layers.conv3d(layer3b,128,(3,3,3),padding='same',activation=tf.nn.relu,name='layer4a')

    layer3a_t = tf.layers.conv3d_transpose(layer4a,64,(3,3,3),(2,2,2),padding='same')
    layer2b_t = tf.layers.conv3d(tf.concat([layer3a_t,layer3a],-1),64,(3,3,3),padding='same',activation=tf.nn.relu)
    layer2a_t = tf.layers.conv3d_transpose(layer2b_t,32,(3,3,3),(2,2,2),padding='same')
    layer1b_t = tf.layers.conv3d(tf.concat([layer2a_t,layer2a],-1),32,(3,3,3),padding='same',activation=tf.nn.relu)
    layer1a_t = tf.layers.conv3d_transpose(layer1b_t,16,(3,3,3),(2,2,2),padding='same')
    layer0_t = tf.layers.conv3d(tf.concat([layer1a_t,layer1a],-1),16,(3,3,3),padding='same',activation=tf.nn.relu)

with tf.name_scope('atom_site') as scope:
    atom_present = tf.add(tf.add(ligand[:,:,:,:,0],ligand[:,:,:,:,1]),ligand[:,:,:,:,2])
    prob_atom = tf.layers.conv3d(layer0_t,1,(3,3,3),padding='same',activation=None)
    prob_atom_loss = tf.nn.sigmoid_cross_entropy_with_logits(logits=prob_atom[:,:,:,:,-1],labels=atom_present)
    predict_atom = tf.nn.sigmoid(prob_atom)
with tf.name_scope('atom_site_classification') as scope:
    predict = tf.layers.conv3d(layer0_t,3,(3,3,3),padding='same',activation=None)
    log_loss = tf.multiply(tf.nn.softmax_cross_entropy_with_logits(logits=predict,labels=ligand,dim=-1),atom_present)
    out = tf.multiply(tf.nn.softmax(predict),predict_atom)
    loss = tf.reduce_mean(tf.add(prob_atom_loss,log_loss))
    
total_parameters = 0
print ''' ### PARAMETERS ### '''
for variable in tf.trainable_variables():
    # shape is an array of tf.Dimension
    shape = variable.get_shape()
    variable_parameters = 1
    for dim in shape:
        variable_parameters *= dim.value
    print variable.name,variable_parameters,variable
    total_parameters += variable_parameters
print' ### model parameters',total_parameters,'###'
