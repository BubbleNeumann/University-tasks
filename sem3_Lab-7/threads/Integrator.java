package threads;

import functions.Functions;
import functions.InappropriateFunctionPointException;

public class Integrator extends Thread {

    private Task task;
    private Switcher switcher;
    private boolean running = false;

    public Integrator(Task task, Switcher switcher) {
        this.task = task;
        this.switcher = switcher;
    }

    @Override
    public void run() {
        running = true;
        for (int i = 0; i < task.getTaskNumber() && running; i++) {
            try {
                switcher.beginRead();
                double res = Functions.integrate(task.getFunc(), task.getLeftX(), task.getRightX(), task.getStep());

                System.out.println("Result leftX = " + task.getLeftX() + " rightX = " + task.getRightX() + " step = "
                        + task.getStep() + " integrate = " + res);

                switcher.endRead();

            } catch (IllegalStateException | InappropriateFunctionPointException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                System.out.println("Thread was correctly interrupted");
            }
        }
    }

    @Override
    public void interrupt() {
        super.interrupt();
        running = false;
    }
}
