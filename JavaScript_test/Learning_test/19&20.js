
let num1 = '150';

console.log(typeof num1) // 执行下面函数前，变量为字符串
console.log(parseInt(`100`)); // 转换为十进制数字 
console.log(parseInt(num1)); // 转换为十进制数字
console.log(parseInt(`ABC`)); // 输出错误 NaN
console.log(parseInt(`0xF`)); // Hexadecimal number，直接认为是十六进制数，转换为十进制数字
console.log(typeof num1) // 执行完毕后，变量还是字符串。可以判断不会改变参数本身。

let flo1 = `1.50`

console.log(flo1)
console.log(parseFloat(`1.00`)); // 1
console.log(parseFloat(flo1)); // 1.5
console.log(parseFloat(`ABC`)); // 报错，返回NaN

console.log(parseInt(`1.5`));  // 只返回整数
console.log(parseInt(`5+1`)); // 先转换了第一个数字，遇到第二个加号后报错退出，只返回了第一个数字
console.log(parseInt(`${1+1}`)); // 先运算，再字符串，再数字

console.log(num1.toString()); // 将数字转换为字符串（可它本身就已经是字符串啦……）
console.log(flo1.toString()); // 同上
console.log((100).toString()); // 任何变量都有内置方法？和python类似了，实质所有变量都是对象