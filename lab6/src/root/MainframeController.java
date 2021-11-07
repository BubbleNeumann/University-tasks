package root;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.Optional;
import java.util.ResourceBundle;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.ButtonType;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.input.KeyEvent;
import javafx.stage.FileChooser;
import javafx.stage.Modality;
import javafx.stage.Stage;
import doc.FunctionPointT;
import functions.Function;
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

    private ArbitraryFileLoader classLoader;
    private FuncParametersController parametersFrame;

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

        edX.setText("0");
        edY.setText("0");
        funcPtrCount.setText(String.valueOf(App.tabDoc.getStructureLength()));
        this.classLoader = new ArbitraryFileLoader();
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
            Alert alert = new Alert(AlertType.WARNING);
            alert.setTitle("Wrong values");
            alert.setContentText("Inappropriate Function Point Exception or Number Format Exception");
            alert.showAndWait();
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

    @FXML
    private void mouseClickOnTable() {
        labelRedraw();
    }

    /**
     * @param event
     */
    @FXML
    private void keyTyped(KeyEvent event) {
        // TODO finish for keyboard events
        // KeyCode key = event.getCode(); // Keyboard code for the pressed key
        // if (key == KeyEvent.VK_UP) {
        // System.out.println("clicked");
        // }
    }

    private void labelRedraw() {
        funcPtrCount.setText("Point " + String.valueOf(table.getSelectionModel().getSelectedIndex() + 1) + " of "
                + String.valueOf(App.tabDoc.getStructureLength()));
    }

    public void redraw() {
        table.getItems().clear();
        funcPtrCount.setText(String.valueOf(App.tabDoc.getStructureLength()));
        for (int i = 0; i < App.tabDoc.getStructureLength(); i++)
            table.getItems().add(new FunctionPointT(App.tabDoc.getPoint(i).getX(), App.tabDoc.getPoint(i).getY()));
    }

    /**
     * Called when the menu item "New" is clicked. The method creates a new stage
     * from FuncParameter.fxml
     */
    @FXML
    private void newFunction(ActionEvent event) {
        showDialog();
    }

    @FXML
    private void openFunctionFromFile() {
        if (App.tabDoc.isFileNameAssigned())
            App.tabDoc.loadFunction(App.tabDoc.getFileName());
        else {
            Alert alert = new Alert(AlertType.WARNING);
            alert.setTitle("File name is not assigned");
            alert.setContentText("Function could not be opened");
            alert.showAndWait();
        }
    }

    @FXML
    private void saveFunctionInDefaultFile() {
        if (App.tabDoc.isFileNameAssigned()) {
            App.tabDoc.saveFunction();
            Alert alert = new Alert(AlertType.INFORMATION);
            alert.setContentText("Function was saved successfully");
            alert.showAndWait();
        } else {
            showMessageDialog("File name is not assigned", "Function could not be saved", AlertType.WARNING);
        }
    }

    @FXML
    private void saveFunctionInCustomFile() {

        // TODO add ability to choose file to save into
        if (App.tabDoc.isFileNameAssigned()) {
            App.tabDoc.saveFunction();
            showMessageDialog("", "Function was saved successfully", AlertType.INFORMATION);
        } else {
            showMessageDialog("File name is not assigned", "Function could not be saved", AlertType.WARNING);
        }
    }

    @FXML
    private void quit(ActionEvent event) {
        if (App.tabDoc.isUnsavedChanges()) {
            Alert alert = new Alert(AlertType.CONFIRMATION);
            alert.setTitle("Exit confirmation");
            alert.setContentText("Document is not saved.\nAre you sure you want to exit?");
            Optional<ButtonType> option = alert.showAndWait();
            if (option.get() == ButtonType.OK) {
                Stage stage = (Stage) table.getScene().getWindow();
                stage.close();
            }

        } else {
            Stage stage = (Stage) table.getScene().getWindow();
            stage.close();
        }
    }

    @FXML
    private void tabulate() {
        final FileChooser fileChooser = new FileChooser();
        Stage stage = (Stage) table.getScene().getWindow();
        try {
            File file = fileChooser.showOpenDialog(stage);
            final Function f = (Function) this.classLoader.loadClassFromFile(file.getAbsolutePath())
                    .getDeclaredConstructor().newInstance();
            if (showDialog() == FuncParametersController.OK) {
                App.tabDoc.tabulateFunction(f, this.parametersFrame.getLeftDomainBorder(),
                        this.parametersFrame.getRightDomainBorder(), this.parametersFrame.getPointsCount());
                redraw();
            }
        } catch (IOException ex2) {
            showMessageDialog("Could not read file", "Reading error", AlertType.WARNING);
        } catch (ClassFormatError ex3) {
            showMessageDialog("The file doesn't contain class byte code", "Reading error", AlertType.WARNING);
        } catch (IllegalAccessError ex4) {
            showMessageDialog("Could not find additional classes", "Reading error", AlertType.WARNING);
        } catch (ClassCastException ex5) {
            showMessageDialog("The file doesn't vontain function", "Creating error", AlertType.WARNING);
        } catch (InstantiationException | IllegalAccessException ex8) {
            showMessageDialog("The class has no public default constructor", "Creating error", AlertType.WARNING);
        } catch (IllegalArgumentException e) {
            showMessageDialog("Exception was thrown", "Illegal Argument Exception", AlertType.WARNING);
        } catch (InappropriateFunctionPointException e) {
            showMessageDialog("Exception was thrown", "Inappropriate Function PointException", AlertType.WARNING);
        } catch (InvocationTargetException e) {
            showMessageDialog("Exception was thrown", "Invocation Target Exception", AlertType.WARNING);
        } catch (NoSuchMethodException e) {
            showMessageDialog("Exception was thrown", "No Such Method Exception", AlertType.WARNING);
        } catch (SecurityException e) {
            showMessageDialog("Exception was thrown", "Security Exception", AlertType.WARNING);
        }

    }

    private int showDialog() {
        try {
            FXMLLoader newLoader = new FXMLLoader(App.class.getResource("/root/FuncParameters.fxml").toURI().toURL());
            Parent newRoot = newLoader.load();
            FuncParametersController newController = newLoader.getController();
            this.parametersFrame = newController;
            Stage newStage = new Stage();
            newController.setStage(newStage);

            newStage.setTitle("Function parameters");
            newStage.setScene(new Scene(newRoot));

            newStage.initModality(Modality.APPLICATION_MODAL);
            newStage.initOwner(App.primaryStage);
            newStage.showAndWait();

            newStage.setResizable(false);

            return newController.getStatus();

        } catch (IOException | URISyntaxException e) {
            e.printStackTrace();
        }

        return -1;
    }

    private void showMessageDialog(String title, String message, AlertType type) {
        Alert alert = new Alert(type);
        alert.setTitle(title);
        alert.setContentText(message);
        alert.showAndWait();
    }

}
