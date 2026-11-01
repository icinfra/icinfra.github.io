document.getElementById("create-discussion-button").addEventListener("click", () => {
    const repoOwner = "icinfra";
    const repoName = "icinfra-discussions";
    const categorySlug = "general"; // 替换为 Discussions 分类的 slug
  
    // 动态生成跳转 URL
    const createDiscussionUrl = `https://github.com/${repoOwner}/${repoName}/discussions/new?category=${categorySlug}`;
  
    // 跳转到 GitHub Discussions 创建页面
    window.location.href = createDiscussionUrl;
  });