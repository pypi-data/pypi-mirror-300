// https://www.runoob.com/regexp/regexp-tutorial.html
// https://mp.weixin.qq.com/s/TIub-jz9KU2ngoDg5FCnDQ
// https://www.runoob.com/try/try-regex.php | 测验工具
// https://www.jyshare.com/front-end/9064/ | AI 正则分析工具


;((str) => {
    // 从字符串 str 中提取数字部分的内容 (match 匹配一次)
    // 0 | 匹配值
    // index | 匹配值在整个字符串中的索引位置, 索引从 0开始, 从左到右

    // [ '123', index: 3, input: 'abc123def', groups: undefined ]
    console.log(str.match(/[0-9]+/))

    // 使用 matchAll 最后要带 g
    // Object [RegExp String Iterator] {}
    console.log(str.matchAll(/[0-9]+/g))

    // [ '123', index: 3, input: 'abc123def456', groups: undefined ],
    // [ '456', index: 9, input: 'abc123def456', groups: undefined ]
    console.log([...str.matchAll(/[0-9]+/g)])
})('abc123def456')

// 正则表达式的模式
// 字面值字符：例如字母、数字、空格等，可以直接匹配它们自身。
// 特殊字符：例如点号 .、星号 *、加号 +、问号 ? 等，它们具有特殊的含义和功能。
// 字符类：用方括号 [ ] 包围的字符集合，用于匹配方括号内的任意一个字符。
// 元字符：例如 \d、\w、\s 等，用于匹配特定类型的字符，如数字、字母、空白字符等。
// 量词：例如 {n}、{n,}、{n,m} 等，用于指定匹配的次数或范围。
// 边界符号：例如 ^、$、\b、\B 等，用于匹配字符串的开头、结尾或单词边界位置。

const fn_00 = (strs, rege) => {
        console.log([...Array(100)].map(v => '-').join(''))
        strs.forEach(v => console.log(v.match(rege)))
    }

// 0: 匹配值
// 1: 如有括号, 匹配括号内的子值
;fn_00([
    'data.dat',
    'data1.dat',
    'dataN.dat',
], /data(\w?).dat/) // ? 0 个或1个

;fn_00([
    'data.dat',
    'data1.dat',
    'data2.dat',
    'data12.dat',
    'datax.dat',
    'dataXYZ.dat',
], /data(.*).dat/) // (.任意字符) (* | 0 个或多个)

// 字符串内只能出现 大小写字母, 数字, 下划线, 中横线 字符, 3 ~ 15 位长度
;fn_00([
    '123',
    'abc',
    'ABC',
    '1aA',
    '_-1aA',
    '123abcABC1aA_-1', // 最多 15位, 含 15位
], /^[a-zA-Z0-9_-]{3,15}$/) // (^ 开始边界) ($ 结束边界) ({起始长度 n,结束长度 m} n ~ m)

// 匹配以数字开头, 并以 abc 结尾的字符串
;fn_00([
    '1abc',
    '2abc'
], /^[0-9]abc$/)

// 匹配以数字开头, 数字可多个, 并以 abc 结尾的字符串
;fn_00([
    '123abc',
    '234abc'
], /^[0-9]+abc$/)

// 正则表达式元字符和特性
// 字符匹配
// 普通字符：普通字符按照字面意义进行匹配，例如匹配字母 "a" 将匹配到文本中的 "a" 字符。
// 元字符：元字符具有特殊的含义，例如 \d 匹配任意数字字符，\w 匹配任意字母数字字符，. 匹配任意字符（除了换行符）等。
// 量词
// *：匹配前面的模式零次或多次。
// +：匹配前面的模式一次或多次。
// ?：匹配前面的模式零次或一次。
// {n}：匹配前面的模式恰好 n 次。
// {n,}：匹配前面的模式至少 n 次。
// {n,m}：匹配前面的模式至少 n 次且不超过 m 次。
// 字符类
// [ ]：匹配括号内的任意一个字符。例如，[abc] 匹配字符 "a"、"b" 或 "c"。
// [^ ]：匹配除了括号内的字符以外的任意一个字符。例如，[^abc] 匹配除了字符 "a"、"b" 或 "c" 以外的任意字符。
// 边界匹配
// ^：匹配字符串的开头。
// $：匹配字符串的结尾。
// \b：匹配单词边界。
// \B：匹配非单词边界。
// 分组和捕获
// ( )：用于分组和捕获子表达式。
// (?: )：用于分组但不捕获子表达式。
// 特殊字符
// \：转义字符，用于匹配特殊字符本身。
// .：匹配任意字符（除了换行符）。
// |：用于指定多个模式的选择。

// JavaScript 正则表达式 | https://www.runoob.com/js/js-obj-regexp.html
// Python 正则表达式 | https://www.runoob.com/python/python-reg-expressions.html

;fn_00([
    'runoob',
    'runooob',
    'runoooooob',
], /runoo+b/) // 需 run开头, 接至少2个o, 最后一个 b

;fn_00([
    'runob',
    'runoob',
    'runooob',
    'runoooooob',
], /runoo*b/) // 需 run开头, 接至少1个o, 最后一个 b | 可替换为 /runo+b/

;fn_00([
    'runob',
    'runoob',
    'runooob',
    'runoooooob',
], /runo+b/)

;fn_00([
    'color',
    'colour'
], /colou?r/) // 需 colo, 可选择是否接 u, 最后 r

// 普通字符
const fn_01 = (str, reg) => {
    console.log([...Array(100)].map(v => '-').join(''))
    console.log([...str.match(reg)].join(', '))
    console.log([...str.matchAll(reg)])
}

fn_01('google runoob taobao', /[aeiou]/g)
fn_01('google runoob taobao', /[^aeiou]/g) // 非 aeiou
fn_01('Google Runoob Taobao', /[A-Z]/g) // A-Z
fn_01('Google Runoob Taobao', /./g) // 匹配除换行符（\n、\r）之外的任何单个字符
// 匹配所有。\s 是匹配所有空白符，包括换行，\S 非空白符，不包括换行。
fn_01(`
Google Runoob Taobao
Runoob
Taobao
`, /[\s\S]/g)
fn_01('Google Runoob 123Taobao', /\w/g) // 匹配字母、数字、下划线。等价于 [A-Za-z0-9_]
fn_01('Google Runoob 123Taobao', /\d/g) // 匹配任意一个阿拉伯数字（0 到 9）。等价于 [0-9]
fn_01('Google 456Runoob 123Taobao', /\d+/g) // 匹配任意多个连续阿拉伯数字（0 到 9）。等价于 [0-9]

// 非打印字符

