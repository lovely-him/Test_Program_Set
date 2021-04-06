// 普通字符串拼接
let str1 = "Hello"
let str2 = "World"

console.log(str1 + str2)        //打印“HelloWorld”
// 有点特殊的是：console.log不能像python中的print一样设置参数，在比如“间隔插入除空格之外的内容”之类的。
console.log(str1,str2)          //打印“Hello World”
console.log(str1+" "+str2)      //打印“Hello World”

// 非常规字符串拼接
let num1 = 1
let num2 = "1"
/* 
    js对与字符串和数字量进行拼接时会有个自适应操作；
    就是把数字量转换为字符串后再和字符串拼接。
*/
console.log(num1 + num2)        //打印“11”，等同于下一条
console.log("1" + num2)         //打印“11”，等同于上一条
console.log(num1 + 1)           //只有数字量和数字量这样拼接才有表达式的作用