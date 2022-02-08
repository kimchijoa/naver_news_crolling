var data = [];
var fill_color = ["","#248F57","#FF4000","#DE214D","#073191","#A1B4E0"];

function rand(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

var today = new Date();
var yesterday = new Date();
var r_yesterday = yesterday.getFullYear() + 
            "-" + ((yesterday.getMonth() + 1) > 9 ? (yesterday.getMonth() + 1).toString() : "0" + 
            (yesterday.getMonth() + 1)) + "-" + ((yesterday.getDate()-1) > 9 ? (yesterday.getDate()-1).toString() : "0" + 
            (yesterday.getDate()-1).toString());
            
var locate = "/get_yesterday_crolling_data/wordcloud/" + r_yesterday;
$.ajax({ 
    url:locate, 
    type:"GET",
    dataType:"JSON",
    success: function(result) { 
        if (result) 
        {   console.log(result[0]);
            $("#svg_03").empty();
            $("#svg_04").empty();
            data = result[0];
            emo_data = result[1];
            draw_wordcloud(data);
            input_keyword_list(data, emo_data);

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
    var size_percent = d3.max(data, (d) => d.size);
    var layout = d3.layout.cloud().size([s_width-10, s_height-10])
        .words(data.map(function(d) { return {text: d.keyword, size:d.size}; }))
        .padding(4)        //space between words
        .rotate(0)
        .fontSize((d) => d.size/size_percent*60 > 17 ?  d.size/size_percent*100 : 17)      // font size of words
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
                .style("fill", (d) => fill_color[rand(1, 5)])
                .attr("text-anchor", "middle")
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) { return d.text; });
      }
}

function input_keyword_list(data, emo_data)
{
    $("#svg_04").css("display","block");
    p_width = $("#svg_04").width();
    p_height = $("#svg_04").width();
    console.log(emo_data);
    console.log(emo_data[0]);
    console.log(emo_data[0].emotion_good_cnt);
    console.log(emo_data[0].emotion_bad_cnt);
    console.log(emo_data[0]);
    var good_cnt = emo_data[0].emotion_good_cnt;
    var bad_cnt = emo_data[0].emotion_bad_cnt;
    var total_cnt = good_cnt + bad_cnt;
    var good_percent = (good_cnt/total_cnt)*100;
    var bad_percent = (bad_cnt/total_cnt)*100;

    $("#svg_04").append("<div class='emo_bar'></div>");
    $(".emo_bar").append("<div class='good'>" + good_percent.toFixed(1) + " % ( " + good_cnt + " 건 )" + "</div>");
    $(".emo_bar").append("<div class='bad'>" + bad_percent.toFixed(1) + " % ( " + bad_cnt + " 건 )"+ "</div>");
    $(".good").css("width",good_percent + "%");
    $(".bad").css("width",bad_percent + "%");

    for(var i=0; i < 32; i++)
    {
        var key_word = data[i].keyword;
        var key_word_size = data[i].size;
        var num = i+1
        $("#svg_04").append("<div class='keyword_list'>[#" + num + "]" + key_word + " : " + key_word_size +"건 </div>");
    }
}

