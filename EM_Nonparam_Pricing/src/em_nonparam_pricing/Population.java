/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package em_nonparam_pricing;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

/**
 *
 * @author feldman
 */
public class Population {
    
    int minTime;
    int maxTime;
    int numPrices;
    int T;
    int totalNumCustomers;
    double[] priceList;
    ArrayList<Customer>  customerList= new ArrayList<Customer>();
    boolean[][] C;
    
    public Population(int minTime_, int maxTime_, int numPrices_, int T_, double[] priceList_ ){
        /* 
        Assuming here are that times are integers and that we consider all the customer types
        */
        minTime = minTime_;
        maxTime = maxTime_;
        numPrices = numPrices_;
        T=T_;
        int diff = maxTime-minTime;
        totalNumCustomers = ((diff*(diff-1))/2)* numPrices;
        priceList = priceList_ ;
        C=new boolean[T][totalNumCustomers];

    

    }
    
    

    public int getTotalNumCustomers(){
    
        return totalNumCustomers;
    
    }
    
    public void createPopulation(){

        for (int i =minTime; i <= maxTime; i++ ){
        
            for (int j = i+1 ; j <=maxTime; j++){
            
                for(int p=0; p <numPrices; p ++){
                
                    Customer cust = new Customer(i, j,  priceList[p]);
                    customerList.add(cust);

                }

            }
   
        }

    }
    
    
    public void setC(int t, ArrayList<Integer> offerTimes, ArrayList<Double> offerPrices, int purchased){
        
        for(int i =0 ; i < totalNumCustomers ; i ++){
        
            Customer current = customerList.get(i);
            int wouldBuy = current.getPurchased(offerTimes, offerPrices);
            if (wouldBuy == purchased){
            
                C[t][i]=true;
            
            }else{
                C[t][i] = false;
            
            }
            
        
        }

    }
    
    
}
