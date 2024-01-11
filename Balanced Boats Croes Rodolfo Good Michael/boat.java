import java.lang.*;

/**
 * @author Rodolfo Croes & Michael Good
 *
 */
public class boat {
    // variables
    private int size;
    private int length;
    private boolean isEven; // false is odd and true is even
    private cargo[][] boatSquares;
    private double xTotalMoment;
    private double yTotalMoment;
    private double wiggleRoom;
    private double middle;

    // constructors
    public boat(int length) {
        this.size = length * length;
        this.length = length;
        this.middle = ((double) this.length - 1) / 2;
        if (this.length % 2 == 1) {
            isEven = false;
            this.wiggleRoom = 2.0;
        } else {
            isEven = true;
            this.wiggleRoom = 1.0;
        }
        boatSquares = new cargo[length][length];
        yTotalMoment = 0;
        xTotalMoment = 0;
    }

    // accessors
    public int getSize() {
        return this.size;

    }

    public int getLength() {
        return this.length;
    }

    // methods
    public void balance() {
        if (isEven) {
            // System.out.println("middle ="+middle);
            int oddI = 0;
            int oddJ = -1;
            int evenI = this.length - 1;
            int evenJ = this.length;

            int travel = this.length;

            int weightCounter = 1;
            double distance;
            double moment;

            while (true) {

                for (int w = 0; w < travel; w++) {
                    // System.out.println("1");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    oddJ++;
                    distance = distance(oddI, oddJ, middle);
                    moment = distance * weightCounter;
                    if (oddI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if (oddJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[oddI][oddJ] = new cargo(weightCounter, distance); // plus j odd
                    weightCounter++;
                    // System.out.println("2");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    evenJ--;
                    distance = distance(evenI, evenJ, middle);
                    moment = distance * weightCounter;
                    if (evenI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if (evenJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[evenI][evenJ] = new cargo(weightCounter, distance); // minus j even
                    weightCounter++;

                }
                if (weightCounter == this.size + 1)
                    break;
                travel = travel - 2;
                for (int x = 0; x < travel; x++) {
                    // System.out.println("3");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    oddI++;
                    distance = distance(oddI, oddJ, middle);
                    moment = distance * weightCounter;
                    if (oddI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if (oddJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[oddI][oddJ] = new cargo(weightCounter, distance); // plus i odd
                    weightCounter++;
                    // System.out.println("4");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    evenI--;
                    distance = distance(evenI, evenJ, middle);
                    moment = distance * weightCounter;
                    if (evenI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if (evenJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[evenI][evenJ] = new cargo(weightCounter, distance); // minus i even
                    weightCounter++;
                }
                if (weightCounter == this.size + 1)
                    break;

                for (int y = 0; y < travel; y++) {
                    // System.out.println("5");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    oddJ--;
                    distance = distance(oddI, oddJ, middle);
                    moment = distance * weightCounter;
                    if (oddI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if (oddJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[oddI][oddJ] = new cargo(weightCounter, distance); // minus j odd
                    weightCounter++;
                    // System.out.println("6");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    evenJ++;
                    distance = distance(evenI, evenJ, middle);
                    moment = distance * weightCounter;
                    if (evenI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if (evenJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[evenI][evenJ] = new cargo(weightCounter, distance); // plus j even
                    weightCounter++;

                }
                if (weightCounter == this.size + 1)
                    break;
                travel = travel - 2;
                for (int z = 0; z < travel; z++) {
                    // System.out.println("7");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    oddI--;
                    distance = distance(oddI, oddJ, middle);
                    moment = distance * weightCounter;
                    if (oddI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if (oddJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[oddI][oddJ] = new cargo(weightCounter, distance); // minus i odd
                    weightCounter++;
                    // System.out.println("8");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    evenI++;
                    distance = distance(evenI, evenJ, middle);
                    moment = distance * weightCounter;
                    if (evenI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if (evenJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[evenI][evenJ] = new cargo(weightCounter, distance); // plus i even
                    weightCounter++;
                }
                if (weightCounter == this.size + 1)
                    break;
            }

        } else {
            int oddI = 0;
            int oddJ = -1;
            int evenI = this.length - 1;
            int evenJ = this.length;

            int travel = this.length;

            int weightCounter = 1;
            double middle = (this.length - 1) / 2;
            double distance;
            double moment;

            while (true) {

                for (int w = 0; w < travel; w++) {
                    // System.out.println("1");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    oddJ++;
                    distance = distance(oddI, oddJ, middle);
                    moment = distance * weightCounter;
                    // System.out.println(moment);
                    if (oddI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else if (oddI < middle) {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if (oddJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else if (oddJ < middle) {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[oddI][oddJ] = new cargo(weightCounter, distance); // plus j odd
                    weightCounter++;
                    // System.out.println("2");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    evenJ--;
                    distance = distance(evenI, evenJ, middle);
                    moment = distance * weightCounter;
                    // System.out.println(moment);
                    if (evenI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else if (evenI < middle) {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if (evenJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else if (evenJ < middle) {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[evenI][evenJ] = new cargo(weightCounter, distance); // minus j even
                    weightCounter++;

                }
                if (weightCounter == this.size)
                    break;
                travel = travel - 2;
                for (int x = 0; x < travel; x++) {
                    // System.out.println("3");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    oddI++;
                    distance = distance(oddI, oddJ, middle);
                    moment = distance * weightCounter;
                    // System.out.println(moment);
                    if (oddI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else if (oddI < middle) {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if (oddJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else if (oddJ < middle) {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[oddI][oddJ] = new cargo(weightCounter, distance); // plus i odd
                    weightCounter++;
                    // System.out.println("4");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    evenI--;
                    distance = distance(evenI, evenJ, middle);
                    moment = distance * weightCounter;
                    // System.out.println(moment);
                    if (evenI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else if ((double) evenI < middle) {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if ((double) evenJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else if ((double) evenJ < middle) {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[evenI][evenJ] = new cargo(weightCounter, distance); // minus i even
                    weightCounter++;
                }
                if (weightCounter == this.size)
                    break;

                for (int y = 0; y < travel; y++) {
                    // System.out.println("5");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    oddJ--;
                    distance = distance(oddI, oddJ, middle);
                    moment = distance * weightCounter;
                    // System.out.println(moment);
                    if ((double) oddI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else if ((double) oddI < middle) {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if ((double) oddJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else if ((double) oddJ < middle) {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[oddI][oddJ] = new cargo(weightCounter, distance); // minus j odd
                    weightCounter++;
                    // System.out.println("6");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    evenJ++;
                    distance = distance(evenI, evenJ, middle);
                    moment = distance * weightCounter;
                    // System.out.println(moment);
                    if ((double) evenI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else if ((double) evenI < middle) {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if ((double) evenJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else if ((double) evenJ < middle) {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[evenI][evenJ] = new cargo(weightCounter, distance); // plus j even
                    weightCounter++;

                }
                if (weightCounter == this.size)
                    break;
                travel = travel - 2;
                for (int z = 0; z < travel; z++) {
                    // System.out.println("7");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    oddI--;
                    distance = distance(oddI, oddJ, middle);
                    moment = distance * weightCounter;
                    // System.out.println(moment);
                    if ((double) oddI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else if ((double) oddI < middle) {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if ((double) oddJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else if ((double) oddJ < middle) {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[oddI][oddJ] = new cargo(weightCounter, distance); // minus i odd
                    weightCounter++;
                    // System.out.println("8");
                    // System.out.println("The total moment on x = " + xTotalMoment);
                    // System.out.println("The total moment on y = " + yTotalMoment);
                    evenI++;
                    distance = distance(evenI, evenJ, middle);
                    moment = distance * weightCounter;
                    // System.out.println(moment);
                    if ((double) evenI > middle) {
                        xTotalMoment = xTotalMoment + moment;
                    } else if ((double) evenI < middle) {
                        xTotalMoment = xTotalMoment - moment;
                    }
                    if ((double) evenJ > middle) {
                        yTotalMoment = yTotalMoment + moment;
                    } else if ((double) evenJ < middle) {
                        yTotalMoment = yTotalMoment - moment;
                    }
                    boatSquares[evenI][evenJ] = new cargo(weightCounter, distance); // plus i even
                    weightCounter++;
                }
                if (weightCounter == this.size)
                    break;
            }

            boatSquares[(int) middle][(int) middle] = new cargo(weightCounter, 0); // centerweight has distance of 0

        }
    }

    public void isBalanced() {
        // System.out.println("The total moment on x/size = " +
        // Math.abs(xTotalMoment)/this.size);
        // System.out.println("The total moment on y/size = " +
        // Math.abs(yTotalMoment)/this.size);
        // System.out.println("The wiggie = " + wiggleRoom);
        if ((Math.abs(xTotalMoment) / this.size <= wiggleRoom) && (Math.abs(yTotalMoment) / this.size <= wiggleRoom)) {
            System.out.println("This boat is balanced!");
        } else {
            System.out.println("This boat is not balanced!");
        }
    }

    public void zero() {
        for (int i = 0; i <= this.length - 1; i++) {
            for (int j = 0; j <= this.length - 1; j++) {
                this.boatSquares[i][j] = new cargo(0, 1.0);
            }
        }
    }

    public void printBoat() {
        for (int i = 0; i <= this.length - 1; i++) {
            System.out.print("{ ");
            for (int j = 0; j <= this.length - 1; j++) {

                System.out.print(this.boatSquares[i][j].getWeight() + " ");
            }
            System.out.print("} \n");
        }
    }

    public double distance(int x, int y, double middle) {
        double xDistance = Math.abs(x - middle);
        double yDistance = Math.abs(y - middle);
        double distance = Math.sqrt(Math.pow(xDistance, 2) + Math.pow(yDistance, 2));
        return distance;
    }
}