var data = [];
var today = new Date();
var yesterday = new Date();
var r_yesterday = yesterday.getFullYear() + 
            "-" + ((yesterday.getMonth() + 1) > 9 ? (yesterday.getMonth() + 1).toString() : "0" + 
            (yesterday.getMonth() + 1)) + "-" + ((yesterday.getDate()-1) > 9 ? (yesterday.getDate()-1).toString() : "0" + 
            (yesterday.getDate()-1).toString());
            
var locate = "/get_yesterday_crolling_sp_info/" + r_yesterday;
$.ajax({ 
    url:locate, 
    type:"GET",
    dataType:"JSON",
    success: function(result) { 
        if (result) 
        { 
            data = result;
            draw_path(data);
        } 

        else{
            console.log("으악 크롤링 데이터를 못들고와써요")
        } 
    } 
});

//var data = [ {"date":1, "close":1},{"date":2, "close":3},{"date":3, "close":2},{"date":4, "close":2} ];
//var data_j = JSON.stringify(data);
function draw_path(data){
    var height=300;
    var svg = d3.select("#svg_02")
                    .append("svg")
                            .attr("width","500")
                            .attr("height",height)

    //y축 정보 추가
    var yscale = d3.scaleLinear()
        .domain([0, d3.max(data, (d) => d.cost_time) + 50]) //실제값의 범위
        .range([height - 20, 20]); //변환할 값의 범위(역으로 처리했음!), 위아래 패딩 20을 줬다!
        

    //x축 정보 추가
    var xscale = d3.scaleBand()
        .domain(data.map((d) => d.idx))
        .range([50, 450]); //변환할 값의 범위(역으로 처리했음!), 위아래 패딩 20을 줬다!

    var line = d3.line()
        .x((d) => xscale(d.idx) +  xscale.bandwidth() / 2)
        .y((d) => yscale(d.cost_time));
    //막대바, x축, y축 그룹 추가
    var group = svg.append('g');
    var x_group = svg.append('g').attr('id',"x_scale");
    var y_group = svg.append('g').attr('id',"y_scale");

    group.append('path')
        .datum(data)
        .attr('fill', 'none') // 라인 안쪽의 색깔을 채울 것인지 지정
        .attr('stroke', 'red') // 라인의 색깔 지정
        .attr('stroke-width', 1) // 라인의 굵기 지정
        .attr('d', line);


    var yAxis = d3.axisLeft()
                .scale(yscale)
                .ticks(4);

    var xAxis = d3.axisBottom()
                .scale(xscale)

    y_group.attr('transform', 'translate(50, 0)') 
            .call(yAxis);
            
    // x 축 추가
    x_group.attr('transform', "translate(0, 280)") 
            .call(xAxis); 

}
