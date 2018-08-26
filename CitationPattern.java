import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.NavigableSet;
import java.util.Set;
import java.util.TreeMap;


public class CitationPattern {
	public static void main(String args[]) throws IOException {
		int WINDOW = Integer.parseInt (args[0]);
		double PEAK = Double.parseDouble (args[1]);
		FileInputStream fis = new FileInputStream("./TemporalEdgeListSim");
		BufferedReader br = new BufferedReader(new InputStreamReader(fis)); 
		
		FileInputStream fis1 = new FileInputStream("./AllPapersSim");
		BufferedReader br1 = new BufferedReader(new InputStreamReader(fis1)); 
		HashMap<String, String> allpaper=new HashMap<String, String>();
		String line="";
		while((line=br1.readLine())!=null){
			allpaper.put(line.trim(),line.trim());
		}
		br1.close();
		fis1.close();
		line="";
		
		HashMap<String, TreeMap<Integer, Integer>> map = new HashMap<String, TreeMap<Integer,Integer>>(); //paper_year_citation
		
		while((line=br.readLine())!=null){
			String[] a=line.split("\\s");
			
			if(a.length==3 && allpaper.containsKey(a[1].trim()) && a[2].trim().length() > 0){
				if(map.containsKey(a[1].trim())){
					if(map.get(a[1].trim()).containsKey(Integer.parseInt(a[2].trim()))){
						map.get(a[1].trim()).put(Integer.parseInt(a[2].trim()), map.get(a[1].trim()).get(Integer.parseInt(a[2].trim()))+1);
					}
					else
						map.get(a[1].trim()).put(Integer.parseInt(a[2].trim()),1);
				}
				else{        
					map.put(a[1].trim(), new TreeMap<Integer, Integer>());
					map.get(a[1].trim()).put(Integer.parseInt(a[2].trim()),1);
				}        			
			}
		}
		
		br.close();
		fis.close();
		
		HashMap<String, TreeMap<Integer, Integer>> reducedmap = new HashMap<String, TreeMap<Integer,Integer>>(); //paper_year_citation

		
		int count=0;
		int countOTH=0;
		int countGood=0;
		for(String paper:map.keySet()){
			NavigableSet<Integer> years=map.get(paper).descendingKeySet();
			int highest=years.first();
			int lowest=years.last();

			//Filter the papers which do not have at least ten years of history
			if(highest-lowest>=10){
				countGood += 1;

				reducedmap.put(paper, new TreeMap<Integer, Integer>());
				float totalCite=0;
				for(int i=lowest;i<=highest;i++){//fill up the empty years
					if(!years.contains(i))
						reducedmap.get(paper).put(i, 0);
					else{
						reducedmap.get(paper).put(i,map.get(paper).get(i));
						totalCite+=map.get(paper).get(i);
					}
				}    
				if(totalCite/(float)(highest-lowest+1)<1){
					reducedmap.remove(paper);
					countOTH++;
				}
			}
			else
				count++;
		}
		
		int countPeakInt=0;
		int countPeakMul=0;
		int countPeakLate=0;
		int countMonIncr=0;
		int countMonDec=0;

		ArrayList<String> peakTimeMul = new ArrayList<String>();
		ArrayList<String> peakTimeLate = new ArrayList<String>();
		
		for(String paper:reducedmap.keySet()){
			NavigableSet<Integer> years=reducedmap.get(paper).descendingKeySet();
			int lastyear=years.first();int firstyear=years.last();
			float highpeak=0;
			for(int i=firstyear;i<=lastyear;i++){
				if(highpeak<reducedmap.get(paper).get(i))
					highpeak=reducedmap.get(paper).get(i);
			}
			
			ArrayList<Integer> peakyear = new ArrayList<Integer>();
			int last=-3;
			for(int i=firstyear;i<=lastyear;i++){
				if((float)reducedmap.get(paper).get(i)/highpeak >= PEAK && (i-last)>2){
					peakyear.add(i);
					last=i;
				}
			}

			if(peakyear.size()>1){
				peakTimeMul.add(pt);
				countPeakMul++;
			}
			else if(peakyear.size()==1 && (peakyear.get(0)-firstyear)<= WINDOW && peakyear.get(0)==firstyear)
				countMonDec++;
			else if(peakyear.size()==1 && (peakyear.get(0)-firstyear)<= WINDOW && peakyear.get(0)!=firstyear)
				countPeakInt++;
			else if(peakyear.size()==1 && (peakyear.get(0)-firstyear)> WINDOW && peakyear.get(0)==lastyear)
				countMonIncr++;
			else if(peakyear.size()==1 && (peakyear.get(0)-firstyear)> WINDOW && peakyear.get(0)<lastyear){
				peakTimeLate.add(pt);
				countPeakLate++;
			}
		}

		System.out.println(Double.toString(100*(countPeakInt+countMonDec)/(double)(countGood)));
		System.out.println(Double.toString(100*countPeakLate/(double)(countGood)));
		System.out.println(Double.toString(100*countPeakMul/(double)(countGood)));
		System.out.println(Double.toString(100*countMonIncr/(double)(countGood)));
		System.out.println(Double.toString(100*countOTH/(double)(countGood)));
	}
}
