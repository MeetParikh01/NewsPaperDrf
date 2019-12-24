
$.ajax({
                url: '/news/',
                type: 'GET',
                data: {

                },
                success: function (data) {
                    var str =data.Mobile[0].news_body
                    var end = str.indexOf('</p>')
                    $('#fields_body').html(Body(data))
                }
            });


function Body(data){
    htmlData = '';
   $.each( data, function( key, value ) {
            htmlData += '<div class="article_title header_pink">'+
                            '<h2>'+ key+'</h2></div>';

            htmlData += '<div class="category_article_wrapper">'+
                            '<div class="row">'
            $.each( value, function( key, value ) {
                    var news_body = value.news_body
                    var end = news_body.indexOf('</p>')

                    htmlData += '<div class="col-md-4" style="min-height: 620px;margin-top:0px">'+
                                    '<div class="category_article_body">'+
                                        '<div class="top_article_img">'+
                                            '<a href="/news_detail/'+value.id+'" target="_self">'+
                                                '<img class="img-responsive" src="'+value.thumbnail+'" alt="feature-top">'+
                                            '</a>'+
                                        '</div>'+
                                        '<div>'+
                                                '<h5 style="font-size:20px"><a href="/news_detail/'+value.id+'" target="_self">'+value.news_title+'</a></h5>'+
                                        '</div>'+
                                        '<div class="article_date"><a href="/news_detail/'+value.id+'">'+value.date+'</a>,  by: <a href="#">'+value.author+'</a></div>'+
                                        '<div class="category_article_content">'+news_body.slice(0, end+4)+'</div>'+
                                    '</div>'+
                                '</div>';

                });
            htmlData += '</div></div>'

        });
        return htmlData;
}


//function Body(){
//
//   htmlData = '<div class="article_title header_pink">
//        <h2><a href="category.html" target="_self">Tablet Pc</a></h2>
//    </div>
//<div class="category_article_wrapper" >'
//   htmlData += '<div class="col-md-4">'+
//                    '<div class="category_article_body">'+
//                    ''<div class="top_article_img">''
//                        <a href="single.html" target="_self">
//                            <img class="img-responsive" src="assets/img/tab_top2.jpg" alt="feature-top">
//                        </a>
//                    </div>
//                    <!-- top_article_img -->
//
//                    <span class="tag pink"><a href="category.html" target="_self">Tablet</a></span>
//
//                    <div class="category_article_title">
//                        <h2><a href="single.html" target="_self">Technology market see the new Android tablets </a>
//                        </h2>
//                    </div>
//                    <!-- category_article_title -->
//
//                    <div class="article_date"><a href="#">10Aug- 2015</a>, by: <a href="#">Eric joan</a></div>
//                    <!----article_date------>
//                    <!-- article_date -->
//
//                    <div class="category_article_content">
//                        Collaboratively administrate empowered markets via plug-and-play networks. Dynamically
//                        procrastinate B2C users after.
//                    </div>
//                    <!-- category_article_content -->
//
//                    <div class="media_social">
//                        <span><a href="#"><i class="fa fa-share-alt"></i>424 </a> Shares</span>
//                        <span><i class="fa fa-comments-o"></i><a href="#">4</a> Comments</span>
//                    </div>
//                    <!-- media_social -->
//
//                </div>
//                <!-- category_article_body -->
//
//            </div>
// }