#include <iostream>
#include <fstream>

class Tree
{
    int val;
    Tree* left;
    Tree* right;

public:

    //default constructor
    Tree(int a = 0) : val(a), left(NULL), right(NULL) {}

    void outprint(std::ofstream& output);
    void mirror();
    Tree* insertLevelOrder(std::ifstream&, Tree*, int, int);

    ~Tree()
    {
        if (left)
        {
            delete left;
        }
        if (right)
        {
            delete right;
        }
    }
};

// recursively put nodes' values into output file
void Tree::outprint(std::ofstream& output)
{

    if (left)
    {
        left->outprint(output);
    }
    if (right)
    {
        right->outprint(output);
    }
    output << val << " ";
}
// for each node recursively swap left and right pointers
void Tree::mirror()
{
    if (left && right)
    {
        left->mirror();
        right->mirror();
        std::swap(left, right);
    }
}

// construct and fill balanced binary tree
Tree* Tree::insertLevelOrder(std::ifstream& fromf, Tree* cur, int i, int n)
{
    if (i < n)
    {
        if (!cur)
        {
            cur = new Tree;
        }
        // insert left child
        cur->left = insertLevelOrder(fromf, cur->left, 2 * i + 1, n);

        // insert right child
        cur->right = insertLevelOrder(fromf, cur->right, 2 * i + 2, n);
        fromf >> cur->val;

    }
    return cur;
}

int calculateElemNum()
{
    std::ifstream fromf("input.txt");
    std::istream_iterator<int> b(fromf), e;
    int len = std::distance(b, e);
    fromf.close();
    return len;
}

int main()
{
    Tree* autom = new Tree;

    int num = calculateElemNum();

    std::ifstream fromf("input.txt");
    autom->insertLevelOrder(fromf, autom, 0, num);
    fromf.close();

    autom->mirror();

    std::ofstream inf("output.txt");
    autom->outprint(inf);
    inf.close();

    return 0;
}
