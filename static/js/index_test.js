window.onload = function(){
    let today = new Date();
    let yesterday = new Date();
    //yyyy-mm-dd 포맷 날짜 생성
    //해당 내용 함수화 하기
    let r_yesterday = yesterday.getFullYear() + "-" + ((yesterday.getMonth() + 1) > 9 ? (yesterday.getMonth() + 1).toString() : "0" + (yesterday.getMonth() + 1)) + "-" + ((yesterday.getDate()-1) > 9 ? (yesterday.getDate()-1).toString() : "0" + (yesterday.getDate()-1).toString());
    //alert(r_yesterday);
    //로딩이 떠야 한다.
    let yesterday_info = document.getElementById("yesterday_info");
    let locate = "/total_data/date/" + r_yesterday;
    let load_message = document.getElementById("load_state");
    $.ajax({ 
        url:locate, 
        type:"GET",
        dataType:"JSON",
        success: function(result) { 
            if (result) 
            { 
                //특정화면에 로딩 성공 떠야한다.
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

    //==================================
     $.ajax({ 
        url:"/check_today_status/" + r_yesterday, 
        type:"GET",
        dataType:"JSON",
        success: function(result) { 
            if (result) 
            { 
                //특정화면에 로딩 성공 떠야한다.
                alert(result)
            } 

            else{
                //load_message.innerHTML="로딩에 실패 하였습니다.";
                //특정 화면에 로딩 실패가 떠야한다.
            } 
        } 
    });

}
let total_search_date_btn = document.getElementById("total_search_date_btn");
//날짜 검색
total_search_date_btn.onclick = function(){
    let search_total_date = document.getElementById("total_search_date").value;

    let locate = "/total_data/date/" + search_total_date;
    $.ajax({ 
        url:locate, 
        type:"GET", 
        success: function(result) { 
            if (result) 
            { 
                alert("불러오기 성공");
                console.log(result);
            } 

            else{ 
                alert("불러오기 실패"); 
            } 
        } 
    });

}