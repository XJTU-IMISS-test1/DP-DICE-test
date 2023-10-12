import math
import numpy as np
import scipy.stats as ss
import mmh3
import time

# distributed discrete gaussian noise

def cal_var_epsilon_d(d, sigma, big_delta):
	tao_d = 0
	for k in range(d-1):
		tao_d += math.exp(-2*(k+1)*math.pi*math.pi*sigma*sigma / (k+2))
	tao_d *= 10
	epsilon_d_0 = math.sqrt(big_delta*big_delta/(d*sigma*sigma) + tao_d/2)
	epsilon_d_1 = big_delta/(math.sqrt(d)*sigma) + tao_d
	epsilon_d = min(epsilon_d_0, epsilon_d_1)
	return epsilon_d

def cal_sigma(d, epsilon_d, big_delta):
	left = 0.5
	right = 10**10
	while(abs(right - left) > 0.01):
		if ((cal_var_epsilon_d(d, (left+right)/2, big_delta) - epsilon_d) < 0):
			right = (left+right)/2
		else:
			left = (left+right)/2
	return (left+right)/2

def converse_epsilon_d(epsilon, delta):
	epsilon_d = -1 * math.sqrt((-2)*math.log(delta)) + math.sqrt((-2)*math.log(delta) + 2*epsilon)
	return epsilon_d

def sample_discrete_gaussian(mu, sigma, size_n):
	if sigma < 1000:
		x = np.arange(-30*sigma, 30*sigma+1)
	else:
		x = np.arange(-sigma, sigma+1)
	prob = ss.norm.pdf(x, scale=sigma)
	prob = prob / prob.sum()
	nums = np.random.choice(x, size=size_n, p=prob)
	return nums

# fm functions

def fm_z(bits):
	z = 0
	for i in bits:
		if i == 1:
			z += 1
		else:
			break
	return z

def cal_fm(z, w, m):
	phi = 0.77351
	z = z/m
	if z >= w:
		z = w
	elif z <= 0:
		z = 0
	return pow(2, z)/phi

def get_w(n):
    if n < 8:
        w = 32
    else:
        w = 40
    return w

def get_w_mod(n):
	n = 10**n
	w = math.ceil(math.log(n, 2) + 7)
	return w

# fms functions

def fms_z(bits):
	return len(bits) - sum(bits)

def ave(n, w, m):
	re = 0
	for i in range(w-1):
		re += pow((1.0-(pow(0.5, i+1)/m)), n)
	re += pow((1.0-(pow(0.5, w-1)/m)), n)
	return re

def dave(n, w, m):
	re = 0
	for i in range(w-1):
		re += pow((1.0-(pow(0.5, i+1)/m)), n) * math.log((1.0-(pow(0.5, i+1)/m)))
	re += pow((1.0-(pow(0.5, w-1)/m)), n) * math.log((1.0-(pow(0.5, w-1)/m)))
	return re

def cal_fms(z, w, m):
	z = z/m
	if z >= w:
		z = w
	elif z <= 0:
		z = 0
	x0 = 100
	dist = 0.25
	while((ave(x0, w, m) - z) * (ave(x0+dist, w, m) - z) > 0):
		x0 -= (ave(x0, w, m) - z)/(dave(x0, w, m))
	return x0

# hyperloglog functions

def ll_z(bits):
	z = 0
	for i in range(len(bits)):
		if bits[i] == 1:
			z = i + 1
	return z

def cal_ll(z, w, m):
	alpha_m = 0.39701
	z = z/m
	if z >= w:
		z = w
	elif z <= 0:
		z = 0
	car = alpha_m * m * (2**z)
	return car

# others

def cal_aare_o(filename, sketch_type, expe, n, w, m):
	''' n: like 3, 5, 7, 9 \n m: like 10, 11, 12, 13'''
	out = (np.loadtxt(filename)).tolist()
	out = [out] if type(out) == float else out
	if sketch_type == "fm":
		out_car = [cal_fm(k, w, 2**m) for k in out]
	elif sketch_type == "fms":
		out_car = [cal_fms(k, w, 2**m) for k in out]
	elif sketch_type == "ll":
		out_car = [cal_ll(k, w, 2**m) for k in out]
	else:
		out_car = 0
	are = [abs(k-10**n) / 10**n for k in out_car]
	aare = sum(are) / expe
	return aare

