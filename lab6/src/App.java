import doc.*;
import functions.ArrayTabulatedFunction;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class App extends Application {

    public static TabulatedFunctionDoc tabDoc;

    @Override
    public void start(Stage primaryStage) throws Exception {
        // tabDoc = new TabulatedFunctionDoc();
        tabDoc = new TabulatedFunctionDoc(new ArrayTabulatedFunction(0, 4, 5), "save.json");
        FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource("mainframe.fxml"));

        Parent root = fxmlLoader.load();
        // Contr ctrl = fxmlLoader.getController();
        Scene scene = new Scene(root);

        primaryStage.setTitle("Tabulated functions");
        primaryStage.setScene(scene);
        primaryStage.show();

    }

    public static void main(String[] args) throws Exception {
        launch(args);
    }
}