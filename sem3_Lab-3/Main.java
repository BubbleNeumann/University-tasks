import functions.*;

public class Main {
    public static void main(String[] args) throws Exception {
        TabulatedFunction func;

        double[] arr = { 1, 0, 1 };

        // func = new ArrayTabulatedFunction(-3, 3, 3);
        func = new LinkedListTabulatedFunction(-1, 1, arr);

        System.out.println("left border " + func.getLeftDomainBorder());
        System.out.println("right border " + func.getRightDomainBorder() + "\n");

        // func.addNodeByIndex(1);

        func.setPointY(1, -0.5);
        func.setPointX(1, -0.4);

        System.out.println(func.getFunctionValue(-0.4));

        func.deleteElemByIndex(1);
        System.out.println(func.getFunctionValue(0.6));

    }
}
