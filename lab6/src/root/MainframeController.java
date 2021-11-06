package root;

import java.net.URL;
import java.util.ResourceBundle;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import doc.FunctionPointT;
import functions.FunctionPoint;
import functions.InappropriateFunctionPointException;

public class MainframeController {

    @FXML
    private ResourceBundle resources;

    @FXML
    private URL location;

    @FXML
    private TextField edX, edY;

    @FXML
    private TableView<FunctionPointT> table;

    @FXML
    private TableColumn<FunctionPointT, Double> xValues, yValues;

    @FXML
    private Label funcPtrCount;

    @FXML
    void initialize() {
        xValues = new TableColumn<FunctionPointT, Double>("X values");

        // name of property is passed as a parameter to PropertyValueFactory constructor
        xValues.setCellValueFactory(new PropertyValueFactory<FunctionPointT, Double>("x"));
        table.getColumns().add(xValues);

        yValues = new TableColumn<FunctionPointT, Double>("Y values");
        yValues.setCellValueFactory(new PropertyValueFactory<FunctionPointT, Double>("y"));
        table.getColumns().add(yValues);

        for (int i = 0; i < App.tabDoc.getStructureLength(); i++)
            table.getItems().add(i, new FunctionPointT(App.tabDoc.getPoint(i).getX(), App.tabDoc.getPoint(i).getY()));

        funcPtrCount.setText(String.valueOf(App.tabDoc.getStructureLength()));
    }

    /**
     * called when the "Add point" button is clicked
     * 
     * @param event
     */
    @FXML
    private void btnNewClick(ActionEvent event) {
        try {
            App.tabDoc.addElemToTail(
                    new FunctionPoint(Double.parseDouble(edX.getText()), Double.parseDouble(edY.getText())));
        } catch (NumberFormatException | InappropriateFunctionPointException e) {
            e.printStackTrace();
        }
    }

    /**
     * called when the "Delete" button is clicked
     * 
     * @param event
     */
    @FXML
    private void btnDeleteClick(ActionEvent event) {
        int rowIndex = table.getSelectionModel().getSelectedIndex();
        App.tabDoc.deleteElemByIndex(rowIndex);
    }

    public void redraw() {
        table.getItems().clear();
        funcPtrCount.setText(String.valueOf(App.tabDoc.getStructureLength()));
        for (int i = 0; i < App.tabDoc.getStructureLength(); i++)
            table.getItems().add(new FunctionPointT(App.tabDoc.getPoint(i).getX(), App.tabDoc.getPoint(i).getY()));
    }

}
