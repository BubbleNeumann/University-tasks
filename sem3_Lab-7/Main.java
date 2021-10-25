import functions.*;
import functions.basic.Exp;
import functions.basic.Log;
import threads.Generator;
import threads.Integrator;
import threads.SimpleGenerator;
import threads.SimpleIntegrator;
import threads.Switcher;
import threads.Task;

public class Main {

    static void nonThread() throws IllegalStateException, InappropriateFunctionPointException {
        Task task = new Task(100);
        for (int i = 0; i < task.getTaskNumber(); i++) {
            task.setFunc(new Log(1 + (Math.random() * 9)));
            task.setLeftX(Math.random() * 100);
            task.setRightX(Math.random() * 100 + 100);
            task.setStep(Math.random());

            System.out.println("Source leftX = " + task.getLeftX() + " rightX = " + task.getRightX() + " step = "
                    + task.getStep());

            double res = Functions.integrate(task.getFunc(), task.getLeftX(), task.getRightX(), task.getStep());

            System.out.println("Result leftX = " + task.getLeftX() + " rightX = " + task.getRightX() + " step = "
                    + task.getStep() + " integral = " + res);
        }
    }

    static void simpleThreads() {
        Task task = new Task(100);
        Thread generator = new Thread(new SimpleGenerator(task));
        generator.start();

        Thread integrator = new Thread(new SimpleIntegrator(task));
        integrator.start();
    }

    static void complicatedThreads() throws InterruptedException {
        Task task = new Task(100);
        Switcher switcher = new Switcher();
        Generator generator = new Generator(task, switcher);
        Integrator integrator = new Integrator(task, switcher);
        generator.setPriority(Thread.MAX_PRIORITY);
        generator.start();
        integrator.start();
        Thread.sleep(50);
        generator.interrupt();
        integrator.interrupt();
    }

    public static void main(String[] args) throws Exception {

        // Function exp = new Exp();
        // double step = 0.00000005;
        // System.out.println(Functions.integrate(exp, 0, 1, step));
        // System.out.println(Math.E - 1);

        // Main.nonThread();

        // Main.simpleThreads();

        Main.complicatedThreads();

    }
}
