# JavaScript 入门笔记 - 下 - 函数语法

> 前言，承接上篇，写完剩下的笔记。



# 十七、普通函数

- js的函数创建比较特殊，有很多种方式，最简单的一种和c语言类似。

> *特点：*
>
> 1. 函数名字可以除了字母、数字、下划线外，还可以存在 “$” 字符。
>
> 2. 在js中，函数名就是一个储存函数对象的变量。使用 typeof 关键字可以查看函数类型。（这个理念和python类似，可以用其他变量接手这个函数）
>
> 3. 函数形参定义时不需要写关键字：var、let、const。应该默认就是局部可修改变量。
>
> 4. JS 语法中 不检查输入参数。这意味着，输入参数可少可多。少了输入undefined代替，多了自动忽略。
>
> 5. 同上理，JS 也不拘束是否有返回值，统一都有返回值。如果没有写明返回值，则统一返回无效值。

```js
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
```

- js还支持匿名函数，就是不写函数名。python中也有类似，在python学习笔记中也有记录：`lambda`匿名函数。

```js
// 6. 函数还可以没名字，直接这样创建。
let him = function(){
    console.log("him");
}
him() // 侧面反映了，名字其实就是一个变量名。

// 8. 函数名字本身不支持传递赋值，但是变量可以。
// him = printHello_1(); // 报错（有点类似数组定义后就不能再赋值？）
let add = him;
add();

// 7. 该变量还是可以赋值其他内容。
him = 6;
console.log(him) // 输出数字 6
```

- ~~在后期用起来，快分不清哪个是数据变量，哪个是功能函数了~~。



# 十八、箭头函数

- js中箭头函数就是“名副其实”的匿名函数了，可快速创建嵌套函数功能体（自创用词）……也更加贴合python的`lambda`匿名函数用法。

> ~~在看实战案例时全是这种匿名函数的创建和传参，第一次接触懵逼得不要不要的~~。下面的代码为了方便看效果，我会把用不到的部分改成假，屏蔽运行。你问为什么不直接注释？因为想锻炼用法。

- 使用方法看似简单，前面括号就是用到的参数，箭头后面紧跟代码。如果是单行的简易代码可不用写括号，单行还自带隐式返回计算值。

```js
if (false)
{
    const add = (a, b) => a + b; // 类似直接创建函数，并且将该函数丢给一个变量调用。
    console.log(add(1,3)); // 没有写返回值，还隐式返回了计算值    
}

if (false)
{
    let add = (a, b) => a + b;
    console.log(add(1,3)); // 打印 4
    const add_0 = add; // 可以正常的变量赋值替换
    add = 5; // 可以看出本质还是变量，如果定义是使用可变类型，则可以改变
    console.log(add); // 打印 5
    console.log(add_0(2, 4)); // 打印 6
}

if (false)
{
    console.log(add_0(10, 4)); // const 变量类型不可以跨作用域
}
```

- 如果是需要换行，就需要用大括弧。常用。

```js
if (false)
{
    const add = (a, b) => 
    {
        return a + b;
    }
    console.log(add(1,3));  // 有返回值，表示如果用了大括号可以表示换行但是不会有隐式返回。而单行总是会有隐式返回的。
}
```



# 十九、数据包 JSON

