import sys
from test import *

data_path = "../../tests/"
start_dir = 271
end_dir = 273

plan_file   = 'empty'
init_file   = '../../tests/00521/00521.xml'
target_file = '../../tests/00521/054_targetMoveObjects.aggt'
train_file  = 'store.data'
threshold   = 0.5
fileName    = 'xxxxxxxxxxxxx'

t = Test(data_path, start_dir, end_dir)
t.mono_test(plan_file, init_file, target_file, train_file)
t.new_domain(threshold, fileName)

