#include<iostream>
#include<fstream>
#include<iterator>
#include<string>
#include<vector>
#include<fstream>
#include<iomanip>
#include<math.h>
#include<cstdlib>
#include<thread>
#include<mutex>
#include<time.h>
#include<chrono>
#include"MurmurHash3.h"

using namespace std;
using namespace chrono;

// output file naming form: fm-3-10.txt fm-3-10-o.txt, the -o option means the estimator of each line.

// vector<int> m_list = {1024, 2048, 4096, 8192};
// vector<int> bits_list = {10, 11, 12, 13};

//!!!!!!!!!!!!!!sketch_type : 1,fm     2,fms    3,ll

vector<int> bits_list = {10, 12};
vector<int> n_list = {3, 5, 7, 9};
int clear_file = 1;
int cores = 70;
int gene_fm = 0, gene_ll = 0, gene_fms = 1;

int max_m = 8192;
int max_w = 40;

mutex re, re1;

bool fm[8192 * 40];
bool fms[8192 * 40];
bool ll[8192 * 40];

unsigned mrands[8192];
unsigned rands[2];

//////////////////////0////1/////2//////3/////4////5////6////7////8/////9/////10////11////12///13/////////14//////15//////////
vector<string> st = {"-", "fm", "fms", "ll", "3", "5", "7", "9", "10", "11", "12", "13", "o", "twitter", ".txt", "./sketches/"};

int m, n, i, j, k, l, expe, fm_w, fms_w, ll_w, bits, cycle;

////////////////////////////////////////////// the tools needed.

void init_sketch_and_mrands(int m, int sketch_type) //to intiate fm, fmsum and mrands.
{
	if (sketch_type == 1)
	{
		fill(fm, fm+max_m*max_w, 0);
		for (int i = 0; i < m; ++i)
		{
			mrands[i] = rand();
		}
	}

	if (sketch_type == 2)
	{
		fill(fms, fms+max_m*max_w, 0);
		rands[0] = rand();
		rands[1] = rand();
	}

	if (sketch_type == 3)
	{
		fill(ll, ll+max_m*max_w, 0);
		rands[0] = rand();
		rands[1] = rand();
	}
}

int rank_tailing_zeros(__uint128_t out, int sketch_type) // to calculate the number of tailing zeros of unsigned.
{
	int zeros = 0, w;
	__uint128_t mask = 1, bench = 0;

	if (sketch_type == 1)
	{
		w = fm_w;
	}

	if (sketch_type == 2)
	{
		w = fms_w;
	}

	if (sketch_type == 3)
	{
		w = ll_w;
	}

	while(zeros < w-1)
	{
		if ((out & mask) == bench)
		{
			++zeros;
		}
		else
		{
			break;
		}
		mask *= 2;
	}
	return zeros;
}

int get_BucketNum_and_Rank(__uint128_t out, int * bucket_index, int sketch_type)
{
	int zeros = 0, w;
	__uint128_t musk = 1, bench = 0, musk_bucket = pow(2, bits) - 1;
	if (sketch_type == 1)
	{
		w = fm_w;
	}

	if (sketch_type == 2)
	{
		w = fms_w;
	}

	if (sketch_type == 3)
	{
		w = ll_w;
	}

	while(zeros < w-1)
	{
		if ((out & musk) == bench)
		{
			++zeros;
		}
		else
		{
			break;
		}
		musk *= 2;
	}
	out = out >> w;
	*bucket_index = musk_bucket & out;
	return zeros;
}

int expe_times(int n, int sketch_type)
{
	int expe = 0;
	if (sketch_type == 2)
	{
		expe = 10;
	}

	if (sketch_type == 3)
	{
		expe = 10;
	}

	if (sketch_type == 1)
	{
		if (n <= 6)
		{
			expe = 10;
		}
		else if (n <= 8)
		{
			expe = 1;
		}
		else if (n <= 9)
		{
			expe = 1;
		}
		else
		{
			expe = 1;
		}
	}
	return expe;
}

