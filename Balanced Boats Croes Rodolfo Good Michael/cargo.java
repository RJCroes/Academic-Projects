/**
 * 
 */

/**
 * @author Rodolfo Croes & Michael Good
 *
 */
public class cargo {
    // variables
    private int weight;
    private double distance;
    private double moment;

    // constructors
    public cargo() {

    }

    public cargo(int weight, double distance) {
        this.weight = weight;
        this.distance = distance;
        this.moment = weight * distance;
    }

    public cargo(int weight, double distance, double moment) {
        this.weight = weight;
        this.distance = distance;
        this.moment = moment;
    }

    // accessors
    public double getMoment() {
        return moment;
    }

    public int getWeight() {
        return weight;
    }

}