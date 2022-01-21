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
                message = request.ERROR_MESSAGE
                if(message == "success"){
                    $(location).attr('href', window.location.href+"QR/");
                }
                else{
                    $('#caption').html(request.ERROR_MESSAGE);
                }
            },
            error: function(request, textStatus, errorThrown) { 
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
});
