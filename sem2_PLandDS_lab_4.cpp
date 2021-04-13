#include <fstream>

class Vessel
{
protected:

	// current amount of content
	unsigned int volume;

	// max amount of content
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
	void transfusion(Vessel&, Vessel&, unsigned int);
	bool isFull();

	Vessel& operator =(const Vessel&);
	
	Vessel& operator +(unsigned int);
	int operator +(Vessel&);

	Vessel& operator -(unsigned int);

	// logical operations overloading
	bool operator >(Vessel&);
	bool operator >=(Vessel&);
	bool operator <(Vessel&);
	bool operator <=(Vessel&);
	bool operator ==(Vessel&);

	friend void operator << (std::ofstream&, Vessel&);
	friend void operator >> (std::ifstream&, Vessel&);
};


class HoleyVessel: public Vessel
{
	// how much content the vessel lose in one minute
	double outflow_per_min;

public:

	// default constructor
	HoleyVessel()
	{
		volume = 0;
		capacity = 0;
		outflow_per_min = 0;
	}

	// initialization constructor
	HoleyVessel(int, int, double);

	// copy constructor
	HoleyVessel(HoleyVessel&);

	// in what time the vessel will become empty
	double countEmptyTime();
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

int Vessel::getVolume()
{
	return volume;
}

void Vessel::transfusion(Vessel& from, Vessel& to, unsigned int n)
{
	// if it is possible to take or place required amount of water
	if (from.volume < n || (to.capacity - to.volume) < n)
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

Vessel& Vessel::operator +(unsigned int n)
{
	// if possible to add sertain amount of water 
	if (capacity - volume < n) n = capacity - volume;
	volume += n;
	return *this;
}

int Vessel::operator +(Vessel& add)
{
	return volume + add.volume;
}

Vessel& Vessel::operator -(unsigned int n)
{
	// if the vessel contains required amount of water
	if (n > volume) n = volume;
	volume -= n;
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

bool Vessel::operator >=(Vessel& another)
{
	if (capacity < another.capacity)
	{
		if (volume < another.volume) return false;
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

bool Vessel::operator <=(Vessel& another)
{
	if (capacity > another.capacity)
	{
		if (volume > another.volume) return false;
	}
	return true;
}

bool Vessel::operator ==(Vessel& another)
{
	// returns true only if all atributes of both objects are equal
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
	if (obj.volume > obj.capacity) obj.volume = obj.capacity;
}

HoleyVessel::HoleyVessel(int vol, int cap, double outflow)
{
	volume = vol;
	capacity = cap;
	outflow_per_min = outflow;
}

HoleyVessel::HoleyVessel(HoleyVessel& templ)
{
	volume = templ.volume;
	capacity = templ.capacity;
	outflow_per_min = templ.outflow_per_min;
}

double HoleyVessel::countEmptyTime()
{
	return volume / outflow_per_min;
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
			if (first == second) inf << "first == second";
			else if (first < second) inf << "first < second";
			else inf << "first > second";
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
			if (first == second) inf << "first == second";
			else if (first < second) inf << "first < second";
			else inf << "first > second";
		}
	}

	fromf.close();
	inf.close();

	return 0;
}
