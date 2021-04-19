#include <fstream>
#include <random>

class Vessel
{
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

    unsigned int getVolume() const;
};

Vessel::Vessel(int vol, int cap)
{
    volume = vol;
    capacity = cap;
}

unsigned int Vessel::getVolume() const
{
    return volume;
}

struct list
{
    Vessel obj;
    list *next;
};

/**
 * initialize new list of vessels with one element
 * @param vol, cap - parameters of the first vessel
 */
list *init(int vol, int cap)
{
    list *temp = new list;

    // create new Vessel object
    temp->obj = Vessel(vol, cap);

    temp->next = temp;
    return temp;
}

/**
 * add element to the end of the cyclic list
 * @param head
 * @param vol, cap - parameters of the new vessel
 */
void pushback(list *&head, int vol, int cap)
{
    list *temp = head;

    // initialize list if it's empty
    if (!head) head = init(vol, cap);
    else
    {
        // move to the end of the list
        while (temp->next != head) temp = temp->next;

        temp->next = init(vol, cap);
        temp = temp->next;
        temp->next = head;
    }
}

/**
 * destructor of a list structure
 * @param head - pointer on the first element of the list
 * @param n - number of elements the list contains
 */
void erase(list *&head, int n)
{
    for (list *tmp = head->next; --n; delete head, head = tmp, tmp = head->next);
}

/**
 * "overloading" of std::swap for 2 list elements
 * @param head - in what list to perform the swap
 * @param i - position of the first element
 * @param j - second elment
 * @return new list with
 */
void swap(list *head, int i, int j)
{
    if (i == j) return;
    if (j < i) std::swap(i, j);
    list **i_ptr = &head;
    for (; *i_ptr && i--; i_ptr = &(*i_ptr)->next, --j);
    list **j_ptr = i_ptr;
    for (; *j_ptr && j--; j_ptr = &(*j_ptr)->next);
    if (*i_ptr && *j_ptr)
    {
        std::swap(*i_ptr, *j_ptr);
        std::swap((*i_ptr)->next, (*j_ptr)->next);
    }
}

void insertionSort(list*& head, int n)
{
    list* temp;
    unsigned int t;
    for (int i = 1; i < n; ++i) {
        temp = head;
        for (int k = 0; k < i; ++k, temp = temp->next);
        t = temp->obj.getVolume();
        int j = i - 1;
        temp = head;
        for (int i = 0 ; i < j; ++i, temp = temp->next);
        while (0 <= j && t < temp->obj.getVolume())
        {
            swap(head, j + 1, j);
            --j;
            temp = head;
            for (int i = 0; i < j; ++i) temp = temp->next;
        }
    }
}

bool isSorted(list* head, int n)
{
    while (--n)
    {
        // check whether next object's value is not less than current's one
        if (head->obj.getVolume() > head->next->obj.getVolume()) return false;
        head = head->next;
    }
    return true;
}

/**
 * create a new list filled with random numbers
 * @param n - number of elements to randomly generate
 * @return pointer on the new list
 */
list* generateList(int n)
{
    std::random_device rd; // to seed the random number generator object called mt
    std::mt19937 mt(rd()); // requests for random data to the operating system.
    std::uniform_int_distribution<int> dist(1, 99);

    list *head = new list;
    while (n--)
    {
        int vol = dist(mt);
        pushback(head, vol, vol + dist(mt));
    }
    return head;
}

void printAnswer(list *head, int n)
{
    std::ofstream inf("output.txt");
    if (inf.is_open())
    {
        isSorted(head, n) ? inf << "sorted\n" : inf << "not sorted\n";
        inf << n;
        inf.close();
    }
}

int main()
{
    // read the number of list elements from file
    std::ifstream fromf("input.txt");
    int elem_num;
    fromf >> elem_num;
    fromf.close();

    // create a new list
    list *list = generateList(elem_num);

    insertionSort(list, elem_num);
    printAnswer(list, elem_num);
    erase(list, elem_num);

    return 0;
}
