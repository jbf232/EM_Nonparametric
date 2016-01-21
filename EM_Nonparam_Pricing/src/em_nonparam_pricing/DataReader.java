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
    
    File salesDataFile;
    File customerDataFile;
    String dels = ",";

    
    
    public DataReader ( File salesDataFile_, File customerDataFile_ )
    {
       salesDataFile = salesDataFile_;
       customerDataFile=customerDataFile_;
    }
    
    
    public Population read()
    {
        try
        {
            BufferedReader burr = new BufferedReader( new InputStreamReader ( new FileInputStream ( customerDataFile ) ) );
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
            
            System.out.println(numPrices);
            
            Population newPop = new Population(minTime, maxTime, numPrices, T, listPrices);
            newPop.createPopulation();
            
            
            burr = new BufferedReader( new InputStreamReader ( new FileInputStream ( salesDataFile ) ) );
            
            for (int t=0 ; t < T ; t++){
                ArrayList<Integer> offerTimes= new ArrayList<Integer>();
                ArrayList<Double> offerPrices= new ArrayList<Double>();
                for(int i =0; i <3 ; i++){
                    
                    line = burr.readLine();
                    stt = new StringTokenizer( line, dels );
                
                }
                
            
            }
      
            
           
            
            
            
            
            return newPop;

                
          
            
            
        }
        catch ( IOException e )
        {
            throw new Error ( e.getClass() + " " + e.getMessage() );
        }
        
        
    }
    

    
    
    public static void main ( String[] args )
    {
        File customerDataFile = new File ( "../Create_Data/CustomerData.csv" );
        File salesDataFile=new File ( "../Create_Data/SalesData.csv");
        DataReader reader = new DataReader( salesDataFile, customerDataFile );
        reader.read();
    }
    
}

    

