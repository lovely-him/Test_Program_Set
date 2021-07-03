
const now = new Date(); // 返回的值是 UTC 制 的日期，要根据不同时区转换

console.log(now);

now.setFullYear(2014);
now.setMonth(6);// 从零开始，所以3就代表4
now.setDate(10); // 具体时间还有时区之分……

now.setHours(8); // 
now.setMinutes(24);
now.setSeconds(46);

console.log(now);

console.log(now.getDay());  // 这个好像是星期几，0代表星期日，4代表星期四
console.log(now.getDate()); // 除了设置，还可以获取

const randomDate = new Date(2015, 3, 12, 6, 25, 58); // 从零开始，所以3就代表4

console.log(randomDate);
