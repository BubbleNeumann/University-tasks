package functions;

// import java.io.EOFException;
import java.io.Externalizable;
import java.io.IOException;
import java.io.ObjectInput;
import java.io.ObjectOutput;

public class LinkedListTabulatedFunction implements TabulatedFunction, Externalizable {
    static private class FunctionNode implements Externalizable {
        private FunctionPoint point;
        private FunctionNode next, prev;

        public FunctionNode() {
            point = new FunctionPoint();
            next = null;
            prev = null;
        }

        @Override
        public void writeExternal(ObjectOutput out) throws IOException {
            out.writeObject(point);
        }

        @Override
        public void readExternal(ObjectInput in) throws IOException, ClassNotFoundException {
            this.point = (FunctionPoint) in.readObject();
        }
    }

    private int length;
    private FunctionNode linkToHead = new FunctionNode(), head;

    public LinkedListTabulatedFunction() {
        head = linkToHead;
        linkToHead.next = head;
        linkToHead.prev = linkToHead;
        length = 1;
    }

    public LinkedListTabulatedFunction(double leftX, double rightX, int pointsCount) throws IllegalArgumentException {
        if (leftX >= rightX || pointsCount < 2)
            throw new IllegalArgumentException();

        head = new FunctionNode();
        linkToHead.next = head;
        linkToHead.prev = linkToHead;
        length = pointsCount;

        double curX = leftX;
        double iterationiterationStep = (rightX - leftX) / (pointsCount - 1);
        FunctionNode cur = head;

        for (int i = 0; i < length; i++) {
            cur.point.setX(curX);
            cur.point.setY(0.0);
            if (i != length - 1) {
                FunctionNode next = new FunctionNode();
                cur.next = next;
                next.prev = cur;
                next.next = head;
                head.prev = next;
                cur = next;
                curX += iterationiterationStep;
            }
        }
    }

    public LinkedListTabulatedFunction(double leftX, double rightX, double values[]) {
        if (leftX >= rightX && values.length < 2)
            throw new IllegalArgumentException();

        length = values.length;
        head = new FunctionNode();
        linkToHead.next = head;

        FunctionNode cur = head;

        cur.point = new FunctionPoint(leftX, values[0]);
        cur.next = new FunctionNode();
        cur.next.prev = cur;
        cur = cur.next;

        double iterationStep = (rightX - leftX) / (values.length - 1);

        for (int i = 1; i < length; i++) {
            // cur.point = new FunctionPoint(cur.prev.point.getX() + iterationStep,
            // values[i]);
            cur.point.setX(cur.prev.point.getX() + iterationStep);
            cur.point.setY(values[i]);
            cur.next = new FunctionNode();
            cur.next.prev = cur;
            cur = cur.next;
        }

        cur.prev.next = head;
        head.prev = cur.prev;

    }

    public LinkedListTabulatedFunction(FunctionPoint points[])
            throws IllegalArgumentException, InappropriateFunctionPointException {
        if (points.length < 2)
            throw new IllegalArgumentException();

        // check if xs are sorted
        for (int i = 1; i < points.length; i++) {
            if (points[i - 1].getX() > points[i].getX()) {
                throw new IllegalArgumentException();
            }
        }

        length = 1;
        head = new FunctionNode();
        linkToHead.next = head;

        head.point = points[0];
        head.next = head;
        head.prev = head;

        for (int i = 1; i < points.length; i++)
            this.addElemToTail(points[i]);
    }

    @Override
    public int getStructureLength() {
        return length;
    }

    FunctionNode getNodeByIndex(int index) {
        if (index >= length)
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");

        FunctionNode cur = head;
        for (int i = 0; i < index - 1; i++)
            cur = cur.next;

        return cur;
    }

    @Override
    public void addElemToTail(FunctionPoint point) throws InappropriateFunctionPointException {
        if (point.getX() < this.getRightDomainBorder())
            throw new InappropriateFunctionPointException("x is less than right domain border");

        FunctionNode cur = head.prev;
        FunctionNode newNode = new FunctionNode();
        newNode.point = point;
        cur.next = newNode;
        newNode.prev = cur;
        newNode.next = head;
        head.prev = newNode;
        length++;
    }

    @Override
    public void addElemByIndex(int index) throws FunctionPointIndexOutOfBoundsException {
        if (index >= length)
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");

        FunctionNode cur = head;
        int i;

        // set i = 1 to stop one element earlier than index element
        for (i = 1; i < index; i++) {
            cur = cur.next;
        }

        // if no exception is thrown, add a new function node
        FunctionNode newNode = new FunctionNode();
        newNode.next = cur.next;
        newNode.prev = cur;
        cur.next = newNode;
        cur.next.prev = newNode;
        length++;
    }

    @Override
    public void deleteElemByIndex(int index) throws FunctionPointIndexOutOfBoundsException {
        if (index < 0 || index >= length)
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");

        FunctionNode cur = head;
        int i;
        for (i = 0; i < index; i++) {
            cur = cur.next;
        }

        cur.next.prev = cur.prev;
        cur.prev.next = cur.next;
        length--;
    }

    @Override
    public double getLeftDomainBorder() {
        if (length == 0)
            throw new IllegalStateException();

        return head.point.getX();
    }

    @Override
    public double getRightDomainBorder() {
        if (length == 0)
            throw new IllegalStateException();

        return head.prev.point.getX();
    }

