package functions.meta;

import functions.Function;
import functions.InappropriateFunctionPointException;

public class Composition implements Function {

    private Function first, second;

    public Composition(Function first, Function second) {
        this.first = first;
        this.second = second;
    }

    @Override
    public double getLeftDomainBorder() throws IllegalStateException {
        return first.getLeftDomainBorder();
    }

    @Override
    public double getRightDomainBorder() throws IllegalStateException {
        return first.getRightDomainBorder();
    }

    @Override
    public double getFunctionValue(double x) throws InappropriateFunctionPointException {
        return first.getFunctionValue(second.getFunctionValue(x));
    }

}
