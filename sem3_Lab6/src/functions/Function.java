package functions;

public interface Function {
    double getLeftDomainBorder() throws IllegalStateException;

    double getRightDomainBorder() throws IllegalStateException;

    double getFunctionValue(double x) throws InappropriateFunctionPointException;

}
