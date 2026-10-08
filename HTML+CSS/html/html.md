# HTML 学习笔记

> 重点看代码里面的参数

## 目录

1. [基础标签](#1-基础标签)
2. [强调重要性标签](#2-强调重要性标签)
3. [块级元素和内联元素](#3-块级元素和内联元素)
4. [图片](#4-图片)
5. [路径介绍](#5-路径介绍)
6. [视频](#6-视频)
7. [音频](#7-音频)
8. [超链接](#8-超链接)
9. [锚点标签](#9-锚点标签)
10. [网站结构标签和无语义标签](#10-网站结构标签和无语义标签)
11. [列表标签](#11-列表标签)
12. [表格标签](#12-表格标签)
13. [表单](#13-表单)

---

## 1. 基础标签

```html
<p> </p>
<h1> </h1>
```

## 2. 强调重要性标签

```html
<strong> </strong>
<em> </em>
<ins> </ins>
<del> </del>
```

## 3. 块级元素和内联元素

块级元素可以嵌套内联元素，然后内联元素可以嵌套其他内联元素。

```text
块级元素    <div> </div>
          <h1> </h1>
          <p> </p>

内联元素    <span> </span>
          <a> </a>
          <strong> </strong>
          <em> </em>
```

## 4. 图片

```html
<img src="" alt="" width="" height="" title="">
```

`alt` 是替代网络出现问题的时候显示图片的文字。

## 5. 路径介绍

- `./` 表示当前目录
- `../` 表示上一级目录

## 6. 视频

可能要考虑兼容性问题，注意自动播放和静音。

```html
<video src="" controls autoplay loop muted poster="" width="" height=""> </video>
```

`controls` 显示浏览器自带播放控件。

```html
<!-- 兼容性写法 -->
<video width="400" controls muted loop poster="./media/yu7.jpg">
  <source src="./media/yu7.mp4" type="video/mp4">
  <p> 您的浏览器不支持视频播放 </p>
</video>
```

## 7. 音频

也是要考虑兼容性问题。

```html
1. <audio src="" controls autoplay loop muted> </audio>

2. <!-- 兼容性写法 -->
<audio controls>
  <source src="./media/ldh.mp3" type="audio/mp3">
  <p> 您的浏览器不支持音频播放 </p>
</audio>
```

## 8. 超链接

可以是邮件、下载等链接。

```html
<a href="http://www.deepseek.com/" title="" target="">Deepseek官网 </a>
```

- `title` 是鼠标悬停的时候显示的文字
- `target="_blank"` 在新窗口打开链接而不是覆盖原来的窗口

## 9. 锚点标签

空锚点：

```html
<a href="#">科技论坛</a>
```

创建锚点，然后标记到锚点：

```html
<h2 id="a1"> </h2>
<a href="#a1"> 跳转到锚点 </a>
```

然后为了增加动态滑动的效果，还要再 `<head>` 中添加如下代码：

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>锚点链接</title>
  <!-- 这里复制代码  让页面实现滑动效果 -->
  <style>
    html {
      scroll-behavior: smooth;
    }
  </style>
</head>
```

## 10. 网站结构标签和无语义标签

布局标签：网站结构标签、无语义标签、列表标签。

```html
<h2>网页结构标签</h2>
<header> 网页头部标签<nav>导航栏标签</nav> </header>

<main>
  <aside>侧边栏标签</aside>
  <article>主要内容区域标签</article>
</main>
<footer>页面底部标签</footer>
<section>区块标签</section>
```

**注意这里的 div 通常用来做跨行的布局，span 通常用来做跨列的布局**

```html
<h2>div和span标签</h2>
<div>我是div标签是块级元素</div>
<div>我是div标签是块级元素</div>
<span>我是span标签是行内元素</span>
<span>我是span标签是行内元素</span>
```

## 11. 列表标签

```html
<h2>一.无序列表</h2>
<ul>
  <li>佩奇</li>
  <li>猪爸爸</li>
  <li>猪妈妈</li>
  <li>乔治</li>
</ul>

<h2>二.有序列表（了解即可）</h2>
<ol>
  <li>看视频</li>
  <li>写代码</li>
  <li>做笔记</li>
  <li>多复习</li>
</ol>

<h2>三.描述列表（自定义列表）</h2>
<dl>
  <dt>家电</dt>
  <dd>电视</dd>
  <dd>洗衣机</dd>
  <dd>冰箱</dd>
</dl>
```

## 12. 表格标签

这里的 `thead` `tbody` `tfoot` 的作用是语义作用，更好区分。

`th` 是让里面的文字加粗，水平和垂直居中显示。

```html
<h2>表格结构标签</h2>
<table border="1">
  <thead>
    <tr>
      <th>姓名</th>
      <th>年龄</th>
      <th>成绩</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>张三</td>
      <td>18</td>
      <td>100</td>
    </tr>
    <tr>
      <td>李四</td>
      <td>20</td>
      <td>90</td>
    </tr>
    <tr>
      <td>王五</td>
      <td>22</td>
      <td>80</td>
    </tr>
  </tbody>
</table>
```

## 13. 表单

用于手机用户输入数据，并将数据提交到后端进行处理。

例如：登录、注册、搜索、文件上传。

由表单容器、表单控件、辅助标签（点击标签可以聚焦输入框，更好的用户体验）构成。

表单控件有：`input` 表单（输入、单选、复选）、`textarea` 文本域、`select` 下拉框、`button` 按钮。

```html
<form action="">
  <!-- 1. 单行文本框和密码框 -->
  <ul>
    <li>
      <label>
        账号：
        <!-- 这里的autocomplete属性表示是否启用自动完成功能，off表示禁用自动完成功能，on表示启用自动完成功能。accesskey属性表示快捷键，用户可以通过按下指定的键来快速访问该输入框。 -->
        <input
          type="text"
          placeholder="请输入账号"
          name="username"
          accesskey="s"
          autocomplete="off"
        />
      </label>
    </li>
    <li>
      密码：
      <input
        type="password"
        placeholder="请输入密码"
        name="pwd"
        maxlength="6"
      />
    </li>
    <!-- 2. 单选框 复选框和文件域 -->
    <li>
      性别：
      <!-- label 方式一   for  id 关联 -->
      <input type="radio" name="gender" value="0" checked id="nv" />
      <label for="nv">女</label>
      <input type="radio" name="gender" value="1" id="nan" />
      <label for="nan">男</label>
    </li>
    <li>
      爱好：
      <!-- label 方式二 -->
      <label>
        <!-- 这里的value属性表示复选框的值，checked属性表示复选框默认选中 -->
        <input type="checkbox" name="hobby" value="0" checked /> 足球
      </label>
      <label> <input type="checkbox" name="hobby" value="1" /> 篮球 </label>
      <label>
        <input type="checkbox" name="hobby" value="2" /> 双色球
      </label>
    </li>
    <li>
      头像：
      <!-- 这里的multiple属性表示可以上传多个文件，accept属性表示只允许上传exe和jpg格式的文件 -->
      <input type="file" name="file" multiple accept=".exe,.jpg" />
    </li>
    <!-- 文本域 下拉列表和button按钮 -->
    <li>
      <label>
        留言：
        <textarea
          name="msg"
          cols="30"
          rows="10"
          placeholder="请输入留言"
        ></textarea>
      </label>
    </li>
    <li>
      城市：
      <select name="city" id="">
        <option value="北京">北京</option>
        <option value="上海" selected>上海</option>
        <option value="广州">广州</option>
      </select>
    </li>
    <li>
      <!-- disabled表示禁用按钮 -->
      <button disabled>注册</button>
    </li>
  </ul>
</form>
```

---

> **注意**：`header` 的里面是 `nav`，而不是独立。
