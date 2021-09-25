
if (false)
{
    const book = new Object({title : "1984", author : "George Orwell"}) // 创建 JSON 对象
    console.log("\n ---------")
    console.log(typeof book) // 查看类型，确实是对象
    console.log(book) // 能正常打印
}

if (false)
{
    const book = ({title : "1984", author : "George Orwell"}) // 就算不加关键词 Object 也能有相同效果。
    console.log("\n ---------")
    console.log(typeof book)
    console.log(book)
}

if (false)
{
    const book = [
        {title : "1984", author : "George Orwella"},
        {title : "1985", author : "George Orwellb"},
        {title : "1986", author : "George Orwellc"},
        {title : "1987", author : "George Orwelld"}
    ]
    console.log("\n ---------")
    console.log(typeof book) // 打印类型还是对象 object，但是实际上一个算是数组
    console.log(book)
}

if (false)
{
    const book = ({title : "1984", author : "George Orwell"}) // 就算不加关键词 Object 也能有相同效果。
    console.log("\n ---------")
    let bookJSON = JSON.stringify(book); // 将对象保留原本格式，转换为了字符串，其中键名变成了字符串（就是加了双引号）？方便用于保存在文本内？
    console.log(typeof bookJSON) // 想起来，JSON不也是之前我写ros工程时用到的参数文件吗，还有百度飞浆的文本文件都是这种格式。
    console.log(bookJSON)
}

if (false)
{
    const book = ([1,23,3,"156"]) 
    console.log("\n ---------")
    console.log(typeof book) // 类型依旧属于 object
    let bookJSON = JSON.stringify(book); // 依旧可以调用，不会出现报错。
    console.log(typeof bookJSON) // 得到的结果 和原结果一模一样的字符串。
    console.log(bookJSON)
}

if (true)
{
    let data_0 = "[1,2,3]";
    let data = "{\"title\" : \"1984\", \"author\" : \"George Orwell\"}"; // 注意，JSON的字符串形式下，键和值都是要加双引号的，弄成类似字符串的形式。有一点不对都会转换失败。
    let parsed = JSON.parse(data); // 逆向操作，将字符串再变回成对象类型。会解析是否符合格式。
    console.log("\n -----")
    console.log(parsed); // 
    console.log(typeof parsed) 
    console.log(typeof data) 
}