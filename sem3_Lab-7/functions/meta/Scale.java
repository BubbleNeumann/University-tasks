package functions.meta;

import functions.Function;
import functions.InappropriateFunctionPointException;

public class Scale implements Function {

    private Function func;
    private double xMult, yMult;

    public Scale(Function func, double x, double y) {
        this.func = func;
        this.xMult = x;
        this.yMult = y;
    }

    @Override
    public double getLeftDomainBorder() {
        if (xMult >= 0) {
            return xMult * func.getLeftDomainBorder();
        } else {
            return func.getLeftDomainBorder() / -xMult;
        }
    }

    @Override
    public double getRightDomainBorder() {
        if (xMult >= 0) {
            return xMult * func.getRightDomainBorder();
        } else {
            return func.getRightDomainBorder() / -xMult;
        }
    }

    @Override
    public double getFunctionValue(double x) throws InappropriateFunctionPointException {
        if (yMult >= 0) {
            return yMult * func.getFunctionValue(x / xMult);
        } else {
            return func.getFunctionValue(x / xMult) / -yMult;
        }
    }

}
