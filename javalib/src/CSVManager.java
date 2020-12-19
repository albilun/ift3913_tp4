import java.io.FileWriter;
import java.io.IOException;

/***
 * Produit les fichiers CSV 
 * @author William Bach (20127144) && Daniel El-Masri (20096261)
 *
 */
public class CSVManager {
    private String PATH_classes = "temp/classes.csv";
    private String PATH_methods = "temp/methods.csv";

    /**
     * Remplit les fichiers CSV avec l'information fournie 
     * @param lines array avec toutes les lignes CSV
     * @param isClassReport true si on update classes.csv
     */
    public void updateCSVFile(String[] lines, boolean isClassReport) 
    {
        //recuperation du chemin du fichier csv
        String PATH;
        
        if (isClassReport)
        {
        	PATH = this.PATH_classes;
        }
        else
        {
        	PATH = this.PATH_methods;
        }

        try {
            FileWriter csvWriter = new FileWriter(PATH, false);
            int i = 0;
            while (i < lines.length) {
                csvWriter.append(lines[i]);
                csvWriter.flush();
                i++;
            }
            csvWriter.close();

        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("Something went wrong. Can't update CSV files.");
        }
    }
}
