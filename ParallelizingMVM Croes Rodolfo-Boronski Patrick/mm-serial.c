/*
 * Created by Patrick Boronski
 * The program will accept three file names from the command line
 * A - the first input matrix
 * B - the second input matrix
 * C - the output matrix
 * it will multiply A and B and write the result to C.
 * If DEBUG is defined, the program will also print A B and C to the screen after multiplying
 * */
#include <stdio.h>
#include <stdlib.h>
#include "utilities.h"
#include "timer.h"

int main(int argc, char **argv){
	char *aFile, *bFile, *cFile; //File names
	if(argc == 4){
		aFile = argv[1];
		bFile = argv[2];
		cFile = argv[3];
	}
	else{
		printf("Usage: ./mm-serial <input_file_a> <input_file_b> <output_file>\n");
		exit(1);
	}

	double **a, **b, **c, sum = 0; //Matrices and sum variable
	double start_time, end_time, elapsed_time;
	int aRows, aCols, bRows, bCols, cRows, cCols; //Row/Collumn info for matrices
	FILE *afp, *bfp, *cfp; //File pointers for reading/writing
	
	//Open files
	afp = fopen(aFile, "rb"); 
	bfp = fopen(bFile, "rb");
	cfp = fopen(cFile, "wb");
		
	//Read input matrices' dimensions
	//Matrix a
	fread(&aRows, sizeof(int), 1, afp);
	fread(&aCols, sizeof(int), 1, afp);
	
	//Matrix b
	fread(&bRows, sizeof(int), 1, bfp);
	fread(&bCols, sizeof(int), 1, bfp);

	//Set dimensions for output matrix
	cRows = aRows;
	cCols = bCols;
	
	//Check compatibility
	if(aCols != bRows){
		printf("ERROR: Incompatible matrices. Cannot multiply.\n");
		exit(1);
	}
	
	//Malloc arrays
	malloc2D(&a, aRows, aCols);
	malloc2D(&b, bRows, bCols);
	malloc2D(&c, cRows, cCols);
	
	//Read data into input matrices
	//Matrix a
	fread(a[0], sizeof(double), (aRows*aCols), afp);
	
	//Matrix b
	fread(b[0], sizeof(double), (bRows*bCols), bfp);

	GET_TIME(start_time);
	//Multiply matrices
	for(int i=0; i<aRows; i++){
		for(int j=0; j<bCols; j++){
			for(int k=0; k<bRows; k++){
				sum += a[i][k] * b[k][j];
			}
			c[i][j] = sum;
			sum = 0;
		}
	}
	GET_TIME(end_time);
	
	elapsed_time = end_time - start_time;
	printf("Computation time: %lf\n", elapsed_time);

#ifdef DEBUG
	printf("A:\n");
	print2D(a, aRows, aCols);
	printf("\nB:\n");
	print2D(b, bRows, bCols);
	printf("\nC:\n");
	print2D(c, cRows, cCols);
#endif
	//Write result to output file
	fwrite(&cRows, sizeof(int), 1, cfp);
	fwrite(&cCols, sizeof(int), 1, cfp);
	fwrite(c[0], sizeof(double), (cRows*cCols), cfp);
	//Free malloc'd addresses
	free(a);
	free(b);
	free(c);
}
