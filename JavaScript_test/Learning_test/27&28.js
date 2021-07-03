
// js会隐式判断布尔类型，比如，字符串的空字符串、对象的空对象（Null）、数字的0、等，都属于假false

// 可以使用“！”颠倒真假

// js也有 &、&& 和 |、|| 运算符，但是和c语言不一样。单符号的意义不是位运算，而是和双符合功能差不多，不同就是是否会跳过之后的判断？

// (x && y) //如果x是假的，y不会被计算，因为答案是假的，（会跳过后面的y）
// (x || y) //如果x是真的，y不会被计算，因为答案是真的，（会跳过后面的y）

// 那这么以来，单符号的不就没用了吗……除非调用的判断是一个函数的返回值？

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