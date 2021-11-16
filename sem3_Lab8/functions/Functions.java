package functions;

import functions.meta.*;

public class Functions {
    public static Function shift(Function f, double shiftX, double shiftY) {
        return new Shift(f, shiftX, shiftY);
    }

    public static Function scale(Function f, double scaleX, double scaleY) {
        return new Scale(f, scaleX, scaleY);
    }

    public static Function power(Function f, double power) {
        return new Power(f, power);
    }

    public static Function sum(Function f1, Function f2) {
        return new Sum(f1, f2);
    }

    public static Function mult(Function f1, Function f2) {
        return new Mult(f1, f2);
    }

    public static Function composition(Function f1, Function f2) {
        return new Composition(f1, f2);
    }

    public static double integrate(Function func, double leftX, double rightX, double step)
            throws IllegalStateException, InappropriateFunctionPointException {
        if (leftX < func.getLeftDomainBorder() || rightX > func.getRightDomainBorder())
            throw new IllegalArgumentException();

        double result = 0, cur = leftX;
        while (cur < rightX) {
            result += (func.getFunctionValue(cur) + func.getFunctionValue(cur + step)) * step / 2;
            cur += step;
        }

        cur -= step;
        result += (func.getFunctionValue(rightX) + func.getFunctionValue(cur)) * (rightX - cur) / 2;
        return result;
    }
}
