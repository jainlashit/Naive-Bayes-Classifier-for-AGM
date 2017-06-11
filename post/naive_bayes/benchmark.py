import sys
from test import *

init_file   = '../../tests/00521/00521.xml'
target_file = '../../tests/00521/054_targetMoveObjects.aggt'
train_file  = 'store.data'
threshold   = 0.1
fileName    = 'xxxxxxxxxxxxx'

t = Test()
t.mono_test(init_file, target_file, train_file)
t.new_domain(threshold, fileName)

