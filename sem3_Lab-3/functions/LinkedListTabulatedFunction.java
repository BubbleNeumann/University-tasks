package functions;

public class LinkedListTabulatedFunction implements TabulatedFunction {
    private class FunctionNode {
        private FunctionPoint point;
        private FunctionNode next, prev;
        // private FunctionNode prev = null, next = null;

    }

    private int length;
    private FunctionNode linkToHead = new FunctionNode(), head;

    public LinkedListTabulatedFunction() {
        // head = new FunctionNode();
        head = linkToHead;
        linkToHead.next = head;
        linkToHead.prev = linkToHead;
        length = 1;
    }

    public LinkedListTabulatedFunction(double leftX, double rightX, int pointsCount) throws IllegalArgumentException {
        if (leftX >= rightX || pointsCount < 2) {
            throw new IllegalArgumentException();
        }

        head = new FunctionNode();
        linkToHead.next = head;
        linkToHead.prev = linkToHead;
        length = pointsCount;

        double curX = leftX;
        double iterationiterationStep = (rightX - leftX) / (pointsCount - 1);
        FunctionNode cur = head;

        for (int i = 0; i < length; i++) {
            cur.point = new FunctionPoint(curX, 0);
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
        if (leftX >= rightX && values.length < 2) {
            throw new IllegalArgumentException();
        }

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
            cur.point = new FunctionPoint(cur.prev.point.getX() + iterationStep, values[i]);
            cur.next = new FunctionNode();
            cur.next.prev = cur;
            cur = cur.next;
        }

        cur.prev.next = head;
        head.prev = cur.prev;

    }

    public int getStructureLength() {
        return length;
    }

    FunctionNode getNodeByIndex(int index) {
        if (index >= length) {
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");
        }

        FunctionNode cur = head;

        if (index < length / 2) {
            for (int i = 0; i < index - 1; i++) {
                cur = cur.next;
            }

        } else {
            for (int i = 0; i < index - 1; i++) {
                cur = cur.prev;
            }

        }
        return cur;
    }

    public void addElemToTail(FunctionPoint point) throws InappropriateFunctionPointException {
        if (point.getX() < this.getRightDomainBorder()) {
            throw new InappropriateFunctionPointException("x is greater than domain border");
        }

        FunctionNode cur = head.prev;
        FunctionNode newNode = new FunctionNode();
        newNode.point = point;
        cur.next = newNode;
        newNode.prev = cur;
        newNode.next = head;
        head.prev = newNode;
        length++;
    }

    public void addElemByIndex(int index) throws FunctionPointIndexOutOfBoundsException {
        if (index >= length) {
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");
        }

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

    public void deleteElemByIndex(int index) throws FunctionPointIndexOutOfBoundsException {
        if (index < 0 || index >= length) {
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");
        }

        FunctionNode cur = head;
        int i;
        for (i = 0; i < index; i++) {
            cur = cur.next;
        }

        cur.next.prev = cur.prev;
        cur.prev.next = cur.next;
        length--;
    }

    public double getLeftDomainBorder() {
        if (length == 0) {
            throw new IllegalStateException();
        }

        return head.point.getX();
    }

    public double getRightDomainBorder() {
        if (length == 0) {
            throw new IllegalStateException();
        }

        return head.prev.point.getX();
    }

    public void setPointX(int index, double x) throws InappropriateFunctionPointException {
        if (length == 0) {
            throw new IllegalStateException();
        }

        if (index < 0 || index >= length) {
            throw new FunctionPointIndexOutOfBoundsException("bad index");
        }

        if (x < this.getLeftDomainBorder() || x > this.getRightDomainBorder()) {
            throw new InappropriateFunctionPointException("out of domain");
        }

        FunctionNode node = getNodeByIndex(index);
        node.point.setX(x);
    }

    public double getPointX(int index) throws FunctionPointIndexOutOfBoundsException {
        if (index >= length) {
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");
        }

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

    public void setPointY(int index, double y) {
        if (length == 0) {
            throw new IllegalStateException();
        }

        if (index < 0 || index >= length) {
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");
        }

        getNodeByIndex(index).point.setY(y);
    }

    public double getPointY(int index) throws FunctionPointIndexOutOfBoundsException {
        if (index >= length) {
            throw new FunctionPointIndexOutOfBoundsException("index is greater than length");
        }

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

    public double getFunctionValue(double x) throws InappropriateFunctionPointException {
        if (x < this.getLeftDomainBorder() || x > this.getRightDomainBorder()) {
            throw new InappropriateFunctionPointException("out of domain");
        }

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
}
