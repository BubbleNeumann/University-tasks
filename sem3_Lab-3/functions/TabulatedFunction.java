package functions;

public interface TabulatedFunction {

    int getStructureLength();

    double getLeftDomainBorder() throws IllegalStateException;

    double getRightDomainBorder() throws IllegalStateException;

    void setPointX(int index, double x) throws InappropriateFunctionPointException;

    double getPointX(int index) throws FunctionPointIndexOutOfBoundsException;

    void setPointY(int index, double y);

    double getPointY(int index) throws FunctionPointIndexOutOfBoundsException;

    double getFunctionValue(double x) throws InappropriateFunctionPointException;

    void addElemToTail(FunctionPoint point) throws InappropriateFunctionPointException;

    // void addElemByIndex(int index);

    void deleteElemByIndex(int index) throws FunctionPointIndexOutOfBoundsException;

}
