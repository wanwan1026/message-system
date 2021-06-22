function post(){
    let file = document.getElementById("file").files[0];

    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function(){
        let file = document.getElementById("file").files[0];
        // 獲取檔名
        let file_name = file["name"]
        // 獲取檔案類型
        let file_type = file["type"]
   
        imgfile = reader.result;
        imgfile = imgfile.split(",")
        // 獲取圖片base64編碼
        imgfile = imgfile[1]
        
        // 取得貼文的內容
        let post_text = document.getElementById("post_text").value

        // 總括
        post_data = {
            "filename":file_name,
            "filetype":file_type,
            "imgfile":imgfile,
            "posttext":post_text
        }
        console.log(post_data)
        
        let primeAPIurl = 'http://127.0.0.1:3000//userpost';
        fetch(primeAPIurl,{
            method:'POST',
            body:JSON.stringify(post_data),
            headers:{
                "Content-Type": "text/html;charset=utf-8"
            }
        })
        .then(function(data) {
            return data.text();
        }).then(function(res) {
            console.log(res)
            window.location.reload();
        })
    }

}