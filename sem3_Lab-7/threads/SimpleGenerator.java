package threads;

import functions.basic.Log;

public class SimpleGenerator implements Runnable {

    Task task;

    /**
     * @param task
     */
    public SimpleGenerator(Task task) {
        this.task = task;
    }

    @Override
    public void run() {
        for (int i = 0; i < task.getTaskNumber(); i++) {
            Log log = new Log(1 + (Math.random() * 9));

            synchronized (task) {
                task.setFunc(log);
                task.setLeftX(Math.random() * 100);
                task.setRightX(Math.random() * 100 + 100);
                task.setStep(Math.random());
                System.out.println("Source leftX = " + task.getLeftX() + " rightX = " + task.getRightX() + " step = "
                        + task.getStep());
            }
        }
    }
}
