import functions.*;

public class Main {
    public static void main(String[] args) {

        double[] funcValues = { 1.0, 4.0, 9.0, 16.0 };

        TabulatedFunction func = new TabulatedFunction(1.0, 4.0, funcValues);

        for (double curX = 1.0; curX < 4.1; curX += 1) {
            System.out.println(func.getFunctionValue(curX));
        }

        System.out.println(func.getFunctionValue(1.5));

        func.deletePoint(3);

        for (int i = 0; i < 3; i++) {
            System.out.println(func.getPointY(i));
        }

    }
}
