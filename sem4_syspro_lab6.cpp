#include<iostream>
#include<string>

int main()
{
	double a = -1;
	double b = 2;
	const double c2 = 2;
	double result;
	int exc = 0;



	__asm
	{
		finit
		fld a ; st(0) = a
		fld b ; st(0) = b, st(1) = a
		fmul c2 ; st(0) = 2 * b
		fld a ; st(0) = a
		ftst
		fstsw ax
		sahf
		jz zero_division
		fdiv; st(0) = 2 * b / a
		fstp result ; result = 2 * b / a
		fld c ; st(0) = c
		fmul c ; st(0) = c*c
		fld result ; st(1) = 2 * b / a
		fxch st(1)
		fsub
		fstp result ; result = 2 * b / a - c * c
		ffree st(0)
		fld c ; st(0) = c
		fmul a ; st(0) = c*a
		fld1 ; st(1) = 1
		fsub ; st(0) = c * a - 1
		ftst
		fstsw ax
		sahf
		jz zero_division
		fld result ; st(0) = 2 * b / a - c * c, st(1) = c * a - 1
		fxch st(1)
		fdiv
		fstp result ; result = st(0)
		jmp ex
		zero_division:
		mov exc, 1
		ex:
	}

	std::cout << (exc  ? "zero division": std::to_string(result));
	return 0;
}