package functions;

import java.io.Externalizable;
import java.io.IOException;
import java.io.ObjectInput;
import java.io.ObjectOutput;
// import java.io.StreamTokenizer;
import java.util.Iterator;
import java.util.NoSuchElementException;

public class ArrayTabulatedFunction implements TabulatedFunction, Externalizable {

    public static class ArrayTabulatedFunctionFactory implements TabulatedFunctionFactory {

        @Override
        public TabulatedFunction createTabulatedFunction(FunctionPoint[] points) {
            return new ArrayTabulatedFunction(points);
        }

        @Override
        public TabulatedFunction createTabulatedFunction(double leftX, double rightX, int pointsCount) {
            return new ArrayTabulatedFunction(leftX, rightX, pointsCount);
        }

        @Override
        public TabulatedFunction createTabulatedFunction(double leftX, double rightX, double[] values) {
            return new ArrayTabulatedFunction(leftX, rightX, values);
        }
    }

    private FunctionPoint[] list;
    private int arrayLength;

    public ArrayTabulatedFunction() {
        arrayLength = 0;
        list = new FunctionPoint[10];
    }

    public ArrayTabulatedFunction(double leftX, double rightX, int listCount) throws IllegalArgumentException {
        if ((leftX >= rightX) || (listCount < 2)) {
            throw new IllegalArgumentException();
        }

        list = new FunctionPoint[listCount + 10];
        arrayLength = listCount;

        double curX = leftX;
        double iterationStep = (rightX - leftX) / (listCount - 1);

        for (int i = 0; i < arrayLength; i++) {
            list[i] = new FunctionPoint(curX, 0);
            curX += iterationStep;
        }
    }

    public ArrayTabulatedFunction(double leftX, double rightX, double[] values) throws IllegalArgumentException {
        if ((leftX >= rightX) || (values.length < 2)) {
            throw new IllegalArgumentException();
        }

        list = new FunctionPoint[values.length + 10];
        arrayLength = values.length;

        double curX = leftX;
        double iterationStep = (rightX - leftX) / (arrayLength - 1);

        for (int i = 0; i < arrayLength; i++) {
            list[i] = new FunctionPoint(curX, values[i]);
            curX += iterationStep;
        }
    }

    public ArrayTabulatedFunction(FunctionPoint[] list) throws IllegalArgumentException {
        if (list.length < 2) {
            throw new IllegalArgumentException();
        }

        // check if xs are sorted
        for (int i = 1; i < list.length; i++) {
            if (list[i - 1].getX() > list[i].getX()) {
                throw new IllegalArgumentException();
            }
        }

        arrayLength = list.length;
        list = new FunctionPoint[list.length + 10];
        System.arraycopy(list, 0, list, 0, list.length);
    }

    @Override
    public int getStructureLength() {
        return arrayLength;
    }

    @Override
    public double getLeftDomainBorder() {
        return list[0].getX();
    }

    @Override
    public double getRightDomainBorder() {
        return list[arrayLength - 1].getX();
    }

    @Override
    public double getFunctionValue(double x) {
        for (int i = 0; i < arrayLength - 1; i++) {
            if (list[i].getX() + 0.001 > x && list[i].getX() - 0.001 < x) {
                return list[i].getY();
            }
        }

        if (x >= this.getLeftDomainBorder() && x <= this.getRightDomainBorder()) {
            return ((x - list[arrayLength - 2].getX()) * (list[0].getY() - list[arrayLength - 2].getY()))
                    / (list[0].getX() - list[arrayLength - 2].getX()) + list[arrayLength - 2].getY();
        }
        return Double.NaN;
    }

    public FunctionPoint getPoint(int index) throws FunctionPointIndexOutOfBoundsException {
        if (index >= arrayLength) {
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");
        }

        return this.list[index];
    }

    public void setPoint(int index, FunctionPoint point) throws FunctionPointIndexOutOfBoundsException {
        if (index >= arrayLength) {
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");
        }

        this.list[index] = point;
    }

    @Override
    public double getPointX(int index) throws FunctionPointIndexOutOfBoundsException {
        if (index >= arrayLength) {
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");
        }

        return this.list[index].getX();
    }

    @Override
    public void setPointX(int index, double x) throws FunctionPointIndexOutOfBoundsException {
        if (index >= arrayLength - 1) {
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");
        }

        if (x >= this.getLeftDomainBorder() && x <= this.getRightDomainBorder()) {
            this.list[index].setX(x);
        }
    }

    @Override
    public double getPointY(int index) throws FunctionPointIndexOutOfBoundsException {
        if (index >= arrayLength) {
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");
        }

        return this.list[index].getY();
    }

    @Override
    public void setPointY(int index, double y) throws FunctionPointIndexOutOfBoundsException {
        if (index >= arrayLength) {
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");
        }

        this.list[index].setY(y);
    }

    @Override
    public void deleteElemByIndex(int index) throws IllegalStateException {
        if (arrayLength <= 3) {
            throw new IllegalStateException();
        }

        FunctionPoint newList[] = new FunctionPoint[this.list.length];
        System.arraycopy(this.list, 0, newList, 0, index);
        System.arraycopy(this.list, index + 1, newList, index, this.arrayLength - index);
        this.list = newList;
        this.arrayLength--;
    }

    @Override
    public void addElemToTail(FunctionPoint point) throws InappropriateFunctionPointException {
        for (int i = 0; i < arrayLength; i++) {
            if (list[i].getX() < point.getX() + 0.01 && list[i].getX() > point.getX() - 0.01) {
                throw new InappropriateFunctionPointException("this x already exists");
            }
        }

        if (this.arrayLength == this.list.length) {
            FunctionPoint newList[] = new FunctionPoint[arrayLength + 10];
            this.list = newList;
        }

        list[arrayLength++] = new FunctionPoint();
        list[arrayLength - 1] = point;
        arrayLength++;
    }

    @Override
    public void addElemByIndex(int index) {
        if (index >= arrayLength || index < 0) {
            throw new FunctionPointIndexOutOfBoundsException("bad index");
        }

        FunctionPoint newList[] = new FunctionPoint[this.list.length + 1];
        System.arraycopy(this.list, 0, newList, 0, index);
        newList[index] = new FunctionPoint();
        System.arraycopy(this.list, index + 1, newList, index + 1, this.arrayLength - index);
        this.list = newList;
        this.arrayLength++;
    }

    @Override
    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeInt(arrayLength);

        for (int i = 0; i < this.arrayLength; i++) {
            out.writeDouble(list[i].getX());
            out.writeDouble(list[i].getY());
        }
    }

    @Override
    public void readExternal(ObjectInput in) throws IOException, ClassNotFoundException {
        int newArrayLength = in.readInt();
        this.list = new FunctionPoint[newArrayLength + 10];

        for (int i = 0; i < newArrayLength; i++) {
            this.list[i] = new FunctionPoint();
            this.list[i].setX(in.readDouble());
            this.list[i].setY(in.readDouble());
        }
    }

    @Override
    public Iterator<FunctionPoint> iterator() {
        return new Iterator<FunctionPoint>() {
            private int currentIndex = 0;

            @Override
            public boolean hasNext() {
                return currentIndex < arrayLength;
            }

            @Override
            public FunctionPoint next() {
                if (currentIndex >= arrayLength) {
                    throw new NoSuchElementException();
                }

                return new FunctionPoint(list[currentIndex++]);
            }

            @Override
            public void remove() {
                throw new UnsupportedOperationException();
            }
        };
    }
}
