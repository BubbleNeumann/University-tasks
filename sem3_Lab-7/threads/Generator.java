package threads;

import functions.basic.Log;

public class Generator extends Thread {

    private Task task;
    private Switcher switcher;
    private boolean running;

    public Generator(Task task, Switcher switcher) {
        this.task = task;
        this.switcher = switcher;
        running = false;
    }

    @Override
    public void run() {
        running = true;
        for (int i = 0; i < task.getTaskNumber() && running; i++) {
            try {
                Log log = new Log(1 + (Math.random() * 9));
                switcher.beginWrite();
                task.setFunc(log);
                task.setLeftX(Math.random() * 100);
                task.setRightX(Math.random() * 100 + 100);
                task.setStep(Math.random());
                switcher.endWrite();
                System.out.println("Source leftX = " + task.getLeftX() + " rightX = " + task.getRightX() + " step = "
                        + task.getStep());

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
