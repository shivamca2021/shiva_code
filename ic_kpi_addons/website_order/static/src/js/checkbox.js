$(document).ready(function(){
//    Checkbox Is Admin validation to select only one ata a time
    $('[type="checkbox"]').change(function(){

        if(this.checked){
            $('[type="checkbox"]').not(this).prop('checked', false);
        }
    });
});
