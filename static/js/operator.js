$(document).ready(function(){
    //fucntion to get the cookie, validation token
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    //reset the html inputs on the purchase ticket webpage
    $('#id__from').on('change',function(){
        $('#id_direction').val('');
        $('#id__to').val('');
        $('#id__to')
            .find('option')
            .remove()
            .end()
            .append('<option value="">Select Travel Direction</option>');
    });
    //loads all the locations given a direction and from via ajax
    $('#id_direction').on('change',function(){     
        //building a request to the server
        $.ajax({
            url: 'getlocations/',
            beforeSending: function(request){
                request.setRequestHeader('Content-Type', 'test/html; charset=utf-8');
            },
            type: 'post',
            data: {csrfmiddlewaretoken: getCookie('csrftoken'),
                location_id: $('#id__from').val(),
                direction: $('#id_direction').val()
            },
            success: function(request){
                location_list = request.location_list;
                console.log(location_list);
                for (let index = 0; index < location_list.length; index++) {
                    console.log(location_list)
                    let newOption = new Option(location_list[index][1],location_list[index][0]);
                    $('#id__to').append(newOption);
                }
            }
        });
    });
    $('.purchaseBtn').on('click',function(e){
        //the purchase clicked row
        tr = e.currentTarget.parentNode.parentNode

        //building a request to the server
        $.ajax({
            url: 'makeTicketPurchase/',
            beforeSending: function(request){
                request.setRequestHeader('Content-Type', 'test/html; charset=utf-8');
            },
            type: 'post',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                bus_run_id : tr.id,
                run_type : tr.children[0].innerHTML,
                from_location : tr.children[1].innerHTML,
                to_location : tr.children[2].innerHTML,
                departure_time : tr.children[3].innerHTML,
                estimated_arrival_time : tr.children[4].innerHTML,
                user_to_from : tr.children[5].id,
                number_of_seats : tr.children[5].innerHTML,
                price : tr.children[6].innerHTML
            },
            success: function(request){
                //generate sweet alert for insufficient credits
                console.log("success");
                $(location).attr('href', window.location.href+"QR/");
            },
            error: function(request, textStatus, errorThrown) { 
                $('#caption').html(request.responseJSON.ERROR_MESSAGE);
            } 
        });
    });
    $('#cancel_ticket').on('click',function(e){
        //building a request to the server
        ticket_id = $('#ticket_from_id').parent()[0].id;
        $.ajax({
            url: 'cancel/',
            beforeSending: function(request){
                request.setRequestHeader('Content-Type', 'test/html; charset=utf-8');
            },
            type: 'post',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                ticket_id
            },
            success: function(request){
                //generate sweet alert for insufficient credits
                console.log('success');
                location.reload();
            } 
        });
    });

    let opts = {
        // Whether to scan continuously for QR codes. If false, use scanner.scan() to manually scan.
        // If true, the scanner emits the "scan" event when a QR code is scanned. Default true.
        continuous: true,
        
        // The HTML element to use for the camera's video preview. Must be a <video> element.
        // When the camera is active, this element will have the "active" CSS class, otherwise,
        // it will have the "inactive" class. By default, an invisible element will be created to
        // host the video.
        video: document.getElementById('preview'),
        
        // Whether to horizontally mirror the video preview. This is helpful when trying to
        // scan a QR code with a user-facing camera. Default true.
        mirror: true,
        
        // Whether to include the scanned image data as part of the scan result. See the "scan" event
        // for image format details. Default false.
        captureImage: true,
        
        // Only applies to continuous mode. Whether to actively scan when the tab is not active.
        // When false, this reduces CPU usage when the tab is not active. Default true.
        backgroundScan: true,
        
        // Only applies to continuous mode. The period, in milliseconds, before the same QR code
        // will be recognized in succession. Default 5000 (5 seconds).
        refractoryPeriod: 5000,
        
        // Only applies to continuous mode. The period, in rendered frames, between scans. A lower scan period
        // increases CPU usage but makes scan response faster. Default 1 (i.e. analyze every frame).
        scanPeriod: 1
      };
    let scanner = new Instascan.Scanner(opts);
    scanner.addListener('scan', function (content) {
        console.log(content);
        user_ticket = content.split(',')
        console.log(user_ticket);
        //username, number_of_seats,busrun_id
        console.log(user_ticket);
        //preparing ajax request to update user ticket to scanned
        //building a request to the server
        $.ajax({
            url: 'ticket/Scan/',
            beforeSending: function(request){
                request.setRequestHeader('Content-Type', 'test/html; charset=utf-8');
            },
            type: 'post',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                username: user_ticket[0],
                number_of_seats: user_ticket[1],
                ticket_id: user_ticket[2]
            },
            success: function(request){
                //generate sweet alert for insufficient credits
                console.log("success",request.status,request.ERROR_MESSAGE);
                if (request.ERROR_MESSAGE != ""){
                    $('#qr_data').html("<p class='btn-danger  text-center' style='color: white; border-radius: 5px; width: 150px; padding: 1px 10px;'>"+request.ERROR_MESSAGE+".</p>");
                }

            },
            error: function(request, textStatus, errorThrown) { 
            } 
        });
        setTimeout(() => {
            $('#qr_data').html("<p class='btn-primary text-center' style='color: white; border-radius: 5px; width: 150px; padding: 1px 10px;'>Please Scan Ticket</p>");
        }, 4000);
        $('#qr_data').html("<p class='btn-success  text-center' style='color: white; border-radius: 5px; width: 150px; padding: 1px 10px;'>Scan Successful.</p>");
    });
    Instascan.Camera.getCameras().then(function (cameras) {
        if (cameras.length > 0) {
        scanner.start(cameras[0]);
        } else {
        console.error('No cameras found.');
        }
    }).catch(function (e) {
    });
});
