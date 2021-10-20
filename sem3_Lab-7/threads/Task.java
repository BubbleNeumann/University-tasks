package threads;

import functions.Function;

public class Task {

    private Function func;
    private double leftX;
    private double rightX;
    private double step;
    private int taskNumber;

    /**
     * @param taskNumber
     */
    public Task(int taskNumber) {
        this.taskNumber = taskNumber;
    }

    /**
     * @return the func
     */
    public Function getFunc() {
        return func;
    }

    /**
     * @param func the func to set
     */
    public void setFunc(Function func) {
        this.func = func;
    }

    /**
     * @return the leftX
     */
    public double getLeftX() {
        return leftX;
    }

    /**
     * @param leftX the leftX to set
     */
    public void setLeftX(double leftX) {
        this.leftX = leftX;
    }

    /**
     * @return the rightX
     */
    public double getRightX() {
        return rightX;
    }

    /**
     * @param rightX the rightX to set
     */
    public void setRightX(double rightX) {
        this.rightX = rightX;
    }

    /**
     * @return the step
     */
    public double getStep() {
        return step;
    }

    /**
     * @param step the step to set
     */
    public void setStep(double step) {
        this.step = step;
    }

    /**
     * @return the taskNumber
     */
    public int getTaskNumber() {
        return taskNumber;
    }

    /**
     * @param taskNumber the taskNumber to set
     */
    public void setTaskNumber(int taskNumber) {
        this.taskNumber = taskNumber;
    }
}
