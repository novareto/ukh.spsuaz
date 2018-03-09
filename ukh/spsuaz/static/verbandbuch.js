$(document).ready(function(){

    $('input#form-field-prsname').attr('maxlength','30');
    $('input#form-field-prsvor').attr('maxlength','30');
    $('input#form-field-diavkt').attr('maxlength','60');
    $('input#form-field-diaadv').attr('maxlength','60');

    $('input#form-field-unfzeit').attr('placeholder', 'HH:MM').mask('99:99');
    $('input#form-field-unfdatum').attr('placeholder', 'TT.MM.JJJJ').mask('99.99.9999');
    $('input#form-field-prsgeb').attr('placeholder', 'TT.MM.JJJJ').mask('99.99.9999');

    var text02 = $('textarea#form-field-unfhg1');
    var characters4000 = 4000;
    checkMaxlength4000(text02);

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
