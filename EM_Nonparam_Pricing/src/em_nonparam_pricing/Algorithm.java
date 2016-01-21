/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package em_nonparam_pricing;

/**
 *
 * @author feldman
 */
public class Algorithm {
    
    DataReader popInfo = new DataReader();
    Population pop = popInfo.read();
    int numCustomers = pop.getTotalNumCustomers();
    int T = pop.getTotalNumCustomers();
    double sumW;
    double[] theta = new double[numCustomers];
    double[][] Q = new double[T][numCustomers];
    double[] W = new double[numCustomers];
    
    public Algorithm(){
        /*Initialize the EM ALgorithm*/
        int totalSumC = pop.getSumFullC();
        for(int i=0; i<numCustomers ; i++){
        
            int sumColumnC= pop.getSumColumnC(i);
            theta[i] = (double) sumColumnC/totalSumC;
        }
    }
    
    public void EStep(){
        for(int t=0 ; t < T ; t++){
            
            double denom = pop.calcDenomEStep(t,theta); 
            for(int i=0; i < numCustomers; i++){
                
                Q[t][i]=theta[i]/denom;                
            }
         }
    }
    
    public void updateW(){
        for(int i=0; i < numCustomers; i++){
            double w=0;
            for(int t=0 ; t < T ; t++){
                w+=Q[t][i];
            
            }
            W[i]=w;
        }
    
    }
    
    public void updateSumW(){
        
        sumW=0;
        for(int i=0; i < numCustomers; i++){
            sumW+=W[i];
        }
    
    }
    

    public void MStep(){
   
        for(int i=0; i < numCustomers; i++){
            theta[i] = W[i]/sumW;
        }
    
    }
    
    
    
    
    
}
