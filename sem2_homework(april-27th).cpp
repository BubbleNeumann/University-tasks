#include <iostream>
template<class type> class vect
{
	type* p;
	type* end;

public:
	vect(int n = 0)
	{
		if (n)
		{
			p = new type[n];
			end = p + n;
			std::cout << '\n';
			for (int i = 0; i++ < n; p[i] = i);
			for (int i = 0; i++ < n; std::cout << p[i] << " ");

		}
		else p = end = NULL;
	}
	
	int size() { return end - p; }
	
	/*int* F2(const int* a, int an, const int* b, int bn)
	{
		int* q = new int[an + bn];
		int cn = an;
		for (;an--;*(q + an) = *(a + an));
		for (;bn--;*(q + cn + bn) = *(b + bn));
		return q;
	}*/

	vect operator+=(vect<type>& arr)
	{
		int n = this->size();
		int n1 = arr.size();
		
		vect<type> V(n + n1); 
		int cn = n;
		int dn = n1;
    	for (; n; *(V.p + n) = *(p + n), n--);
		for (; n1; *(V.p + cn + n1) = *(arr.p + n1), n1--);

		std::cout << '\n';
		for (int i = 0; i++ < (cn+dn); std::cout << V.p[i] << " ");
		std::swap(p, V.p);
		std::swap(arr.end, V.end);

		return V;
	}
};

int main()
{
	vect<int> a(2);
	vect<int> b(3);
	a += b;

	return 0;
}