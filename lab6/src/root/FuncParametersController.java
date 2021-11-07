package root;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.Spinner;
import javafx.scene.control.TextField;
import javafx.scene.control.Alert.AlertType;
import javafx.stage.Stage;

public class FuncParametersController {

    public static int OK;
    public static int CANCEL;
    private int status;

    private double leftX;
    private double rightX;
    private int pointCount;

    @FXML
    private TextField edLeftDomainBorder, edRightDomainBorder;

    @FXML
    private Spinner<Integer> spinner;

    @FXML
    private Button closeButton, btnOK;

    @FXML
    void initialize() {
        this.edLeftDomainBorder.setText("0");
        this.edRightDomainBorder.setText("10");
        // this.spinner.setI(11);
    }

    @FXML
    private void btnOKClick(ActionEvent event) {
        try {
            leftX = Double.parseDouble(this.edLeftDomainBorder.getText());
            rightX = Double.parseDouble(this.edRightDomainBorder.getText());
            pointCount = spinner.getValue();
            this.status = OK;

            App.tabDoc.newFunction(leftX, rightX, pointCount);

            Stage stage = (Stage) btnOK.getScene().getWindow();
            stage.close();

        } catch (NumberFormatException e) {
            Alert alert = new Alert(AlertType.WARNING);
            alert.setTitle("Wrong values");
            alert.setContentText("Domain borders shoud be numbers");
            alert.showAndWait();
        }
    }

    @FXML
    private void btnCancelClick(ActionEvent event) {
        Stage stage = (Stage) closeButton.getScene().getWindow();
        stage.close();
    }

    public void setStage(Stage stage) {
    }

    public void setStatus(int status) {
        this.status = status;
    }

    public int getStatus() {
        return status;
    }

    public int showDialog() {
        // this.setVisible(true);
        return this.status;
    }

    static {
        OK = 1;
        CANCEL = 0;
    }

    public double getLeftDomainBorder() {
        return leftX;
    }

    public double getRightDomainBorder() {
        return rightX;
    }

    public int getPointsCount() {
        return pointCount;
    }

}
