// 专业术语：模板字符串（注意是反单引号）
let str1 = "JavaScript"
let str2 = "fun"
// 像极了Python中的“f-string”
console.log(`I am writing code in ${str1}`)
console.log(`Formatting in ${str1} is ${str2}`)

// 也同样支持内嵌表达式
let bool1 = true        // js也支持true关键字

console.log(`1 + 1 is ${1 + 1}`)
console.log(`The opposite of true is ${!bool1}`)    //也支持！运算符


// 有趣的是，还支持这样的换行，输出也会带有换行。如果不使用反单引号会报错
console.log(`
This 
is 
test1
`)
