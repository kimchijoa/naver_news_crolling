function load_data_state(date, url_route)
{
     //====================================================================
     $.ajax({ 
        url:url_route,
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
//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
function load_category_count(date, url_route)
{
    $.ajax({ 
        url:url_route, 
        type:"GET",
        dataType:"JSON",
        success: function(result) { 
            if (result) 
            { 
                $("#svg_01").empty();
                data = result;
                draw_rect(data);
            } 
    
            else{
                console.log("으악 크롤링 데이터를 못들고와써요")
            } 
        } 
    });
    function draw_rect(data){
        var color=['red','green','blue','yellow'];
        var svg = d3.select("#svg_01")
                        .append("svg")
                                .attr("width","calc(100% - 20px)")
                                .attr("height","calc(100% - 20px)")
        var s_width = $("#svg_01").width();
        var s_height = $("#svg_01").height();
        //막대 그래프의 높이 비율을 조정한다.
        var height_scale =  (d3.max(data, (d) => d.cnt) + 1000) / (s_height -40);
    
        //y축 정보 추가
        var yscale = d3.scaleLinear()
            .domain([0, d3.max(data, (d) => d.cnt) + 1000]) //실제값의 범위
            .range([s_height-40, 0]); //변환할 값의 범위(역으로 처리했음!), 위아래 패딩 20을 줬다!
        //x축 정보 추가
        var xscale = d3.scaleBand()
            .domain(data.map((d) => d.category)) //실제값의 범위
            .range([50, s_width-50]); //변환할 값의 범위(역으로 처리했음!), 위아래 패딩 20을 줬다!
        //막대바, x축, y축 그룹 추가
        var group = svg.append('g');
        var x_group = svg.append('g').attr('id',"x_scale");
        var y_group = svg.append('g').attr('id',"y_scale");
        //데이터 별로 막대바를 추가
        group.attr("transform","translate(50," + (s_height-40) + ")");
        group.selectAll('rect').data(data)
            .enter().append('rect').attr('class',(d,i)=>color[i])
                                    .attr('x', (d,i)=> xscale.bandwidth()/4 + i*xscale.bandwidth())
                                    .attr('height',10)
                                    .attr('width', xscale.bandwidth()/2)
                                    .attr('y', 10)
                                    .attr('rx',5)
            .transition().duration(2000)
                .attr('height', d=>d.cnt/height_scale)
                .attr('y', d=>-1*d.cnt/height_scale);
        //각 막대별 수치를 삽입
        group.selectAll('text').data(data)
            .enter().append('text').text(d=>d.cnt)
                                    .attr('x', (d,i)=> xscale.bandwidth()/4 + i*xscale.bandwidth() + xscale.bandwidth()/6)
                                    .attr('y', d=>-1*d.cnt/height_scale -10 );
        // y축 추가
        var yAxis = d3.axisLeft()
                    .scale(yscale)
                    .ticks(6);
        var xAxis = d3.axisBottom()
                    .scale(xscale)
        y_group.attr('transform', 'translate(50, 0)') 
                .call(yAxis);
        // x 축 추가
        x_group.attr('transform', "translate(0," + (s_height-40) + ")") 
                .call(xAxis); 
    }
}

function load_crolling_job_info(date, url_route)
{
    $.ajax({ 
        url:url_route, 
        type:"GET",
        dataType:"JSON",
        success: function(result) { 
            if (result) 
            { 
                $("#svg_02").empty();
                data = result;
                draw_path(data);
            } 
   
            else{
                console.log("으악 크롤링 데이터를 못들고와써요")
            } 
        } 
    });
    
    function draw_path(data){
        var svg = d3.select("#svg_02")
                        .append("svg")
                                .attr("width","calc(100% - 20px)")
                                .attr("height","calc(100% - 20px)")
        var s_width = $("#svg_02").width();
        var s_height = $("#svg_02").height();
        //y축 정보 추가
        var yscale = d3.scaleLinear()
            .domain([0, d3.max(data, (d) => d.cost_time) + 50]) //실제값의 범위
            .range([s_height - 40, 0]); //변환할 값의 범위(역으로 처리했음!), 위아래 패딩 20을 줬다!
            
    
        //x축 정보 추가
        //var xscale = d3.scaleBand()
        var xscale = d3.scaleLinear()
            .domain([0, d3.max(data, (d) => d.RNUM)]) 
            //.domain(data.map((d) => d.RNUM))
            //.domain([0,1,2,3,4,5])
            .range([50, s_width-50]); //변환할 값의 범위(역으로 처리했음!), 위아래 패딩 20을 줬다!
    
        var line = d3.line()
            //.x((d) => xscale(d.RNUM) +  xscale.bandwidth() / 2)
            .x((d) => xscale(d.RNUM))
            .y((d) => yscale(d.cost_time));
        //막대바, x축, y축 그룹 추가
        var group = svg.append('g');
        var group_label01 = svg.append('g');
        var group_label02 = svg.append('g');
        var x_group = svg.append('g').attr('id',"x_scale");
        var y_group = svg.append('g').attr('id',"y_scale");
    
        group.append('path')
            .datum(data)
            .attr('fill', 'none') // 라인 안쪽의 색깔을 채울 것인지 지정
            .attr('stroke', 'red') // 라인의 색깔 지정
            .attr('stroke-width', 1) // 라인의 굵기 지정
            .attr('d', line);
    
        group_label01.attr('transform', "translate(" + (s_width-140) + ", 20)");
        group_label01.append('text').text("MAX : " + d3.max(data, (d) => d.cost_time) + "(s)").attr("font-size", "0.9rem").attr("font-weight","700")
        group_label02.attr('transform', "translate(" + (s_width-140) + ", 40)");
        group_label02.append('text').text("AVERAGE : " + Math.round(d3.mean(data, (d) => d.cost_time))  + "(s)").attr("font-size", "0.9rem").attr("font-weight","700")
    
    
        var yAxis = d3.axisLeft()
                    .scale(yscale)
                    .ticks(10);
    
        var xAxis = d3.axisBottom()
                    .scale(xscale)
                    .ticks(10);
    
        y_group.attr('transform', 'translate(50, 0)') 
                .call(yAxis);
                
        // x 축 추가
        x_group.attr('transform', "translate(0," + (s_height-40) + ")") 
                .call(xAxis); 
    }
    
}
//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
function load_wordcloud_keyword(date, category, url_route)
{
    //var data = [];
    var fill_color = [{"사회일반":"#248F57", "사건사고":"#DE214D","경제일반":"#FF4000", "정치일반":"#073191"}];
    var $wordcloud = $("#svg_03");
    $wordcloud.empty();
    $wordcloud.append("<img src='/static/img/content_loading.gif'>");
    var $topic_display = $("#svg_04").find(".content_display");
    $topic_display.empty();
    $topic_display.append("<img src='/static/img/content_loading.gif'>");
                
    var locate = url_route;
    $.ajax({ 
        url:locate, 
        type:"GET",
        dataType:"JSON",
        success: function(result) { 
            if (result) 
            {   
                $("#svg_03").empty();
                $(".content_display").empty();
                $(".content_display").append("<p class='menu_title_small'>Topic Top 5</p>");
                $(".content_display").append("<div class='keyword'></div>");
                $(".content_display").append("<div class='top5_news_list'></div>");
                $(".content_display").append("<div class='emotion_temp'></div>");
                //$("#svg_04").empty();
                data = result[0];
                top5_news_list = result[1];
                emo_data = result[2];
                //console.log(data);
                //console.log(emo_data);
                //console.log(top5_news_list);
                draw_wordcloud(data);
                input_keyword_list(data, emo_data, top5_news_list);

            } 

            else{
                console.log("으악 크롤링 데이터를 못들고와써요")
            } 
        } 
    });


    //data는 keyword, size로 이루어져있음
    function draw_wordcloud(data){
        var svg = d3.select("#svg_03")
                        .append("svg")
                                .attr("width","calc(100% - 20px)")
                                .attr("height","calc(100% - 20px)")

        // var word_c =  d3.words()
        //     .text((d) => d.keyword)
        //     .size((d) => d.size);

        var s_width = $("#svg_03").width();
        var s_height = $("#svg_03").height();
        var size_percent = d3.max(data, (d) => d.count);
        var layout = d3.layout.cloud().size([s_width-10, s_height-10])
            .words(data.map(function(d) { return {text: d.keyword, size:d.count, category:d.n_category}; }))
            .padding(4)        //space between words
            .rotate(0)
            //.fontSize((d) => d.size/size_percent*60 > 17 ?  d.size/size_percent*100 : 17)      // 원본값
            .fontSize((d) => d.size/size_percent*60 > 17 ?  d.size/size_percent*60 : 17)      // font size of words
            .on("end", draw);
        layout.start();

        function draw(data) {
            svg
            .append("g")
                .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
                .selectAll("text")
                .data(data)
                    .enter().append("text")
                    .style("font-size", (d) => d.size)
                    .style("font-weight", "bold")
                    //.style("fill", (d) => fill_color[rand(1, 5)])
                    .style("fill", (d) => fill_color[0][String(d.category)])
                    .attr("text-anchor", "middle")
                    .attr("transform", function(d) {
                        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                    })
                    .text(function(d) { return d.text; });
        }
    }

    function input_keyword_list(data, emo_data, top5_news_list)
    {
        $("#svg_04").css("display","block");
        p_width = $("#svg_04").width();
        p_height = $("#svg_04").width();

        //카테고리별 키워드 생성
        var $display_keyword = $('#svg_04').find('.content_display').find(".keyword");
        for(var i=0; i < 5; i++)
        {
            var key_word = data[i].keyword;
            var key_word_size = data[i].count;
            var num = i+1
            $display_keyword.append("<div class='keyword_list'>[#" + num + "]" + key_word + " : " + key_word_size +"건 </div>");
        }

        //카테고리별 top5 news 리스트 생성
        var $display_news = $('#svg_04').find('.content_display').find(".top5_news_list");
        for(var i=0; i < 5; i++)
        {
            var category = top5_news_list[i].n_category;
            var title = top5_news_list[i].n_title;
            var e_sum = top5_news_list[i].e_sum;
            $display_news.append("<div class='n_list'>[" + category + "]" + title + " // 감정합계 : " + e_sum +"</div>");
        }

        //감정 온도계 생성
        var good_cnt = parseInt(emo_data[0].e_good);  //긍정 count 건
        var bad_cnt = parseInt(emo_data[0].e_bad);  //부정 count 건
        var total_cnt = good_cnt + bad_cnt;
        var good_percent = (good_cnt/total_cnt)*100;
        var bad_percent = (bad_cnt/total_cnt)*100;
        var $temp_emotion_loc = $('#svg_04').find('.emotion_temp');
        $temp_emotion_loc.append("<p class='menu_title_small'>Emotion</p>");
        $temp_emotion_loc.append("<div class='emo_bar'></div>");
        $('#svg_04').find('.emo_bar').append("<div class='good'>" + good_percent.toFixed(1) + "% ( "+ good_cnt + " )</div>");
        $('#svg_04').find('.emo_bar').append("<div class='bad'>" + bad_percent.toFixed(1) + "% ( "+ bad_cnt + " )</div>");
        $('#svg_04').find('.good').css("width",good_percent + "%");
        $('#svg_04').find('.bad').css("width",bad_percent + "%");

    }
}