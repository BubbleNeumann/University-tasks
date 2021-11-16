package functions;

// import java.io.Externalizable;
// import java.io.Serializable;

public interface TabulatedFunction extends Function, Iterable<FunctionPoint> {

    int getStructureLength();

    void setPointX(int index, double x) throws InappropriateFunctionPointException;

    double getPointX(int index) throws FunctionPointIndexOutOfBoundsException;

    void setPointY(int index, double y);

    double getPointY(int index) throws FunctionPointIndexOutOfBoundsException;

    void addElemToTail(FunctionPoint point) throws InappropriateFunctionPointException;

    void addElemByIndex(int index);

    void deleteElemByIndex(int index) throws FunctionPointIndexOutOfBoundsException;

}
