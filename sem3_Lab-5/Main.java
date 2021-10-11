import functions.*;
// import java.io.*;

public class Main {
    public static void main(String[] args) throws Exception {

        // double[] arr = { 1, 0, 1 };

        TabulatedFunction func = new ArrayTabulatedFunction(0, 0, 2);

        System.out.println(func.hashCode());
        // TabulatedFunction func1 = new LinkedListTabulatedFunction(0, 3, 4);
        // System.out.println(func.equals(func1));

        // func.addElemToTail(new FunctionPoint());

        // TabulatedFunction func1 = (ArrayTabulatedFunction) func.clone();

        // int hashFunc = func.hashCode();
        // int hashFunc1 = func1.hashCode();

        // System.out.println(func1.toString());
        // System.out.println(func.equals(func1));
        // System.out.println(hashFunc == hashFunc1);
        // System.out.println(hashFunc);

        // TabulatedFunction func = new LinkedListTabulatedFunction(-1.0, 2.0, 4);

        // for (int i = 0; i < func.getStructureLength(); i++) {
        // System.out.println(func.getPointX(i));
        // }
    }
}
