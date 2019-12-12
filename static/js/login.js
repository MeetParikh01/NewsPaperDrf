<script>
     $("#save").click(function(){
            event.preventDefault();
             var data = $('#signup').serialize();
             $.post('/login/', data, function(response){

        if (response.status == 'success'){
            window.location.href = " ";
        }
        else
        {
            console.log(response.status)
        }


    })
});
</script>