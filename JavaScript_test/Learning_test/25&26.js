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

// 同样有三目运算符（三元函数）
const message = (statis === 200) ? `OK` : `Error!`; // 这个常量 只在创建时赋值了
