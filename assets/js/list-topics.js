async function fetchDiscussions() {
    const repoOwner = "icinfra";
    const repoName = "icinfra-discussions";
    const categorySlug = "general"; // 分类的 slug
  
    // GitHub REST API URL
    const apiUrl = `https://api.github.com/repos/${repoOwner}/${repoName}/discussions`;
  
    try {
      const response = await fetch(apiUrl, {
        method: "GET",
        headers: {
          "Accept": "application/vnd.github.v3+json", // 使用 GitHub Discussions 的 API 版本
        },
      });
  
      if (!response.ok) {
        throw new Error(`GitHub API returned an error: ${response.status}`);
      }
  
      const data = await response.json();
  
      // 过滤出属于指定分类 (categorySlug) 的讨论
      const filteredDiscussions = data.filter(
        (discussion) => discussion.category.slug === categorySlug
      );
  
      const discussionsContainer = document.getElementById("topics-list");
      discussionsContainer.innerHTML = ""; // 清空容器
  
      filteredDiscussions.forEach((discussion) => {
        const discussionItem = document.createElement("div");
        discussionItem.style.display = "flex"; // 使用 flex 布局
        discussionItem.style.justifyContent = "space-between"; // 两端对齐
        discussionItem.style.alignItems = "center"; // 垂直居中
        discussionItem.style.marginBottom = "10px"; // 每个条目之间的间距
        discussionItem.style.whiteSpace = "nowrap"; // 防止换行
  
        discussionItem.innerHTML = `
          <span style="flex: 1;">
            <a href="${discussion.html_url}" target="_blank" style="font-weight: bold; text-decoration: none;">
              ${discussion.title}
            </a>
            <span style="margin: 0 10px;">😊</span>
            <span style="color: #555;">By ${discussion.user.login} on ${new Date(discussion.created_at).toLocaleDateString()}</span>
          </span>
        `;
  
        discussionsContainer.appendChild(discussionItem);
      });
    } catch (error) {
      console.error("Failed to fetch discussions:", error);
      const discussionsContainer = document.getElementById("discussions-list");
      discussionsContainer.innerHTML = `<p>Error loading discussions. Please try again later.</p>`;
    }
  }
  
  fetchDiscussions();