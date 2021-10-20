package functions.basic;

import functions.Function;

public class Log implements Function {

    private double base;

    public Log() {
        this.base = Double.NaN;
    }

    public Log(double base) {
        if (base > 0) {
            this.base = base;
        }
    }

    @Override
    public double getLeftDomainBorder() {
        return 0;
    }

    @Override
    public double getRightDomainBorder() {
        return Double.POSITIVE_INFINITY;
    }

    @Override
    public double getFunctionValue(double x) {
        if (x > 0 && base != Double.NaN) {
            return Math.log(x) / Math.log(base);
        } else {
            return Double.NaN;
        }
    }
}
