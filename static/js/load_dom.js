function load_dom_content_search(date){
    var $wrap = $("#wrap");
    $wrap.empty();
    $wrap.append("<p id='section_title'><span>Data State</span></p>");
    $wrap.append("<div class='section_wrap section_size_S' id='data_status'>");
        $("#data_status").append("<img src='/static/img/content_loading.gif' height:50 width:50>");
        load_data_state(date, data_state_url + date );  //ajax 함수


    $wrap.append("<p id='section_title'><span>Category Data & Crolling info</span></p>");
    $wrap.append("<div class='section_wrap' id='data_section01'>");
    var $data_section01 = $("#data_section01");
        $data_section01.append("<div class='content'>");
        $data_section01.find('.content').append("<p id='menu_title'>카테고리별 뉴스 현황</p>");
        $data_section01.find('.content').append("<div id='svg_01' class='graph_content'>");
            $("#svg_01").append("<img src='/static/img/content_loading.gif'>");
            load_category_count(date, data_category_count_url + date ); //ajax 함수

        $data_section01.append("<div class='content sec01_sec'>");
        $data_section01.find('.sec01_sec').append("<p id='menu_title'>크롤링 속도 정보</p>");
        $data_section01.find('.sec01_sec').append("<div id='svg_02' class='graph_content'>");
            $("#svg_02").append("<img src='/static/img/content_loading.gif'>");
            load_crolling_job_info(date, data_crolling_job_info_url + date ); //ajax 함수

    $wrap.append("<p id='section_title'><span>WordCloud Data</span></p>");
    $wrap.append("<div class='section_wrap section_size_L' id='data_section02'>");
    var $data_section02 = $("#data_section02");
        $data_section02.append("<div class='content'>");
        $data_section02.find('.content').append("<p id='menu_title'>WordCloud Keyword</p>");
        $data_section02.find('.content').append("<div id='svg_03' class='graph_content'></div>");
            $("#svg_03").append("<img src='/static/img/content_loading.gif'>");

        $data_section02.append("<div class='content sec02_sec'>");
        $data_section02.find('.sec02_sec').append("<p id='menu_title'>Topic</p>");
        $data_section02.find('.sec02_sec').append("<div id='svg_04' class='graph_content'>");
            $("#svg_04").append("<ul class='wc_category_list'>");
            $("#svg_04").find(".wc_category_list").append("<li class='list_title' id='wc_keyword_cat01'><p class='cat_kind_01'></p>종합</li>");
            $("#svg_04").find(".wc_category_list").append("<li class='list_title' id='wc_keyword_cat02'><p class='cat_kind_02'></p>사회</li>");
            $("#svg_04").find(".wc_category_list").append("<li class='list_title' id='wc_keyword_cat03'><p class='cat_kind_03'></p>사건</li>");
            $("#svg_04").find(".wc_category_list").append("<li class='list_title' id='wc_keyword_cat04'><p class='cat_kind_04'></p>경제</li>");
            $("#svg_04").find(".wc_category_list").append("<li class='list_title' id='wc_keyword_cat05'><p class='cat_kind_05'></p>정치</li>");
            $("#wc_keyword_cat01").attr("onclick","load_wordcloud('none')");
            $("#wc_keyword_cat02").attr("onclick","load_wordcloud('c1')");
            $("#wc_keyword_cat03").attr("onclick","load_wordcloud('c2')");
            $("#wc_keyword_cat04").attr("onclick","load_wordcloud('c3')");
            $("#wc_keyword_cat05").attr("onclick","load_wordcloud('c4')");

            $("#svg_04").append("<div class='wc_display'>");
            $("#svg_04").find(".wc_display").append("<div class='content_display'></div>");
            $("#svg_04").find(".wc_display").find(".content_display").append("<img src='/static/img/content_loading.gif'>");
            load_wordcloud_keyword(date, category_default ,data_wordcloud_keyword_url + category_default + "/" + date ); //ajax 함수
}

