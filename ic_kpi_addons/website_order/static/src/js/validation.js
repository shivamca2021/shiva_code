function email_validate(el){
    if (!$("#email_from").val()) {
        return;
    }
    $.ajax({
        type: "POST",
        route: "/check_partner_email",
        params: {
            email: $("#email_from").val(),
        },
    }).done(function (data) {
        if(data.email_exist){
                $("#email_from").value = '';
                alert('Customer Email Already exist. Please try another.Please try another Email Id');
            }
    });
}