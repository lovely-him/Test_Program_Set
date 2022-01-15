# JavaScript 入门笔记 - 上 - 基本语法

> 前言：
>
> 1. 本系列笔记是针对《[微软官方 JavaScript 入门教程【完结撒花】](https://www.bilibili.com/video/BV18a4y1L7kD)》教程编写，感谢小甲鱼组织的翻译和转载。我先边看视频边敲练习代码边写注释笔记，看完后才重新写博客汇总笔记。
>
> 2. 因为我已学过python和c语言，所以我在学js时总是类比三者的区别以加强记忆和学习。所以对于没学过python或c语言的，可能看不懂。我个人也比较推荐先学c语言或python，相对简单易懂，之后再扩展学其他语言。



# 一、JS是什么？能做什么？

- 我目前的认识是：`JavaScript`是一种编程语言，类似`Python`或`C语言`；它可用在浏览器网页中，可在网页运行时添加程序。

> 1. 对网页，我总结由三部分组成：数据（文字、图片或文件），布局（条条框框），再则就是实现功能的程序。
>
> 2. 结合这个视频形成新概念，方便理解：[[ Alex 宅幹嘛 ] 👨_💻 深入淺出 Javascript30 快速導覽](https://www.bilibili.com/video/BV1La4y1Y75p)；挑第一个看就好。虽然看不懂，但是起码明白了`JavaScript`在其中扮演的角色。
> 3. 在浏览器网页运用是之一，还有更多用途。冷知识：vscode和灵瞳的串口助手就是`JS`编写的。

- 只要安装编译器，就可以类似Python一样在终端中运行或编译代码。很方便。



# 二、安装与运行

- *国际推荐*，使用`vscode`编写程序。
- 为了摆脱浏览器运行JS程序，选择`Node.js`工具。用于搭建JS运行环境。使得其可以像Python一样在终端直接运行代码或文件。也和Python一样没有图形界面，只有终端的黑底白字。

> 认为：`Node.js`是一种工具，其使用`JavaScript`编程语言。类比`Python`编程语言也有（很多）工具，不过重名，也叫`Python`工具……？（乱，略，过）

- Node.js有很多软件包需要安装或更新，使用`nvm`工具。类比Python中的`pip`工具。nvm工具在JS中作用重大，常用来同步项目软件包（重要）。
- 安装后想要运行，可直接在终端输入`node`指令启动node环境，输入代码就可以逐行编译。或是使用指令运行后缀为`.js`的**单个**文本程序。类比`python`指令的使用，几乎一模一样。



# 三、你好，世界！

- 学编程语言的第一个程序总是先从打印“*Hello World*”开始。JS的打印函数不同于Python或c语言的`print()`，而是`console.log()`。
- 和Python类似，对于字符串可以用双引号也可以用单引号，使用上并无区别。c语言的单引号特指一个字符。

```js
//js中有类似python中print的打印函数，使用方法雷同。
console.log("1 Hello World");           //（久经不衰的"Hello World"）
console.log('2 Hello World');           //js不区分双引号和单引号，所以二者作用一致
console.log('3 Hello World')            //好像没有分号也可以（习惯还是加上吧）
```

> 和python类似，结尾处可以不加分号，但是作用域还是和c语言类似，用花括号表示。

- 和Python类似，可以使用花括号代替转义字符，在字符串中穿插变量。

```js
//还有一个和python中类似的用法
//对照pyhton的使用方法：使用双引号和加了前缀f；
//而js使用的是反单引号（在键盘左上角，数字1左边）和前缀$。
//print(f"6 {greeting} {place}");
console.log(`6 ${greeting} ${place}`);  //注意是反单引号
```



- 和Python与c语言类似，都有字符串格式化，可以使用`%s`等转义字符在字符串中穿插变量。

```js
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
```



# 四、注释

- 从上面的代码中已提前看到了，js的注释和c语言的类似，单行注释`//`与多行注释`/*`+`*/`。

```js
// TODO: Add in database connection string
console.log("Hello, infinity and beyond!");

/* --------------------------------------
    Add in database connection string
 --------------------------------------*/
console.log("Hello, infinity and beyond!");

// 和C语言的格式完全一样啊！
```



# 五、声明变量

- js属于**弱类型语言**，即无须声明数据类型，**八位变量**`uint8/int8`、**十六位变量**`uint16/int16`之类的。但还是需要声明，**全局变量**`var`、**局部变量**`let`、**不变常量**`const`。

> 也就是声明了变量的作用域，这个机制可以节省空间，应该是设计初期为了某特定的运用场景。（个人理解）

```js
// 三种声明变量的方式
var one = 1         //全局变量
let two = 2         //局部变量
const three = 3     //不变常量
```



## 1.全局变量  var

- 对于全局变量`var`的用法不同于c语言或python时的理解——**var的作用域是整个文件**。体现在：只要声明了，即使程序未运行到那一行或是放到局部作用域花括号内，这个变量也已经存在，只是未被赋值而属于`undefined`。

> 1. **js中关键字`undefined`可以类比python中的`null`，同样代表“空”的意思**。
>
> 2. js中也有`false`与`true`关键字，与类比python，同样代表“假”与“真”。

```js
// var全局变量的作用域
hello = 1314				// 不会报错，正确调用，因为已经声明全局变量，即使声明所在行数还未运行。
// var hello = "Hello"
if (false)					// 这里已经为假，但是其中的全局变量声明依旧有效。
{
    console.log(hello)      //在定义之前就可以使用了，var的作用域是整个文件（可以把整个.js文件看作一个巨大函数）
    var hello = "Hello"     //全局变量，已经定义了但是没有赋值，所以打印undefined
    console.log(hello)      //再打印就正常了
}

// var变量可重新赋值
hello = 1314            //没有固定变量类型，和python类似，就算定义的部分已经不会被调用，还是会被定义。表明其实全局函数的定义是在编译时就已经写好的。所以无论写在哪里定义都没关系？
console.log(hello)      //
```

- ~~类比c语言的宏定义记忆（不知为何我大脑自动归为一类了），部分IDE可以预先设置工程的宏定义，不用在工程里包含~~。



## 2.局部变量 let

> 在python或c语言中，如果根据作用域自动划分局部变量，或者说除了全局变量就是局部变量。但是在js中，却需要特别声明局部变量。

- 局部变量和全局变量的主要区别是：作用域是不是整个文件。上一知识点已提到，var声明的变量，可以在程序任意地方调用。**即使**，在声明前面或声明不被执行。而局部变量则是遵循了“**先声明后使用**”的原则，和python或c语言类似。

> ~~个人总感觉“var的作用域是整个文件”这个说法好奇怪，不过我是摘抄教程的直译。姑且算比较正式的说法吧~~。

```js
// let局部变量的作用域1
if(true)                //这个格式和c语言一模一样，同样是使用中括号表示参数，大括号表示作用域
{
    // console.log(world)   不可以在定义前调用，不然直接报错
    let world = "world"
    console.log(world)
}
// console.log(world)       不可以在定义域之外调用，也会直接报错
```

- 如果直接在整个文件的开头声明，那就类似与全局变量，可以在整个文件内使用。（理所当然）

```js
let two = 2         //局部变量
// let局部变量的作用域2
if(true)                //如果是在大括号外定义的，那作用域就是整个文件了
{
    console.log(two)    //既可以在内部函数调用
    two = "我是2"       //也是没有固定类型，可随意赋值（可以输出中文）
}
console.log(two)        //也可以在外部调用
```



## 3.不变常量 const

- c语言中也有`const`关键字，意思类似，也是代表不变常量，不可以修改的“变量”。

```js
// const不变常量
const aaron1 = "Aaron"
console.log(aaron1)
// const aaron1 = 10    不变常量，这样也算修改值，会直接报错

if(true)
{
    const aaron2 = 10
}
// console.log(aaron2)  报错，同样准守作用域规则。看来只有var不符合常量，不准守规则~~
```



## 4.总结

1.  `var`  关键字少用，因为let和const已经能满足绝大需求，使用var还有可能造成意料之外的错误，所以少用。

2.  `let`  常用，类比发现，其实这个就是平时最常用的情况，覆盖整个作用域的变量，且只能定义后使用。

3.  `const` 推荐多用，因为方便看程序，知道这个值不会改变。（~~如果定义一个常量变量，那不是和宏定义差不多吗~~……）



# 六、字符串拼接

- python中也可以字符串拼接，js类似。数个字符串可以直接通过加号`+`组合成新的字符串，非常常用。

```js
// 普通字符串拼接
let str1 = "Hello"
let str2 = "World"

console.log(str1 + str2)        //打印“HelloWorld”
// 有点特殊的是：console.log不能像python中的print一样设置参数，在比如“间隔插入除空格之外的内容”之类的。
console.log(str1,str2)          //打印“Hello World”，因为默认间隔是空格“ ”
console.log(str1+" "+str2)      //打印“Hello World”
```

- js的特殊点是，在进行字符串拼接时，还会自适应对数据进行转换。

> 另一种理解，js会先尝试相加数字1和字符串1，相加失败。js会寻求二者的共同点，尝试将二者都变为字符串再相加，成功了。好，返回字符串~

```js
// 非常规字符串拼接
let num1 = 1
let num2 = "1"
/* 
    js对与字符串和数字量进行拼接时会有个自适应操作；
    就是把数字量转换为字符串后再和字符串拼接。
*/
console.log(num1 + num2)        //打印“11”，等同于下一条！！！！！
console.log("1" + num2)         //打印“11”，等同于上一条
console.log(num1 + 1)           //只有数字量和数字量这样拼接才有表达式的作用
```

- 上述代码中，数字和字符串拼接，数字自动转换为字符串后再拼接！！不用手动进行数据转换，也不会报错，挺方便的，~~就是怕迷惑自己~~。



# 七、模板字符串

- 也就是第三章中提到的，在字符串中穿插变量的方法。js中的专业术语为：模板字符串。

> 模板字符串的用处很多，打印只是其中一种。

```js
// 专业术语：模板字符串（注意是反单引号）
let str1 = "JavaScript"
let str2 = "fun"
// 像极了Python中的“f-string”
console.log(`I am writing code in ${str1}`)
console.log(`Formatting in ${str1} is ${str2}`)

// 也同样支持内嵌表达式
let bool1 = true        // js也支持true关键字

console.log(`1 + 1 is ${1 + 1}`)
console.log(`The opposite of true is ${!bool1}`)    //也支持！运算符
```

> 注意：一定要用反单引号。

```js
// 有趣的是，还支持这样的换行，输出也会带有换行。如果不使用反单引号会报错
console.log(`
This 
is 
test1
`)
```



# 八、数据类型

- js为弱类型语言，类似python，和c语言相对。js也有对象`object`、数字`number`、字符串`string`、布尔`boolean`等类型。比较特殊的变量为：非数`NaN`、`null`（js也有！）、`undefined`。
- 值得注意就是在js中不区分整形和浮点型，他们都统称为数字。

## 1.typeof

- 和python的关键字`type`类似，js中提供了关键字`typeof`，可以使用它查看变量的数据类型。使用方法和python较大区别，不是一个函数，不用括号传参，它会返回对应的数据类型。

```js
// 先定义一些一会要用到的变量
const people = ["Aaron", "Mel", "John"]  // 这个也是数组的形式。
const one = 1
const str = "Hello World"
const b = true
const person = {                //这个看起来就是个字典的样子。
    firstName: "Aaron",
    lastName: "Powell"
}
// 除了常规的数组、数字、布尔、字符串，还有结构体。愈发感觉这是c语言和Python的结合体。
//下面这个是函数的定义格式，提前了解一下
function sayHello(person)
{
    console.log("I am Him.")
}

/*
    js中有个关键字“typeof”可以返回变量的数据类型，对比python中的“type”函数理解。（js中的使用格式不像函数调用）
*/
console.log("-- typeof --")
console.log(typeof people)      //输出 object （对象）注意！！！
console.log(typeof one)         //输出 number （数字）注意！！！
console.log(typeof str)         //输出 string （字符串）注意！！！
console.log(typeof b)           //输出 boolean （布尔）
console.log(typeof person)      //输出 object （对象）
console.log(typeof sayHello)    //输出 function （函数）
```

- python中字典数组的本质上也是对象，不过如果用类型查看还是会显示出对应的类型。js在这方面毕竟特殊。**具体看视频教程，我也没能完全理透**。



## 2.instanceof

- js还提供了另一种查询数据类型的方法。使用`instanceof`可以查询变量是否为某类型，同样返回布尔真假。

```js
// 和上面使用的变量一样。
console.log("-- instanceof --")
console.log(people instanceof Array)        // 输出 true 注意！！！和上面有不一样的效果
console.log(one instanceof Number)          // 输出 flase  注意！！！
console.log(str instanceof String)          // 输出 flase  注意！！！
console.log(b instanceof Boolean)           // 输出 flase  注意！！！
console.log(person instanceof Object)       // 输出 true（看来木有字典这个类型吗）
console.log(sayHello instanceof Function)   // 输出 true
// 如果采用小写判断，会直接报错！！！
// console.log(people instanceof array)
// console.log(one instanceof number)
```

- 教程中提到，使用另一种方法创建数字时：（~~迷、略、过~~）这是js的特别之处，如果需要进行判断数据类型时，请无比注意。

```js
const one = new Number(1)
console.log(typeof one)    					// 输出 object  和上面的结果又反转了
console.log(one instanceof Number)    		// 输出 true  
```



## 3.绝对等于

- js中有`==`和`===`两种符号，因为**js是松散类型系统**（教程用语），所以经常会出现前置返回true，而后者返回flase。

```js
/*
    == js会将左右进行自适应判断，类似字符串拼接时的加号“+”。
    0在数字中为假，‘’在字符串中为假，所以认为相等，返回true。

    === js中就是普通的相等，是否一样，一样才返回true，否者为假。
*/
let x = 0 == '';        // 输出 true
let y = 0 === '';       // 输出 flase
console.log(x,y);
```



# 九、数学运算

- 普通的加减乘除。

```js
let num1 = 100;

/* 加减乘除 */
console.log("-- num1 --"); 
console.log(num1 + 25);
console.log(num1 - 100)
console.log(num1 * 100); 
console.log(num1 / 1500); // 自
```

- 还有求余、自加、自减。

```js
let num2 = 100;

/* 更多运算 */
console.log("-- num2 --"); 
console.log(num2 % 1500); // Remainder
console.log(++num2); // Increment  先自加再输出
console.log(--num2); // Decrement  先自减再输出
```

- 还有一些特殊数学表达式。

```js
console.log("-- num3 --"); 
let num3 = 100;

console.log(Math.PI); // Pi，注意，Math对象不需要导入就可以用了，方便
console.log(Math.sqrt(num3)); // Square root，视频里打错了，应该是sqrt 而不是squrt
```



十、数字和字符串类型转换

- 在通讯传输时，时常需要作数字和字符串互换。在python中可以用类似**数据类型转换**的方式实现各种进制与字符串之间的转换。js中的方法类似，也是函数传参的形式。

```js
let num1 = '150';

console.log(typeof num1) // 执行下面函数前，变量为字符串
console.log(parseInt(`100`)); // 转换为十进制数字 
console.log(parseInt(num1)); // 转换为十进制数字
console.log(parseInt(`ABC`)); // 输出错误 NaN
console.log(parseInt(`0xF`)); // Hexadecimal number，直接认为是十六进制数，转换为十进制数字
console.log(typeof num1) // 执行完毕后，变量还是字符串。可以判断不会改变参数本身。

// python中可以使用：str('字符串')
```

- 小数也可以，使用js的模板字符串也可以。但是字符串表达式不可以，参考第8行代码。

```js
let flo1 = `1.50`

console.log(parseFloat(`1.00`)); // 1
console.log(parseFloat(flo1)); // 1.5
console.log(parseFloat(`ABC`)); // 报错，返回NaN

console.log(parseInt(`1.5`));  // 只返回整数
console.log(parseInt(`5+1`)); // 先转换了第一个数字，遇到第二个加号后报错退出，只返回了第一个数字
console.log(parseInt(`${1+1}`)); // 先运算，再字符串，再数字。模板字符串。

console.log(num1.toString()); // 将数字转换为字符串（可它本身就已经是字符串啦……）
console.log(flo1.toString()); // 同上
console.log((100).toString()); // 任何变量都有内置方法？和python类似了，实质所有变量都是对象
```



# 十、异常处理

- 和python类似，js也有异常处理的关键词，不过和python的不太一样。python的关键词组合为：`try~except~else/finally`，而js的关键词组合为：`try~catch~finally`。基本一致，三个词分别代表可能异常的代码、异常后运行的代码、无论是否异常都运行的代码。python中`else`代表无异常后才运行的代码。

```js
try // 可能报错的地方
{
    throw true; // （手动）弹出报错，报错内容为后者
    
    throw `myException`;
}
catch(ex) // 报错就会运行
{
    console.log("Got an error"); 

    console.log(ex); // 打印报错内容 ，这里就是 true
}
finally // 每次都运行，无论有没有报错
{
    console.log("Code that always will run"); 
}

console.log(`ok`) // 报错经过try后，还会继续运行
```



# 十一、时间对象Date

- 与python类似，js中也有类和对象。这一节通过`Date`类的使用方法，简单了解。

- 注意创建时使用的关键词`new`。

```js
const now = new Date(); // 返回的值是 UTC 制 的日期，要根据不同时区转换

console.log(now);

now.setFullYear(2014);
now.setMonth(6);// 从零开始，所以3就代表4
now.setDate(10); // 具体时间还有时区之分……

now.setHours(8); // 
now.setMinutes(24);
now.setSeconds(46);

console.log(now);

console.log(now.getDay());  // 这个好像是星期几，0代表星期日，4代表星期四
console.log(now.getDate()); // 除了设置，还可以获取

const randomDate = new Date(2015, 3, 12, 6, 25, 58); // 从零开始，所以3就代表4

console.log(randomDate);
```

- ~~教程中解释传参的作用时，我也听的有点懵，因为这个类感觉暂时不怎么用。所以没深究~~。



# 十二、比较操作符

- 和python与c语言类似，常规的操作符都有。还有2个特殊的完全等于的操作符。在前面第八节讲数据类型时有提及。
- 注意`===`操作符，常用来检查数据类型，因为只用`==`不能判断，js会自动转换判断。

```js
 /*
 >
 <
 <=
 >=
 ==
 === 因为js在运算时会对数据进行自动的转换，所以如果用 == 会出现字符串等于数字的情况
 != （同理）不检查数据类型
 !== 检查数据类型
 */
```

- 以下是看视频时的一些笔记注释。

```js
// js会隐式判断布尔类型，比如，字符串的空字符串、对象的空对象（Null）、数字的0、等，都属于假false

// 可以使用“！”颠倒真假

// js也有 &、&& 和 |、|| 运算符，但是和c语言不一样。单符号的意义不是位运算，而是和双符合功能差不多，不同就是是否会跳过之后的判断？（毕竟c语言是针对单片机等的机器语言？）

// (x && y) //如果x是假的，y不会被计算，因为答案是假的，（会跳过后面的y）
// (x || y) //如果x是真的，y不会被计算，因为答案是真的，（会跳过后面的y）

// 那这么以来，单符号的不就没用了吗……除非调用的判断是一个函数的返回值？需要都判断才能使程序正常运行

const a = 10;
const b = 12;

if (a === 10 || b === 11)
{
    console.log(`if`);
}
else
{
    console.log(`else`);  
}
```

> 结合下两节判断和选择语句运用。



# 十三、判断语句 if~else

- 和c语言类似，js的判断语句使用格式基本一致。

```js
const statis = `200`;

if (statis === 200)  // 格式和c语言一样
{
    console.log(`OK!`);
}
else if (statis === 400)
{
    console.log(`Error!`);
}
else
    console.log(`Unknown status`);

// 和c一样，如果只有一行，可以省略括号
```

- 和c语言类似，也有三目运算符。

```js
// 同样有三目运算符（三元函数）
const message = (statis === 200) ? `OK` : `Error!`; // 这个常量 只在创建时赋值了
```



# 十四、选择语句 switch~case

- 和c语言类似，也有`switch`（开关）关键词。用法也基本一模一样。

```js
// js也有 switch - case - break - default 关键词

const status = `200`;

switch(status){
    case 200:                   // 和c语言类似，是判断相等性，而且是带数据类型的判断，就是 ===
        console.log(`ok!`);
        break;                  // 好吧，不能说类似了，只能说是一样了
    case 400:
    case 500:
        console.log(`Error`);
        break;
    default:                    // 好吧，不能说类似了，只能说是一样了
        console.log(`Unknown value`);
        break;
}
```



# 十五、数组

- 和python类似，js的数组中可以容纳各种数据类型，比如字符串、布尔类型、纯数字等。c语言规定只能放一种。
- 创建方式也可以python类似，可以使用直接指定赋值，也可以使用函数创建空数组。

```js
let arr1 = ["ABC", true, 2]; // 创建数组的同时赋值，注意，没有数据类型，一个元素什么都类型和大小都可以，和python的列表类似，已经和c语言完全不一样了。
let arr2 = Array(2);


console.log(arr1[0]); // 引索依旧是从0开始
console.log(arr1[1]);

console.log(arr1[3]); // 没有报错，而是返回 undefined
console.log(arr2[1]); // 同样是返回 undefined
```

- 注意，通过上面第8、9行代码，可以明白，js的数组可以越位访问而没有直接报错，和c语言类似，python中如果越位就会报错。能越位代表更灵活，也有风险。

```js
console.log(arr1.length); // 返回 长度 3 ，不变
console.log(arr1[arr1.length - 1]); // 突然发现一个理解 “引索负数” 的角度，就是 长度 + 引索负数，只是编译器允许省略前面的长度。这也解释了为什么0代表第一个，-1代表最后一个
```

- 和python类似，js的数组有内置方法，可以对数组本体进行删减等操作。具体如下。

> 小知识，在vscode上写js代码时，将鼠标放在内置函数上，可以查看相关说明。

## 1.添加末尾元素 push

- 注意是在添加末尾元素，且返回新的长度，原数组已经改变。

```js
let arr1 = ["A", true, 2];

/*==================== push ==========================*/
console.log(arr1); // 查看数组内容，

// 将新元素追加到数组的末尾，并返回数组的新长度。 （官方解释，鼠标放上去查看）
let arr1_0 = arr1.push("new value"); // 作用：在数组末尾添加一个新元素，同时返回该数组新的长度
let arr1_1 = arr1.push("new value1","new value2"); // 这个函数还可以同时添加多个元素，依次添加

console.log(arr1); // 查看数组内容，和上面做比较，
console.log(arr1_0); // 返回 4 = 3 + 1
console.log(arr1_1); // 返回 6 = 4 + 2
```



## 2.弹出末尾元素 pop

- 注意是弹出末尾元素，且返回被弹出的元素，原数组已经改变。这个方法也当中删除用。

```js
/*==================== pop ==========================*/
console.log(arr1); // 查看数组内容，

// 从数组中删除最后一个元素并返回它。如果数组为空，则返回undefined，并且不修改数组。（官方解释，鼠标放上去查看）
let arr1_2 = arr1.pop(); 

console.log(arr1); // 查看数组内容，和上面做比较，
console.log(arr1_2); // 返回 "new value2" ,也就是最后一个元素的内容
```



## 3.插入开始元素 unshift

- 注意是在开始处插入元素，并返回数组的新长度，原数组已经改变。也就说和`push`相对立。

```js
/*==================== unshift ==========================*/
console.log(arr1); // 查看数组内容，

// 在数组开始处插入新元素，并返回数组的新长度。（官方解释）
let arr1_3 = arr1.unshift("11","22");  // 同样可以同时添加多个元素

console.log(arr1); // 查看数组内容，和上面做比较，
console.log(arr1_3); // 返回 7 = 5 + 2
```



## 4.弹出开始元素 shift

- 注意是在开始处弹出元素，且返回被弹出的元素，原数组已经改变。也就说和`pop`相对立。

> 而且`unshift`关键词只有前面两个字母的差别。

```js
/*==================== shift ==========================*/
console.log(arr1); // 查看数组内容，

// 从数组中删除第一个元素并返回它。如果数组为空，则返回undefined，并且不修改数组。（官方解释）
let arr1_4 = arr1.shift();  // 同样可以同时添加多个元素

console.log(arr1); // 查看数组内容，和上面做比较，
console.log(arr1_4); // 返回 "11" , 也就是弹出的第一个元素
```



## 5.组合数组 concat

- 注意是组合数组，可以是多个，返回为组合好的新数组，并不修改原数组。
- 可作为添加元素的用法，组合时是按传参顺序组合。

```js
/*==================== concat ==========================*/
let arr2 = ["B", false, 3];
console.log(arr1); // 查看数组内容，
console.log(arr2); // 

// 组合两个或多个数组。此方法返回一个新数组，而不修改任何现有数组。（官方解释）
let arr1_5 = arr1.concat(arr2);  // 添加到数组末尾的其他数组和/或项。
let arr1_6 = arr1.concat([1,2,3],[4,5]);  // 同上，是可以输入多个参数，也是依次排列在后面

console.log(arr1); // 查看数组内容，和上面做比较，
console.log(arr2); // 可以发现2个数组都没有变化，只有返回值是组合值，那为什么这个方法是数组的内置方法……，这样容易让人误解啊
console.log(arr1_5); // 组合的数组
console.log(arr1_6);
```



# 十六、循环 for/while

- 和c语言类似，循环`for`是分4个代码段，按特定的顺序执行。循环`for/while`的使用格式也一样。

> 在写这一部分练习时，忽然结合for和while的特点，和作用域的特点，使for和while等效时的形式（绕口令）。所以我写很多层作用域。为了测试js中和c语言中的作用域理念是否相同，经过我的实验，个人认为是相同的。

```js
console.log(`-------- 作用域 + while ----------`) // javascript具有分号自动插入规则
{   // 这个作用域，就相当于 for
    let whileIndex = 0; // for 的第一个表达式
    while(whileIndex < names.length) // for 的第二个表达式
    {
        {
            let whileIndex = 1; // 作用域外的同名变量不会有任何影响，
            let test_name = "test_name";
            console.log(names[whileIndex]); // for 循环的内容
            console.log(test_name); // 只有这里才不报错，表明作用域是可以套娃的
        }
        // console.log(test_name); // 报错，不在作用域内
        whileIndex++; // for 的第三个表达式
    }
    console.log(whileIndex); // 返回3，
    // console.log(test_name); // 报错，不在作用域内
}
// console.log(whileIndex); // 报错了，单纯空的大括号也可以作为一个新的作用域
```

```js
console.log(`-------- 作用域 + for ----------`); // 验证了不同作用域内的变量是不会相互影响的
const nums = [`1`,`2`,`3`];
if (0) // 取消执行，快捷
for (let whileIndex = 0; whileIndex < nums.length; whileIndex++) // 不同作用域命名重复也没关系
{
    for (let whileIndex = 0; whileIndex < nums.length; whileIndex++) // 不同作用域命名重复也没关系
    {
        for (let whileIndex = 0; whileIndex < nums.length; whileIndex++) // 不同作用域命名重复也没关系
        {
            for (let whileIndex = 0; whileIndex < nums.length; whileIndex++) // 不同作用域命名重复也没关系
            {
                for (let whileIndex = 0; whileIndex < nums.length; whileIndex++) // 不同作用域命名重复也没关系
                {
                    console.log(`--1`); // for 循环的内容
                    console.log(nums[whileIndex]); // for 循环的内容
                }
                console.log(`--2`); // for 循环的内容
                console.log(nums[whileIndex]); // for 循环的内容
            }
            console.log(`--3`); // for 循环的内容
            console.log(nums[whileIndex]); // for 循环的内容
        }
        console.log(`--4`); // for 循环的内容
        console.log(nums[whileIndex]); // for 循环的内容
    }
    console.log(`--5`); // for 循环的内容
    console.log(nums[whileIndex]); // for 循环的内容
}
```

- js中的循环`for`还有python的类似用法，很特别。注意不要混淆。

```js
const names = [`justin`,`burke`,`sarah`];

console.log(`-------- for + of ----------`); // 有点类似python的 for in

for (let name of names) // 相当于每次都重新创建了一个变量 name ？ ！！！！
{
    console.log(name);
    name = 'test'; // 如果创建时不用 const 而是用 let 甚至还可以改变该值
    console.log(name);
}

console.log(`-------- for + in ----------`); // js也有 for in 啊！！……

for (let name in names) // 和of不同，取的是下标索引？？
{
    console.log(name);  // 返回的是 下标
    console.log(names[name]); // 通过下标再取出元素
}
```



# 零、分界线

- 避免太长就分上下两篇。

- 本篇主要讲些类似python和c语言的基本语法，下篇再讲完剩下的视频教程内容。主要设计到`JavaScript`特有的函数构筑。
