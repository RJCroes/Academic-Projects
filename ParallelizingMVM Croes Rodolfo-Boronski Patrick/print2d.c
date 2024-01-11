#include <stdlib.h>
#include <stdio.h>
#include "utilities.h"
/*
 * Created by Patrick Boronski for CSCI 473
 * Note: I have changed the order of j and i because I'm not coding in fortran and it was bugging me.
 * */

int main(int argc, char **argv)
{
	int imax, jmax;
    	double **a;
 	FILE *fp;
	char *pname;
	char fileName[10];
	
	if(argc == 2){
		pname = argv[1];
		sprintf(fileName, "%s", pname);
	}
	else{
		printf("Usage: ./print2d <fileName>");
		exit(1);
	}
	
	fp = fopen(fileName, "rb");	
	
	fread(&imax, sizeof(int), 1, fp);
	fread(&jmax, sizeof(int), 1, fp);
	
	malloc2D(&a, imax,jmax);
	
	fread(a[0], sizeof(double), (imax*jmax), fp);	
	
    	print2D(a, imax, jmax);
	exit(0);
}
