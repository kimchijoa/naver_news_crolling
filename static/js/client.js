// GSP정보는 Geolocation API 사용 https://developer.mozilla.org/ko/docs/Web/API/Geolocation_API
// 날씨 API는 OpenWeatherMap https://openweathermap.org/ 참고 https://namjackson.tistory.com/27
//하루 횟수 제한? 있는지 확인해보기

function setCookie(cookie_name, value, days) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + days);
    // 설정 일수만큼 현재시간에 만료값으로 지정
    var cookie_value = escape(value) + ((days == null) ? '' : '; expires=' + exdate.toUTCString() + "; domain=https://www.dogdrip.net");
    document.cookie = cookie_name + '=' + cookie_value;
  }


function showYourLocation(position) {
    var userLat = position.coords.latitude;
    var userLng = position.coords.longitude;
    //api.openweathermap.org/data/2.5/weather?lat={userLat}&lon={userLng}&appid={9849949a54a5f6d166856739c3541ad9};
    var apiURI = "http://api.openweathermap.org/data/2.5/weather?lat=" + userLat + "&lon=" + userLng + "&appid="+"9849949a54a5f6d166856739c3541ad9";
        $.ajax({
            url: apiURI,
            dataType: "json",
            type: "GET",
            async: "false",
            success: function(resp) {
                console.log(resp);

                var now_weather_info = "";
                now_weather_info += "\n" + "현재온도 : "+ Math.round(Number((resp.main.temp- 273.15))) + "ºC";
                now_weather_info += "\n" + "현재습도 : "+ resp.main.humidity;
                now_weather_info += "\n" + "날씨 : "+ resp.weather[0].main.toLowerCase();                
                //now_weather_info += "\n" + "상세날씨설명 : "+ resp.weather[0].description;
                now_weather_info += "\n" + "날씨 이미지 : "+ resp.weather[0].icon;
                //now_weather_info += "\n" + "바람   : "+ resp.wind.speed;
                now_weather_info += "\n" + "나라   : "+ resp.sys.country;
                now_weather_info += "\n" + "도시이름  : "+ resp.name;
                now_weather_info += "\n" + "구름  : "+ (resp.clouds.all) +"%";                 
                console.log(resp)
                //alert(now_weather_info);

                $(".today_weather").empty();
                //$(".today_weather").text(now_weather_info);
                
                $(".today_weather").append("<div class='emotion_title'>오늘의 날씨</div>");
                $(".today_weather").append("<div class='temp'>" +  Math.round(Number((resp.main.temp- 273.15))) + "ºC" +"</div>");
                $(".today_weather").append("<div class='hum'>" + "습도 "+  resp.main.humidity + "%" + "</div>");
                $(".today_weather").append("<img src='img/weather/"  + resp.weather[0].main.toLowerCase() + ".png' >");
                
            }
        })
}



console.dir(navigator.cookieEnabled);
navigator.geolocation
//위치정보 받음
if (navigator.geolocation) { 
    console.log(navigator.geolocation);
    navigator.geolocation.getCurrentPosition(showYourLocation); 
} else { 
    loc.innerHTML = "이 문장은 사용자의 웹 브라우저가 Geolocation API를 지원하지 않을 때 나타납니다!"; 
}





$(".notice_close").click(function(){
    $("#notice").fadeOut(500);
})


function fnMove(my, object_id){
    if (my == "m0") {
        // $(".side_menu").removeClass('select_menu');
        // $(".side_menu").addClass('no_select_menu');
        $('html, body').animate({scrollTop : 0}, 400);
    }
    else{
        // $(".side_menu").removeClass('select_menu');
        // $(".side_menu").addClass('no_select_menu');
        // $("." + my).addClass('select_menu');
        var offset = $("#" + object_id).offset();
        $('html, body').animate({scrollTop : offset.top - 180}, 400);
    }
    
}


$(window).scroll(function(){
    //스크롤 이동시 작동코드
    m_h = 300;
    var offset = [ 0, $("#menu01").offset().top - m_h, $("#menu02").offset().top - m_h, $("#menu03").offset().top - m_h, $("#menu04").offset().top - m_h ];
    console.log($(window).scrollTop());
    var now_top = $(window).scrollTop();

    if ( now_top >= offset[1] &&  now_top <= offset[2])
    {
        $(".side_menu").removeClass('select_menu');
        $(".side_menu").addClass('no_select_menu');
        $(".m1").addClass('select_menu');
    }
    else if ( now_top >= offset[2] &&  now_top <= offset[3])
    {
        $(".side_menu").removeClass('select_menu');
        $(".side_menu").addClass('no_select_menu');
        $(".m2").addClass('select_menu');
    }
    else if ( now_top >= offset[3] &&  now_top <= offset[4])
    {
        $(".side_menu").removeClass('select_menu');
        $(".side_menu").addClass('no_select_menu');
        $(".m3").addClass('select_menu');
    }

    else if ( now_top >= offset[4])
    {
        $(".side_menu").removeClass('select_menu');
        $(".side_menu").addClass('no_select_menu');
        $(".m4").addClass('select_menu');
    }
    else if ( now_top >= offset[0] &&  now_top <= offset[1])
    {
        $(".side_menu").removeClass('select_menu');
        $(".side_menu").addClass('no_select_menu');
    }
});