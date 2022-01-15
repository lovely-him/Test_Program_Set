// 三种声明变量的方式
var one = 1         //全局变量
let two = 2         //局部变量
const three = 3     //不变常量

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

// let局部变量的作用域1
if(true)                //这个格式和c语言一模一样，同样是使用中括号表示参数，大括号表示作用域
{
    // console.log(world)   不可以在定义前调用，不然直接报错
    let world = "world"
    console.log(world)
}
// console.log(world)       不可以在定义域之外调用，也会直接报错

// let局部变量的作用域2
if(true)                //如果是在大括号外定义的，那作用域就是整个文件了
{
    console.log(two)    //既可以在内部函数调用
    two = "我是2"       //也是没有固定类型，可随意赋值（可以输出中文）
}
console.log(two)        //也可以在外部调用

// console.log(four)    //但是同样需要在调用前定义，不然会直接报错
let four = 4            
console.log(four)       

// const不变常量
const aaron1 = "Aaron"
console.log(aaron1)
// const aaron1 = 10    不变常量，这样也算修改值，会直接报错
if(true)
{
    const aaron2 = 10
}
// console.log(aaron2)  报错，同样准守作用域规则。看来只有var不符合常量，不准守规则~~

/* 总结：
 var    关键字少用，因为let和const已经能满足绝大需求，使用var还有可能造成意料之外的错误，所以少用。
 let    常用，类比发现，其实这个就是平时最常用的情况，覆盖整个作用域的变量，且只能定义后使用。
 const  推荐多用，因为方便看程序，知道这个值不会改变。（如果定义一个常量变量，那不是和宏定义差不多吗……）
*/ 
