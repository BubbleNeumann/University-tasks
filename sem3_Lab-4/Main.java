import functions.*;
// import functions.basic.*;
// import functions.basic.Sin;

import java.io.*;

public class Main {
    // private static ObjectInputStream ois;

    public static void main(String[] args) throws Exception {

        // double[] arr = { 1, 0, 1 };

        TabulatedFunction func = new LinkedListTabulatedFunction(-1.0, 2.0, 4);

        for (int i = 0; i < func.getStructureLength(); i++) {
            System.out.println(func.getPointX(i));
        }

        FileOutputStream outputStream = new FileOutputStream("temp.txt");
        ObjectOutputStream oos = new ObjectOutputStream(outputStream);
        oos.writeObject(func);
        oos.close();

        FileInputStream inputStream = new FileInputStream("temp.txt");
        ObjectInputStream ois = new ObjectInputStream(inputStream);
        ois.readObject();
        ois.close();

        for (int i = 0; i < func.getStructureLength(); i++) {
            System.out.println(func.getPointX(i));
        }

        // TrigonometricFunction sin, cos;
        // sin = new Sin();
        // System.out.println("Sinus");

        // for (double i = 0; i < 2 * Math.PI; i += 0.1) {
        // System.out.println("Значение в точке x=" + i + ": " +
        // sin.getFunctionValue(i));
        // }

        // cos = new Cos();
        // System.out.println("Cosinus");

        // for (double i = 0; i < 2 * Math.PI; i += 0.1) {
        // System.out.println("Значение в точке x=" + i + ": " +
        // cos.getFunctionValue(i));
        // }

        // TabulatedFunction tabCos, tabSin;
        // tabSin = TabulatedFunctions.tabulate(sin, 0, 2 * Math.PI, 10);
        // System.out.println("Tabulated sinus");

        // for (double i = 0; i < 2 * Math.PI; i += 0.1) {
        // System.out.println("point x=" + i + ": " + tabSin.getFunctionValue(i));
        // }

        // tabCos = TabulatedFunctions.tabulate(cos, 0, 2 * Math.PI, 10);

        // System.out.println("Tabulated cosinus");

        // for (double i = 0; i < 2 * Math.PI; i += 0.1) {
        // System.out.println("point x=" + i + ": " + tabCos.getFunctionValue(i));
        // }

        // Function cos2 = Functions.power(tabCos, 2);
        // Function sin2 = Functions.power(tabSin, 2);

        // Function Sum = Functions.sum(sin2, cos2);

        // System.out.println("Tabulated summ");

        // for (double i = 0; i < 2 * Math.PI; i += 0.1) {
        // System.out.println("point x=" + i + ": " + Sum.getFunctionValue(i));
        // }

        // System.out.println("Tabulated exponent");

        // Exp e = new Exp();
        // TabulatedFunction tabulatedExp = TabulatedFunctions.tabulate(e, 0, 10, 11);

        // FileWriter writer = new FileWriter("exp.txt");
        // TabulatedFunctions.writeTabulatedFunction(tabulatedExp, writer);
        // writer.flush();
        // writer.close();

        // FileReader reader = new FileReader("exp.txt");
        // TabulatedFunction expi = TabulatedFunctions.readTabulatedFunction(reader);
        // reader.close();

        // System.out.println("Tabulated logarithm");

        // Log log = new Log(Math.E);
        // TabulatedFunction logo = TabulatedFunctions.tabulate(log, 0, 10, 11);
        // OutputStream output = new FileOutputStream("log.txt");
        // TabulatedFunctions.outputTabulatedFunction(logo, output);
        // output.flush();

        // output.close();

        // InputStream input = new FileInputStream("log.txt");
        // TabulatedFunction logi = TabulatedFunctions.inputTabulatedFunction(input);
        // // ObjectOutputStream objectOutputStream = new ObjectOutputStream(logi);
        // // objectOutputStream.writeObject(tabLn);
        // // objectOutputStream.close();
        // input.close();

        // System.out.println("Logarithm of exponent (9th task)");

        // Log ln = new Log(Math.E);
        // Exp nl = new Exp();
        // Function comp = Functions.composition(ln, nl);
        // TabulatedFunction tabLn = TabulatedFunctions.tabulate(comp, 0, 10, 11);

        // // for (double x = 0; x < 11; x++) {
        // // System.out.println("point x=" + x + ": " + tabLn.getFunctionValue(x));
        // // }

        // // serialize into file a tabulated logarithm of exponent
        // FileOutputStream fos = new FileOutputStream("temp.txt");
        // ObjectOutputStream objectOutputStream = new ObjectOutputStream(fos);
        // objectOutputStream.writeObject(tabLn);
        // objectOutputStream.close();

        // // (deserialization) read from file
        // FileInputStream fos1 = new FileInputStream("temp.txt");
        // ObjectInputStream objectInputStream = new ObjectInputStream(fos1);

        // // object type specification needed since readObject() returns 'object'
        // TabulatedFunction comp1 = (TabulatedFunction) objectInputStream.readObject();
        // objectInputStream.close();

        // for (double i = 0; i < 11; i++) {
        // System.out.println("point x=" + i + ": " + comp1.getFunctionValue(i));
        // }

    }
}
