package functions.meta;

import functions.Function;
import functions.InappropriateFunctionPointException;

public class Sum implements Function {

    private Function first, second;

    public Sum(Function first, Function second) {
        this.first = first;
        this.second = second;
    }

    @Override
    public double getLeftDomainBorder() {
        return Math.max(first.getRightDomainBorder(), second.getRightDomainBorder());
    }

    @Override
    public double getRightDomainBorder() {
        return Math.min(first.getRightDomainBorder(), second.getRightDomainBorder());
    }

    @Override
    public double getFunctionValue(double x) throws InappropriateFunctionPointException {
        return first.getFunctionValue(x) + second.getFunctionValue(x);
    }

}
