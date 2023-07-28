odoo.define('website_sale_order.OrderForm', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var current_fs, next_fs, previous_fs; //fieldsets
var opacity;
var current = 1;
var steps = $(".company_info").length;
var ajax = require('web.ajax');
var PaymentForm = require('payment.payment_form');

publicWidget.registry.OrderForm = publicWidget.Widget.extend({
    selector: '.cst_website_order',
    events: {
        'click .add_user_info': '_onAddUserClick',
        'click .remove_user_info': '_onRemoveUserClick',
        'click .next': '_onNextClick',
        'click .previous': '_onPrevClick',
        'click .company_form_submit': '_onSubmitForm',
        'click .user_form_submit': '_onSubmitUserForm',
        'change select[name="country_id"]': '_onChangeCountry',
        'change input[name="email"]': '_onChangeEmail',
    },
    init: function (parent, options) {
        $( "form" ).each(function() {
            var form = this;
            form.addEventListener( "invalid", function( event ) {
                event.preventDefault();
            }, true );
        });
        this._super.apply(this, arguments);
    },
    _onAddUserClick: function($el){
        var $user_div = $($el.currentTarget).parents('div.user_info_div').next('div.user_info_div');
        $user_div.find('.remove_user_info').removeClass('o_hidden')
        $user_div.removeClass('o_hidden');
        $user_div.find('input').prop('required',true);
        $($el.currentTarget).addClass('o_hidden');
    },
    _onRemoveUserClick: function($el){
        $($el.currentTarget).parents().prev('div.user_info_div').find('input').val(" ");
        $($el.currentTarget).parents().prev('div.user_info_div').addClass('o_hidden');
        $($el.currentTarget).addClass('o_hidden');
        $($el.currentTarget).parent().prev('div.user_info_div').find('input').prop('required',false);
        $($el.currentTarget).next('.add_user_info').removeClass('o_hidden');
    },
    _onNextClick: function($el){
        $el.preventDefault();
        var is_allow_submit = 0;

        current_fs = $($el.currentTarget).parents('.company_info');
        next_fs = $($el.currentTarget).parents('.company_info').next();
        const list_email = new Set();
        const error_list_email_syntax = new Set();
        const error_list_email_form_exit = new Set();
        const error_list_email_db_exit = new Set();
        if(current_fs.hasClass('o_web_user_info_div')){
            var user_div_info = current_fs.find('.user_info_div');
            for(var j = 0; j <= user_div_info.length; j++){
                if (!$(user_div_info[j]).hasClass("o_hidden")) {
                    var input_text = $(user_div_info[j]).find("input");
                    for(var i = 0; i <= input_text.length; i++){
                        if (input_text[i] != undefined && !$(input_text[i]).hasClass("o_hidden")){
                            var text = $(input_text[i]).val();
                            if (text.trim().length == 0){
                                input_text[i].setCustomValidity("");
                                $(input_text[i]).addClass('error_input');
                                $(input_text[i]).next('p').removeClass('o_hidden');
                                if ($(input_text[i]).hasClass('email_from')){
                                    $(user_div_info[j]).find('.syntax_error').addClass('o_hidden');
                                    $(user_div_info[j]).find('.email_exit_error').addClass('o_hidden');
                                    $(user_div_info[j]).find('.user_email_exit_error').addClass('o_hidden');
                                }
                                input_text[i].reportValidity();
                                is_allow_submit += 1;
                            } else{
                                $(input_text[i]).removeClass('error_input');
                                $(input_text[i]).next('p').addClass('o_hidden');
                            }
                            if($(input_text[i]).hasClass('email_from')){
                                if (text.trim().length !== 0) {
                                    var user_email = 'user_email_'+j;
                                    // Check for Email Syntax error
                                    var email_validate = this.checkEmail($(input_text[i]), $(user_div_info[j]));
                                    if (email_validate){
                                        error_list_email_syntax.delete(user_email);
                                    }
                                    else{
                                        error_list_email_syntax.add(user_email);
                                        is_allow_submit += 1;
                                    }
                                    // Check in set of list if current email id is present or not
                                    if(list_email.has(text)){
                                        $( "input[name='"+user_email+"']" ).addClass('error_input');
                                        $( "input[name='"+user_email+"']" ).parent().find('.email_exit_error').removeClass('o_hidden');
                                        error_list_email_form_exit.add(user_email);
                                        is_allow_submit += 1;
                                    }else{
                                        if ($("input[name='"+user_email+"']" ).find('error_input')){
                                            $( "input[name='"+user_email+"']" ).removeClass('error_input');
                                            $( "input[name='"+user_email+"']" ).parent().find('.email_exit_error').addClass('o_hidden');
                                            error_list_email_form_exit.delete(user_email);
                                        }
                                    }
                                    // check emial id is present in database
                                    var email_exit_validate = this.checkEmailExist($(input_text[i]), $(user_div_info[j]));
                                    email_exit_validate.then((is_validate) => {
                                        if (is_validate){
                                            error_list_email_db_exit.add(user_email);
                                            is_allow_submit += 1;
                                        }
                                        else{
                                            error_list_email_db_exit.delete(user_email);
                                        }
                                        this.is_allow_next_fs(error_list_email_syntax, error_list_email_form_exit, error_list_email_db_exit, is_allow_submit, next_fs,current_fs);
                                    });

                                    list_email.add(text);
                                }
                            }
                        }
                    }
                }
            }
        } else {
            var input_text = current_fs.find("input");
            var is_allow_submit = 0;
            for(var i = 0; i <= input_text.length; i++){
                if (input_text[i] != undefined){
                    var text = $(input_text[i]).val();
                    if (text.trim().length == 0){
                        input_text[i].setCustomValidity("");
                        input_text[i].reportValidity();
                        $(input_text[i]).addClass('error_input');
                        $(input_text[i]).next('p').removeClass('o_hidden');
                        is_allow_submit += 1;
                    }else{
                        $(input_text[i]).removeClass('error_input');
                        $(input_text[i]).next('p').addClass('o_hidden');
                    }
                    if($(input_text[i]).hasClass('email_from')){
                        if (text.trim().length !== 0) {
                            var user_email = 'user_email_'+j;
                            // Check for Email Syntax error
                            var email_validate = this.checkEmail($(input_text[i]), current_fs);
                            if (email_validate){
                                error_list_email_syntax.delete(user_email);
                            }
                            else{
                                error_list_email_syntax.add(user_email);
                                is_allow_submit += 1;
                            }
                            // check emial id is present in database
                            var email_exit_validate = this.checkEmailExist($(input_text[i]), current_fs);
                            email_exit_validate.then((is_validate) => {
                                if (is_validate){
                                    error_list_email_db_exit.add(user_email);
                                    is_allow_submit += 1;
                                }
                                else{
                                    error_list_email_db_exit.delete(user_email);
                                }
                                this.is_allow_next_fs(error_list_email_syntax, error_list_email_form_exit, error_list_email_db_exit, is_allow_submit, next_fs,current_fs);
                            });
                        }
                    }
                }
            }
        }
    },
    _onPrevClick: function($el){
        current_fs = $($el.currentTarget).parents('.company_info');
        previous_fs = $($el.currentTarget).parents('.company_info').prev();
        //Remove class active
        previous_fs.show();
        current_fs.parents('.cst_website_order').find('.import-data-title').addClass('o_hidden')
        current_fs.parents('.cst_website_order').find('.user-information-title').removeClass('o_hidden')
        current_fs.animate({opacity: 0}, {
            step: function(now) {
                // for making fielset appear animation
                opacity = 1 - now;
                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                previous_fs.css({'opacity': opacity});
            },
            duration: 500
        });
    },
    is_allow_next_fs: function (error_list_email_syntax, error_list_email_form_exit, error_list_email_db_exit, is_allow_submit, next_fs,current_fs){
        if( error_list_email_syntax.size !== 0 || error_list_email_form_exit.size !== 0 || error_list_email_db_exit.size !== 0 ){
            return;
        }
        if(is_allow_submit === 0){
            next_fs.parents('.cst_website_order').find('.import-data-title').removeClass('o_hidden')
            next_fs.parents('.cst_website_order').find('.user-information-title').addClass('o_hidden')
            next_fs.show();
            $('.company_info').removeClass('active');
            next_fs.addClass('active');
            //hide the current fieldset with style
            current_fs.animate({opacity: 0}, {
                step: function(now) {
                    opacity = 1 - now;
                    current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                    });
                    next_fs.css({'opacity': opacity});
                },
                duration: 500
            });
        }
    },
    checkEmailExist: function (input, form) {
        //var isEmailExist= null;
        if (!input.val()) {
            return;
        }
        var that=this;
        return new Promise(function(res, rej){

       that._rpc({
            route: "/check_partner_email",
            params: {
                email: input.val(),
                model: "user_info",
            },
        })
        .then(function (data) {
            if(data.email_exist){
                input.val('');
               input.addClass('error_input');
                form.find('.user_email_exit_error').removeClass('o_hidden');
                input.next('.error').addClass('o_hidden');
                form.find('.syntax_error').addClass('o_hidden');
                form.find('.email_exit_error').addClass('o_hidden');
               res(true);
            }else {
                input.removeClass('error_input');
                form.find('.user_email_exit_error').addClass('o_hidden');
             res(false);
            }
        });
        });
    },
    checkZip: function (input, form) {
        const re = /^(?=.*\d.*)[A-Za-z0-9]{4,10}$/
        if(re.test(input.val().trim())) {
            input.removeClass('error_input');
            form.find('.zip_syntax_error').addClass('o_hidden');
            return true;
        }else {
            input.addClass('error_input');
            form.find('.zip_syntax_error').removeClass('o_hidden');
            input.next('.error').addClass('o_hidden');
            return false;
        }
    },
    checkEmail: function (input, form) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        // check if email id is not in proper email format
        if(re.test(input.val().trim())) {
            input.removeClass('error_input');
            form.find('.syntax_error').addClass('o_hidden');
            return true;
        }else {
            input.addClass('error_input');
            form.find('.syntax_error').removeClass('o_hidden');
            input.next('.error').addClass('o_hidden');
            input.next('.email_exit_error').addClass('o_hidden');
            if (form.find('.user_email_exit_error')){
                form.find('.user_email_exit_error').addClass('o_hidden');
            }
            return false;
        }
    },
    _onSubmitForm:function($el){
        var form = $('#company_info_form');
        var self = this;
        var $_this = $(this);
        this.form_fields = form.serializeArray();
        var form_values = {};
        var is_allow_submit = 0;
        var input_text = form.find(".form-req");
        var $email = form.find('#email_from');
        var $phone = form.find('.phone');
        var $zip = form.find('#zip');
        if ($zip.val().trim().length !== 0){
            var zip_validate = this.checkZip($zip, form);
        }

        for(var i = 0; i <= input_text.length; i++){
            if (input_text[i] != undefined){
                var text = $(input_text[i]).val();
                if (text.trim().length == 0){
                    input_text[i].setCustomValidity("");
                    input_text[i].reportValidity();
                    $(input_text[i]).addClass('error_input');
                    $(input_text[i]).next('p').removeClass('o_hidden');
                    if ($(input_text[i]).has('#email_from')){
                        form.find('.syntax_error').addClass('o_hidden');
                        form.find('.email_exit_error').addClass('o_hidden');
                    }
                    is_allow_submit += 1;
                }else{
                    $(input_text[i]).removeClass('error_input');
                    $(input_text[i]).next('p').addClass('o_hidden');
                }
            }
        }
        if ($email.val().trim().length !== 0){
            var email_validate = this.checkEmail($email, form);

            if(!email_validate){
                is_allow_submit += 1;
            }
        }
        if (email_validate && zip_validate){
            $.each(form.find('input[type=file]'), function (outer_index, input) {
                $.each($(input).prop('files'), function (index, file) {
                    self.form_fields.push({
                        name: input.name,
                        value: file
                    });
                });
            });
            _.each(this.form_fields, function (input) {
                if (input.name in form_values) {
                    if (Array.isArray(form_values[input.name])) {
                        input.setCustomValidity("");
                        input.reportValidity();
                        form_values[input.name].push(input.value);
                    } else {
                        form_values[input.name] = [form_values[input.name], input.value];
                    }
                } else {
                    if (input.value !== '') {
                        form_values[input.name] = input.value;
                    }
                }
            });
            if(is_allow_submit == 0){
                ajax.post(form.attr('action'), form_values)
                .then(function (result_data) {
                     window.location.href = '/website-order/payment-information?partner_id='+result_data;
                });
            }
        }
    },
    _onSubmitUserForm: function($el){
        var form = $('#user_info_form');
        this.form_fields_user = form.serializeArray();
        var self = this;
        var $_this = $(this);
        var input_text = form.find(".form-req");

        for(var i = 0; i <= input_text.length; i++){
            if (input_text[i] != undefined){
                var text = $(input_text[i]).val();
                if (text.trim().length == 0){
                    input_text[i].setCustomValidity("");
                    input_text[i].reportValidity();
                    $(input_text[i]).addClass('error_input');
                    $(input_text[i]).next('p').removeClass('o_hidden');

                }else{
                    $(input_text[i]).removeClass('error_input');
                    $(input_text[i]).next('p').addClass('o_hidden');
                }
            }
        }

        $.each(form.find('input[type=file]'), function (outer_index, input) {
            $.each($(input).prop('files'), function (index, file) {
                self.form_fields_user.push({
                    name: input.name,
                    value: file
                });
            });
        });
        var form_values = {};
        _.each(this.form_fields_user, function (input) {
            if (input.name in form_values) {
                if (Array.isArray(form_values[input.name])) {
                    form_values[input.name].push(input.value);
                } else {
                    form_values[input.name] = [form_values[input.name], input.value];
                }
            } else {
                if (input.value !== '' && input.value.length != 0) {
                    form_values[input.name] = input.value;
                }
            }
        });
        ajax.post(form.attr('action'), form_values)
        .then(function (result_data) {
            if(result_data){
                if(result_data == "C"){
                    alert('Customer import template mismatch');
                }
                else if(result_data == "V"){
                    alert('Vendor import template mismatch');
                }else if(result_data == "E"){
                    alert('Employee import template mismatch');
                }
                else if(result_data == "C_M"){
                    alert("Customer import file type must be ('XLS','XLSX','CSV')");
                }
                else if(result_data == "V_M"){
                    alert("Vendor import file type must be ('XLS','XLSX','CSV')");
                }else if(result_data == "E_M"){
                    alert("Employee import file type must be ('XLS','XLSX','CSV')");
                }
                else{
                window.location.href = '/website-order/thank-you';
                }
            }
        });
    },
    _onChangeCountry:function($el){
        if (!$("#country_id").val()) {
            return;
        }
        this._rpc({
            route: "/shop/country_infos/" + $("#country_id").val(),
            params: {
                mode: $("#country_id").attr('mode'),
            },
        }).then(function (data) {
            var selectStates = $("select[name='state_id']");
            // dont reload state at first loading (done in qweb)
            if (selectStates.data('init')===0 || selectStates.find('option').length >= 1) {
                if (data.states.length || data.state_required) {
                    selectStates.html('');
                    _.each(data.states, function (x) {
                        var opt = $('<option>').text(x[1])
                            .attr('value', x[0])
                            .attr('data-code', x[2]);
                        selectStates.append(opt);
                    });
                    selectStates.parent().parent('div').show();
                } else {
                    selectStates.val('').parent().parent('div').hide();
                }
                selectStates.data('init', 0);
            } else {
                selectStates.data('init', 0);
            }
        });
    },
    _onChangeEmail:function($el){
        if (!$("#email_from").val()) {
            return;
        }
        this._rpc({
            route: "/check_partner_email",
            params: {
                email: $("#email_from").val(),
            },
        }).then(function (data) {
            if(data.email_exist){
                $("#email_from").val('');
                $("#email_from").addClass('error_input');
                $('#company_info_form').find('.email_exit_error').removeClass('o_hidden');
                $('#company_info_form').find('.syntax_error').addClass('o_hidden');
                $("#email_from").next('.error').addClass('o_hidden');
            }else {
                $("#email_from").removeClass('error_input');
                $('#company_info_form').find('.email_exit_error').addClass('o_hidden');
            }
        });
    },
});
PaymentForm.include({
    /**
     * @override
     */
    payEvent: function (ev) {
        ev.preventDefault();
        var $checkedRadio = this.$('input[type="radio"]:checked');
        //this._super.apply(this, arguments);
        // first we check that the user has selected a authorize as s2s payment method
        var acquirer_id = this.getAcquirerIdFromRadio($checkedRadio);
        var acquirer_form = false;
        if (this.isNewPaymentRadio($checkedRadio)) {
            acquirer_form = this.$('#o_payment_add_token_acq_' + acquirer_id);
        } else {
            acquirer_form = this.$('#o_payment_form_acq_' + acquirer_id);
        }
        var inputs_form = $('input', acquirer_form);
        var form_data = this.getFormData(inputs_form);
        console.log(form_data);
        if ("bank_name" in form_data){
            this._rpc({
                route: "/update/partner/bank_details",
                params: form_data,
            }).then(function (data) {
                window.location.href = data['redirect_url'];
            });
        } else {
            this._super.apply(this, arguments);
        }
    },
    /**
     * @override
     */
    updateNewPaymentDisplayStatus: function () {
        console.log('override');
        this._super.apply(this, arguments);
        var checked_radio = this.$('input[type="radio"]:checked');
        // we hide all the acquirers form
        this.$('[id*="o_payment_add_token_acq_"]').addClass('d-none');
        this.$('[id*="o_payment_form_acq_"]').addClass('d-none');
        if (checked_radio.length !== 1) {
            return;
        }
        checked_radio = checked_radio[0];
        var acquirer_id = this.getAcquirerIdFromRadio(checked_radio);
        
        //var acquirer_id = $(checked_radio).data('acquirer-id');
        console.log(acquirer_id);
        // if we clicked on an add new payment radio, display its form
        if (this.isNewPaymentRadio(checked_radio)) {
            this.$('#o_payment_add_token_acq_' + acquirer_id).removeClass('d-none');
        }
        else if (this.isFormPaymentRadio(checked_radio)) {
            this.$('#o_payment_form_acq_' + acquirer_id).removeClass('d-none');
        }
    },
});
});
