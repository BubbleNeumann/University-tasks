package threads;

public class Switcher {

    private boolean canWrite = true;

    public synchronized void beginRead() throws InterruptedException {
        while (canWrite)
            wait();
    }

    public synchronized void endRead() {
        canWrite = true;
        notifyAll();
    }

    public synchronized void beginWrite() throws InterruptedException {
        while (!canWrite)
            wait();
    }

    public synchronized void endWrite() {
        canWrite = false;
        notifyAll();
    }
}
