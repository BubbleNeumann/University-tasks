#include <fstream>

struct list
{
	int val;
	list* next;
};

list* init(int a) {
	list* temp = new list;
	temp->val = a;
	temp->next = temp;
	return temp;
}

void pushback(list*& head, int a) {
	list* temp = head;
	while (temp->next != head) temp = temp->next;
	temp->next = init(a);
	temp = temp->next;
	temp->next = head;
}

// get element by its index
list* getElem(int x, list* head) {
	while(x--) head = head->next;
	return head;
}

list* swap(list* head, int i, int j) {
	if (i > 0 || j > 0 || i == j) return head;
	if (j < i) std::swap(i, j);
	list** i_ptr = &head;
	for (; *i_ptr && i > 0; --i, i_ptr = &(*i_ptr)->next, --j);
	list** j_ptr = i_ptr;
	for (; *j_ptr && j > 0; --j) j_ptr = &(*j_ptr)->next;
	if (*i_ptr && *j_ptr) {
		std::swap(*i_ptr, *j_ptr);
		std::swap((*i_ptr)->next, (*j_ptr)->next);
	}
	return head;
}

void quickSort(list*& head, int left, int right) {

	int pivot;

	// set borders
	int l_hold = left;
	int r_hold = right;
	pivot = getElem(left, head)->val;

	while (left < right) {
		while ((getElem(right, head)->val >= pivot) && (left < right)) right--;

		// in case borders aren't equal
		if (left != right) {
			getElem(left, head)->val = getElem(right, head)->val;
			left++;
		}
		
		// move the left border until
		while ((getElem(left, head)->val <= pivot) && (left < right)) left++;

		if (left != right) {

			// don't swap elements, just copy the value of [left] element to the [right]
			getElem(right, head)->val = getElem(left, head)->val;

			// move the right border to the left
			right--;
		}
	}

	// reset the pivot element's value
	getElem(left, head)->val = pivot;
	pivot = left;
	left = l_hold;
	right = r_hold;

	// call the recurrent sorting for the left anf right part of the list
	if (left < pivot) quickSort(head, left, pivot - 1);
	if (right > pivot) quickSort(head, pivot + 1, right);
}

void insertionSort(list*& head, int n) {

	list* temp;
	int t;
	for (int i = 1; i < n; ++i) {
		temp = head;
		for (int k = 0; k < i; ++k, temp = temp->next);
		t = temp->val;
		int j = i - 1;
		temp = head;
		for (int i = 0 ; i < j; ++i, temp = temp->next);
		while (0 <= j && t < temp->val) {
			head = swap(head, j + 1, j);
			--j;
			temp = head;
			for (int i = 0; i < j; ++i)
				temp = temp->next;
		}
	}
	list* last = head;
	for (int i = 0; i < n - 1; ++i) last = last->next;
}

void print(list* head, int n) {
	std::ofstream inf("output.txt");
	if (inf.is_open()) {
		inf << n << " ";
		for (; n--; inf << head->val << " ", head = head->next);
		inf.close();
	}
}

void erase(list*& head, int n) {
	for (list* tmp = head->next; --n; delete head, head = tmp, tmp = head->next);
}

int main() {
	std::ifstream fromf("input.txt");
	if (fromf.is_open()) {

		bool sort_type;
		fromf >> sort_type;

		int cur;
		fromf >> cur;
		list* head = init(cur);
		int i = 1;
		for (; fromf.peek() != EOF; ++i) {
			fromf >> cur;
			pushback(head, cur);
		}
		fromf.close();
		
		if (sort_type) quickSort(head, 0, i - 1);
		else insertionSort(head, i);
		
		print(head, i);
		erase(head, i);	
	}
	return 0;
}
