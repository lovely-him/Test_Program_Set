/*
    JS为弱类型语言，类似Python，和C语言相对。
    教程中列举了几个常规变量类型：Number/float(数字)、String(字符串)、Boolean(布尔)、Date(日期)、Function(函数)、Array(数组)、Object(对象)
    一些不常规的，比较特殊的变量为：NaN(非数)、null、undefined。
    值得注意就是在js中不区分整形和浮点型，他们都统称为数字。
*/

// 先定义一些一会要用到的变量
const people = ["Aaron", "Mel", "John"] 
const one = 1
const str = "Hello World"
const b = true
const person = {
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
console.log(typeof people)      //输出 object （对象）
console.log(typeof one)         //输出 number （数字）
console.log(typeof str)         //输出 string （字符串）
console.log(typeof b)           //输出 boolean （布尔）
console.log(typeof person)      //输出 object （对象）
console.log(typeof sayHello)    //输出 function （函数）

/*
    js中另一个查看
*/
