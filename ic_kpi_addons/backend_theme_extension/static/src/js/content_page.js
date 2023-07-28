$(document).ready(function(){

    $.ajax({
    type: 'POST',
    url: '/get_state',
    dataType: 'json',
    data : {},
    }).done(function(data){

        company_select= $('#connect').empty();
        company_copyright= $('#copyright').empty();
        company_copyright.html ('<span class="o_footer_copyright_name mr-2" id="copyright">'+'Copyright @'+'  '+data.company_name+ '</span>')
//        company_select.html ('<h5 class="footer_head">Prism</h5><div class="footer_txt">'+data["company_phone"]+'<br/>'+data.company_email+'</div>');
         company_select.html ('<h5 class="mb-3">Connect with us</h5><ul class="list-unstyled"><li><i class="fa fa-comment fa-fw mr-2"/><span><a href="/contactus">Contact us</a></span></li><li><i class="fa fa-envelope fa-fw mr-2"/><span><a href="mailto:"'+data.company_email+'>'+data.company_email+'</a></span></li><li><i class="fa fa-phone fa-fw mr-2"/><span class="o_force_ltr"><a href="tel:"'+data["company_phone"]+'>'+data["company_phone"]+'</a></span></li></ul><div class="s_share text-left" data-snippet="s_share" data-name="Social Media"><h5 class="s_share_title d-none">Follow us</h5><a href="/website/social/facebook" class="s_share_facebook" target="_blank"><i class="fa fa-facebook rounded-circle shadow-sm"/></a><a href="/website/social/twitter" class="s_share_twitter" target="_blank"><i class="fa fa-twitter rounded-circle shadow-sm"/></a><a href="/website/social/linkedin" class="s_share_linkedin" target="_blank"><i class="fa fa-linkedin rounded-circle shadow-sm"/></a><a href="/" class="text-800 float-right"><i class="fa fa-home rounded-circle shadow-sm"/></a></div>');
    })

});