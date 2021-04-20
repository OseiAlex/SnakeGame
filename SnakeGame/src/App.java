import java.awt.EventQueue;

public class App {

    public static GUI gui;

    public static void main(String[] args) {
        EventQueue.invokeLater(() -> {
            try {
                gui = new GUI();
                gui.createGameWindow();
            } catch (Exception e) {
                e.printStackTrace();
            }
        });

    }

}




