 
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
            this.isAvailable = false;
        }
    };
    
    console.log(book);
    console.log(typeof book);
}

// 2. 另一种创建对象的方法，使用构造函数创建
if (true)
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

    console.log(book.checkIn); // 如果是访问函数，如果不加括号，会返回对象。
    console.log(book.checkIn()); // 如果加括号就相当于调用执行.（返回值空，因为函数内没用写返回值）
    
    console.log(book["checkIn"]); // 也可以使用字典的形式访问，结果一样
    console.log(book["checkIn"]());  // 就是这个括号是在方括号外面的。
}

 // 上下文机制： this ,并不完全是在对象内值指对象的名字，而是指代上下文使用的变量？

if (false)
{
    const bookObj = {
        checkIn : function(){
            return this;
        }
    }

    function anotherCheckIn(){
        return this;
    }

    console.log(bookObj.checkIn() == bookObj); // 对的
    console.log(bookObj.checkIn() == globalThis); // 错的
    console.log(anotherCheckIn() == globalThis); // 对的
}