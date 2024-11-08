  
// 监听来自 content script 的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'saveLinks') {
      const links = message.links;
  
      // 创建下载链接
      const blob = new Blob([links.join("\n")], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
  
      // 创建一个隐藏的下载链接并触发下载
      const a = document.createElement('a');
      a.href = url;
      a.download = 'links.txt';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
  
      sendResponse({ status: 'success' });
    }
  });
  