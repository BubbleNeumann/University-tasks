package functions.meta;

import functions.Function;
import functions.InappropriateFunctionPointException;

public class Shift implements Function {

    private Function func;
    private double shiftX, shiftY;

    public Shift(Function func, double x, double y) {
        this.func = func;
        this.shiftX = x;
        this.shiftY = y;
    }

    @Override
    public double getLeftDomainBorder() {
        return shiftX + func.getLeftDomainBorder();
    }

    @Override
    public double getRightDomainBorder() {
        return shiftX + func.getRightDomainBorder();
    }

    @Override
    public double getFunctionValue(double x) throws InappropriateFunctionPointException {
        return shiftY + func.getFunctionValue(x - shiftX);
    }

}
