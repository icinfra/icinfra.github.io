---
layout: post
title: Github Bookmarklet Quickly Generate New Post Link
date: 2025-04-03 00:00:00 +0800
categories: [blog]
tags: [jekyll, github]
---


# 🚀 在浏览器中快速生成 GitHub 新博客文章链接（使用 Bookmarklet）

## 🎯 背景

在使用 GitHub Pages 构建 Jekyll 博客时，每次创建新博客文章都需要手动填写 `filename` 和 `front matter`。为了解决这个问题，我们可以通过 **Bookmarklet**（书签链接）来自动生成这些内容，快速跳转到 GitHub 创建博客文章页面。

通过这种方式，我们不仅提高了博客发布的效率，还能让这一过程更加简单和快捷。今天我将向大家介绍如何通过 **浏览器书签** 自动生成并跳转到 GitHub 创建新文章页面的链接。

---

## 💡 方案概述

我使用 **Bookmarklet**（书签链接），通过在浏览器中点击一个书签链接来生成一个新的 GitHub 页面链接，并且该链接会自动填充：

- **文件名**：自动生成文件名（例如：`2025-04-03-my-title.md`）
- **内容**：自动填充 Jekyll 标准的 front matter 和模板内容

点击生成的链接后，GitHub 将自动为你打开一个新建博客页面，省去了很多繁琐的步骤。

---

## 🛠️ 步骤一：创建 Bookmarklet 书签

### 1. 打开浏览器的书签栏

- 在浏览器中，确保书签栏已经打开。如果没有打开，可以按下 **Ctrl + Shift + B** 来显示书签栏。

### 2. 创建新的书签

- 右键点击书签栏，选择 **添加书签** 或者 **新建书签**。
- 在弹出的对话框中，填写书签的名称（例如：`一键创建新博客`），然后在 **URL** 部分粘贴以下 JavaScript 代码：

```javascript
javascript:(function(){
  const date = new Date().toISOString().slice(0, 10);
  const file = `${date}-my-title.md`;

  const content = `---
layout: post
title: "Your post's title"
date: ${date} 00:00:00 +0800
categories: [blog]
tags: [web]
---`

  const url = `https://github.com/icinfra/icinfra.github.io/new/main/_posts?filename=${encodeURIComponent(file)}&value=${encodeURIComponent(content)}`;
  window.open(url, '_blank');
})();
```

### 3. 保存书签

- 点击 **保存** 按钮，书签就会出现在书签栏中。

---

## 📝 步骤二：使用 Bookmarklet 生成 GitHub 新博客链接

### 1. 打开书签

- 访问 GitHub Pages 项目的 **`_posts`** 页面创建新文章。
- 在书签栏中点击刚才创建的书签（例如：`一键创建新博客`）。

### 2. 自动生成并打开链接

- 点击书签后，浏览器会自动生成包含文件名和内容的 GitHub 新建页面链接，并在新标签页中打开该链接。

### 3. 修改标题（可选）

- GitHub 新建页面会自动填充文件名和模板内容，你只需修改文章标题和正文内容。

---

## ⚡ 提升效率的小窍门

### 📚 自定义文件名和模板内容
如果你希望在每次使用时能快速更改文件名或模板内容，可以在 Bookmarklet 代码中进行适当修改，例如：

```javascript
const content = `---
layout: post
title: "自定义标题"
date: ${date} 00:00:00 +0800
categories: [自定义分类]
tags: [自定义标签]
---`;

const filename = `${date}-your-custom-title.md`;
```

### 🚀 快速发布
每次点击书签后，GitHub 会直接跳转到新建文章页面，减少了你重复输入文件名和 front matter 的时间。让博客发布变得更加轻松高效。

---

## 🌟 总结

通过 Bookmarklet（书签链接），我们可以轻松在浏览器中创建 Jekyll 博客文章，并自动填充所需的文件名和模板内容。只需一次配置，今后每次发布博客都能节省大量时间。

希望这个小工具能够帮助你提高工作效率。如果你有任何问题，或者希望进一步优化该工具，欢迎在评论区留言讨论！

---

希望这篇指导对你发布博客有帮助！你可以将其直接作为文章发布到你的博客中，帮助更多的读者提高效率！🚀
