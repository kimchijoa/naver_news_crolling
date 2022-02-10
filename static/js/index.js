window.onload = function(){
    // var list = [ $('<span>domTest</span>'), $('<span>domTest</span>'), $('<span>domTest</span>') ];    
    // $("#crolling_state").append(list[0]);
    // $("#crolling_state").append(list[1]);
    // $("#crolling_state").append(list[2]);

    let today = new Date();
    let yesterday = new Date();
    //yyyy-mm-dd 포맷 날짜 생성
    //해당 내용 함수화 하기
    let r_yesterday = yesterday.getFullYear() + "-" + ((yesterday.getMonth() + 1) > 9 ? (yesterday.getMonth() + 1).toString() : "0" + (yesterday.getMonth() + 1)) + "-" + ((yesterday.getDate()-1) > 9 ? (yesterday.getDate()-1).toString() : "0" + (yesterday.getDate()-1).toString());
    //alert(r_yesterday);
    //로딩이 떠야 한다.
    let yesterday_info = document.getElementById("data_status");
    let locate = "/total_data/date/" + r_yesterday;
    let load_message = document.getElementById("load_state");
    $.ajax({ 
        url:locate, 
        type:"GET",
        dataType:"JSON",
        success: function(result) { 
            if (result) 
            { 
                
                load_message.innerHTML="로딩이 완료되었습니다. 오늘의 데이터 양 : " + result.length + " 개";
                var i = 0;
                var json_list = ["idx", "n_category", "n_title", "n_e_like", "n_e_good", "n_e_sad", "n_e_angry","n_e_expect"];
                for(i=0; i < 10; i++)
                {
                    var obj_row = document.all["yesterday_info"].insertRow();
                    for(j=0; j < json_list.length; j++)
                    {
                        let td01 = obj_row.insertCell();
                        td01.innerHTML = result[i][json_list[j]]
                    }
                    
                    //console.log(result[i]);
                }
                

            } 

            else{
                load_message.innerHTML="로딩에 실패 하였습니다.";
                //특정 화면에 로딩 실패가 떠야한다.
            } 
        } 
    });
    //====================================================================
    $.ajax({ 
        url:"/check_today_status/" + r_yesterday, 
        type:"GET",
        dataType:"JSON",
        success: function(result) {
            if(result)
            {
                $("#db_count").append("<span>DB COUNT : " + result[0][0]['db_news_cnt'] + "</span>");
                $("#local_count").append("<span>LOCAL COUNT : " + result[1]['local_news_cnt'] + "</span>");
                $("#loss_count").append("<span class='loss_data'>" + (result[1]['local_news_cnt'] - result[0][0]['db_news_cnt']) + "</span>");
                // total_data_file_name.innerHTML = "수집 데이터 파일명 : " + result[2][0]["s3_file_name"];
                // total_data_file_size.innerHTML = "수집 데이터 사이즈 : " + result[2][0]["s3_file_size"];
                // crolling_speed_file_name.innerHTML = "크롤링 속도 측정 파일명 : " + result[2][1]["s3_file_name"];
                // crolling_speed_file_size.innerHTML = "크롤링 속도 측정 파일 사이즈 : " + result[2][1]["s3_file_size"];
                let file_size01 = fileSizePrint(result[2][0]["s3_file_size"]);
                let file_size02 = fileSizePrint(result[2][1]["s3_file_size"]);
                let download_link01 = "https://toenewsdata.s3.ap-northeast-2.amazonaws.com/total_news/" + result[2][0]["s3_file_name"];
                let download_link02 = "https://toenewsdata.s3.ap-northeast-2.amazonaws.com/total_greph_info/" + result[2][1]["s3_file_name"];
                $("#download_data01").append("<a href=' " + download_link01 + "'>" + result[2][0]["s3_file_name"] + file_size01 + "</a><p>");
                $("#download_data02").append("<a href=' " + download_link02 + "'>" + result[2][1]["s3_file_name"] + file_size02 + "</a><p>");
            }
         
            else{
                //load_message.innerHTML="로딩에 실패 하였습니다.";
                //특정 화면에 로딩 실패가 떠야한다.
            } 
        } 
    });

    function fileSizePrint (data)
    {
        var size = "";
        if (data < 1024) size = data + " Byte";
        else if (data < 1024 * 1024) size = parseInt (data / 1024) + " KB";
        else if (data < 1024 * 1024 * 1024) size = parseInt (data / (1024 * 1024)) + " MB";
        else size = parseInt (data / (1024 * 1024 * 1024)) + " GB";
        return "(" + size + ")";
    }

}