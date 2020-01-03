function ClickLogin()
{
    clicked=true;
}
var token = ''
function onSignIn(googleUser) {
        if(clicked){
            var  profile = googleUser.getAuthResponse()
        var token = 'Bearer '+profile.id_token
        console.log(token)
        var csrftoken = getCookie('csrftoken');
         $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("Http-Authentication", token),
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            });
         $.ajax({
            url: '/login/',
            type: 'POST',
            data: {

            },
            dataType: "json",
            contentType: 'json',
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
        }

        }
function signOut() {
var auth2 = gapi.auth2.getAuthInstance();
auth2.signOut().then(function () {
  console.log('User signed out.');
});
}


