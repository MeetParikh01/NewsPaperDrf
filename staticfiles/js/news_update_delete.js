$("#update_post_button").click(function(){
        event.preventDefault();
        var url = $('#update_post').data('url')
        var id = $('#update_post').data('id')
        var formData = new FormData($('#update_post')[0]);
        formData.delete('news_body')
        formData.append('news_body', CKEDITOR.instances.news_body.getData())
//        for (var pair of formData.entries()) {
//    console.log(pair[0]+ ', ' + pair[1]);
//}
         var csrftoken = getCookie('csrftoken');
         $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            });
        $("#update_post_button").prop("disabled", true);
        $.ajax({
        url: url,
        type: 'PUT',
        processData: false,
        contentType: false,
        data: formData,
        dataType: "json",
        success: function (data) {
           if(data.status == 'success')
           {
            console.log('success')
            window.location.href = '/news_postedby_user/'
           }
           else{
                alert("Please enter valid data")
           }
        }
    });
});



$("#delete_post_button").click(function(){
        event.preventDefault();
        var url = $('#update_post').data('url')
        var id = $('#update_post').data('id')
         var csrftoken = getCookie('csrftoken');
         $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            });

        $.ajax({
        url: url,
        type: 'DELETE',
        data: {

        },
        dataType: "json",

        success: function (data) {
           if(data.status == 'success')
           {
            window.location.href = '/news_postedby_user/'
           }
           else{
                alert("Please enter valid data")
           }
        }
    });
});