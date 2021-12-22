#include <iostream>
#include<omp.h>
#include<stdio.h>
#include<stdlib.h>
#define N 1000

using namespace std;
int a[N];

int maximum(int A[])
{
    long idx;
    int max_val=0; 
    #pragma omp parallel for reduction(max:max_val) num_threads(4)
    for (idx = 0; idx < N; idx++)
       max_val = max_val > A[idx] ? max_val : A[idx];

    return max_val;
}

int minimum(int A[])
{
    long idx;
    int min_val=0; 
    #pragma omp parallel for private(idx) reduction(min:min_val) num_threads(4)
    for (idx = 0; idx < N; idx++)
       min_val = min_val < A[idx] ? min_val : A[idx];

    return min_val;
}

int main(int argc, char const *argv[])
{
	double start, end;
    long sum1=0,sum2=0;
    int max,min;
    long i;
    
    for (i = 0; i < N; ++i)
    {
    	a[i]=rand()%10;
    }
    
    //Serial block for array sum
    cout<<"The Serial Block for Sum:\n";
    start = omp_get_wtime( );
    for (i = 0; i < N; ++i)
    {
    	sum1+=a[i];
    }
    cout<<"Sum="<<sum1<<endl;
    cout<<"Average="<<float(sum1)/float(N)<<endl;
    end = omp_get_wtime( );
    cout<<"The time taken is: "<<(end-start)<<endl;
    cout<<endl;

    //Parallel block for array sum
    cout<<"The Parallel Block for Sum:\n";
    start = omp_get_wtime( );
    #pragma omp parallel for private(i) reduction(+:sum2) num_threads(4)
    for (i = 0; i < N; ++i)
    {
    	sum2 += a[i];
    }
    
   
    cout<<"Sum="<<sum2<<endl;
    cout<<"Average="<<float(sum2)/float(N)<<endl;
    end = omp_get_wtime( );
    cout<<"The time taken is:"<<(end-start)<<endl<<endl;
    
    //max
    cout<<"Serial block for max:\n";
    start=omp_get_wtime();
    max=a[i];
    for(i=0;i<N;i++)
    {
    	max = max > a[i] ? max : a[i];
    }
    cout<<"Max="<<max<<endl;
    end=omp_get_wtime();
    cout<<"The time taken is:"<<(end-start)<<endl<<endl;
    
    cout<<"Parallel Block for Max:\n";
    start=omp_get_wtime();
    max=maximum(a);
    cout<<"Max="<<max<<endl;
    end=omp_get_wtime();
    cout<<"The time taken is:"<<(end-start)<<endl<<endl;
    
    
    //min
    cout<<"Serial block for min:\n";
    start=omp_get_wtime();
    min=a[i];
    for(i=0;i<N;i++)
    {
    	min = min < a[i] ? min : a[i];
    }
    cout<<"Min="<<min<<endl;
    end=omp_get_wtime();
    cout<<"The time taken is:"<<(end-start)<<endl<<endl;
    
    cout<<"Parallel Block for min:\n";
    start=omp_get_wtime();
    min=minimum(a);
    cout<<"Min="<<min<<endl;
    end=omp_get_wtime();
    cout<<"The time taken is:"<<(end-start)<<endl<<endl;
	return 0;
}       







