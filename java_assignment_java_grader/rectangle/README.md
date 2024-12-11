# Rectangle (Java)

[< Home](../../README.md)

Write a Java class Rectangle that takes in two integers, width and height, and has a methods `getArea` and `getPerimeter` that return the area and perimeter of the rectangle respectively.


### Examples

```java
new Rectangle(2, 3).getArea(); // 6
new Rectangle(5, 8).getPerimeter(); // 26
```


### Grade command

This is the command to set up the grader in RamDesk.

```bash
mv {{submission.file_path}} . && javac *.java && java Tester || echo  "Compilation failure\n0"
```
