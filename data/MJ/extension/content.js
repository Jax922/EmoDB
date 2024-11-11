

let data = []
let round_counts = 0
let all_counts = 0
let save_round = 0

function simulateRightClick(element) {
    // let element = document.getElementById('targetElement');  // 获取目标元素
  
    if (element) {
      // 创建右键点击事件
      let event = new MouseEvent('contextmenu', {
        bubbles: true,
        cancelable: true,
        view: window,
        button: 2,  // 2 为右键
        clientX: 100, // 右键点击的 X 坐标
        clientY: 100, // 右键点击的 Y 坐标
      });
  
      // 派发事件
      element.dispatchEvent(event);
      setTimeout(() => {
        console.log("right click")
        download_img()
      }, 1000)
    }
  }

function download_img() {
    const menu = document.querySelector("#contextMenu")
    const btns = menu.querySelectorAll("button")
    btns[1].click()
}

function get_info() {
    // imgs
    const img_elems = document.querySelectorAll("div.shadow-2xl")[0].querySelectorAll("img")
    const small_img_url = img_elems[0].src
    const full_img_url = img_elems[1].src
    // prompt
    const prompt_text = document.querySelector("#lightboxPrompt").querySelectorAll("p")[0].innerText
    // create_time
    const create_time = document.querySelectorAll("span.font-medium.relative")[0].title

    simulateRightClick(img_elems[1])
    
    let data_item = {
        small_img_url: small_img_url,
        full_img_url: full_img_url,
        prompt_text: prompt_text,
        create_time: create_time
    }
    data.push(data_item)
}

function save_data() {
    save_round += 1
    const blob = new Blob([JSON.stringify(data)], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `MJ_data_${save_round}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    console.log("data saved")
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}



window.addEventListener('load', async () => {

    //  find the a link
    const anchors = document.querySelectorAll('a.block');
    //  click the first link, enter the detail page
    anchors[0].click();
    await sleep(3000);
    //  get the info of first 10 items
    let all_img_buttons = document.querySelectorAll("img.progress-img")
    for (let i = 0; i < 10; i++) {
        
        all_img_buttons[i].click()
        await sleep(1000)
        get_info()
        round_counts += 1
        all_counts += 1
        await sleep(2000)
    }
    
    all_img_buttons = document.querySelectorAll("img.progress-img")
    while (all_img_buttons.length > 10 && all_counts <= 5000) {
        all_img_buttons[9].click()
        await sleep(1000)
        get_info()
        round_counts += 1
        all_counts += 1
        await sleep(2000); // Ensure sleep for each iteration
        all_img_buttons = document.querySelectorAll("img.progress-img")
        if (round_counts >= 500) {
            // save the data to a json file
            save_data()
            round_counts = 0
        }
    }

    if (all_counts < 5000) {
       all_img_buttons = document.querySelectorAll("img.progress-img")
       for (let i = 0; i < all_img_buttons.length; i++) {
           all_img_buttons[i].click()
           await sleep(1000)
           get_info()
           all_counts += 1
           await sleep(2000); // Ensure sleep for each iteration
       }
    } 

    save_data()
    console.log("all data saved")
    console.log("all counts: ", all_counts)
    
});