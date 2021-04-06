//js中有类似python中print的打印函数，使用方法雷同。
console.log("1 Hello World");           //（久经不衰的"Hello World"）
console.log('2 Hello World');           //js不区分双引号和单引号，所以二者作用一致
console.log('3 Hello World')            //好像没有分号也可以（习惯还是加上吧）

//同样有“格式化字符串”的类似概念。
const place = "World";                  //创建常量字符串，关键字“const”和C语言中的类似
const greeting = "Hello";
console.log('4 %s,%s',greeting,place);  
console.log("5 %s,%s",greeting,place);  //单双引号无区别
/* 
    console.log()可以通过一些特有的占位符进行信息的加工输出，当然你只要粗略的了解一下即可
    %s：字符串
    %d：整数
    %i：整数
    %f：浮点数
    %o：obj对象
    %O：obj对象
    %c：CSS样式
*/

//还有一个和python中类似的用法
//对照pyhton的使用方法：使用双引号和加了前缀f；
//而js使用的是反单引号（在键盘左上角，数字1左边）和前缀$。
//print(f"6 {greeting} {place}");
console.log(`6 ${greeting} ${place}`);  //注意是反单引号

