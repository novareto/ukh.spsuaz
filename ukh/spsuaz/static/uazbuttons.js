$(document).ready(function() {

    $("#form-action-speichern").val("Als Entwurf speichern");

    $('#field-form-basicinformation-field-behandlung input:radio').change(function() {
        if ($(this).val() == 'Versand') {
           $("#form-action-speichern").val("Unfallanzeige versenden und speichern")
        }
        if ($(this).val() == 'Entwurf speichern') {
           $("#form-action-speichern").val("Als Entwurf speichern")
        }
    })

});
