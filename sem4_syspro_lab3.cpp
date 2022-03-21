#include<iostream>
#include<string>

int main()
{
	int a, b, result;
	int exctype = 0; // type of thrown exception if there is any
	std::cin >> a >> b;
	__asm
	{
		mov eax, a           ; eax = a
		mov ebx, b           ; ebx = b
		cmp eax, ebx         ; compare a and b
		jg greater
		jl less
		neg eax              ; eax = -a
		jo ofExc
		add eax, ebx         ; eax = b-a
		mov result, eax
		jmp ex
		greater: mov eax, 1  ; eax = 1
		mov ebx, b           ; ebx = b
		cmp ebx, 0           ; check if possible to divide by b
		je zfExc
		cdq
		idiv ebx             ; eax = 1 / b
		inc eax              ; eax = 1 / b + 1 
		mov ebx, a           ; ebx = a
		cmp ebx, 0           ; check if possible to divide by a
		je zfExc
		cdq
		idiv ebx             ; eax = (1 / b + 1) / a
		inc eax              ; eax = (1 / b + 1) / a + 1
		jo ofExc             ; overflow check
		mov result, eax		
		jmp ex		
		less: add eax, -9    ; eax = a - 9
		jo ofExc
		cmp ebx, 0           ; check if possible to divide by b
		je zfExc
		cdq
		idiv ebx             ; eax = (a - 9) / b
		mov result, eax
		jmp ex
		ofExc: mov exctype, 1
		jmp ex
		zfExc: mov exctype, 2		
		ex:		
	}

	std::cout << (exctype == 1 ? "overflow exc" : (exctype == 2 ? "zero division" : std::to_string(result))) << "\n";
	return 0;
}