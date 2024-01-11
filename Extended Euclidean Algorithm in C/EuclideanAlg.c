/*************************************************************
 * EuclideanAlg.c - program that calculates the gcd, checks for relative prime, and solve ax = congr b (mod n)              *
 *                                                                            *
 * Name: Rodolfo Ofo Croes                                             *
 * Assignment: ExtendedEuclideanAlg                   *
 * Email: rjcroes@coastal.edu                                   *
 * Date: 10/14/2020
 * Class: MATH408 - Cryptography                                                  *
 **************************************************************/
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "EuclideanAlg.h"

//Driver
int main(int argc, char *argv[]) {
    int isDone = 0;
    
    //variables
    int a, b, n, g, x, invA, invB, gap, size, a1, b1, n1, g1, invA1, invB1, oldn;
    do{
        char line[256];
        /* Prompt user to enter digits */
        printf("Enter 3 integers separated by spaces in the order: a b n where ax is equivalent to congruent b mod n\n or enter anything else to quit:\n");
        if(fgets(line, sizeof(line), stdin)) {
            if(3 == sscanf(line, "%d %d %d", &a, &b, &n)) { //take in input
                //error handling
                if(a < 1 || b < 1|| n < 1){
                    printf("One of the numbers that you entered was less than 1. Please try again");
                }
            }else{
                break;
            }
        }
        //print out what we are solving for
        printf("solving for x where %dx is equivalent to congruent %d mod %d\n", a, b, n);
        //calculate gcd of a and n
        
        g = gcd(n, a);
        //calculate the gap between each unique answer
        gap = n / g;
        //define amount of x's
        size = g;

        //check whether gcd(a,n) divides b, if it does not, there is no solution.
        if(b % g != 0) {
            printf("%d does not divide %d, so there is no solution.\n", g, b);
        //if gcd(a,n) = 1, use extended algorithm on a and n to get inverse of a
        }else if(g == 1) {
            g = gcdExtended(a, n, &invA, &invB);
            printf("inverse of %d in mod %d = %d \n", a, n, invA);
        //if gcd(a,n) > 1, divide a, b and n by g to get new values of a, b and n.
        }else if(g != 1) {
            g = gcdPrint(n, a);
            printf("gcd(%d, %d) = %d \n", a, n, g);
            a1 = a / g;
            b1 = b / g;
            n1 = n / g;
            //apply extended algorithm to get inverse of the new a
            g1 = gcdExtended(a1, n1, &invA1, &invB1);

            printf("gcd(%d, %d) = %d \n", a1, n1, g1);

            printf("inverse of %d in mod %d = %d \n", a1, n1, invA1);

            invA = invA1;
            oldn = n;
            n = n1;
        }

        if(b%g == 0){
            //case 1: 1-to-many solutions

            x = (invA * b)%n;
            //make first value of x positive if it isn't
            if(x < 0){
                x = x + n;
            }
            //set the n to the original value if it has been previously changed
            if(g > 1) {
                n = oldn;
            }
            //place to store all values of x
            int manyx[size];
            int i = 0;
            int k = size-1;
            //assign first value of x to first value in array
            manyx[i] = x;
            //add the gap to x, place x in array until all the space of the array is taken
            do{
                k--;
                i++;
                x = x + gap;
                manyx[i] = x;
            }while(k >= 0);
            //print out x('s)
            printf("x = %d", manyx[0]);
            for(int j = 1; j < size; j++){
                printf(", %d", manyx[j]);
            }
    
            printf("(mod %d) \n", n);
        }

    }while(isDone == 0);

    return 0;
}

//Functions
/*------------------------------------------------------------------
 * Function:  gcdExtended
 * Purpose:   given two numbers and two adresses, calculate gcd and return result of gcd and the multiplicative inverses, 
 *            as wel as print out the steps for the gcd and their multiplicative inverses. 
 * In arg :   a, b, *x, *y
 */
int gcdExtended(int a, int b, int *x, int *y) {
    if (a == 0) { 
        *x = 0; 
        *y = 1; 
        return b; 
    } 
    int b1 = b%a;
    int a1 = floor(b/a);
    int x1, y1;
    printf("%d = %.0d(%d) + %d\n", b, a1, a, b1);
    int gcd = gcdExtended(b1, a, &x1, &y1); 
  
    *x = y1 - ((b/a) * x1); 
    *y = x1;
    printf("%d = (%d)%d + (%d)%d\n", gcd, *y, b, *x, a);

    return gcd; 
} /* gcdExtended */
/*------------------------------------------------------------------
 * Function:  gcd
 * Purpose:   given two numbers, calculate gcd and return result of gcd 
 * In arg :   a, b
 */
int gcd(int a, int b) {
    if(a%b == 0) {
        return b;
    }
    int gcdE = gcd(b, a%b);
    return gcdE;
}/* gcd */
/*------------------------------------------------------------------
 * Function:  gcd
 * Purpose:   given two numbers, calculate gcd and prints out the steps for doing so 
 * In arg :   a, b
 */
int gcdPrint(int a, int b) {
    printf("%d = %.0f(%d) + %d\n", a, floor(a/b), b, a%b);
    if(a%b == 0) {
        return b;
    }
    int gcdE = gcdPrint(b, a%b);
    return gcdE;
}/* gcdPrint */