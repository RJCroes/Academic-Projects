
/**
 * Small Project
 * Bank class that contains the main method of the program.
 * 
 *
 * @author Rodolfo Croes
 * @version 1.0
 */
import java.util.Scanner;
import java.util.HashMap;
import java.util.Map;

public class Bank
{
    // global variables
    private static Map<String, CustomerAccount> accounts = new HashMap<>();
    private static Scanner scanner = new Scanner(System.in);
    /**
     * main: function that handles the main components of the Bank system
     * 
     * @param args String argument to take in input from command line
     */
    public static void main(String[] args) {
        int choice;
        do {
            displayMenu();
            choice = scanner.nextInt();
            scanner.nextLine(); // Consume newline character
            handleChoice(choice);
        } while (choice != 5);
    }
    /**
     * displayMenu: function that displays the main menu of options to choose
     */
    private static void displayMenu() {
        System.out.println("\nWelcome to Basics Bank. Please choose one of the following:");
        System.out.println("1. Create Account");
        System.out.println("2. Login to Account");
        System.out.println("3. Check Balance");
        System.out.println("4. Deposit/Withdraw");
        System.out.println("5. Exit");
        System.out.print("Enter your choice: ");
    }
    /**
     * handleChoice: function that handles what should be done given the user's
     * input from the main menu
     * 
     * @param choice - the inputted choice from the user when viewing the main menu
     */
    private static void handleChoice(int choice) {
        switch (choice) {
            case 1:
                createAccount();
                break;
            case 2:
                loginAccount();
                break;
            case 3:
                checkBalance();
                break;
            case 4:
                depositWithdraw();
                break;
            case 5:
                System.out.println("Thank you for using Basics Bank. Goodbye!");
                break;
            default:
                System.out.println("Invalid choice. Please try again.");
        }
    }
    /**
     * createAccount: Create a new bank account with user inputed bank number
     * and PIN number. If the number is not unique the account will not be
     * created.
     */
    private static void createAccount() {
        System.out.print("Enter account number: ");
        String accountNumber = scanner.nextLine();
        System.out.print("Enter PIN: ");
        String pin = scanner.nextLine();

        if (accounts.containsKey(accountNumber)) {
            System.out.println("Account number already exists.");
        } else {
            accounts.put(accountNumber, new CustomerAccount(pin));
            System.out.println("Account created successfully.");
        }
    }
    /**
     * loginAccount: function that attempts to login the user inputed account
     * number and PIN and checks if what is inputed is in the HashMap. If it
     * is not in the structure or the account number and PIN do not match then
     * it will not log in.
     * 
     */
    private static void loginAccount() {
        System.out.print("Enter account number: ");
        String accountNumber = scanner.nextLine();
        System.out.print("Enter PIN: ");
        String pin = scanner.nextLine();

        if (accounts.containsKey(accountNumber) && accounts.get(accountNumber).validatePin(pin)) {
            System.out.println("Login successful.");
            handleLoggedInAccount(accountNumber);
        } else {
            System.out.println("Invalid account number or PIN.");
        }
    }
    /**
     * handleLoggedInAccount: function that handles the menu when a user sucessfully
     * logs in. Displays an account menu and handles the transaction associated with
     * the choice made by the user
     * 
     * @param accountNumber - the account number that has been logged into.
     */
    private static void handleLoggedInAccount(String accountNumber) {
        int choice;
        do {
            System.out.println("\nAccount Menu:");
            System.out.println("1. Check Balance");
            System.out.println("2. Deposit");
            System.out.println("3. Withdraw");
            System.out.println("4. Logout");
            System.out.print("Enter your choice: ");
            choice = scanner.nextInt();
            scanner.nextLine(); // Consume newline character

            switch (choice) {
                case 1:
                    accounts.get(accountNumber).checkBalance();
                    break;
                case 2:
                    System.out.print("Enter deposit amount: ");
                    double depositAmount = scanner.nextDouble();
                    scanner.nextLine(); // Consume newline character
                    accounts.get(accountNumber).deposit(depositAmount);
                    break;
                case 3:
                    System.out.print("Enter withdrawal amount: ");
                    double withdrawalAmount = scanner.nextDouble();
                    scanner.nextLine(); // Consume newline character
                    accounts.get(accountNumber).withdraw(withdrawalAmount);
                    break;
                case 4:
                    System.out.println("Logged out of account.");
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        } while (choice != 4);
    }
    /**
     * checkBalance: function that logs into an account and checks the balance.
     * 
     */
    private static void checkBalance() {
        System.out.print("Enter account number: ");
        String accountNumber = scanner.nextLine();
        System.out.print("Enter PIN: ");
        String pin = scanner.nextLine();

        if (accounts.containsKey(accountNumber) && accounts.get(accountNumber).validatePin(pin)) {
            accounts.get(accountNumber).checkBalance();
        } else {
            System.out.println("Invalid account number or PIN.");
        }
    }
    /**
     * depositWithdraw: function that logs in a user and shows them a menu
     * to either deposit or withdraw money to or from their account.
     * Function also handles the input of the menu.
     *
     */
    private static void depositWithdraw() {
        System.out.print("Enter account number: ");
        String accountNumber = scanner.nextLine();
        System.out.print("Enter PIN: ");
        String pin = scanner.nextLine();

        if (accounts.containsKey(accountNumber) && accounts.get(accountNumber).validatePin(pin)) {
            int choice;
            do {
                System.out.println("\nDeposit/Withdraw Menu:");
                System.out.println("1. Deposit");
                System.out.println("2. Withdraw");
                System.out.println("3. Back");
                System.out.print("Enter your choice: ");
                choice = scanner.nextInt();
                scanner.nextLine(); // Consume newline character

                switch (choice) {
                    case 1:
                        System.out.print("Enter deposit amount: ");
                        double depositAmount = scanner.nextDouble();
                        scanner.nextLine(); // Consume newline character
                        accounts.get(accountNumber).deposit(depositAmount);
                        break;
                    case 2:
                        System.out.print("Enter withdrawal amount: ");
                        double withdrawalAmount = scanner.nextDouble();
                        scanner.nextLine(); // Consume newline character
                        accounts.get(accountNumber).withdraw(withdrawalAmount);
                        break;
                    case 3:
                        System.out.println("Returning to main menu.");
                        break;
                    default:
                        System.out.println("Invalid choice. Please try again.");
                }
            } while (choice != 3);
        } else {
            System.out.println("Invalid account number or PIN.");
        }
    }
}
