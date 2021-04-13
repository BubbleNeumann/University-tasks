#include <fstream>

class Vessel
{
protected:

	unsigned int volume;
	unsigned int capacity;

public:

	// default constructor
	Vessel () 
	{
		volume = 0;
		capacity = 0;
	}

	// initialization constructor
	Vessel(int, int);

	// copy constructor
	Vessel(Vessel&);


	int getVolume();
	void transfusion(Vessel&, Vessel&, int);
	bool isFull();

	Vessel& operator =(const Vessel&);
	
	Vessel& operator +(int);
	Vessel& operator +(Vessel&);

	Vessel& operator -(int);
	Vessel& operator -(Vessel&);


	bool operator >(Vessel&);
	bool operator <(Vessel&);
	bool operator ==(Vessel&);

	friend void operator << (std::ofstream& fin, Vessel& obj);
	friend void operator >> (std::ifstream& strin, Vessel& obj);
};


class HoleyVessel: public Vessel
{
	int outflow_per_min;

public:
	HoleyVessel()
	{
		volume = 0;
		capacity = 0;
		outflow_per_min = 0;
	}
	HoleyVessel(int);
};

Vessel::Vessel(int vol, int cap)
{
	volume = vol;
	capacity = cap;
}

Vessel::Vessel(Vessel& templ)
{
	volume = templ.volume;
	capacity = templ.capacity;
}


HoleyVessel::HoleyVessel(int n)
{
	outflow_per_min = n;
}

int Vessel::getVolume()
{
	return volume;
}

void Vessel::transfusion(Vessel& from, Vessel& to, int n)
{
	if (from.volume < n || (to.capacity - to.volume < n))
	{ 
		n = std::min(from.volume, to.capacity - to.volume);
	}
	from.volume -= n;
	to.volume += n;
}

bool Vessel::isFull()
{
	return volume == capacity;
}


Vessel& Vessel::operator =(const Vessel& templ)
{
	if (this == &templ) return *this;
	volume = templ.volume;
	capacity = templ.capacity;
	return *this;
}


Vessel& Vessel::operator +(int n)
{
	if (capacity - volume < n) n = capacity - volume;
	volume += n;
	return *this;
}

Vessel& Vessel::operator +(Vessel& add)
{
	this->transfusion(add, *this, add.volume);
	return *this;
}

Vessel& Vessel::operator -(int n)
{
	if (n > volume) n = volume;
	volume -= n;
}

Vessel& Vessel::operator -(Vessel& dec)
{
	this->transfusion(*this, dec, dec.volume);
	return *this;
}

bool Vessel::operator >(Vessel& another)
{
	if (capacity <= another.capacity)
	{
		if (volume <= another.volume) return false;
	}
	return true;
}

bool Vessel::operator <(Vessel& another)
{
	if (capacity >= another.capacity)
	{
		if (volume >= another.volume) return false;
	}
	return true;
}

bool Vessel::operator ==(Vessel& another)
{
	if (capacity == another.capacity && volume == another.volume) return true;
	return false;
}

void operator << (std::ofstream& fin, Vessel& obj)
{
	fin << "Vessel volume: " << obj.volume << ", capacity: " << obj.capacity << '\n';
}

void operator >> (std::ifstream& fromf, Vessel& obj)
{
	fromf >> obj.volume >> obj.capacity;
}


int main()
{
	std::ifstream fromf("input.txt");
	std::ofstream inf("output.txt");

	unsigned int key;
	fromf >> key;

	if (key == 0 || key == 1)
	{
		Vessel first, second;
		
		fromf >> first;
		fromf >> second;

		if (key == 0)
		{
			inf << first + second;
		}
		else
		{
			inf << (bool)(first > second);
		}

	}
	else if (key == 2 || key == 3)
	{
		HoleyVessel first, second;
		fromf >> first;
		fromf >> second;

		if (key == 2)
		{
			inf << first + second;
		}
		else
		{
			inf << (bool)(first > second);
		}
	}

	fromf.close();
	inf.close();

	return 0;
}
