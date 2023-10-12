import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker

# plt.rcParams.update({
#   "text.usetex": True,
#   "font.family": "Times New Roman"
# })

pics = [1, 3] # the pic series line number
epsi_list = [0.1, 0.2, 0.3, 0.4, 0.5]
shows = [] # the pic series line number to display
captain = False
cols = 2

def pic1():
	file_name = 'aare/cdp_aare_epsi.txt'
	aare = (np.loadtxt(file_name)).tolist()
	same_distance = [i + 1 for i in range(len(epsi_list))]
	len_e = len(epsi_list)
	n_list = [3, 5, 7, 9]
	for i in range(len(n_list)): # for i in range(len(n_list)):
		plt.figure(figsize=(6,4))
		plt.yscale("log")
		plt.plot(same_distance, [aare[i * len_e + j][0] for j in range(len_e)], linestyle="-",marker="o", linewidth=1, color='darkgoldenrod',markeredgewidth=1, label = 'FM sketch')
		plt.plot(same_distance, [aare[i * len_e + j][2] for j in range(len_e)], linestyle="-",marker="^",  linewidth=1,color='royalblue', markeredgewidth=1, label = 'HLL sketch')
		plt.plot(same_distance, [aare[i * len_e + j][1] for j in range(len_e)], linestyle="-",marker="s",  linewidth=1,color='crimson', markeredgewidth=1, label = 'FMS sketch')
		plt.legend(loc = 'upper right', fontsize=15 ,framealpha=1.0, ncol = cols)
		plt.xticks(fontsize=20)
		plt.yticks(fontsize=20)
		_ = plt.xticks(same_distance,epsi_list)
		plt.xlabel(r'$\varepsilon$', fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.ylabel("AARE", fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.ylim(10**-2.4, 10**4)
		if captain:
			plt.title(r'CDP, cardinality = $10^' + str(n_list[i]) + '$', fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.subplots_adjust(left=0.184, right=0.929, top=0.906, bottom=0.176)
		plt.savefig('pics/cdp_aare_epsi_' + str(n_list[i]) + '.pdf')
		if 1 in shows:
			plt.show()

def pic2():
	file_name = 'aare/cdp_aare_m.txt'
	aare = (np.loadtxt(file_name)).tolist()
	m_list = [10, 11, 12, 13]
	n_list = [3, 5, 7, 9]
	for i in range(len(n_list)):
		plt.figure(figsize=(6,4))
		plt.yscale('log')
		plt.plot(m_list, [aare[i * 4 + j][0] for j in range(4)], linestyle="-",marker="o", linewidth=1, color='darkgoldenrod',markeredgewidth=1, label = 'FM sketch')
		plt.plot(m_list, [aare[i * 4 + j][2] for j in range(4)], linestyle="-",marker="^",  linewidth=1,color='royalblue', markeredgewidth=1, label = 'HLL sketch')
		plt.plot(m_list, [aare[i * 4 + j][1] for j in range(4)], linestyle="-",marker="s",  linewidth=1,color='crimson', markeredgewidth=1, label = 'FMS sketch')
		plt.legend(loc = 'upper right', fontsize=15 ,framealpha=1.0, ncol = cols)
		plt.xticks(fontsize=20)
		_ = plt.xticks(m_list, [2**i for i in m_list])
		plt.yticks(fontsize=20)
		plt.xlabel(r'$m$', fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.ylabel("AARE", fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.ylim(10**-2.4, 10**4)
		if captain:
			plt.title(r'CDP, cardinality = $10^' + str(n_list[i]) + '$', fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.subplots_adjust(left=0.184, right=0.929, top=0.906, bottom=0.176)
		plt.savefig('pics/cdp_aare_m_' + str(n_list[i]) + '.pdf')
		if 2 in shows:
			plt.show()

def pic3():
	file_name = 'aare/ddp_aare_epsi.txt'
	aare = (np.loadtxt(file_name)).tolist()
	same_distance = [i + 1 for i in range(len(epsi_list))]
	len_e = len(epsi_list)
	n_list = [3, 5, 7, 9]
	for i in range(len(n_list)): # for i in range(len(n_list)):
		plt.figure(figsize=(6,4))
		plt.yscale("log")
		plt.plot(same_distance, [aare[i * len_e + j][0] for j in range(len_e)], linestyle="-",marker="o", linewidth=1, color='darkgoldenrod',markeredgewidth=1, label = 'FM sketch')
		plt.plot(same_distance, [aare[i * len_e + j][2] for j in range(len_e)], linestyle="-",marker="^",  linewidth=1,color='royalblue', markeredgewidth=1, label = 'HLL sketch')
		plt.plot(same_distance, [aare[i * len_e + j][1] for j in range(len_e)], linestyle="-",marker="s",  linewidth=1,color='crimson', markeredgewidth=1, label = 'FMS sketch')
		plt.legend(loc = 'upper right', fontsize=15 ,framealpha=1.0, ncol = cols)
		plt.xticks(fontsize=20)
		plt.yticks(fontsize=20)
		_ = plt.xticks(same_distance,epsi_list)
		plt.xlabel(r'$\varepsilon$', fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.ylabel("AARE", fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.ylim(10**-2.4, 10**4)
		if captain:
			plt.title(r'DDP, cardinality = $10^' + str(n_list[i]) + '$', fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.subplots_adjust(left=0.184, right=0.929, top=0.906, bottom=0.176)
		plt.savefig('pics/ddp_aare_epsi_' + str(n_list[i]) + '.pdf')
		if 3 in shows:
			plt.show()

def pic4():
	file_name = 'aare/ddp_aare_m.txt'
	aare = (np.loadtxt(file_name)).tolist()
	m_list = [10, 11, 12, 13]
	n_list = [3, 5, 7, 9]
	for i in range(len(n_list)):
		plt.figure(figsize=(6,4))
		plt.yscale('log')
		plt.plot(m_list, [aare[i * 4 + j][0] for j in range(4)], linestyle="-",marker="o", linewidth=1, color='darkgoldenrod',markeredgewidth=1, label = 'FM sketch')
		plt.plot(m_list, [aare[i * 4 + j][2] for j in range(4)], linestyle="-",marker="^",  linewidth=1,color='royalblue', markeredgewidth=1, label = 'HLL sketch')
		plt.plot(m_list, [aare[i * 4 + j][1] for j in range(4)], linestyle="-",marker="s",  linewidth=1,color='crimson', markeredgewidth=1, label = 'FMS sketch')
		plt.legend(loc = 'upper right', fontsize=15 ,framealpha=1.0, ncol = cols)
		plt.xticks(fontsize=20)
		_ = plt.xticks(m_list, [2**i for i in m_list])
		plt.yticks(fontsize=20)
		plt.xlabel(r'$m$', fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.ylabel("AARE", fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.ylim(10**-2.4, 10**4)
		if captain:
			plt.title(r'DDP, cardinality = $10^' + str(n_list[i]) + '$', fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.subplots_adjust(left=0.184, right=0.929, top=0.906, bottom=0.176)
		plt.savefig('pics/ddp_aare_m_' + str(n_list[i]) + '.pdf')
		if 4 in shows:
			plt.show()

def pic5():
	file_name = 'aare/ddp_aare_d.txt'
	aare = (np.loadtxt(file_name)).tolist()
	d_list = [5, 10, 15, 20, 25]
	n_list = [3, 5, 7, 9]
	for i in range(len(n_list)): # for i in range(len(n_list)):
		plt.figure(figsize=(6,4))
		plt.yscale("log")
		plt.plot(d_list, [aare[i * 5 + j][0] for j in range(5)], linestyle="-",marker="o", linewidth=1, color='darkgoldenrod',markeredgewidth=1, label = 'FM sketch')
		plt.plot(d_list, [aare[i * 5 + j][2] for j in range(5)], linestyle="-",marker="^",  linewidth=1,color='royalblue', markeredgewidth=1, label = 'HLL sketch')
		plt.plot(d_list, [aare[i * 5 + j][1] for j in range(5)], linestyle="-",marker="s",  linewidth=1,color='crimson', markeredgewidth=1, label = 'FMS sketch')
		plt.legend(loc = 'upper right', fontsize=15 ,framealpha=1.0, ncol = cols)
		plt.xticks(d_list, fontsize=20)
		plt.yticks(fontsize=20)
		plt.xlabel('No. DHs', fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.ylabel("AARE", fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.ylim(10**-2.4, 10**4)
		if captain:
			plt.title(r'DDP, cardinality = $10^' + str(n_list[i]) + '$', fontdict={'family' : 'Times New Roman', 'size' : 20})
		plt.subplots_adjust(left=0.184, right=0.929, top=0.906, bottom=0.176)
		plt.savefig('pics/ddp_aare_d_' + str(n_list[i]) + '.pdf')
		if 5 in shows:
			plt.show()

if __name__ == '__main__':
	if 1 in pics:
		pic1()
	if 2 in pics:
		pic2()
	if 3 in pics:
		pic3()
	if 4 in pics:
		pic4()
	if 5 in pics:
		pic5()