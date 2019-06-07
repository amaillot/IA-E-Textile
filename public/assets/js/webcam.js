(function() {

    var streaming = false,
        video        = document.querySelector('#video'),
        cover        = document.querySelector('#cover'),
        canvas       = document.querySelector('#canvas'),
        photo        = document.querySelector('#photo'),
        mask         = document.querySelector('#mask'),
        basePhoto    = document.querySelector("#basePhoto"),
        startbutton  = document.querySelector('#startbutton'),
        width = 700,
        height = 0;

    navigator.getMedia = ( navigator.getUserMedia ||
                        navigator.webkitGetUserMedia ||
                        navigator.mozGetUserMedia ||
                        navigator.msGetUserMedia);

    navigator.getMedia({
        video: true,
        audio: false
    }, function(stream) {
        if (navigator.mozGetUserMedia) {
            video.mozSrcObject = stream;
        } else {
            video.srcObject = stream;
        }
        video.play();
    }, function(err) {
        console.log("An error occured! " + err);
    });

    video.addEventListener('canplay', function(ev){
        if (!streaming) {
            height = video.videoHeight / (video.videoWidth/width);
            video.setAttribute('width', width);
            video.setAttribute('height', height);
            canvas.setAttribute('width', width);
            canvas.setAttribute('height', height);
            streaming = true;
        }
    }, false);

    function takepicture() {
        canvas.width = width;
        canvas.height = height;
        canvas.getContext('2d').drawImage(video, 0, 0, width, height);
        var data = canvas.toDataURL('image/png');
        basePhoto.setAttribute('src', data);
        let sketch = data;
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/getContours",
            data: {
                imgBase64: data
            }
        }).done(function( response ) {

            console.log('return python : ' + response);
            mask.setAttribute('src', 'assets/img/' + response);

            imageToBase64('assets/img/' + response)
                .then(
                    (img64) => {
                        let data = { 'sketch': sketch, 'hint': img64, 'opacity': 1 };
                        data = JSON.stringify(data);
                        $.ajax({
                            url: 'https://dvic.devinci.fr/dgx/paints_torch/api/v1/colorizer',
                            type: 'POST',
                            data: data,
                            contentType: 'application/json; charset=utf-8',
                            dataType: 'json',
                            success: function (res) {
                                //console.log(res);
                                if ('colored' in res) {
                                    let colored = res.colored;
                                    console.log(colored);
                                    photo.setAttribute('src', colored);
                                }
                            },
                            error: function (error) {
                                console.log("error");
                                console.log(error);
                            }
                        })
                    }
                );
        });
    }

    startbutton.addEventListener('click', function(ev){
        takepicture();
        ev.preventDefault();
    }, false);

})();