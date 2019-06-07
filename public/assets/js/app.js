$(document).ready(function() {
    $('#city-input').on('input', function() {

        $.getJSON("http://api.openweathermap.org/data/2.5/weather?q=" + $(this).val() + ",fr&APPID=fd2539cf97bd0383e7c833647f6c2d7b", {
            zip:11355,
            units:"metric"
        }, function(data) {
            console.log(data);
            $('#startbutton').removeAttr('disabled');
            $('.temperature').append(data.main.temp + '°C');
        }).fail(function() {
            $('#startbutton').attr('disabled', '');
            $('.temperature').empty();
        });
    });
});