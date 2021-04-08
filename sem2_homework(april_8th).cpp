// the total number of nodes of a binary tree
int Tree::size()
{
    int n = 0;
    if (left) n += left->size();
    if (right) n += right->size();
    return ++n;
}

// the number of final vertices of a binary tree
void Tree::leafs(int& n)
{
    if (!left && !right) ++n;
    if (left) left->leafs(n);
    if (right) right->leafs(n);
}

// the number of vertices of a binary tree
void Tree::nodes(int& n)
{
    if (left || right)
    {
        ++n;
        if (left) left->nodes(n);
        if (right) right->nodes(n);
    }
}