def cal_aare_o_n(filename, sketch_type, expe, n, w, m):
	''' n: like 30000 \n m: like 10, 11, 12, 13'''
	out = (np.loadtxt(filename)).tolist()
	out = [out] if type(out) == float else out
	if sketch_type == "fm":
		out_car = [cal_fm(k, w, 2**m) for k in out]
	elif sketch_type == "fms":
		out_car = [cal_fms(k, w, 2**m) for k in out]
	elif sketch_type == "ll":
		out_car = [cal_ll(k, w, 2**m) for k in out]
	else:
		out_car = 0
	are = [abs(k-n) / n for k in out_car]
	aare = sum(are) / expe
	return aare

def cal_aare_o_cdp(filename, sketch_type, expe, n, w, m, epsi, delta, expand):
	out = (np.loadtxt(filename)).tolist()
	out = [out] if type(out) == float else out
	out_car = []
	if sketch_type == 'fm':
		noise = np.random.normal(0, math.sqrt(2 * math.log(1.25 / delta)) * w * (2**m) / epsi, expe * expand).tolist()
		for k in range(len(out)):
			for i in range(expand):
				out_car.append(cal_fm(out[k] + noise[k*expand + i], w, 2**m))
	if sketch_type == 'fms':
		noise = np.random.normal(0, math.sqrt(2 * math.log(1.25 / delta)) / epsi, expe * expand).tolist()
		for k in range(len(out)):
			for i in range(expand):
				out_car.append(cal_fms(out[k] + noise[k*expand + i], w, 2**m))
	if sketch_type == 'll':
		noise = np.random.normal(0, math.sqrt(2 * math.log(1.25 / delta)) * (w + 1) / epsi, expe * expand).tolist()
		for k in range(len(out)):
			for i in range(expand):
				out_car.append(cal_ll(out[k] + noise[k*expand + i], w, 2**m))
	are = [abs(k-10**n) / 10**n for k in out_car]
	aare = sum(are) / len(are)
	return aare

def cal_aare_o_ddp(filename, sketch_type, expe, n, w, m, epsi, delta, d, expand):
	'''sketch_type: 'fm', 'fms', 'll'  \nexpe:100, 10  \nn:3, 5, 7, 9  \nw:6, 7, 8  \nm:10, 11, 12, 13'''
	out = (np.loadtxt(filename)).tolist()
	out = [out] if type(out) == float else out
	out_car = []
	epsi = converse_epsilon_d(epsi, delta)
	if sketch_type == 'fm':
		sigma = cal_sigma(d, epsi, w * (2**m))
		noise = sample_discrete_gaussian(0, sigma, expe * d * expand)
		for i in range(len(out)):
			for j in range(expand):
				out_car.append(cal_fm(out[i] + sum(noise[i * expand * d + j * d: i * expand * d + j * (d + 1)]), w, 2**m))
	if sketch_type == 'fms':
		sigma = cal_sigma(d, epsi, 1)
		noise = sample_discrete_gaussian(0, sigma, expe * d * expand)
		for i in range(len(out)):
			for j in range(expand):
				out_car.append(cal_fms(out[i] + sum(noise[i * expand * d + j * d: i * expand * d + j * (d + 1)]), w, 2**m))
	if sketch_type == 'll':
		sigma = cal_sigma(d, epsi, (w + 1))
		noise = sample_discrete_gaussian(0, sigma, expe * d * expand)
		for i in range(len(out)):
			for j in range(expand):
				out_car.append(cal_ll(out[i] + sum(noise[i * expand * d + j * d: i * expand * d + j * (d + 1)]), w, 2**m))
	are = [abs(k-10**n) / 10**n for k in out_car]
	aare = sum(are) / len(are)
	return aare

