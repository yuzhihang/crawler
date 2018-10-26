
1. commit 提交格式
Commit message 的格式
每次提交，Commit message 都包括三个部分：Header，Body 和 Footer。

<type>(<scope>): <subject>
// 空一行
<body>
// 空一行
<footer>
其中，Header 是必需的，Body 和 Footer 可以省略。
不管是哪一个部分，任何一行都不得超过72个字符（或100个字符）。这是为了避免自动换行影响美观。
2.1 Header
Header部分只有一行，包括三个字段：type（必需）、scope（可选）和subject（必需）。
（1）type
type用于说明 commit 的类别，只允许使用下面7个标识。
1.  feat：新功能（feature）
2.  fix：修补bug
3.  docs：文档（documentation）
4.  style： 格式（不影响代码运行的变动）
5.  refactor：重构（即不是新增功能，也不是修改bug的代码变动）
6.  test：增加测试
7.  chore：构建过程或辅助工具的变动
如果type为feat和fix，则该 commit 将肯定出现在 Change log 之中。其他情况（docs、chore、style、refactor、test）由你决定，要不要放入 Change log，建议是不要。
（2）scope
scope用于说明 commit 影响的范围，比如数据层、控制层、视图层等等，视项目不同而不同。
（3）subject
subject是 commit 目的的简短描述，不超过50个字符。
1.  以动词开头，使用第一人称现在时，比如change，而不是changed或changes
2.  第一个字母小写
3.  结尾不加句号（.）
