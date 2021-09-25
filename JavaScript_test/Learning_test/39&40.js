
// 箭头函数 =>

if (false)
{
    const add = (a, b) => a + b; // 类似直接创建函数，并且将该函数丢给一个变量调用。
    console.log(add(1,3)); // 没有写返回值，还隐式返回了计算值    
}

if (false)
{
    let add = (a, b) => a + b;
    console.log(add(1,3));
    const add_0 = add; // 可以正常的变量赋值替换
    add = 5; // 可以看出本子还是变量，如果定义是使用可变类型，则可以改变
    console.log(add);
    console.log(add_0(2, 4));
}
if (false)
{
    console.log(add_0(10, 4)); // const 变量类型不可以跨作用域
}

if (false)
{
    const add = (a, b) => 
    {
        a + b;
    }
    console.log(add(1,3));  // 没有返回值，打印 unddefined
}

if (false)
{
    const add = (a, b) => 
    {
        return a + b;
    }
    console.log(add(1,3));  // 有返回值，表示如果用了大括号可以表示换行但是不会有隐式返回。而单行总是会有隐式返回的。
}

/* 总结：感觉就像是匿名函数一样。 */