/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package em_nonparam_pricing;

import java.io.FileWriter;
import java.io.IOException;
import static java.lang.Math.log;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;

/**
 *
 * @author feldman
 */
public class Algorithm {
    
    DataReader popInfo;
    Population pop ;
    int numCustomers;
    int Ttotal;
    double trainPercentage =0.75;
    int T;
    int numProds;
    int numPrices;
    double sumW;
    double[] theta;
    double[] QDenom ;
    double[] W;
    String COMMA_DELIMITER = ",";
    String NEW_LINE_SEPARATOR = "\n";
    
    public Algorithm(int step){
        /*Initialize the EM ALgorithm*/
        popInfo = new DataReader();
        pop = popInfo.read(step);
        numCustomers = pop.getTotalNumCustomers();
        Ttotal = pop.getT();
        numProds = pop.getNumProds();
        numPrices = pop.getnumPrices();
        T = (int) (Ttotal*trainPercentage);
        System.out.println(T);
        theta = new double[numCustomers];
        QDenom = new double[T];
        W = new double[numCustomers];
        
        
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
    
    public double IncompleteLikeTest(){
        double like=0;
        for(int t=T ; t < Ttotal ; t++){
            
            double probArrival = pop.calcDenomEStep(t,theta);
            like+=log(probArrival);
        
        }
        return like;
    
    }
    
    public void writeModel(int step){
        
        
        FileWriter fileWriter = null;


        try{
            fileWriter = new FileWriter("../Create_Data/Fitted_Interval_Models/IntervalModel" + step +".csv");
            
            fileWriter.append(String.valueOf(numProds));
            fileWriter.append(COMMA_DELIMITER);
            fileWriter.append(String.valueOf(numPrices));
            fileWriter.append(COMMA_DELIMITER);
            fileWriter.append(NEW_LINE_SEPARATOR);
            for(int p=0; p < numPrices; p++){
                fileWriter.append(String.valueOf(p*step));
                fileWriter.append(NEW_LINE_SEPARATOR);
            
            }
            ArrayList<Customer> customerList = pop.getCustomerList();
            for(int i=0; i<numCustomers ; i++){
                Customer cust = customerList.get(i);
                int[] prefList = cust.getPrefList();
                double budget = cust.getBudget();
                fileWriter.append(String.valueOf(prefList[0]));
                fileWriter.append(COMMA_DELIMITER);
                fileWriter.append(String.valueOf(prefList[1]));
                fileWriter.append(COMMA_DELIMITER);
                fileWriter.append(String.valueOf(budget/step));
                fileWriter.append(COMMA_DELIMITER);
                fileWriter.append(String.valueOf(theta[i]));
                fileWriter.append(NEW_LINE_SEPARATOR);



            }

        }catch ( Exception e )
            {
                System.out.println(e.getMessage());
            }finally {
              try {

                    fileWriter.flush();

                    fileWriter.close();

                } catch (IOException e) {

                    System.out.println("Error while flushing/closing fileWriter !!!");

                    e.printStackTrace();

                }

            }


        
       
    }
    
  
    
}
