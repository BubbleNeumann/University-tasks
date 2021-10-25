package functions.meta;

import functions.Function;
import functions.InappropriateFunctionPointException;

public class Power implements Function {

    private Function func;
    private double power;

    public Power(Function func, double power) {
        this.func = func;
        this.power = power;
    }

    @Override
    public double getLeftDomainBorder() {
        return func.getLeftDomainBorder();
    }

    @Override
    public double getRightDomainBorder() {
        return func.getRightDomainBorder();
    }

    @Override
    public double getFunctionValue(double x) throws InappropriateFunctionPointException {
        return Math.pow(func.getFunctionValue(x), power);
    }

}
