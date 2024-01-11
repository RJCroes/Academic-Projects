CC=gcc
CFLAGS=-g -Wall -fno-stack-protector -Wstrict-prototypes -std=gnu99
LFLAGS=-lm -lpthread

all:	mm-serial make-2d print-2d pth_mat_vect_rand_split

mm-serial:	utilities.o mm-serial.o
	$(CC) -o mm-serial utilities.o mm-serial.o $(LFLAGS)

make-2d:	utilities.o make-2d.o
	$(CC) -o make-2d utilities.o make-2d.o $(LFLAGS)

print-2d:	utilities.o print2d.o
	$(CC) -o print-2d utilities.o print2d.o $(LFLAGS)

pth_mat_vect_rand_split:	pth_mat_vect_rand_split.o
	$(CC) -o pth_mat_vect_rand_split pth_mat_vect_rand_split.o $(LFLAGS)

utilities.o: utilities.c utilities.h
	$(CC) $(CFLAGS) -c utilities.c

mm-serial.o: mm-serial.c utilities.h
	$(CC) $(CFLAGS) -c mm-serial.c

make-2d.o: make-2d.c utilities.h
	$(CC) $(CFLAGS) -c make-2d.c

print2d.o: print2d.c utilities.h
	$(CC) $(CFLAGS) -c print2d.c

pth_mat_vect_rand_split.o:
	$(CC) $(CFLAGS) -c pth_mat_vect_rand_split.c

clean:
	rm -f *.o core* test* mm-serial make-2d print-2d pth_mat_vect_rand_split

clearData:
	rm -f *.dat
