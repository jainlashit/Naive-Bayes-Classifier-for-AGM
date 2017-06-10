import sys
import test

if len(sys.argv) != 7:
	print sys.argv[0], 'plan_file init_file target_file train_file threshold fileName'
	sys.exit(0)



plan_file   = sys.argv[1]
init_file   = sys.argv[2]
target_file = sys.argv[3]
train_file  = sys.argv[4]
threshold   = sys.argv[5]
fileName    = sys.argv[6]

t = Test()
t.mono_test(plan_file, init_file, target_file, train_file)
t.new_domain(threshold, fileName)

