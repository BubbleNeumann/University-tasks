package root;

import doc.TabulatedFunctionDoc;
import functions.ArrayTabulatedFunction;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class App extends Application {

    public static TabulatedFunctionDoc tabDoc;
    public static Stage primaryStage;

    @Override
    public void start(Stage primaryStage) throws Exception {
        try {
            // tabDoc = new TabulatedFunctionDoc();
            tabDoc = new TabulatedFunctionDoc(new ArrayTabulatedFunction(0, 4, 5), "save.json");
            FXMLLoader fxmlLoader = new FXMLLoader(App.class.getResource("/root/Mainframe.fxml").toURI().toURL());
            // FXMLLoader fxmlLoader = new
            // FXMLLoader(MainframeController.class.getResource("Mainframe.fxml"));

            Parent root = fxmlLoader.load();

            MainframeController ctrl = fxmlLoader.getController();
            tabDoc.registerRedrawFunctionController(ctrl);

            primaryStage.setTitle("Tabulated functions");
            primaryStage.setScene(new Scene(root));
            primaryStage.show();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws Exception {
        launch(args);
    }
}