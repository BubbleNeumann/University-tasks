package doc;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import root.*;
import functions.ArrayTabulatedFunction;
import functions.FunctionPoint;
import functions.FunctionPointIndexOutOfBoundsException;
import functions.InappropriateFunctionPointException;
import functions.TabulatedFunction;
import functions.TabulatedFunctions;
import functions.Function;

public class TabulatedFunctionDoc implements TabulatedFunction {

    private TabulatedFunction function;
    private String fileName;
    private boolean unsavedChanges;
    private boolean modified;
    private boolean fileNameAssigned;
    private MainframeController controller;

    public TabulatedFunctionDoc() {
        this.function = new ArrayTabulatedFunction();
        this.fileName = "save.json";
        unsavedChanges = true;
        modified = false;

        if (fileName.isEmpty())
            fileNameAssigned = false;
        else
            fileNameAssigned = true;
    }

    public TabulatedFunctionDoc(TabulatedFunction function, String fileName) {
        this.function = function;
        this.fileName = fileName;
        unsavedChanges = true;
        modified = false;

        if (fileName.isEmpty())
            fileNameAssigned = false;
        else
            fileNameAssigned = true;
    }

    public TabulatedFunction getFunction() {
        return function;
    }

    public void setFunction(TabulatedFunction function) {
        this.function = function;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public boolean isUnsavedChanges() {
        return unsavedChanges;
    }

    public void setUnsavedChanges(boolean unsavedChanges) {
        this.unsavedChanges = unsavedChanges;
    }

    public boolean isModified() {
        return modified;
    }

    public boolean isFileNameAssigned() {
        return fileNameAssigned;
    }

    /**
     * replace a tabulated function object with a new one with given parameters
     * 
     * @param leftX
     * @param rightX
     * @param pointsCount
     */
    public void newFunction(double leftX, double rightX, int pointsCount) {
        function = new ArrayTabulatedFunction(leftX, rightX, pointsCount);
        this.callRedraw();
    }

    /**
     * tabulates a given function, i.e. splits the function on pieces
     * 
     * @param f
     * @param leftX
     * @param rightX
     * @param pointsCount
     * @return TabulatedFunction
     * @throws IllegalArgumentException
     * @throws InappropriateFunctionPointException
     */
    public TabulatedFunction tabulateFunction(Function f, double leftX, double rightX, int pointsCount)
            throws IllegalArgumentException, InappropriateFunctionPointException {
        this.function = TabulatedFunctions.tabulate(f, leftX, rightX, pointsCount);
        return TabulatedFunctions.tabulate(f, leftX, rightX, pointsCount);
    }

    public void saveFunctionAs(String fileName) {
        JSONObject outer = new JSONObject();
        // JSONObject pointsCount = new JSONObject();
        // pointsCount.put("pointsCount", function.getStructureLength());

        JSONArray points = new JSONArray();

        for (int i = 0; i < function.getStructureLength(); i++) {
            JSONObject point = new JSONObject();
            point.put("x", function.getPointX(i));
            point.put("y", function.getPointY(i));
            points.add(point);
        }

        outer.put("pointsCount", function.getStructureLength());
        outer.put("points", points);

        try (FileWriter file = new FileWriter(fileName)) {
            file.write(outer.toJSONString());
            file.flush();
            unsavedChanges = false;

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * get the function from json file fills the 'pointsCount' parameter and creates
     * a new TabulatedFunction
     * 
     * @param fileName
     */
    public void loadFunction(String fileName) {
        JSONParser parser = new JSONParser();

        try (FileReader reader = new FileReader(fileName)) {
            JSONObject rJsonObject = (JSONObject) parser.parse(reader);
            long pointsCount = (long) rJsonObject.get("pointsCount");
            JSONArray pointsJsonArray = (JSONArray) rJsonObject.get("points");

            FunctionPoint[] points = new FunctionPoint[(int) pointsCount];
            int index = 0;

            for (Object item : pointsJsonArray) {
                JSONObject point = (JSONObject) item;

                double x = (double) point.get("x");
                double y = (double) point.get("y");

                points[index++] = new FunctionPoint(x, y);
            }

            function = new ArrayTabulatedFunction(points);

        } catch (IOException | ParseException e) {
            System.out.println(e.toString());
        }

        this.callRedraw();

    }

    public void saveFunction() {
        saveFunctionAs(this.fileName);
        unsavedChanges = false;
    }

    @Override
    public double getLeftDomainBorder() throws IllegalStateException {
        return function.getLeftDomainBorder();
    }

    @Override
    public double getRightDomainBorder() throws IllegalStateException {
        return function.getRightDomainBorder();
    }

    @Override
    public double getFunctionValue(double x) throws InappropriateFunctionPointException {
        return function.getFunctionValue(x);
    }

    @Override
    public int getStructureLength() {
        return function.getStructureLength();
    }

    @Override
    public void setPointX(int index, double x) throws InappropriateFunctionPointException {
        unsavedChanges = true;
        modified = true;
        function.setPointX(index, x);
        this.callRedraw();
    }

    @Override
    public double getPointX(int index) throws FunctionPointIndexOutOfBoundsException {
        return function.getPointX(index);
    }

    @Override
    public void setPointY(int index, double y) {
        unsavedChanges = true;
        modified = true;
        function.setPointY(index, y);
        this.callRedraw();
    }

    @Override
    public double getPointY(int index) throws FunctionPointIndexOutOfBoundsException {
        return function.getPointY(index);
    }

    @Override
    public void addElemToTail(FunctionPoint point) throws InappropriateFunctionPointException {
        unsavedChanges = true;
        modified = true;
        function.addElemToTail(point);
        this.callRedraw();
    }

    @Override
    public void addElemByIndex(int index, FunctionPoint point) {
        unsavedChanges = true;
        modified = true;
        function.addElemByIndex(index, point);
        this.callRedraw();
    }

    @Override
    public void deleteElemByIndex(int index) throws FunctionPointIndexOutOfBoundsException {
        unsavedChanges = true;
        modified = true;
        function.deleteElemByIndex(index);

        // since the function was modified
        this.callRedraw();
    }

    @Override
    public Object clone() throws CloneNotSupportedException {
        return new TabulatedFunctionDoc(function, fileName);
    }

    @Override
    public FunctionPoint getPoint(int index) {
        return function.getPoint(index);
    }

    @Override
    public String toString() {
        return this.function.toString();
    }

    public void registerRedrawFunctionController(MainframeController ctrl) {
        controller = ctrl;
    }

    public void callRedraw() {
        controller.redraw();
    }

}
