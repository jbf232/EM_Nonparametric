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
public class EM_Nonparam_Pricing {

    
    
    public static void main(String[] args) {
        double tol = 0.001;
        double currentLike;
        double pastLike=-10000000;
        double likeDiff;
        double compLike;
        
        Algorithm Alg=new Algorithm();
        currentLike = Alg.IncompleteLike();
        likeDiff = currentLike -pastLike;
        while(likeDiff > tol){
        
            pastLike = currentLike;
            Alg.EStep();
            compLike =Alg.CompleteLike();
            System.out.println("Complete Likelihood: " + compLike);
            Alg.updateW();
            Alg.updateSumW();
            Alg.MStep();
            currentLike = Alg.IncompleteLike();
            System.out.println("Incomplete Likelihood: " + currentLike);
            likeDiff = currentLike - pastLike;
        
        }
        
        
       
    }
    
}
