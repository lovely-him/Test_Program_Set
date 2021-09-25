
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