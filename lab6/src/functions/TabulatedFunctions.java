package functions;

import java.io.*;

public class TabulatedFunctions {

    private TabulatedFunctions() {
    }

    public static TabulatedFunction tabulate(java.util.function.Function func, double leftX, double rightX,
            int pointsCount) throws InappropriateFunctionPointException, IllegalArgumentException {

        if (leftX < ((Function) func).getLeftDomainBorder() || rightX > ((Function) func).getRightDomainBorder()) {
            throw new IllegalArgumentException();
        }

        FunctionPoint[] points = new FunctionPoint[pointsCount];
        points[0] = new FunctionPoint(leftX, ((Function) func).getFunctionValue(leftX));

        double iterationStep = (rightX - leftX) / (pointsCount - 1);

        for (int i = 1; i < pointsCount; i++) {
            points[i] = new FunctionPoint(points[i - 1].getX() + iterationStep,
                    ((Function) func).getFunctionValue(points[i - 1].getX() + iterationStep));
        }

        return new ArrayTabulatedFunction(points);
    }

    // put the tabulated function into a byte stream
    public static void outputTabulatedFunction(TabulatedFunction function, OutputStream out) throws IOException {
        int pointCount = function.getStructureLength();
        DataOutputStream stream = new DataOutputStream(out);
        stream.writeInt(pointCount);

        for (int i = 0; i < pointCount; i++) {
            stream.writeDouble(function.getPointX(i));
            stream.writeDouble(function.getPointY(i));
        }

        stream.flush();
    }

    // get a tabulated function's values from a byte stream
    public static TabulatedFunction inputTabulatedFunction(InputStream in) throws IOException {
        DataInputStream stream = new DataInputStream(in);
        int pointCount = stream.readInt();
        FunctionPoint points[] = new FunctionPoint[pointCount];

        for (int i = 0; i < pointCount; i++) {
            points[i] = new FunctionPoint(stream.readDouble(), stream.readDouble());
        }

        return new ArrayTabulatedFunction(points);
    }

    // put a tabulated function into a character stream
    public static void writeTabulatedFunction(TabulatedFunction function, Writer out) {
        PrintWriter writer = new PrintWriter(out);
        int pointCount = function.getStructureLength();
        writer.println(pointCount);

        for (int i = 0; i < pointCount; i++) {
            writer.println(function.getPointX(i));
            writer.println(function.getPointY(i));
        }
    }

    // get a tabulated function's values from a character stream
    public static TabulatedFunction readTabulatedFunction(Reader in) throws IOException {
        StreamTokenizer tokenizer = new StreamTokenizer(in);

        // get first token from the tokenized input stream
        tokenizer.nextToken();

        int pointCount = (int) tokenizer.nval;
        FunctionPoint points[] = new FunctionPoint[pointCount];
        double x, y;

        for (int i = 0; i < pointCount; i++) {
            tokenizer.nextToken();
            x = tokenizer.nval;
            tokenizer.nextToken();
            y = tokenizer.nval;
            points[i] = new FunctionPoint(x, y);
        }

        return new ArrayTabulatedFunction(points);
    }

}
