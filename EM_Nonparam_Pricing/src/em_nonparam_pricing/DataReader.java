/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package em_nonparam_pricing;

import java.io.*;
import java.util.*;

/**
 *
 * @author feldman
 */
public class DataReader {
    

    String dels = ",";

    
    public Population read(int step)
    {
        try
        {
            BufferedReader burr = new BufferedReader( new InputStreamReader ( new FileInputStream ( "../Create_Data/Real_Data/CustomerData" + step +".csv" ) ) );
            String line = burr.readLine();
            StringTokenizer stt = new StringTokenizer( line, dels );
            int T = Integer.parseInt( stt.nextToken() );
            line = burr.readLine();
            stt = new StringTokenizer( line, dels );
            int minTime = Integer.parseInt( stt.nextToken() );
            line = burr.readLine();
            stt = new StringTokenizer( line, dels );
            int maxTime = Integer.parseInt( stt.nextToken() );
            line = burr.readLine();
            stt = new StringTokenizer( line, dels );
            int numPrices = Integer.parseInt( stt.nextToken() );
            line = burr.readLine();
            stt = new StringTokenizer( line, dels );
            double[] listPrices = new double[numPrices];
            for(int i =0 ; i < numPrices ; i++){
            
                listPrices[i] = Double.parseDouble( stt.nextToken() );
            }
            
            
            Population newPop = new Population(minTime, maxTime, numPrices, T, listPrices);
            newPop.createPopulation();
            
            
            burr = new BufferedReader( new InputStreamReader ( new FileInputStream ( "../Create_Data//Real_Data/SalesData.csv" ) ) );
            
            for (int t=0 ; t < T ; t++){
                
                ArrayList<Integer> offerTimes= new ArrayList<Integer>();
                ArrayList<Double> offerPrices= new ArrayList<Double>();
                line = burr.readLine();
                stt = new StringTokenizer( line, dels );
                int numOffered = Integer.parseInt( stt.nextToken() );
                line = burr.readLine();
                stt = new StringTokenizer( line, dels );
                for (int j=0;  j < numOffered; j ++){
                    offerTimes.add(Integer.parseInt( stt.nextToken() ));
                }
                line = burr.readLine();
                stt = new StringTokenizer( line, dels );
                for (int j=0;  j < numOffered; j ++){
                    offerPrices.add(Double.parseDouble( stt.nextToken() ));
                }
                line = burr.readLine();
                stt = new StringTokenizer( line, dels );
                int purchased = Integer.parseInt( stt.nextToken() );
                newPop.setC(t, offerTimes, offerPrices, purchased);
                

            }
            System.out.println("Done Reading Data");
            return newPop;

                
          
            
            
        }
        catch ( IOException e )
        {
            throw new Error ( e.getClass() + " " + e.getMessage() );
        }
        
        
    }
    
    public static void main(String[] args) {
    
        
        
    }
    

    
 
    
}

    

