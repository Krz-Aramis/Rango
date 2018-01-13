$(document).ready( function() {

    $('#likes').click(function(){
        // get the id from the button attribute
        catid = $(this).attr("data-catid");

        $.ajax({
            //The URL to process the request
              url : '/rango/like_category/',
              dataType: "text",
            //  crossDomain: true,
            //The type of request, also known as the "method" in HTML forms
            //Can be 'GET' or 'POST'
              type : 'GET',
            //Any post-data/get-data parameters
            //This is optional
              data : {
                'category_id' : catid
              },
            //The response from the server
              success : function(data) {
                //You can use any jQuery/JavaScript here!!!

                $('#like_count').html(data);
                $('#likes').hide();
              },
              error: function (request, status, error) {
                console.log('req: ' + request.responseText);
                console.log('status: ' + status)
                console.log('error: ' + error)
                }
            });
        console.log('done?');
    });

    /* for future reference
    $('#example').click(
        function(){
            $.get('/rango/test', {},
            function(data){
                console.log('data');
            }
        );
        }
    );
    */

});
