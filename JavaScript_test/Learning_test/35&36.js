
const names = [`justin`,`burke`,`sarah`];

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
