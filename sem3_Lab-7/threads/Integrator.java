package threads;

import functions.Functions;
import functions.InappropriateFunctionPointException;

public class Integrator extends Thread {

    private Task task;
    private Switcher switcher;
    private boolean running;

    public Integrator(Task task, Switcher switcher) {
        this.task = task;
        this.switcher = switcher;
        running = false;
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

            } catch (InterruptedException e) {
                System.out.println("Интегратор прервали во время сна, он корректно завершил свою работу");

            } catch (IllegalStateException | InappropriateFunctionPointException e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    public void interrupt() {
        super.interrupt();
        running = false;
    }
}
