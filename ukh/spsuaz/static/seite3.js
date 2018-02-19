$(document).ready(function(){

    var text01 = $('textarea#form-accidenti-field-unfkn1');
    var text02 = $('textarea#form-accidenti-field-unfhg1');
    var text03 = $('textarea#form-accidenti-field-unfort');
    var characters80 = 80;
    var characters240 = 240;
    var characters4000 = 4000;

    checkMaxlength80(text03);
    checkMaxlength240(text01);
    checkMaxlength4000(text02);

    function checkMaxlength80(vartag){
        vartag.on('keyup change', function(){
            var str = $(this).val();
            if (str.length > characters80){
                $(this).val(str.substr(0,characters80));
                return false;
                }
        });
    }

    function checkMaxlength240(vartag){
        vartag.on('keyup change', function(){
            var str = $(this).val();
            if (str.length > characters240){
                $(this).val(str.substr(0,characters240));
                return false;
                }
        });
    }

    function checkMaxlength4000(vartag){
        vartag.on('keyup change', function(){
            var str = $(this).val();
            if (str.length > characters4000){
                $(this).val(str.substr(0,characters4000));
                return false;
                }
        });
    }

});
