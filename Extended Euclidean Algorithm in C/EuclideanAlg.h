/**********************************************************************
 * EuclideanAlg.h - header file for EuclideanAlg.c
 *
 * Name: Rodolfo Ofo Croes                                             *
 * Assignment: ExtendedEuclideanAlg                   *
 * Email: rjcroes@coastal.edu                                   *
 * Date: 10/14/2020
 * Class: MATH408 - Cryptography                                            *
 **************************************************************/

#ifndef EUCLIDEANALG_H_
#define EUCLIDEANALG_H_
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

//functions defined

int gcd(int a, int b);

int gcdPrint(int a, int b);

int gcdExtended(int a, int b, int *x, int *y);

#endif /* EUCLIDEANALG_H_ */