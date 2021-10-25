package doc;

import functions.*;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class TabulatedFunctionDoc implements TabulatedFunction {

    private TabulatedFunction function;
    private String fileName;
    private boolean unsavedChanges;
    private boolean modified;
    private boolean fileNameAssigned;

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

    public void newFunction(double leftX, double rightX, int pointsCount) {

        function = new ArrayTabulatedFunction(leftX, rightX, pointsCount);
        // if (fileName == "ArrayTabulatedFunction") {
        // function = new ArrayTabulatedFunction(leftX, rightX, pointsCount);
        // } else if (fileName == "LinkedListTabulatedFunction") {
        // function = new LinkedListTabulatedFunction(leftX, rightX, pointsCount);
        // }
    }

    public TabulatedFunction tabulateFunction(Function func, double leftX, double rightX, int pointsCount)
            throws IllegalArgumentException, InappropriateFunctionPointException {
        return TabulatedFunctions.tabulate(func, leftX, rightX, pointsCount);
    }

    public void saveFunctionAs(String fileName) {

        JSONObject pointsCount = new JSONObject();
        pointsCount.put("pointsCount", function.getStructureLength());

        JSONArray points = new JSONArray();

        for (int i = 0; i < function.getStructureLength(); i++) {
            JSONObject point = new JSONObject();
            point.put("x", function.getPointX(i));
            point.put("y", function.getPointY(i));
            points.add(point);
        }

        try (FileWriter file = new FileWriter(fileName)) {
            file.write(points.toJSONString());
            file.flush();
            unsavedChanges = false;

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

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
    }

    @Override
    public void addElemByIndex(int index) {
        unsavedChanges = true;
        modified = true;
        function.addElemByIndex(index);
    }

    @Override
    public void deleteElemByIndex(int index) throws FunctionPointIndexOutOfBoundsException {
        unsavedChanges = true;
        modified = true;
        function.deleteElemByIndex(index);
    }

    @Override
    public Object clone() throws CloneNotSupportedException {
        return new TabulatedFunctionDoc(function, fileName);
    }

    @Override
    public FunctionPoint getPoint(int index) {
        return function.getPoint(index);
    }

}
