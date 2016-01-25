/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package em_nonparam_pricing;

import static java.lang.Math.log;

/**
 *
 * @author feldman
 */
public class Algorithm {
    
    DataReader popInfo = new DataReader();
    Population pop = popInfo.read();
    int numCustomers = pop.getTotalNumCustomers();
    int T = pop.getT();
    double sumW;
    double[] theta = new double[numCustomers];
    double[] QDenom = new double[T];
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
            QDenom[t] = denom;
            

         }
    }
    
    public double CompleteLike(){
        double like=0;
        double QValue;
        for(int t=0 ; t < T ; t++){
            for(int i=0; i < numCustomers; i++){
                if(pop.getEntryC(t, i)){
                    QValue = theta[i]/QDenom[t];
                    like+=QValue*log(theta[i]/QValue);   
                }
            }

        }
        return like;
    }
    
    public void updateW(){
        for(int i=0; i < numCustomers; i++){
            double w=0;
            for(int t=0 ; t < T ; t++){
                if(pop.getEntryC(t, i)){
                    w+=theta[i]/QDenom[t];
                }
                
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
    
    public double IncompleteLike(){
        double like=0;
        for(int t=0 ; t < T ; t++){
            double probArrival = pop.calcDenomEStep(t,theta); 
            like+=log(probArrival);
        
        }
        return like;
    
    }
    
    public double[] getTheta(){
    
        return theta;
    }
    
  
    
}
