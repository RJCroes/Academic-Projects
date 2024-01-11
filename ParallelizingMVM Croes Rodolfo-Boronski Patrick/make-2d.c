#include <stdio.h>
#include <stdlib.h>
#include "utilities.h"

int main(int argc, char **argv){
	
	int rows, cols;
	char *fileName;	
	if(argc == 4){
		rows = atoi(argv[1]);
		cols = atoi(argv[2]);
		fileName = argv[3];
		if(rows <= 0 || cols <= 0){
			printf("ERROR: Rows and collumns must be positive and non-zero\n");
			exit(1);
		}
	//	printf("%d x %d matrix printed to %s\n", rows, cols, fileName);
	}
	else{
		printf("Usage: ./make-2d <rows> <cols> <output_file>\n");
		exit(1);
	}
	
	FILE *fp;
	double **a;

	fp = fopen(fileName, "wb");
	
	malloc2D(&a, rows, cols);
//	fill2D(a, rows, cols);
//	wallFill(a, rows, cols);
//	print2D(a, rows, cols);
	randFill(a, rows, cols);

	fwrite(&rows, sizeof(int), 1, fp);
	fwrite(&cols, sizeof(int), 1, fp);
	fwrite(a[0], sizeof(double), (rows*cols), fp);	

}
