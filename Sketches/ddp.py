import numpy as np
import math
import scipy.stats as ss
from tools import *

pre = 'sketches/'

# gene aare  v.s. epsilon
default_m = 12
default_d = 20
epsi_list = [0.1, 0.2, 0.3, 0.4, 0.5]
# epsi_list = [0.01, 0.1, 1.0, 10.0]
n_list = [3, 5, 7, 9]
aare_vs_epsi = []

for i in range(len(n_list)):
	for j in range(len(epsi_list)):
		aare_temp = []
		aare_temp.append(cal_aare_o_ddp(pre + 'fm-' + str(n_list[i]) + '-' + str(default_m) + '-o.txt', 'fm', 100, n_list[i], w_no_bucket(n_list[i]), default_m, epsi_list[j], 10**(-12), default_d, 10))
		aare_temp.append(cal_aare_o_ddp(pre + 'fms-' + str(n_list[i]) + '-' + str(default_m) + '-o.txt', 'fms', 100, n_list[i], w_bucket(n_list[i], default_m), default_m, epsi_list[j], 10**(-12), default_d, 10))
		aare_temp.append(cal_aare_o_ddp(pre + 'll-' + str(n_list[i]) + '-' + str(default_m) + '-o.txt', 'll', 100, n_list[i], w_bucket(n_list[i], default_m), default_m, epsi_list[j], 10**(-12), default_d, 10))
		aare_vs_epsi.append(aare_temp)

# gene aare  v.s. m
default_epsi = 0.1
default_d = 20
m_list = [10, 11, 12, 13]
n_list = [3, 5, 7, 9]
aare_vs_m = []

for i in range(len(n_list)):
	for j in range(len(m_list)):
		aare_temp = []
		aare_temp.append(cal_aare_o_ddp(pre + 'fm-' + str(n_list[i]) + '-' + str(m_list[j]) + '-o.txt', 'fm', 100, n_list[i], w_no_bucket(n_list[i]), m_list[j], default_epsi, 10**(-12), default_d, 10))
		aare_temp.append(cal_aare_o_ddp(pre + 'fms-' + str(n_list[i]) + '-' + str(m_list[j]) + '-o.txt', 'fms', 100, n_list[i], w_bucket(n_list[i], m_list[j]), m_list[j], default_epsi, 10**(-12), default_d, 10))
		aare_temp.append(cal_aare_o_ddp(pre + 'll-' + str(n_list[i]) + '-' + str(m_list[j]) + '-o.txt', 'll', 100, n_list[i], w_bucket(n_list[i], m_list[j]), m_list[j], default_epsi, 10**(-12), default_d, 10))
		aare_vs_m.append(aare_temp)

# gene aare  v.s. d
default_epsi = 0.1
default_m = 12
d_list = [5, 10, 15, 20, 25]
n_list = [3, 5, 7, 9]
aare_vs_d = []

for i in range(len(n_list)):
	for j in range(len(d_list)):
		aare_temp = []
		aare_temp.append(cal_aare_o_ddp(pre + 'fm-' + str(n_list[i]) + '-' + str(default_m) + '-o.txt', 'fm', 100, n_list[i], w_no_bucket(n_list[i]), default_m, default_epsi, 10**(-12), d_list[j], 10))
		aare_temp.append(cal_aare_o_ddp(pre + 'fms-' + str(n_list[i]) + '-' + str(default_m) + '-o.txt', 'fms', 100, n_list[i], w_bucket(n_list[i], default_m), default_m, default_epsi, 10**(-12), d_list[j], 10))
		aare_temp.append(cal_aare_o_ddp(pre + 'll-' + str(n_list[i]) + '-' + str(default_m) + '-o.txt', 'll', 100, n_list[i], w_bucket(n_list[i], default_m), default_m, default_epsi, 10**(-12), d_list[j], 10))
		aare_vs_d.append(aare_temp)

# gene file
file_name_1 = 'aare/ddp_aare_epsi.txt'
file_name_2 = 'aare/ddp_aare_m.txt'
file_name_3 = 'aare/ddp_aare_d.txt'

f = open(file_name_1, 'w')
for i in range(len(aare_vs_epsi)):
	for j in range(3):
		f.write(str(aare_vs_epsi[i][j]))
		f.write(' ')
	f.write('\n')
f.close()

f = open(file_name_2, 'w')
for i in range(len(aare_vs_m)):
	for j in range(3):
		f.write(str(aare_vs_m[i][j]))
		f.write(' ')
	f.write('\n')
f.close()

f = open(file_name_3, 'w')
for i in range(len(aare_vs_d)):
	for j in range(3):
		f.write(str(aare_vs_d[i][j]))
		f.write(' ')
	f.write('\n')
f.close()

# # print to screen
# for i in range(4):
# 	for j in range(5):
# 		print(aare_vs_epsi[i*5 + j])
# 	print()

# print('#####################')

# for i in range(4):
# 	for j in range(4):
# 		print(aare_vs_m[i*4 + j])
# 	print()

# print('#####################')

# for i in range(4):
# 	for j in range(5):
# 		print(aare_vs_d[i*5 + j])
# 	print()