def cal_aare_o_ddp_n(filename, sketch_type, expe, n, w, m, epsi, delta, d, expand):
	'''sketch_type: 'fm', 'fms', 'll'  \nexpe:100, 10  \nn:20000, 40000  \nw:6, 7, 8  \nm:10, 11, 12, 13'''
	out = (np.loadtxt(filename)).tolist()
	out = [out] if type(out) == float else out
	out_car = []
	epsi = converse_epsilon_d(epsi, delta)
	if sketch_type == 'fm':
		sigma = cal_sigma(d, epsi, w * (2**m))
		noise = sample_discrete_gaussian(0, sigma, expe * d * expand)
		for i in range(len(out)):
			for j in range(expand):
				out_car.append(cal_fm(out[i] + sum(noise[i * expand * d + j * d: i * expand * d + j * (d + 1)]), w, 2**m))
	if sketch_type == 'fms':
		sigma = cal_sigma(d, epsi, 1)
		noise = sample_discrete_gaussian(0, sigma, expe * d * expand)
		for i in range(len(out)):
			for j in range(expand):
				out_car.append(cal_fms(out[i] + sum(noise[i * expand * d + j * d: i * expand * d + j * (d + 1)]), w, 2**m))
	if sketch_type == 'll':
		sigma = cal_sigma(d, epsi, (w + 1))
		noise = sample_discrete_gaussian(0, sigma, expe * d * expand)
		for i in range(len(out)):
			for j in range(expand):
				out_car.append(cal_ll(out[i] + sum(noise[i * expand * d + j * d: i * expand * d + j * (d + 1)]), w, 2**m))
	are = [abs(k-n) / n for k in out_car]
	aare = sum(are) / len(are)
	return aare


def cal_aare2_o(filename, sketch_type, expe, n, w, m):
	out = (np.loadtxt(filename)).tolist()
	out = [out] if type(out) == float else out
	if sketch_type == "fm":
		out_car = [cal_fm(k, w, 2**m) for k in out]
	elif sketch_type == "fms":
		out_car = [cal_fms(k, w, 2**m) for k in out]
	elif sketch_type == "ll":
		out_car = [cal_ll(k, w, 2**m) for k in out]
	else:
		out_car = 0
	are2 = [(k-10**n)**2 for k in out_car]
	aare2 = sum(are2)**0.5 / 10**n
	return aare2

def cal_aare(filename, sketch_type, expe, n, w, m):
	''' n: like 3, 5, 7, 9 \n m: like 10, 11, 12, 13'''
	out = (np.loadtxt(filename)).tolist()
	out_car = []
	if sketch_type == "fm":
		for i in range(expe):
			out_z = 0
			for j in range(2**m):
				out_z += fm_z(out[i*(2**m)+j])
			out_car.append(cal_fm(out_z, w, 2**m))
	elif sketch_type == "fms":
		for i in range(expe):
			out_z = 0
			for j in range(2**m):
				out_z += fms_z(out[i*(2**m)+j])
			out_car.append(cal_fms(out_z, w, 2**m))
	elif sketch_type == "ll":
		for i in range(expe):
			out_z = 0
			for j in range(2**m):
				out_z += ll_z(out[i*(2**m)+j])
			out_car.append(cal_ll(out_z, w, 2**m))
	else:
		out_car = 0
	are = [abs(k-10**n) / 10**n for k in out_car]
	aare = sum(are) / expe
	return aare



def cal_fm_z(n):
	phi = 0.77351
	return math.log(n * phi, 2)

# manipulate_files

def merge_files(files):
	"""files[0]: output \n
	   files[1:]: input"""
	lines = []
	for i in files[1:]:
		with open(i, 'r') as f:
			for line in f:
				lines.append(line)
	with open(files[0], 'w') as f:
		for i in lines:
			f.write(i)

def gene_sudo_sketch(files, m, expe):
	"""files[0]: input \n
	   files[1]: output"""
	ori_lines = []
	with open(files[0], 'r') as f:
		for line in f:
			ori_lines.append(line)
	lines = []
	for i in range(expe):
		sub_lines = np.random.choice(ori_lines, m)
		lines.extend(sub_lines)
	with open(files[1], 'w') as f:
		for i in lines:
			f.write(i)

