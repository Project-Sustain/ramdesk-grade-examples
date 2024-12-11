public class Sum {
    public static int sum(int[] nums) {
        int total = 0;
        for (int num: nums) {
            total += num;
        }
        return total;
    }
    
    public static void main(String[] args) {
        int[] nums = new int[args.length];
        
        for (int i = 0; i < args.length; i++) {
            nums[i] = Integer.parseInt(args[i]);
        }
        
        System.out.println(
            sum(nums)
        );
    }
}
