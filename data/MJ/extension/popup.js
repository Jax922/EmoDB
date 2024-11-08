document.getElementById('scrape').addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {action: 'scrape'}, function(response) {
        console.log(response)
        })
    })
})

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'api_response') {
      console.log('收到 API 响应数据:', message.data);
      // 处理 API 返回的数据
    }
  });