int chose_w(int n_i, int m_i, int sketch_type)
{
	int w = 0;
	double n = n_i, m = m_i;

	if (sketch_type == 1)
	{
		w = ceil(log2(pow(10, n)) + 4);
	}

	if (sketch_type == 2)
	{
		w = ceil(log2(pow(10, n) / m) + 4);
	}

	if (sketch_type == 3)
	{
		w = ceil(log2(pow(10, n) / m) + 4);
	}
	return w;

}

////////////////////////////////////////////// perform data collection

// void collect(int scale, ifstream * input_file)
// {
// 	int i = 0, j = 0, tailing_zeros, bucket_index, rank;
// 	__uint128_t hash_output;
// 	const char *key;
// 	string sentence;
// 	for (i = 0; i < scale; ++i)
// 	{
// 		getline(*input_file, sentence);
// 		key = sentence.c_str();
// 		for (j = 0; j < m; ++j)
// 		{
// 			MurmurHash3_x64_128(key, sentence.size(), mrands[j], &hash_output);
// 			tailing_zeros = rank_tailing_zeros(hash_output, 4);
// 			fm[j * fm_w + tailing_zeros] = 1;
// 		}
// 		MurmurHash3_x64_128(key, sentence.size(), rands[0], &hash_output);
// 		rank = get_BucketNum_and_Rank(hash_output, &bucket_index, 4);
// 		fms[bucket_index * fm_w + rank] = 1;
// 		MurmurHash3_x64_128(key, sentence.size(), rands[1], &hash_output);
// 		rank = get_BucketNum_and_Rank(hash_output, &bucket_index, 4);
// 		ll[bucket_index * w + rank] = 1;
// 	}
// }

void collect_fm(int scale, int core, int cardi)
{
	ifstream input_file;
	input_file.open("./twitter-" + to_string(cardi) + "/" + st[13] + st[0] + to_string(cardi) + st[0] + to_string(core) + st[14]);
	int i = 0, j = 0, tailing_zeros;
	__uint128_t hash_output;
	const char *key;
	string sentence;
	for (i = 0; i < scale; ++i)
	{
		getline(input_file, sentence);
		key = sentence.c_str();
		for (j = 0; j < m; ++j)
		{
			MurmurHash3_x64_128(key, sentence.size(), mrands[j], &hash_output);
			tailing_zeros = rank_tailing_zeros(hash_output, 1);
			fm[j * fm_w + tailing_zeros] = 1;
		}
	}
}

void collect_ll(int scale, int core, int cardi)
{
	ifstream input_file;
	input_file.open("./twitter-" + to_string(cardi) + "/" + st[13] + st[0] + to_string(cardi) + st[0] + to_string(core) + st[14]);
	int i = 0, j = 0, tailing_zeros, bucket_index, rank;
	__uint128_t hash_output;
	const char *key;
	string sentence;
	for (i = 0; i < scale; ++i)
	{
		getline(input_file, sentence);
		key = sentence.c_str();
		MurmurHash3_x64_128(key, sentence.size(), rands[1], &hash_output);
		rank = get_BucketNum_and_Rank(hash_output, &bucket_index, 3);
		ll[bucket_index * ll_w + rank] = 1;
	}
}

void collect_fms(int scale, int core, int cardi, double * thread_time)
{
	ifstream input_file;
	input_file.open("./twitter-" + to_string(cardi) + "/" + st[13] + st[0] + to_string(cardi) + st[0] + to_string(core) + st[14]);
	int i = 0, j = 0, tailing_zeros, bucket_index, rank;
	__uint128_t hash_output;
	const char *key;
	string sentence;
	auto start = system_clock::now();
	for (i = 0; i < scale; ++i)
	{
		getline(input_file, sentence);
		key = sentence.c_str();
		MurmurHash3_x64_128(key, sentence.size(), rands[0], &hash_output);
		rank = get_BucketNum_and_Rank(hash_output, &bucket_index, 2);
		fms[bucket_index * fms_w + rank] = 1;
	}
	auto end   = system_clock::now();
	auto duration = duration_cast<microseconds>(end - start);
	*thread_time = double(duration.count()) * microseconds::period::num / microseconds::period::den;
}


