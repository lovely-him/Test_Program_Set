
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