function load_dom_content(){
    date = calc_date();
    $("#search_text").val(date);
    $(".search_date").text(date + " 검색 결과");
    var $wrap = $("#wrap");
    $wrap.empty();
    $wrap.append("<p id='section_title'><span>Data State</span></p>");
    $wrap.append("<div class='section_wrap section_size_S' id='data_status'>");
        $("#data_status").append("<img src='/static/img/content_loading.gif' height:50 width:50>");
        load_data_state(date, data_state_url + date );  //ajax 함수


    $wrap.append("<p id='section_title'><span>Category Data & Crolling info</span></p>");
    $wrap.append("<div class='section_wrap' id='data_section01'>");
    var $data_section01 = $("#data_section01");
        $data_section01.append("<div class='content'>");
        $data_section01.find('.content').append("<p id='menu_title'>카테고리별 뉴스 현황</p>");
        $data_section01.find('.content').append("<div id='svg_01' class='graph_content'>");
            $("#svg_01").append("<img src='/static/img/content_loading.gif'>");
            load_category_count(date, data_category_count_url + date ); //ajax 함수

        $data_section01.append("<div class='content sec01_sec'>");
        $data_section01.find('.sec01_sec').append("<p id='menu_title'>크롤링 속도 정보</p>");
        $data_section01.find('.sec01_sec').append("<div id='svg_02' class='graph_content'>");
            $("#svg_02").append("<img src='/static/img/content_loading.gif'>");
            load_crolling_job_info(date, data_crolling_job_info_url + date ); //ajax 함수

    $wrap.append("<p id='section_title'><span>WordCloud Data</span></p>");
    $wrap.append("<div class='section_wrap section_size_L' id='data_section02'>");
    var $data_section02 = $("#data_section02");
        $data_section02.append("<div class='content'>");
        $data_section02.find('.content').append("<p id='menu_title'>WordCloud Keyword</p>");
        $data_section02.find('.content').append("<div id='svg_03' class='graph_content'></div>");
            $("#svg_03").append("<img src='/static/img/content_loading.gif'>");

        $data_section02.append("<div class='content sec02_sec'>");
        $data_section02.find('.sec02_sec').append("<p id='menu_title'>Topic</p>");
        $data_section02.find('.sec02_sec').append("<div id='svg_04' class='graph_content'>");
            $("#svg_04").append("<ul class='wc_category_list'>");
            $("#svg_04").find(".wc_category_list").append("<li class='list_title' id='wc_keyword_cat01'><p class='cat_kind_01'></p>종합</li>");
            $("#svg_04").find(".wc_category_list").append("<li class='list_title' id='wc_keyword_cat02'><p class='cat_kind_02'></p>사회</li>");
            $("#svg_04").find(".wc_category_list").append("<li class='list_title' id='wc_keyword_cat03'><p class='cat_kind_03'></p>사건</li>");
            $("#svg_04").find(".wc_category_list").append("<li class='list_title' id='wc_keyword_cat04'><p class='cat_kind_04'></p>경제</li>");
            $("#svg_04").find(".wc_category_list").append("<li class='list_title' id='wc_keyword_cat05'><p class='cat_kind_05'></p>정치</li>");
            $("#wc_keyword_cat01").attr("onclick","load_wordcloud('none')");
            $("#wc_keyword_cat02").attr("onclick","load_wordcloud('c1')");
            $("#wc_keyword_cat03").attr("onclick","load_wordcloud('c2')");
            $("#wc_keyword_cat04").attr("onclick","load_wordcloud('c3')");
            $("#wc_keyword_cat05").attr("onclick","load_wordcloud('c4')");

            $("#svg_04").append("<div class='wc_display'>");
            $("#svg_04").find(".wc_display").append("<div class='content_display'></div>");
            $("#svg_04").find(".wc_display").find(".content_display").append("<img src='/static/img/content_loading.gif'>");
            load_wordcloud_keyword(date, category_default ,data_wordcloud_keyword_url + category_default + "/" + date ); //ajax 함수
}