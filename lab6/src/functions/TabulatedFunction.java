package functions;

public interface TabulatedFunction extends Function, Cloneable {

    int getStructureLength();

    FunctionPoint getPoint(int index);

    void setPointX(int index, double x) throws InappropriateFunctionPointException;

    double getPointX(int index) throws FunctionPointIndexOutOfBoundsException;

    void setPointY(int index, double y);

    double getPointY(int index) throws FunctionPointIndexOutOfBoundsException;

    void addElemToTail(FunctionPoint point) throws InappropriateFunctionPointException;

    void addElemByIndex(int index);

    void deleteElemByIndex(int index) throws FunctionPointIndexOutOfBoundsException;

    Object clone() throws CloneNotSupportedException;

}
