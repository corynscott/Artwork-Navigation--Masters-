import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;


public class ImageDownloader {
	//Location of the CSV File containing the metadata
	String srcDir ="F:/Coryn/Google Drive/Project/Image Collection/Tate/";
	
	//the CSV filename
	String csvFilename = "turner-images.csv";
	
	
	String csvFile = srcDir + csvFilename;
	
	String rootURL = "http://www.tate.org.uk";
	
	//locations to store the images	
	String destDir = "F:/Coryn/Google Drive/Project/Image Collection/Tate/Images";
	
	
	public ImageDownloader(){
		
		csvParser cp = new csvParser();
		ArrayList<String> imageLocations = cp.extractLocations(csvFile);

		htmlParser hp = new htmlParser();
		for(String il : imageLocations){
			if(il != null){
			String imageUrl = hp.extractImgURL(il);
			if(imageUrl !=null){
				System.out.println(imageUrl);
				 try {
						downloadImage(imageUrl);
					} catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
			}
			
		   
			}
		}
		
	}
		
	public void downloadImage(String imageUrl) throws IOException{
		URL url = new URL(rootURL+imageUrl);
		String fileName = url.getFile();
		//String destName = destDir + fileName.substring(fileName.lastIndexOf("/"));
		String destName = destDir + imageUrl;
		
		File temp = new File(destName.substring(0, destName.lastIndexOf("/")));
		temp.mkdirs();
		
		
		InputStream is = url.openStream();
		OutputStream os = new FileOutputStream(destName);
		
		byte[] b = new byte[2048];
		int length;
	 
		while ((length = is.read(b)) != -1) {
			os.write(b, 0, length);
		}
	 
		is.close();
		os.close();
	}
	


	public static void main (String[] args){
		ImageDownloader id = new ImageDownloader();
		
	}
}
	
	