    @Override
    public void setPointX(int index, double x) throws InappropriateFunctionPointException {
        if (length == 0)
            throw new IllegalStateException();

        if (index < 0 || index >= length)
            throw new FunctionPointIndexOutOfBoundsException("bad index");

        if (x < this.getLeftDomainBorder() || x > this.getRightDomainBorder())
            throw new InappropriateFunctionPointException("out of domain");

        FunctionNode node = getNodeByIndex(index);
        node.point.setX(x);
    }

    @Override
    public double getPointX(int index) throws FunctionPointIndexOutOfBoundsException {
        if (index >= length)
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");

        FunctionNode cur = head;
        if (index < length / 2) {
            for (int i = 0; i < index; i++) {
                cur = cur.next;
            }
        } else {
            for (int i = length; i > index; i--) {
                cur = cur.prev;
            }
        }
        return cur.point.getX();
    }

    @Override
    public void setPointY(int index, double y) {
        if (length == 0)
            throw new IllegalStateException();

        if (index < 0 || index >= length)
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");

        getNodeByIndex(index).point.setY(y);
    }

    @Override
    public double getPointY(int index) throws FunctionPointIndexOutOfBoundsException {
        if (index >= length)
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");

        FunctionNode cur = head;
        if (index < length / 2) {
            for (int i = 0; i < index; i++) {
                cur = cur.next;
            }
        } else {
            for (int i = length; i > index; i--) {
                cur = cur.prev;
            }
        }
        return cur.point.getY();
    }

    @Override
    public double getFunctionValue(double x) throws InappropriateFunctionPointException {
        if (x < this.getLeftDomainBorder() || x > this.getRightDomainBorder())
            throw new InappropriateFunctionPointException("out of domain");

        FunctionNode cur = head;

        for (int i = 0; i < length; i++) {
            if (cur.point.getX() + 0.001 > x && cur.point.getX() - 0.001 < x) {
                return cur.point.getY();
            }
            cur = cur.next;
        }

        return ((x - head.prev.point.getX()) * (head.point.getY() - head.prev.point.getY()))
                / (head.point.getX() - head.prev.point.getX()) + head.prev.point.getY();
    }

    @Override
    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeInt(length);

        FunctionNode cur = head;
        for (int i = 0; i < this.length; i++) {
            if (cur != null) {
                out.writeObject(cur);
                cur = cur.next;
            }
        }
    }

    @Override
    public void readExternal(ObjectInput in) throws IOException, ClassNotFoundException {
        length = in.readInt();
        FunctionNode cur = head;

        for (int i = 1; i < this.length; i++) {

            cur = (FunctionNode) in.readObject();
            // cur.point.setX(in.readDouble());
            // cur.point.setY(in.readDouble());
            cur.next = new FunctionNode();
            cur.next.prev = cur;
            cur = cur.next;
            cur.next = head;
            head.prev = cur;
        }
    }

    @Override
    public FunctionPoint getPoint(int index) {
        return new FunctionPoint(getNodeByIndex(index).point);
    }

    @Override
    public String toString() {
        String res = "{";
        FunctionNode iterator = head;
        for (int i = 0; i < length; i++) {
            // res += "(" + this.getNodeByIndex(i).point.getX() + "; " +
            // this.getNodeByIndex(i).point.getX() + ")";
            res += "(" + iterator.point.getX() + "; " + iterator.point.getX() + ")";
            iterator = iterator.next;
            if (i != length - 1) {
                res += ", ";
            }
        }

        return res + "}";
    }

    @Override

    public boolean equals(Object obj) {
        if (obj == null)
            return false;

        if (obj instanceof TabulatedFunction) {
            if (obj instanceof LinkedListTabulatedFunction) {
                LinkedListTabulatedFunction func = (LinkedListTabulatedFunction) obj;

                if (func.length != this.length)
                    return false;

                FunctionNode iterator = this.head;
                FunctionNode funccur = func.head;

                for (int i = 0; i < length; i++) {
                    if (iterator.point.getX() != funccur.point.getX()
                            || iterator.point.getY() != funccur.point.getY()) {
                        return false;
                    }

                    iterator = iterator.next;
                    funccur = funccur.next;
                }

                return true;

            } else {
                TabulatedFunction func = (TabulatedFunction) obj;
                if (func.getStructureLength() != this.length)
                    return false;

                for (int i = 0; i < this.length; i++) {
                    if (!(this.getPoint(i).equals(func.getPoint(i)))) {
                        return false;
                    }
                }

                return true;
            }

        } else {
            return false;
        }
    }

    @Override
    public int hashCode() {
        FunctionNode cur = head;
        int res = 0;

        for (int i = 0; i < length; i++) {
            res += cur.point.hashCode();
            cur = cur.next;
        }

        return length + res;
    }

    @Override
    public Object clone() throws CloneNotSupportedException {
        FunctionPoint points[] = new FunctionPoint[length];
        FunctionNode cur = head;

        for (int i = 0; i < this.length; i++) {
            points[i] = cur.point;
            cur = cur.next;
        }

        // catch exceptions from LinkedListTabulatedFunction constructor
        try {
            return new LinkedListTabulatedFunction(points);
        } catch (IllegalArgumentException | InappropriateFunctionPointException e) {
            e.printStackTrace();
        }

        return null;
    }
}
