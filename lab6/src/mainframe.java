import java.net.URL;
import java.util.ResourceBundle;

import doc.FunctionPointT;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;

public class mainframe {

    @FXML
    private ResourceBundle resources;

    @FXML
    private URL location;

    @FXML
    private TextField edX, edY;

    @FXML
    private TableView<FunctionPointT> table;

    @FXML
    void initialize() {
        FunctionPointT[] tableContent = new FunctionPointT[App.tabDoc.getStructureLength()];

        for (int i = 0; i < tableContent.length; i++) {
            tableContent[i] = new FunctionPointT(App.tabDoc.getPoint(i).getX(), App.tabDoc.getPoint(i).getY());
        }

        ObservableList<FunctionPointT> pointTs = FXCollections.observableArrayList(tableContent);

        table = new TableView<FunctionPointT>(pointTs);

        TableColumn<FunctionPointT, Double> xValues = new TableColumn<FunctionPointT, Double>("X value");
        xValues.setCellValueFactory(new PropertyValueFactory<FunctionPointT, Double>("x"));
        table.getColumns().add(xValues);

        TableColumn<FunctionPointT, Double> yValues = new TableColumn<FunctionPointT, Double>("Y value");
        yValues.setCellValueFactory(new PropertyValueFactory<FunctionPointT, Double>("y"));
        table.getColumns().add(yValues);

    }

    /**
     * called when the "Add point" button is clicked
     * 
     * @param event
     */
    @FXML
    private void btnNewClick(ActionEvent event) {

        if (table.getColumns() == null)
            edX.setText("we're good");

    }

    /**
     * called when the "Delete" button is clicked
     * 
     * @param event
     */
    @FXML
    private void btnDeleteClick(ActionEvent event) {

    }

    public void redraw() {

    }

}
