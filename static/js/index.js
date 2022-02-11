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
    let locate = "/crolling/data/data_state/" + r_yesterday;

    //====================================================================
    $.ajax({ 
        url:"/crolling/data/data_state/" + r_yesterday, 
        type:"GET",
        dataType:"JSON",
        success: function(result) {
            if(result)
            {
                $("#data_status").empty();
                $("#data_status").append("<div class='content horizen'></div>");
                var $data_status_inner = $("#data_status").find(".content");
                $data_status_inner.append("<p class='explain_title' id='db_count'><span class='material-icons'>storage</span></p>");
                $data_status_inner.append("<p class='explain_title' id='local_count'><span class='material-icons'>source</span></p>");
                $data_status_inner.append("<p class='explain_title' id='loss_count'>LOSS DATA COUNT: </p>");
                $data_status_inner.append("<p class='explain_title' id='download_data01'><span class='material-icons'>file_download</span>CROLLING DATA : </p>");
                $data_status_inner.append("<p class='explain_title' id='download_data02'><span class='material-icons'>file_download</span>CROLLING SPEED DATA : </p>");

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
                $("#download_data01").append("<a href=' " + download_link01 + "'> " + result[2][0]["s3_file_name"] + file_size01 + "</a><p>");
                $("#download_data02").append("<a href=' " + download_link02 + "'> " + result[2][1]["s3_file_name"] + file_size02 + "</a><p>");
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