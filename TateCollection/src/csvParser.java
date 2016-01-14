import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;


public class csvParser {
	String srcDir ="F:/Coryn/Google Drive/Project/Image Collection/Tate/";
	String csvFilename = "turner-images.csv";
	
	public ArrayList<String> extractLocations(String csvFile){
		BufferedReader br = null;
		String line = "";
		String splitChar = ",";
	 
		ArrayList<String> imageLocations = new ArrayList<String>(); 
		
		try {
			br = new BufferedReader(new FileReader(csvFile));
			while ((line = br.readLine()) != null) {
				 
				//String[] work = line.split(splitChar);
				String[] work = line.split(",(?=([^\"]*\"[^\"]*\")*[^\"]*$)", -1);
				imageLocations.add(work[19]);
			}
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return imageLocations;
		
		
	}
	
	public static void main(String[] args){
		csvParser cp = new csvParser();
		
		
	}

}
