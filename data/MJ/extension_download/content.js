

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function downloadFile(url, fileName) {
    try {
        // 使用 fetch 获取文件内容
        let response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        // 转换为 Blob 对象
        let blob = await response.blob();

        // 创建临时链接下载文件
        let a = document.createElement('a');
        let urlObject = URL.createObjectURL(blob);
        a.href = urlObject;
        a.download = fileName; // 自定义文件名
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        // 释放 URL 对象
        URL.revokeObjectURL(urlObject);
    } catch (error) {
        console.error('Download failed:', error);
    }
}

window.addEventListener('load', async () => {
    await sleep(3000);
    //  for loop the data list
    // let data1 = data.slice(0,2);
    data.forEach(async (item, index) => {
        //  open the detail page
        let url = item.small_img_url
        // let a = document.createElement('a');
        // a.href = url;
        // a.target = "_blank";

        // 使用正则表达式提取 URL 中的特定段 "00159e23-f228-40e1-92d7-6be5343fe8d9"
        let match = url.match(/\/([a-zA-Z0-9-]{36})\//);
        let fileName = match ? match[1] + '.webp' : 'default_name.webp'; // 如果匹配到，就用匹配的结果，否则使用默认名称

        // a.download = fileName; 
        // document.body.appendChild(a);
        // a.click();
        // document.body.removeChild(a);
        downloadFile(url, `${fileName}`);
        await sleep(1000);
    });
});