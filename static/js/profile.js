$("#update_button").click(function(){
        event.preventDefault();
        var url = $('#update').data('url')
        var id = $('#update').data('id')
         var csrftoken = getCookie('csrftoken');
         $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            });

        $.ajax({
        url: url,
        type: 'PUT',
        //contentType: 'application/json',
        data: {
            'username': $('#username').val(),
            'address':$('#address').val().replace(/^\s+|\s+$/g, ''),
            'first_name':$('#first_name').val(),
            'last_name':$('#last_name').val(),
            'email':$('#email').val(),
            'contact':$('#contact').val(),
            'pincode':$('#pincode').val()

        },
        //contentType: "application/json",
        dataType: "json",
        // headers: {
        //     'Accept': 'application/json',
        //     'Content-Type': 'application/json'
        //  },
        success: function (data) {
           if(data.status == 'success')
           {
            window.location.href = '/profile/'+id
           }
           else{
                alert("Please enter valid data")
           }
        }
    });
});

$("#delete_button").click(function(){
        event.preventDefault();
        var url = $('#update').data('url')
        var id = $('#update').data('id')
         var csrftoken = getCookie('csrftoken');
         $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            });

        $.ajax({
        url: url,
        type: 'DELETE',
        //contentType: 'application/json',
        data: {

        },
        //contentType: "application/json",
        dataType: "json",
        // headers: {
        //     'Accept': 'application/json',
        //     'Content-Type': 'application/json'
        //  },
        success: function (data) {
           if(data.status == 'success')
           {
            window.location.href = '/'
           }
           else{
                alert("Please enter valid data")
           }
        }
    });
});