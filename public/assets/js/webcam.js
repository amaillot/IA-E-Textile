(function() {

    var streaming = false,
        video        = document.querySelector('#video'),
        cover        = document.querySelector('#cover'),
        canvas       = document.querySelector('#canvas'),
        photo        = document.querySelector('#photo'),
        startbutton  = document.querySelector('#startbutton'),
        width = 1280,
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
        photo.setAttribute('src', data);

        // $.ajax({
        //     type: "POST",
        //     url: "localhost:5000",
        //     data: {
        //        imgBase64: data
        //     },
        //     success: function(response){
        //         var newData = {
        //             "sketch"  : data,
        //             "hint"    : response,
        //             "opacity" : 0.0 /* Opcaity can vary from 0 to 1 */
        //         }

        //         $.ajax({
        //             url         : 'https://dvic.devinci.fr/dgx/paints_torch/api/v1/colorizer',
        //             type        : 'POST',
        //             data        : newData,
        //             contentType : 'application/json; charset=utf-8',
        //             dataType    : 'json',
        //             success     : function(response){
        //                 console.log(response);
        //                 if('colored' in response) {
        //                     let colored = response.color;
        //                     photo.setAttribute('src', colored);
        //                 }
        //             },
        //             error       : function (error) {
        //                 console.log("error");
        //                 console.log(error);
        //             }
        //         })
        //     },
        //     error: function (error) {
        //         console.log("error");
        //         console.log(error);
        //     }
        // });
    }

    startbutton.addEventListener('click', function(ev){
        takepicture();
        ev.preventDefault();
    }, false);

})();