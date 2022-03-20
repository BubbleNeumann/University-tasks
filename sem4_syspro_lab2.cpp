#include<iostream>
#include<string>

int main()
{
	int a, b, c, result;
	int exctype = 0; // type of thrown exception if there is any
	std::cin >> a >> b >> c;
	__asm
	{
		mov eax, b; eax = b
		jo ofExc
		mov ebx, 2; ebx = 2
		imul ebx; eax = 2 * b
		jo ofExc
		cdq		
		mov ebx, a; ebx = a
		cmp ebx, 0
		je zfExc
		idiv ebx; eax = 2 * b / a
		mov ecx, eax; ecx = 2 * b / a
		mov eax, c; eax = c
		jo ofExc
		mov ebx, c; ebx = c
		imul ebx; eax = c * c
		jo ofExc
		sbb ecx, eax; ecx = (2 * b / a) - (c * c)
		mov eax, a; eax = a
		mov ebx, c; ebx = c
		imul ebx; eax = a * c
		jo ofExc
		dec eax; eax = a * c - 1
		jz zfExc
		jo ofExc		
		mov ebx, eax; ebx = a * c - 1
		mov eax, ecx; eax = (2 * b / a) - (c * c)
		cdq
		idiv ebx; eax = ((2 * b / a) - (c * c)) / (a * c - 1)		
		mov result, eax
		jmp ex
		ofExc : mov exctype, 1
		jmp ex
		zfExc : mov exctype, 2
		ex:
	}

	std::cout << (exctype == 1 ? "overflow exc" : (exctype == 2 ? "zero division" : std::to_string(result))) << "\n";
	return 0;
}