void write_files(ofstream * output_file, ofstream * output_file_o, int sketch_type)
{
	int i, j, fm_o = 0, fms_o = 0, ll_o = 0, flag = 0, ll_temp, w;
	if (sketch_type == 1)
	{
		w = fm_w;
	}

	if (sketch_type == 2)
	{
		w = fms_w;
	}

	if (sketch_type == 3)
	{
		w = ll_w;
	}

	if (sketch_type == 1)
	{
		for (i = 0; i < m; ++i)
		{
			flag = 0;
			for (j = 0; j < w; ++j)
			{
				if (flag == 0 && fm[i*w + j] == 0)
				{
					flag = 1;
					fm_o += j;
				}
				* output_file << fm[i*w + j] << " ";
			}
			if (flag == 0)
			{
				fm_o += w;
			}
			* output_file << endl;
		}
		* output_file_o << fm_o << endl;
	}

	if (sketch_type == 2)
	{
		for (i = 0; i < m; ++i)
		{
			for (j = 0; j < w; ++j)
			{
				if (fms[i*w + j] == 0)
				{
					fms_o += 1;
				}
				* output_file << fms[i*w + j] << " ";
			}
			* output_file << endl;
		}
		* output_file_o << fms_o << endl;
	}

	if (sketch_type == 3)
	{
		for (i = 0; i < m; ++i)
		{
			ll_temp = 0;
			for (j = 0; j < w; ++j)
			{
				if (ll[i*w + j] == 1)
				{
					ll_temp = (j + 1);
				}
				* output_file << ll[i*w + j] << " ";
			}
			ll_o += ll_temp;
			* output_file << endl;
		}
		* output_file_o << ll_o << endl;
	}
}

void create_and_clear_files(int n, int i, int sketch_type)
{
	if (sketch_type == 1)
	{
		ofstream output_file_fm;
		ofstream output_file_fm_o;
		output_file_fm.open(st[15]+st[1]+st[0]+to_string(n)+st[0]+to_string(bits_list[i])+st[14]);
		output_file_fm_o.open(st[15]+st[1]+st[0]+to_string(n)+st[0]+to_string(bits_list[i])+st[0]+st[12]+st[14]);
		output_file_fm.close();
		output_file_fm_o.close();
	}
	if (sketch_type == 2)
	{
		ofstream output_file_fms;
		ofstream output_file_fms_o;
		output_file_fms.open(st[15]+st[2]+st[0]+to_string(n)+st[0]+to_string(bits_list[i])+st[14]);
		output_file_fms_o.open(st[15]+st[2]+st[0]+to_string(n)+st[0]+to_string(bits_list[i])+st[0]+st[12]+st[14]);
		output_file_fms.close();
		output_file_fms_o.close();
	}
	if (sketch_type == 3)
	{
		ofstream output_file_ll;
		ofstream output_file_ll_o;
		output_file_ll.open(st[15]+st[3]+st[0]+to_string(n)+st[0]+to_string(bits_list[i])+st[14]);
		output_file_ll_o.open(st[15]+st[3]+st[0]+to_string(n)+st[0]+to_string(bits_list[i])+st[0]+st[12]+st[14]);
		output_file_ll.close();
		output_file_ll_o.close();
	}
}

void process_fm()
{
	ofstream output_file_fm;
	ofstream output_file_fm_o;
	srand((unsigned int)(time(NULL)));
	for (j = 0; j < n_list.size(); j++)
	{
		for (i = 0; i < bits_list.size(); i++)
		{
			m = pow(2, bits_list[i]);
			n = n_list[j];
			expe = expe_times(n, 1);
			fm_w = chose_w(n, m, 1);
			bits = bits_list[i];
			if (clear_file == 1)
			{
				create_and_clear_files(n, i, 1);
			}
			for (cycle = 0; cycle < expe; ++cycle)
			{
				init_sketch_and_mrands(m, 1);
				thread threads[cores];
				output_file_fm.open(st[15]+st[1]+st[0]+to_string(n)+st[0]+to_string(bits_list[i])+st[14], ios::app);
				output_file_fm_o.open(st[15]+st[1]+st[0]+to_string(n)+st[0]+to_string(bits_list[i])+st[0]+st[12]+st[14], ios::app);
				for (k = 0; k < cores-1; ++k)
				{
					threads[k] = thread(collect_fm, (int)pow(10, n) / cores, k, n);
				}
				threads[cores-1] = thread(collect_fm, ((int)pow(10, n) / cores) + ((int)pow(10, n) % cores), k, n);
				for (k = 0; k < cores; ++k)
				{
					threads[k].join();
				}
				write_files(& output_file_fm, & output_file_fm_o, 1);
				output_file_fm.close();
				output_file_fm_o.close();
			}
		}
	}
}

