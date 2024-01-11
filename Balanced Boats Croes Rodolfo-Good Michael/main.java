import java.util.InputMismatchException;
import java.util.Scanner;

/**
 * @author Rodolfo Croes & Michael Good
 *
 */
public class main {

	/**
	 * @param args cannot be null
	 */
	public static void main(String[] args) {
		System.out.println("Hello! Welcome to our balance boat! These are your captains speaking, Ofo & Michael!");
		boolean isFinished = false;
		Scanner scanner = new Scanner(System.in);
		do {
			// variables
			int n = 0;
			String input = "";

			do {

				System.out.println(
						"Please enter the size of the n by n boat that needs balancing(n >= 4 and if n > 11 it will not be printed): ");
				try {
					n = scanner.nextInt();
				} catch (InputMismatchException e) {
					System.out.println("You inputed something other than a number matey...");
					break;

				}
				if (n <= 3) {
					System.out.println("That value is too small sailor, try making it larger than 3");
				}
			} while (n < 4);

			if (n >= 4) {
				try {
					boat theBoat = new boat(n);

					// theBoat.zero();

					theBoat.balance();

					if (n <= 11) {
						theBoat.printBoat();
					}

					theBoat.isBalanced();
				} catch (OutOfMemoryError e1) {
					System.out.println("Your machine be too weak for this boat matey..");

				}
			}
			scanner.nextLine();
			do {
				System.out.println(
						"Nice Boat! You wanna make another one? Type Y to make another one, Type N if you're done. \n");
				input = scanner.next();
				if (input.equals("N")) {
					isFinished = true;
				} else if (input.equals("Y")) {
					isFinished = false;
				} else {
					System.out.println("This input is not accepted matey, let's try again.");
				}
			} while (!input.equals("Y") && !input.equals("N"));

		} while (isFinished == false);

		System.out.println("We hope you enjoyed sailing with us. So long partner!");

		scanner.close();
	}

}
// am i main
// camelCsase
// snake_case
// camel_Snake_Case
