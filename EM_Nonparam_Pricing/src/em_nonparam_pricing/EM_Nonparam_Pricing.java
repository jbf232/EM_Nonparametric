/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package em_nonparam_pricing;

import java.util.Arrays;

/**
 *
 * @author feldman
 */
public class EM_Nonparam_Pricing {

    
    
    public static void main(String[] args) {
        double numItersEM = 200;
        double currentLike;
        double pastLike=-10000000;
        double likeDiff;
        double compLike;
        double testLike;
        int[] priceSteps ={5,2,1};
        
        for(int j =0; j < priceSteps.length; j++){
            int step = priceSteps[j];
            Algorithm Alg=new Algorithm(step);
            currentLike = Alg.IncompleteLike();
            //System.out.println("I: " + currentLike);
            likeDiff = currentLike -pastLike;
            for(int i=0; i <numItersEM ; i ++){
               
                pastLike = currentLike;
                Alg.EStep();
                //compLike =Alg.CompleteLike();
                //System.out.println("C: " + compLike);
                Alg.updateW();
                Alg.updateSumW();
                Alg.MStep();
                currentLike = Alg.IncompleteLike();
                System.out.println(currentLike + " " + i);
                likeDiff = currentLike - pastLike;

            }
            System.out.println("I: " + currentLike);
            testLike = Alg.IncompleteLikeTest();
            System.out.println("Test: " + testLike);
            Alg.writeModel(step);

        
        }
       
    }
    
}
