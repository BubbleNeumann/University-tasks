package functions;

/**
 * Thrown to indicate that the given to the method FunctionPoint argument is out
 * of bounds or that FunctionPoint with given x coordinate already exists.
 */
public class InappropriateFunctionPointException extends Exception {
    public InappropriateFunctionPointException() {
    }

    public InappropriateFunctionPointException(String message) {
        super(message);
    }
}
