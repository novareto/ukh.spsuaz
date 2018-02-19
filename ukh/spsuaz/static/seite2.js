$(document).ready(function(){

    var text01 = $('textarea#form-person-field-prsvtr');
    var characters150 = 150;

    checkMaxlength150(text01);

    function checkMaxlength150(vartag){
        vartag.on('keyup change', function(){
            var str = $(this).val();
            if (str.length > characters150){
                $(this).val(str.substr(0,characters150));
                return false;
                }
        });
    }

});
