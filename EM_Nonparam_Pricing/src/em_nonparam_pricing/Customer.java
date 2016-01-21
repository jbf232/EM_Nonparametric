/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package em_nonparam_pricing;

import java.util.ArrayList;
import java.util.Arrays;

/**
 *
 * @author feldman
 */
public class Customer {
    
    int[] prefList = new int[2];
    double budget;
    int step = 1;
    
    
    public Customer(int low, int high ,  double budget_){
        
        prefList[0] = low;
        prefList[1] = high;
        budget = budget_;
    
    }
    
    public int[] getPrefList(){
    
        return prefList;
    }
    
    public double getBudget(){
    
        return budget;
    }
    
    public int getPurchased(ArrayList<Integer> offerTimes, ArrayList<Double> offerPrices){
    
        int numOffered = offerTimes.size();
        int countProds=0;
        for(int i  = prefList[0]; i <= prefList[1]; i+=step){
        
            if (offerTimes.contains(i)){
                
                double priceCharged = offerPrices.get(countProds);
                
                if(priceCharged <= budget){
                
                    return i;                
                }
            } 
            countProds++;
        }
        return 0;

    }
   
    
}
