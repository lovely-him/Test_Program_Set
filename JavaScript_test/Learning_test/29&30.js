
// 创建数组
let arrayLength = 5;
let arr1 = []; // 创建数组、无指定长度，
let arr2 = Array(arrayLength); // 创建数组对象，指定数组长度

console.log(arr1.length); // 使用内置方法返回数组的长度。0
console.log(arr2.length); // 所以，其实数组类似是对象。5

console.log(arr1[0]); // 返回 undefined ，没有值，连零都不是。开始体现和c语言这种和底层单片机接触的语言的差异了。