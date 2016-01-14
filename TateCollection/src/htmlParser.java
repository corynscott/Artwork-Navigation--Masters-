import java.io.IOException;





import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;


public class htmlParser {
	

	
	public String extractImgURL(String url){
		Document doc;
		try {
			//System.out.println(url);
			doc = Jsoup.connect(url).get();
			Elements lbms = doc.getElementsByClass("lbMain");
			if(!lbms.isEmpty()){
				Element lbm = lbms.first();
				String imgURL = lbm.attr("href");
				return  imgURL;
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
		
		
	}
	
	
	public static void main(String[] args){
		
		htmlParser hp = new htmlParser();
	}
}
