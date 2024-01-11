#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "utilities.h"

void malloc2D(double***a , int imax, int jmax)
{
   // first allocate a block of memory for the row pointers and the 2D array
   double **x = (double **)malloc(imax*sizeof(double *) + imax*jmax*sizeof(double));

   // Now assign the start of the block of memory for the 2D array after the row pointers
   x[0] = (double *)x + imax;

   // Last, assign the memory location to point to for each row pointer
   for (int i = 1; i < imax; i++) {
      x[i] = x[i-1] + jmax;
   }

    *a = x;
}

void fill2D(double** a, int imax, int jmax) {
	int count = 0;
    	for(int i=0; i<imax; i++) {
        	for(int j=0; j<jmax; j++) {
            		a[i][j] = count;
            		count++;
        	}
    	}
}

void print2D(double** a, int imax, int jmax) {
    for(int i=0; i<imax; i++) {
        printf("%d |", i);
	for(int j=0; j<jmax; j++) {
            printf("%lf\t", a[i][j]);
        } printf("\n");
    }
}
void zeroFill(double **array, int rows, int cols){
	for(int i=0;i<rows;i++){
		for(int j=0;j<cols;j++){
			array[i][j] = 0;
		}
	}
}
void wallFill(double **array, int rows, int cols){
	for(int i=0;i<rows;i++){
		array[i][0] = 1;
		array[i][cols - 1] = 1;
	}
}
void randFill(double **array, int rows, int cols){
	srand48((unsigned int) time(NULL));
	for(int i=0; i<rows; i++){
		for(int j=0; j<cols; j++){
			array[i][j] = drand48();
		}
	}
}
void swapPointers(double ***array1, double ***array2){
	double **temp = *array1;
	*array1 = *array2;
	*array2 = temp;	
}
void applyStencil(double **start, double **stencil, int rows, int cols){
	for(int i=0;i<rows;i++){ 
		for(int j=0;j<cols;j++){
			stencil[0][j] = start[0][j]; //copy over the top and bottom most rows from the original matrix
			stencil[rows - 1][j] = start[rows - 1][j];
		}
		stencil[i][0] = start[i][0];//copy over the left and right most collumns from the original matrix
		stencil[i][cols - 1] = start[i][cols - 1];
	}
	for(int i=1;i<=rows - 2;i++){
		for(int j=1;j<=cols - 2;j++){
			stencil[i][j] = (start[i][j] + start[i][j-1] + start[i][j+1] + start[i-1][j] + start[i+1][j])/5;
		}
	}
}
