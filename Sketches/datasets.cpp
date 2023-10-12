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

void hash_x64_128()
{
    int i = 0;
    const char *key;
    ifstream input;
    string sentence;
    __uint128_t hash_output;
    input.open("twitter-8.txt");
    for (i = 0; i < 100000000; ++i)
    {
        getline(input, sentence);
        key = sentence.c_str();
        MurmurHash3_x64_128(key, sentence.size(), 1234, &hash_output);
    }
}

void hash_x86_128()
{
    int i = 0;
    const char *key;
    ifstream input;
    string sentence;
    __uint128_t hash_output;
    input.open("twitter-8.txt");
    for (i = 0; i < 100000000; ++i)
    {
        getline(input, sentence);
        key = sentence.c_str();
        MurmurHash3_x86_128(key, sentence.size(), 1234, &hash_output);
    }
}

void hash_32()
{
    int i = 0;
    const char *key;
    ifstream input;
    string sentence;
    unsigned hash_output;
    input.open("twitter-8.txt");
    for (i = 0; i < 100000000; ++i)
    {
        getline(input, sentence);
        key = sentence.c_str();
        MurmurHash3_x86_32(key, sentence.size(), 1234, &hash_output);
    }
}

void measure_time(void (*fp)(void))
{
    auto start = system_clock::now();
    fp();
    auto end   = system_clock::now();
    auto duration = duration_cast<microseconds>(end - start);
    cout << "time: " << double(duration.count()) * microseconds::period::num / microseconds::period::den << endl;
}

void compare_time()
{
    void (*fp)(void);
    fp = hash_x64_128;
    measure_time(fp);

    fp = hash_x86_128;
    measure_time(fp);

    fp = hash_32;
    measure_time(fp);
}

int expe_times(int n)
{
	int expe = 0;
	switch(n)
	{
		case 3:
		case 4:
		case 5:
		case 6:
			expe = 100;
			break;
		case 7:
			expe = 5;
			break;
		case 8:
		case 9:
			expe = 1;
			break;
		default:
			expe = 0;
	}
	return expe;
}

void divide_files(int n)
{
    int i, j, cores = 70;
    ifstream input_file;
    input_file.open("twitter-" + to_string(n) + ".txt");
    ofstream output_file;
    string pre("twitter-" + to_string(n) + "/twitter-"  + to_string(n) +  "-");
    string suf(".txt");
    string sentence;
    for (i = 0; i < cores; ++i)
    {
        output_file.open(pre + to_string(i) + suf, ios::app);
        for (j = 0; j < (int)pow(10, n) / cores; j++)
        {
            getline(input_file, sentence);
            output_file << sentence;
            output_file << '\n';
        }
        output_file.close();
    }
    output_file.open(pre + to_string(cores-1) + suf, ios::app);
    for (j = 0; j < (int)pow(10, n) % cores; j++)
    {
        getline(input_file, sentence);
        output_file << sentence;
        output_file << '\n';
    }
    output_file.close();
    input_file.close();
}

int main(void)
{
    divide_files(3);
    divide_files(5);
    divide_files(7);
    divide_files(9);
    return 0;
}