void process_ll()
{
	ofstream output_file_ll;
	ofstream output_file_ll_o;
	srand((unsigned int)(time(NULL)));
	for (j = 0; j < n_list.size(); j++)
	{
		for (i = 0; i < bits_list.size(); i++)
		{
			m = pow(2, bits_list[i]);
			n = n_list[j];
			expe = expe_times(n, 3);
			ll_w = chose_w(n, m, 3);
			bits = bits_list[i];
			if (clear_file == 1)
			{
				create_and_clear_files(n, i, 3);
			}
			for (cycle = 0; cycle < expe; ++cycle)
			{
				init_sketch_and_mrands(m, 3);
				thread threads[cores];
				output_file_ll.open(st[15]+st[3]+st[0]+to_string(n)+st[0]+to_string(bits_list[i])+st[14], ios::app);
				output_file_ll_o.open(st[15]+st[3]+st[0]+to_string(n)+st[0]+to_string(bits_list[i])+st[0]+st[12]+st[14], ios::app);
				for (k = 0; k < cores-1; ++k)
				{
					threads[k] = thread(collect_ll, (int)pow(10, n) / cores, k, n);
				}
				threads[cores-1] = thread(collect_ll, ((int)pow(10, n) / cores) + ((int)pow(10, n) % cores), cores-1, n);
				for (k = 0; k < cores; ++k)
				{
					threads[k].join();
				}
				write_files(& output_file_ll, & output_file_ll_o, 3);
				output_file_ll.close();
				output_file_ll_o.close();
			}
		}
	}
}

void process_fms()
{
	ofstream output_file_fms;
	ofstream output_file_fms_o;
	double total_time[cores] = {0};
	double ave_time = 0;
	srand((unsigned int)(time(NULL)));
	for (j = 0; j < n_list.size(); j++)
	{
		for (i = 0; i < bits_list.size(); i++)
		{
			m = pow(2, bits_list[i]);
			n = n_list[j];
			ave_time = 0;
			expe = expe_times(n, 2);
			fms_w = chose_w(n, m, 2);
			bits = bits_list[i];
			if (clear_file == 1)
			{
				create_and_clear_files(n, i, 2);
			}
			for (cycle = 0; cycle < expe; ++cycle)
			{
				init_sketch_and_mrands(m, 2);
				thread threads[cores];
				output_file_fms.open(st[15]+st[2]+st[0]+to_string(n)+st[0]+to_string(bits_list[i])+st[14], ios::app);
				output_file_fms_o.open(st[15]+st[2]+st[0]+to_string(n)+st[0]+to_string(bits_list[i])+st[0]+st[12]+st[14], ios::app);
				for (k = 0; k < cores-1; ++k)
				{
					threads[k] = thread(collect_fms, (int)pow(10, n) / cores, k, n, &total_time[k]);
				}
				threads[cores-1] = thread(collect_fms, ((int)pow(10, n) / cores) + ((int)pow(10, n) % cores), cores-1, n, &total_time[cores-1]);
				for (k = 0; k < cores; ++k)
				{
					threads[k].join();
				}
				for (k = 0; k < cores; ++k)
				{
					ave_time += total_time[k];
				}
				write_files(& output_file_fms, & output_file_fms_o, 2);
				output_file_fms.close();
				output_file_fms_o.close();
			}
			cout << "n: " << n << "  m: " << m << "  time: " << ave_time / (expe * cores) << endl;
		}
	}
}

int main()
{
	if (gene_fm == 1)
	{
		process_fm();
	}

	if (gene_fms == 1)
	{
		process_fms();
	}

	if (gene_ll == 1)
	{
		process_ll();
	}
	return 0;
}