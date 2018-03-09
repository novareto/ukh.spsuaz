$(document).ready(function() {

    $("#form-action-speichern").val("Als Entwurf speichern");

    $('#field-form-basicinformation-field-behandlung input:radio').change(function() {
        if ($(this).val() == 'Versand') {
            $("#form-action-speichern").val("Unfallanzeige versenden und speichern");
            $("#form-action-speichern").css("border-width", "8px");
            $("#form-action-speichern").css("border-color", "#58A618");
        }
        if ($(this).val() == 'Entwurf speichern') {
            $("#form-action-speichern").val("Als Entwurf speichern");
            $("#form-action-speichern").css("border-width", "1px");
            $("#form-action-speichern").css("border-color", "#CCCCCC");
        }
    })

});
