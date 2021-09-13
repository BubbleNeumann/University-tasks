package functions;

public class TabulatedFunction {

    private FunctionPoint[] list;
    private int arrayLength;

    public TabulatedFunction(double leftX, double rightX, int pointsCount) {
        this.list = new FunctionPoint[pointsCount + 10];
        this.arrayLength = pointsCount;

        double curX = leftX;
        double iterationStep = (rightX - leftX) / (pointsCount - 1);

        for (int i = 0; i < arrayLength - 1; i++) {
            list[i] = new FunctionPoint(curX, 0);
            curX += iterationStep;
        }
    }

    public TabulatedFunction(double leftX, double rightX, double[] values) {
        this.list = new FunctionPoint[values.length + 10];
        this.arrayLength = values.length;

        double curX = leftX;
        double iterationStep = (rightX - leftX) / (arrayLength - 1);

        for (int i = 0; i < arrayLength; i++) {
            list[i] = new FunctionPoint(curX, values[i]);
            curX += iterationStep;
        }
    }

    public int getArrayLength() {
        return this.arrayLength;
    }

    public double getLeftDomainBorder() {
        return list[0].getX();
    }

    public double getRightDomainBorder() {
        return list[arrayLength - 1].getX();
    }

    public double getFunctionValue(double x) {

        if (x >= this.list[0].getX() && x <= this.list[arrayLength - 1].getX()) {
            return ((x - list[arrayLength - 1].getX()) * (list[0].getY() - list[arrayLength - 1].getY()))
                    / (list[0].getX() - list[arrayLength - 1].getX()) + list[arrayLength - 1].getY();
        }
        return Double.NaN;
    }

    public int getPointCount() {
        return this.arrayLength;
    }

    public FunctionPoint getPoint(int index) {
        return this.list[index];
    }

    public void setPoint(int index, FunctionPoint point) {
        this.list[index] = point;
    }

    public double getPointX(int index) {
        return this.list[index].getX();
    }

    public void setPointX(int index, double x) {
        if (x >= this.getLeftDomainBorder() && x <= this.getRightDomainBorder()) {
            this.list[index].setX(x);
        }
    }

    public double getPointY(int index) {
        return this.list[index].getY();
    }

    public void setPointY(int index, double y) {
        this.list[index].setY(y);
    }

    public void deletePoint(int index) {
        FunctionPoint newList[] = new FunctionPoint[this.list.length];
        System.arraycopy(this.list, 0, newList, 0, index);
        System.arraycopy(this.list, index + 1, newList, index, this.arrayLength - index);
        this.list = newList;
        this.arrayLength--;
    }

    public void addPoint(FunctionPoint point) {
        if (this.arrayLength == this.list.length) {
            FunctionPoint newList[] = new FunctionPoint[arrayLength + 10];
            this.list = newList;
        }
        list[arrayLength++] = new FunctionPoint();
        list[arrayLength - 1] = point;
    }

}
