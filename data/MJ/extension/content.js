// content.js
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'scrape') {
        // 在这里写 scrape 逻辑
        // 比如抓取页面中的内容
        const links = document.querySelectorAll('a.block'); // 获取所有 class 为 .block 的 <a> 标签
        const hrefs = [];

        // 遍历所有找到的 <a> 标签
        links.forEach(link => {
        const href = link.getAttribute('href');  // 获取 href 属性
        if (href) {
            hrefs.push(href);  // 将 href 加入数组
        }
        });

        console.log(hrefs);  // 输出所有 href 属性的数组
        sendResponse({scrapedData: pageData});
    }
  });

  let links = []; 
// 提取页面中的所有 a 标签的 href
function extractLinks() {
    // scrollPage();
    setTimeout(() => {
        const anchors = document.querySelectorAll('a.block');
        anchors.forEach(anchor => {
            const href = anchor.getAttribute('href');
            if (href) {
            links.push(href);  // 存储链接
            }
        });
        console.log(`提取了 ${links.length} 个链接`);
    }, 2000);
}

// 自动点击按钮
function clickButton() {
  const button = document.querySelector('button.min-w-fit');
  if (button) {
    button.click();  // 点击按钮
  }
}

// 将链接保存到文件中（通过与背景脚本通信）
function saveLinksToFile() {
//   chrome.runtime.sendMessage({ action: 'saveLinks', links: links }, function(response) {
//     console.log('Links saved to file:', response);
//   });
if (links.length === 0) {
    console.log("没有可保存的链接");
    return;
  }

  // 创建一个 Blob 对象，将链接保存为文本文件
  const blob = new Blob([links.join("\n")], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);

  // 创建一个下载链接并触发下载
  const a = document.createElement('a');
  a.href = url;
  a.download = 'extracted_links.txt';  // 设置文件名
  document.body.appendChild(a);
  a.click();  // 触发下载
  document.body.removeChild(a);  // 移除临时下载链接

  // 释放 URL 对象
  URL.revokeObjectURL(url);
  console.log("链接已保存为文件");
}
function scrollPage() {
    window.scrollBy(0, 800);  // 每次滚动100px
  }
// 自动点击并提取链接的循环函数
function startClicking() {
  let clickCount = 0;
  const maxClicks = 10000;  // 点击次数

  const interval = setInterval(() => {
    if (clickCount >= maxClicks) {
      clearInterval(interval); // 停止循环
      console.log('点击结束');
      setTimeout(() => {
        saveLinksToFile();
      }, 3000);
      return;
    }

    // 点击按钮并提取链接
    clickButton();
    // scrollPage();
    extractLinks();

    clickCount++;
    console.log(`点击第${clickCount}次，提取了 ${links.length} 个链接`);
    // saveLinksToFile(links);  // 保存链接到文件
  }, 3000);  // 每5秒点击一次



}

// 在页面加载完成后开始执行
window.addEventListener('load', () => {
//    first scroll
    // scrollPage();
    // setTimeout(() => {
    //     extractLinks();
    // }, 2000);
    setTimeout(() => {
        extractLinks();
    }, 5000);
   
//   startClicking();
});
