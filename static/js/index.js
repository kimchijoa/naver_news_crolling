let data_state_url = "/crolling/data/data_state/";
let data_category_count_url = "/crolling/data/category/count/";
let data_crolling_job_info_url = "/crolling/job/info/";
let data_wordcloud_keyword_url = "/crolling/data/wordcloud/";
let category_default = "none";

window.onload = function() { 
    load_dom_content();
    var now = calc_date();
    $("#search_text").val(now);
    $(".search_date").text(now + " 검색 결과");
};

//----------------------------------------------------------------------------------------------------------------------------------------------------------
function calc_date(){
    let today = new Date();
    let yesterday = new Date();
    //yyyy-mm-dd 포맷 날짜 생성
    //해당 내용 함수화 하기
    let r_yesterday = yesterday.getFullYear() + "-" + 
    ((yesterday.getMonth() + 1) > 9 ? (yesterday.getMonth() + 1).toString() : "0" + 
    (yesterday.getMonth() + 1)) + "-" + 
    ((yesterday.getDate()-1) > 9 ? (yesterday.getDate()-1).toString() : "0" + 
    (yesterday.getDate()-1).toString());

    return r_yesterday;
}
function search(){
    var date = $("#search_text").val();
    $(".search_date").text(date + " 검색 결과");
    load_dom_content_search(date);
}
