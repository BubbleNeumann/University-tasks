import functions.*;
import functions.basic.Cos;
import functions.basic.Sin;

public class Main {

    public static void main(String[] args) throws InappropriateFunctionPointException {

        TabulatedFunction func = new LinkedListTabulatedFunction(-1, 1, 5);
        for (FunctionPoint p : func) {
            System.out.println(p);
        }

        Function f = new Cos();
        TabulatedFunction tf;
        tf = TabulatedFunctions.tabulate(f, 0, Math.PI, 11);
        System.out.println(tf.getClass());
        TabulatedFunctions
                .setTabulatedFunctionFactory(new LinkedListTabulatedFunction.LinkedListTabulatedFunctionFactory());
        tf = TabulatedFunctions.tabulate(f, 0, Math.PI, 11);
        System.out.println(tf.getClass());
        TabulatedFunctions.setTabulatedFunctionFactory(new ArrayTabulatedFunction.ArrayTabulatedFunctionFactory());
        tf = TabulatedFunctions.tabulate(f, 0, Math.PI, 11);
        System.out.println(tf.getClass());

        // TabulatedFunction f;
        // f = TabulatedFunctions.createTabulatedFunction(ArrayTabulatedFunction.class,
        // 0, 10, 3);
        // System.out.println(f.getClass());
        // System.out.println(f);
        // f = TabulatedFunctions.createTabulatedFunction(ArrayTabulatedFunction.class,
        // 0, 10, new double[] { 0, 10 });
        // System.out.println(f.getClass());
        // System.out.println(f);
        // f =
        // TabulatedFunctions.createTabulatedFunction(LinkedListTabulatedFunction.class,
        // new FunctionPoint[] { new FunctionPoint(0, 0), new FunctionPoint(10, 10) });
        // System.out.println(f.getClass());
        // System.out.println(f);
        // f = TabulatedFunctions.tabulate(LinkedListTabulatedFunction.class, new Sin(),
        // 0, Math.PI, 11);
        // System.out.println(f.getClass());
        // System.out.println(f);

    }
}
