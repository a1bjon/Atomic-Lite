import javax.swing.*;
import javax.swing.plaf.basic.BasicScrollBarUI;
import java.awt.*;


public class AtomicGUI extends JFrame{
    public JPanel mainPane;

    public JTextArea textBox;

    public JPanel fileInfoCon;

    public JLabel fileInfo;

    public AtomicGUI(){
        super("Atomic Lite");
        this.setSize(Constants.WIDTH, Constants.HEIGHT);
        this.setIconImage(new ImageIcon("images/icon.png").getImage());
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setResizable(false);
        this.setLayout(null);


        mainPane = new JPanel();
        mainPane.setBackground(Constants.grey12);
        mainPane.setBounds(0, 0, 884, 600);
        mainPane.setLayout(null);
        mainPane.setVisible(true);

        JLabel title = new JLabel("[Atomic Lite]");
        title.setFont(new Font("consolas", Font.BOLD, 25));
        title.setForeground(Constants.purple);
        title.setBounds(355, 10, 200, 30);
        mainPane.add(title);

        Menu menuBar = new Menu(this);
        menuBar.setBounds(0, 46, 884, 35);
        mainPane.add(menuBar);

        fileInfoCon = new JPanel();
        fileInfoCon.setLayout(null);
        fileInfoCon.setBackground(Constants.grey12);
        fileInfoCon.setBorder(BorderFactory.createLineBorder(Constants.grey, 3, true));
        fileInfoCon.setBounds(0, 76, 884, 35);
        fileInfo = new JLabel("-- No File --");
        fileInfo.setForeground(Constants.purple);
        fileInfo.setFont(new Font("consolas", Font.BOLD, 14));
        fileInfo.setBounds(400, 9, 884, 17);
        fileInfoCon.add(fileInfo);
        this.add(fileInfoCon);


        // Text Box
        textBox = new JTextArea();
        textBox.setForeground(Constants.grey);
        textBox.setFont(new Font("consolas", Font.PLAIN, 15));
        textBox.setBackground(Constants.grey12);

        // Scroll Container
        JScrollPane scrollCon = new JScrollPane(textBox);
        scrollCon.setBounds(0, 110, 884, 451);
        scrollCon.setBorder(BorderFactory.createLineBorder(Constants.grey, 3, true));
        scrollCon.setBackground(Constants.grey12);
        scrollCon.getVerticalScrollBar().setBackground(Constants.dark_grey);

        // Vertical Bar
        scrollCon.getVerticalScrollBar().setUI(new BasicScrollBarUI() {
            @Override
            public void configureScrollBarColors(){
                this.thumbColor = Constants.grey;
            }
        });

        // Vertical Bar Arrows
        scrollCon.getVerticalScrollBar().getComponent(0).setBackground(Constants.dark_grey);
        scrollCon.getVerticalScrollBar().getComponent(1).setBackground(Constants.dark_grey);

        // Horizontal Bar
        scrollCon.getHorizontalScrollBar().setBackground(Constants.dark_grey);
        scrollCon.getHorizontalScrollBar().setUI(new BasicScrollBarUI() {
            @Override
            public void configureScrollBarColors(){
                this.thumbColor = Constants.grey;
            }
        });

        // Horizontal Bar Arrows
        scrollCon.getHorizontalScrollBar().getComponent(0).setBackground(Constants.dark_grey);
        scrollCon.getHorizontalScrollBar().getComponent(1).setBackground(Constants.dark_grey);

        mainPane.add(scrollCon);

        this.add(mainPane);
        this.setVisible(true);
    }

}