> [JSON](https://baike.baidu.com/item/JSON)([JavaScript](https://baike.baidu.com/item/JavaScript) Object Notation, JS 对象简谱) 是一种轻量级的数据交换格式。它基于 [ECMAScript](https://baike.baidu.com/item/ECMAScript) (欧洲计算机协会制定的js规范)的一个子集，采用完全独立于编程语言的文本格式来存储和表示数据。简洁和清晰的层次结构使得 JSON 成为理想的数据交换语言。 易于人阅读和编写，同时也易于机器解析和生成，并有效地提升网络传输效率。【截至百科】

- 在之前学习神经网络和`ros`时也有接触这类数据包，一个小小的后缀`.json`文件，装着一堆参数或数据集。从格式上看，很像字典，有键和值成对。如果展开图形化，其实是一个列表，有表头和数据。
- js提供`Object`类来创建json对象。（其实就是创建对象，下一节再细说）

```js
// 例子1
if (false)
{
    const book = new Object({title : "1984", author : "George Orwell"}) // 创建 JSON 对象
    console.log("\n ---------")
    console.log(typeof book) // 查看类型，确实是对象
    console.log(book) // 能正常打印
}
// 例子2（下一节细说，对象的知识点）
if (false)
{
    const book = ({title : "1984", author : "George Orwell"}) // 就算不加关键词 Object 也能有相同效果。
    console.log("\n ---------")
    console.log(typeof book)
    console.log(book)
}
// 例子3
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
```

- **js提供将json对象数据转换为字符串的方法**：`JSON.stringify()`。

```js
if (false)
{
    const book = ({title : "1984", author : "George Orwell"}) // 就算不加关键词 Object 也能有相同效果。
    console.log("\n ---------")
    let bookJSON = JSON.stringify(book); // 将对象保留原本格式，转换为了字符串，其中键名变成了字符串（就是加了双引号）？方便用于保存在文本内？
    console.log(typeof bookJSON) // 想起来，JSON不也是之前我写ros工程时用到的参数文件吗，还有百度飞浆的文本文件都是这种格式。
    console.log(bookJSON)
}
/* 输出内容如下：
 ---------
string
{"title":"1984","author":"George Orwell"}
*/
// 可以发现键值还是原本的字符串，但是键名已经变换为字符串
```

> 我做了一个类比实验，看如下注释。

```js
if (false)
{
    const book = ([1,23,3,"156"]) 
    console.log("\n ---------")
    console.log(typeof book) // 类型依旧属于 object
    let bookJSON = JSON.stringify(book); // 依旧可以调用，不会出现报错。
    console.log(typeof bookJSON) // 得到的结果 和原结果一模一样的字符串。
    console.log(bookJSON)
}
/* 输出内容如下：
 ---------
object
string
[1,23,3,"156"]
*/
// 可以发现函数好像没有起到作用。判断格式不符合json要求时不会起作用，也不会报错。
```

- **js提供将字符串数据转换为json对象的方法**：`JSON.parse()`。就是`JSON.stringify()`的逆操作了。

```js
if (false)
{
    let data_0 = "[1,2,3]";
    let data = "{\"title\" : \"1984\", \"author\" : \"George Orwell\"}"; // 注意，JSON的字符串形式下，键和值都是要加双引号的，弄成类似字符串的形式。有一点不对都会转换失败。
    let parsed = JSON.parse(data); // 逆向操作，将字符串再变回成对象类型。会解析是否符合格式。
    console.log("\n -----")
    console.log(parsed); // 
    console.log(typeof parsed) 
    console.log(typeof data) 
}
/* 输出内容如下：
 -----
{ title: '1984', author: 'George Orwell' }
object
string
*/
// 需要注意的就是字符串中的斜杆表示比较麻烦
```

- 学习JSON格式数据的使用非常重要，json变量其实并非普通的数据，而是包含众多数据处理函数的对象。比如上述2个字符串和数据之间相互转换的函数，检查在实战中用到。分别是读取数据和存储数据的2个操作。



# 二十、对象 Object

- js中的对象创建不同于python的类，而是直接创建对象。我直接看例子，结合例子展开。

```js
  // 1. 创建对象，
if (false)
{
    const book = {
        title : "1984",
        author : "George Orwell",
        isAvailable : false, // 定义个别属性数据
        
        checkIn : function(){ // 还可以定义匿名函数
            this.isAvailable = true; // 使用this关键字代表本对象，继而可以引用属性
        },
        checkOut : function(){
            this.isAvailable = false; // 这个this有点类似python类中代指的self关键字
        }
    };
    
    console.log(book); // 打印所有属性
    console.log(typeof book); // 打印 object
}
```

- 从格式可以看出，感觉是一堆属性，有字符串，有匿名函数。而且不是用等于号而是用冒号赋值，就像字典的键对一样。

> 所以现在看来，其实json数据包，在js中相当于对象的存在。如果是直接打印函数方法，会输出类似字符：`[Function (anonymous)]`。

- 除了一开始直接赋值，也可以采用先创建空对象，再逐步添加值。如果已经存在的属性会覆盖，否则就当作是添加。（很简单粗暴）

```js
// 2. 另一种创建对象的方法，使用构造函数创建
if (false)
{
    const book = new Object();
    console.log(book); // 一开始创建是空的
    console.log(typeof book); //类型是 object

    book.title = "1984";
    book.author = "George Orwell";
    book.isAvailable = false; // 添加属性

    book.checkIn = function(){
        this.isAvailable = true;  // 添加方法
    };
    book.checkOut = function(){
        this.isAvailable = false; 
    };

     console.log(book); // 打印正常
     console.log(typeof book);

    // 3. 访问对象内元素的方法：
    console.log(book.title); // 类似结构体的访问
    console.log(book["title"]); // 类似字典的访问，输出结果是一样的，注意，这样访问的话，键名一定要加双引号，看作字符串形式

    console.log(book.checkIn); // 如果是访问函数，如果不加括号，会返回对象。打印类似字符：[Function (anonymous)]
    console.log(book.checkIn()); // 如果加括号就相当于调用执行.（返回值空，因为函数内没用写返回值）
    
    console.log(book["checkIn"]); // 也可以使用字典的形式访问，结果一样
    console.log(book["checkIn"]());  // 就是这个括号是在方括号外面的。
}
```

- **上下文机制**： `this` ,并不完全是在对象内值指对象的名字，而是指代上下文使用的变量？（具体看视频讲解，我理解还不太透彻）
- 类似于我使用的主体，我使用的主体是对象，返回的就是对象，我使用的函数，返回的就是函数。所以`this`还可以在函数中使用，虽然函数本身也是一个对象（？）。

```js
if (false)
{
    const bookObj = {    			// 创建一个对象
        checkIn : function(){		// 添加一个属性
            return this;			// 这个属性是一个方法，且有返回值，返回对象本身
        }
    }

    function anotherCheckIn(){		// 创建一个函数
        return this;				// 返回一个函数本身
    }

    console.log(bookObj.checkIn() == bookObj); // 返回值是不是对象本身，对的
    console.log(bookObj.checkIn() == globalThis); // 返回值是不是函数，错的
    console.log(anotherCheckIn() == globalThis); // 返回值是不是函数，对的
}
```



# 二十一、Promise

> 懵逼的一节，讲js中的异步运行机制？不多解释，怕越说越错。

```js
// Promise 对象用于表示一个异步操作的最终完成 (或失败)及其结果值。
if (true)
{
    function promiseTimeout(ms){ // 创建一个函数
        return new Promise((resolve, reject) => { // 返回一个 Promise 对象， 输入参数是一个匿名函数，其中匿名函数又有2个参数，一个是成功时会执行的内容，一个是失败时会执行的内容
            setTimeout(resolve, ms); // js内部函数，延时第二个参数ms后执行 第一个参数的内容。
        });
    }

    promiseTimeout(2000) // 调用函数，传入参数2000ms；
        .then(() => { // 返回的 Promise 对象的内置方法；如果成功则会调用。该内置方法也有一个参数，该参数是匿名函数
            console.log('Done!!'); // 该匿名函数无参入参数，内部功能只有打印
            return promiseTimeout(1000); // 再调用一次函数，又返回一个变量
        }).then(() => { // 因为上面又返回了一个变量，所以可以链式调用，
            console.log('Also done!!'); // 延时1000ms，运行成功后会接着调用
            return Promise.resolve(42); // 又返回一个对象，无限套娃
        }).then((result_0) => { // 传入参数,这个参数名字是随意的，我修改后还是能实现效果。ide自动标红，应该能知道是变量，而非语法关键字
            console.log(result_0); // 打印参数
        })
        .catch(() => { // 同上，不过是失败时调用
            console.log('Error!');
        })
    // 因为 Promise.prototype.then 和  Promise.prototype.catch 方法返回的是 promise， 所以它们可以被链式调用。

}

/*
运行结果为：
先稍等一会打印一行：
Done！
稍等片刻后再同时先后打印两行：
Also done！
42
*/
```

- ~~可以看到疯狂嵌套对象的内置方法和使用箭头函数作为传参。看得我人都傻了~~……



# 二十二、Async : Await

> 和`Promise`机制相反。

```js
// Async:Await

function promiseTimeout(ms){
    return new Promise((resolve, reject) => {
        setTimeout(resolve, ms);
    });
}

async function longRunningOperation(){
    return 42;
}

async function run(){
    console.log('Start!');
    await promiseTimeout(2000); // 添加await关键字，结果类似去同步运行。本来使用Promise会使先打印，后延时，如果加上A/A后就会按顺序先延时再打印。

    const response = await longRunningOperation();
    console.log(response); // 按道理应该直接返回42并打印，实际上，如果不加await关键字，会立刻返回一个Promise对象，而不是42.

    console.log('Stop!!');
}

run();

/*
运行结果为：
先打印一行：
Start！
稍等片刻后再同时先后打印两行：
42
Stop！
*/
```



# 二十三、包

- 使用node.js中附带的nvm工具，可以很好的管理js软件包。而且工程可以配备了相关软件包目录。只需要在其中添加对应软件包，再输入更新工程指令就可以在工程中添加软件包。

> 类似于编译一样，不过这个是下载。过去python提倡将软件包直接安装在电脑工作环境空间内。而c语言的相关库是建议在工程内。js也是提倡在工程内。不过如果要转移程序时，会讲软件包文件夹删除。只转移工程代码部分。转移完毕后在别的电脑上再使用更新下载功能即可。这个操作有点像之前学过的ros工程。不过ros工程就算不设置正确也能正常运行，js如果设置不准确，在编译时就不通过了。



# 二十四、总结

- 后面这几章比较复杂，我都还没完全弄清楚，只是看了视频教程后大概有概念。
- 在跟着js小项目做时还是看不到那个离谱的 *对象+箭头函数传参* 的用法。
- 日后再补充详细。
