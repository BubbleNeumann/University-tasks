package threads;

import functions.Functions;
import functions.InappropriateFunctionPointException;

public class SimpleIntegrator implements Runnable {

    Task task;

    /**
     * @param task
     */
    public SimpleIntegrator(Task task) {
        this.task = task;
    }

    @Override
    public void run() {
        for (int i = 0; i < task.getTaskNumber(); i++) {
            double res = Double.NaN;
            if (task.getFunc() == null)
                continue;

            synchronized (task) {
                try {
                    res = Functions.integrate(task.getFunc(), task.getLeftX(), task.getRightX(), task.getStep());
                } catch (IllegalStateException | InappropriateFunctionPointException e) {
                    e.printStackTrace();
                }

                System.out.println("Result leftX = " + task.getLeftX() + " rightX = " + task.getRightX() + " step = "
                        + task.getStep() + " integrate = " + res);
            }
        }
    }
}
