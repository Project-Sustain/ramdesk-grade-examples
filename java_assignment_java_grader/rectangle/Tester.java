import java.util.Random;

public class Tester {
    public static void main(String[] args) {
        Random rand = new Random();
        int width = rand.nextInt(100) + 1;
        int height = rand.nextInt(100) + 1;
        int area = width * height;
        int perimeter = 2 * (width + height);
        Rectangle r = new Rectangle(width, height);
        if (r.getArea() == area && r.getPerimeter() == perimeter) {
            // Test passed: 10 points
            System.out.println("Test passed");
            System.out.println(10);
        } else {
            // Test failed: 0 points
            System.out.println("Test failed");
            System.out.println(0);
        }
    }
}
