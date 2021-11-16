package functions;

public interface TabulatedFunctionFactory {

    public TabulatedFunction createTabulatedFunction(double leftX, double rigthX, double[] values);

    public TabulatedFunction createTabulatedFunction(double leftX, double rigthX, int pointsCount);

    public TabulatedFunction createTabulatedFunction(FunctionPoint[] array);

}
