# Gitbook 
## 1. Gitbook 概述
 GitBook 是一个基于 Node.js 的命令行工具，可使用 Github/Git 和 Markdown 来制作精美的电子书。

所以，GitBook 不是 Markdown 编辑工具，也不是 Git 版本管理工具。市面上我们可以找到很多 Markdown 编辑器，比如 Typora、MacDown、Bear、MarkdownPad、MarkdownX、JetBrains’s IDE（需要安装插件）、Atom、简书、CSDN 以及 GitBook 自家的 GitBook Editor 等等。

<center>
<img src="../img/20180718161741325.png">
</center>

## 2. Gitbook 安装
当你听了我的怂恿 😂，并决定尝试使用 GitBook 的时候，首先面临的问题是 —— 如何搭建 GitBook 环境？

因为 GitBook 是基于 Node.js，所以我们首先需要安装 Node.js（下载地址：https://nodejs.org/en/download/），找到对应平台的版本安装即可。

```shell
node -v
npm -v
```

现在安装 Node.js 都会默认安装 npm（node 包管理工具），所以我们不用单独安装 npm，打开命令行，执行以下命令安装 GitBook：

```shell
npm install -g gitbook-cli
```

安装完之后，就会多了一个 gitbook 命令（如果没有，请确认上面的命令是否加了 -g），输入 `gitbook -V` 查看本版信息（输入该命令可能会继续安装一些东西，不要慌张，等待安装完毕即可）。

## 3. gitbook-editor 安装
如果你对 markdown 很熟悉，那么你可以选择人一个编辑器（记事本也可以）来完成 markdown 文档的编写。如果你是第一次接触 markdown 那么我的建议是你安装一个 gitbook-editor ，虽然现在 gitbook 官方提倡使用 web 版本，不再维护桌面版的 gitbook-editor 了，但是 gitbook-editor 依然是可以使用的。

[gitbook-editor下载地址： https://legacy.gitbook.com/editor](https://legacy.gitbook.com/editor)

## 4. gitbook 常见操作

- `gitbook -V`  查看版本信息
- `gitbook init`  初始化
- `gitbook serve`  本地预览
- `gitbook build`  生成html文件
- `gitbook build --gitbook=2.6.7` 生成指定版本的gitbook，本地没有的话会进行下载
- `gitbook uninstall 2.6.7`  卸载指定版本的gitbook
- `gitbook --help`  显示帮助文档

## 5. 导出各种格式的文档

- `gitbook pdf ./ ./book.pdf`
- `gitbook epub ./ ./book.epub`
- `gitbook mobi ./ ./book.mobi`

## 6. 最后
就先写到这里，后续想起来什么再添加...

<center>
<img src="../img/20190509150744837.jpg">
</center>