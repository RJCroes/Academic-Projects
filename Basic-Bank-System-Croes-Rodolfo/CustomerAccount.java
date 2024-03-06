
/**
 * CustomerAccount - Account Class that has a PIN and a balance.
 * Account number is handled in main method class
 * @see Bank
 *
 * @author Rodolfo Croes
 * @version 1.0
 */
public class CustomerAccount
{
    // global variables
    private double balance;
    private String pin;
    /**
     * CustomerAccount: Constructor of a CustomerAccount object with default 
     * balance = 0.0
     * 
     * @param pin - user inputted PIN
     */
    public CustomerAccount(String pin) {
        this.pin = pin;
        balance = 0.0;
    }
    /**
     * validatePin: checks whether the entered PIN is equal to the saved PIN
     * 
     * @param enteredPin - user inputted PIN
     * @return True if the PIN entered matches the saved PIN
     */
    public boolean validatePin(String enteredPin) {
        return pin.equals(enteredPin);
    }
    /**
     * checkBalance: prints out the current balance of the account
     */
    public void checkBalance() {
        System.out.println("Current balance: $" + balance);
    }
    /**
     * deposit: updates the account with the amount deposited and prints the 
     * updated account
     * 
     * @param amount - the amount inputted to be deposited
     */
    public void deposit(double amount) {
        balance += amount;
        System.out.println("Deposit successful. New balance: $" + balance);
    }
    /**
     * withdraw: updates the account with the amount withdrawn if possible.
     * prints either insufficient funds or the new balance of the account.
     * 
     * @param amount - the amount inputted to be withdrawn
     */
    public void withdraw(double amount) {
        if (amount > balance) {
            System.out.println("Insufficient funds.");
        } else {
            balance -= amount;
            System.out.println("Withdrawal successful. New balance: $" + balance);
        }
        }
}
