$(document).ready(function(){

    var text01 = $('textarea#form-accidentii-field-unfeba1');
    var characters100 = 100;

    checkMaxlength100(text01);

    function checkMaxlength100(vartag){
        vartag.on('keyup change', function(){
            var str = $(this).val();
            if (str.length > characters100){
                $(this).val(str.substr(0,characters100));
                return false;
                }
        });
    }

});