def gene_o(file, expe, m, sketch_type):
	"""file: input"""
	sketch = (np.loadtxt(file)).tolist()
	out_file = []
	if sketch_type == "fm":
		for i in range(expe):
			out_z = 0
			for j in range(m):
				out_z += fm_z(sketch[i*m + j])
			out_file.append(out_z)

	if sketch_type == "fms":
		for i in range(expe):
			out_z = 0
			for j in range(m):
				out_z += fms_z(sketch[i*m + j])
			out_file.append(out_z)

	if sketch_type == "ll":
		for i in range(expe):
			out_z = 0
			for j in range(m):
				out_z += ll_z(sketch[i*m + j])
			out_file.append(out_z)
	with open(file[:-4] + '-o' + file[-4:], 'w') as f:
		for i in out_file:
			f.write(str(i))
			f.write('\n')

def truncate_fm_files(in_file, out_file, in_w, out_w):
	""" out_w must be lower than in_w """
	in_sketch = (np.loadtxt(in_file)).tolist()
	out_sketch = []
	for i in range(len(in_sketch)):
		out_sketch.append(in_sketch[i][ : out_w - 1])
		if (1 in in_sketch[i][out_w - 1 : ]):
			out_sketch[-1].append(1)
		else:
			out_sketch[-1].append(0)
	with open(out_file, 'w') as f:
		for i in range(len(out_sketch)):
			for j in range(out_w):
				f.write(str(int(out_sketch[i][j])))
				f.write(' ')
			f.write('\n')

def w_bucket(n, m):
	'''n: like 3, 5, 7, 9 \n m: like 10, 11, 12, 13'''
	return math.ceil(math.log(10**n / 2**m, 2) + 4)

def w_bucket_n(n, m):
	'''n: like 20000, 30000 \n m: like 10, 11, 12, 13'''
	return math.ceil(math.log(n / 2**m, 2) + 4)

def w_no_bucket(n):
	'''n: like 3, 5, 7, 9'''
	return math.ceil(math.log(10**n, 2) + 4)

def bench_hash():
	scale = 10**7
	seeds = np.random.randint(2**31, size = scale)
	start_time = time.time()
	for i in range(scale):
		h = mmh3.hash("foo", seeds[i])
	print(time.time() - start_time)

if __name__ == '__main__':
	print('abc')
	# print(cal_aare_o_n('sketches/fms-20000-13-o.txt', 'fms', 100, 20000, w_bucket_n(20000, 13), 13))
	# prefix = 'sketches/'
	# merge_files([prefix+'fms-7-10-merge.txt', prefix+'fms-7-10.txt'])
	# gene_sudo_sketch([prefix+'fms-7-10-merge.txt', prefix+'fms-7-10.txt'], 2**10, 100)
	# gene_o(prefix+'fms-7-10.txt', 100, 2**10, 'fms')

	# merge_files([prefix+'fms-7-11-merge.txt', prefix+'fms-7-11.txt'])
	# gene_sudo_sketch([prefix+'fms-7-11-merge.txt', prefix+'fms-7-11.txt'], 2**11, 100)
	# gene_o(prefix+'fms-7-11.txt', 100, 2**11, 'fms')

	# merge_files([prefix+'fms-7-12-merge.txt', prefix+'fms-7-12.txt'])
	# gene_sudo_sketch([prefix+'fms-7-12-merge.txt', prefix+'fms-7-12.txt'], 2**12, 100)
	# gene_o(prefix+'fms-7-12.txt', 100, 2**12, 'fms')

	# merge_files([prefix+'fms-7-13-merge.txt', prefix+'fms-7-13.txt'])
	# gene_sudo_sketch([prefix+'fms-7-13-merge.txt', prefix+'fms-7-13.txt'], 2**13, 100)
	# gene_o(prefix+'fms-7-13.txt', 100, 2**13, 'fms')