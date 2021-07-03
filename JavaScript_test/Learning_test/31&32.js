
let arr1 = ["ABC", true, 2]; // 创建数组的同时赋值，注意，没有数据类型，一个元素什么都类型和大小都可以，和python的列表类似，已经和c语言完全不一样了。
let arr2 = Array(2);


console.log(arr1[0]); // 引索依旧是从0开始
console.log(arr1[1]);

console.log(arr1[3]); // 没有报错，而是返回 undefined
console.log(arr2[1]); // 同样是返回 undefined

console.log(arr1.length); // 返回 长度 3 ，不变
console.log(arr1[arr1.length - 1]); // 突然发现一个理解 “引索负数” 的角度，就是 长度 + 引索负数，只是编译器允许省略前面的长度。这也解释了为什么0代表第一个，-1代表最后一个


