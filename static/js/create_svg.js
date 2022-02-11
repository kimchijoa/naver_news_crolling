var data = [];
var today = new Date();
var yesterday = new Date();
var r_yesterday = yesterday.getFullYear() + 
            "-" + ((yesterday.getMonth() + 1) > 9 ? (yesterday.getMonth() + 1).toString() : "0" + 
            (yesterday.getMonth() + 1)) + "-" + ((yesterday.getDate()-1) > 9 ? (yesterday.getDate()-1).toString() : "0" + 
            (yesterday.getDate()-1).toString());
            
var locate = "/crolling/data/category/count/" + r_yesterday;
$.ajax({ 
    url:locate, 
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
    var height_scale =  (d3.max(data, (d) => d.cnt) + 500) / (s_height -40);

    //y축 정보 추가
    var yscale = d3.scaleLinear()
        .domain([0, d3.max(data, (d) => d.cnt) + 500]) //실제값의 범위
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
