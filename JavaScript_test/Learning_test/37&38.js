
/* 特点：

1. 函数名字可以除了字母、数字、下划线外，还可以存在 “$” 字符。
2. 使用 typeof 关键字可以查看函数类型。
3. 函数形参定义时不需要写关键字：var、let、const。应该默认就是局部可修改变量。
4. JS 语法中 不检查输入参数。这意味着，输入参数可少可多。少了输入undefined代替，多了自动忽略。
5. 同上理，JS 也不拘束是否有返回值，统一都有返回值。如果没有写明返回值，则统一返回无效值。


*/

// 1. Function Definition
function printHello_1$_(name_0) 
{
    // execution
    console.log("Hello World!" + name_0);
}
console.log(typeof printHello_1$_);

// 2. Function Invocation
printHello_1$_(); 

// 3. Function Naming

// 4. Function Parameters

// 5. Function Return

// 6. 函数还可以没名字，直接这样创建。
let him = function(){
    console.log("him");
}
him()

// 8. 函数名字本身不支持传递赋值，但是变量可以。
// him = printHello_1(); // 报错
let add = him;
add();

// 7. 该变量还是可以赋值其他内容。
him = 6;
console.log(him)




