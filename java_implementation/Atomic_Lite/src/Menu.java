import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;

public class Menu extends JPanel {

    private final AtomicGUI mainGui;

    JFileChooser chooser = new JFileChooser();

    public Menu(AtomicGUI mainGui){

        this.mainGui = mainGui;

        this.setBackground(Constants.grey);
        this.setBorder(BorderFactory.createLineBorder(Constants.grey, 3, true));
        this.setVisible(true);
        this.setLayout(null);

        drawMenu();

    }

    private void drawMenu(){
        JButton openFileButton = new JButton("Open File");
        openFileButton.setBackground(Constants.grey12);
        openFileButton.setForeground(Constants.grey);
        openFileButton.setFont(new Font("consolas", Font.BOLD, 14));
        openFileButton.setFocusable(false);
        openFileButton.setBorderPainted(false);
        openFileButton.setBounds(4, 4, 106, 25);
        openFileButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    openFile();
                    mainGui.fileInfo.setText(chooser.getSelectedFile().getName());
                }
                catch (IOException ex) {
                    JOptionPane.showMessageDialog(mainGui, "File Not Found");
                }
            }
        });
        this.add(openFileButton);

        JButton saveFileButton = new JButton("Save As");
        saveFileButton.setBackground(Constants.grey12);
        saveFileButton.setForeground(Constants.grey);
        saveFileButton.setFont(new Font("consolas", Font.BOLD, 14));
        saveFileButton.setFocusable(false);
        saveFileButton.setBorderPainted(false);
        saveFileButton.setBounds(115, 4, 106, 25);
        saveFileButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                saveFile();
            }
        });
        this.add(saveFileButton);

        JButton removeFileButton = new JButton("RM File");
        removeFileButton.setBackground(Constants.grey12);
        removeFileButton.setForeground(Constants.grey);
        removeFileButton.setFont(new Font("consolas", Font.BOLD, 14));
        removeFileButton.setFocusable(false);
        removeFileButton.setBorderPainted(false);
        removeFileButton.setBounds(226, 4, 106, 25);
        removeFileButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                removeFile();
            }
        });
        this.add(removeFileButton);

        JPanel fontSizeCon = new JPanel();
        fontSizeCon.setLayout(null);
        fontSizeCon.setBounds(337, 4, 106, 25);
        fontSizeCon.setBackground(Constants.grey12);

        JButton fontUpButton = new JButton("▲");
        fontUpButton.setBackground(Constants.grey12);
        fontUpButton.setForeground(Constants.grey);
        fontUpButton.setFocusable(false);
        fontUpButton.setBorderPainted(false);
        fontUpButton.setBounds(0, 0, 44, 25);
        fontSizeCon.add(fontUpButton);

        JLabel fontSizeLabel = new JLabel("10");
        fontSizeLabel.setForeground(Constants.grey);
        fontSizeLabel.setFont(new Font("consolas", Font.BOLD, 14));
        fontSizeLabel.setBounds(44, 2, 18, 25);
        fontSizeCon.add(fontSizeLabel);

        JButton fontDownButton = new JButton("▼");
        fontDownButton.setBackground(Constants.grey12);
        fontDownButton.setForeground(Constants.grey);
        fontDownButton.setFocusable(false);
        fontDownButton.setBorderPainted(false);
        fontDownButton.setBounds(62, 0, 44, 25);
        fontSizeCon.add(fontDownButton);
        this.add(fontSizeCon);

        JButton copyTextButton = new JButton("Copy Text");
        copyTextButton.setBackground(Constants.grey12);
        copyTextButton.setForeground(Constants.grey);
        copyTextButton.setFont(new Font("consolas", Font.BOLD, 14));
        copyTextButton.setFocusable(false);
        copyTextButton.setBorderPainted(false);
        copyTextButton.setBounds(448, 4, 106, 25);
        this.add(copyTextButton);

        JButton resetButton = new JButton("Reset");
        resetButton.setBackground(Constants.grey12);
        resetButton.setForeground(Constants.grey);
        resetButton.setFont(new Font("consolas", Font.BOLD, 14));
        resetButton.setFocusable(false);
        resetButton.setBorderPainted(false);
        resetButton.setBounds(559, 4, 106, 25);
        this.add(resetButton);

        JButton helpButton = new JButton("Help");
        helpButton.setBackground(Constants.grey12);
        helpButton.setForeground(Constants.grey);
        helpButton.setFont(new Font("consolas", Font.BOLD, 14));
        helpButton.setFocusable(false);
        helpButton.setBorderPainted(false);
        helpButton.setBounds(670, 4, 106, 25);
        this.add(helpButton);

        JButton quitButton = new JButton("Quit");
        quitButton.setBackground(Constants.grey12);
        quitButton.setForeground(Constants.grey);
        quitButton.setFont(new Font("consolas", Font.BOLD, 14));
        quitButton.setFocusable(false);
        quitButton.setBorderPainted(false);
        quitButton.setBounds(781, 4, 99, 25);
        this.add(quitButton);
    }

    private void openFile() throws IOException {
        int fileExp = chooser.showOpenDialog(mainGui);
        if(fileExp == JFileChooser.APPROVE_OPTION){
            String path = chooser.getSelectedFile().getAbsolutePath();
            BufferedReader reader = new BufferedReader(new FileReader(path));
            String line = reader.readLine();
            while(line != null){
                mainGui.textBox.append(line + "\n");
                line = reader.readLine();
            }
        }
    }

    private void saveFile(){
        String textContent = mainGui.textBox.getText();
        int fileExp = chooser.showSaveDialog(mainGui);
        if(fileExp == JFileChooser.APPROVE_OPTION){
            String path = chooser.getSelectedFile().getAbsolutePath();
            mainGui.fileInfo.setText(chooser.getSelectedFile().getName());
            try{
                FileWriter file = new FileWriter(path);
                BufferedWriter output = new BufferedWriter(file);
                output.write(textContent);
                output.close();
            }
            catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private void removeFile(){
        mainGui.fileInfo.setText("-- No File --");
        mainGui.textBox.setText("");
    }
}
