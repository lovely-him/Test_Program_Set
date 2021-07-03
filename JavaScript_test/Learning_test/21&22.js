
try // 可能报错的地方
{
    throw true; // （手动）弹出报错，报错内容为后者
    
    throw `myException`;
}
catch(ex) // 报错就会运行
{
    console.log("Got an error"); 

    console.log(ex); // 打印报错内容 ，这里就是 true
}
finally // 每次都运行，无论有没有报错
{
    console.log("Code that always will run"); 
}

console.log(`ok`) // 报错经过try后，还会继续运行