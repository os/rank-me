$(function () {
    // focus "add result" button on load
    $('body.home #add-result-button').focus();

    $('body.add-result').keyup(function(event) {
        var username = $('#nav-user-name').text();

        // press 'w' to set yourself as winner
        if (event.keyCode == 87) {
            if (selectOptionFromText('#id_winner', username)) {
                $('#id_loser').focus();
            }
        }
        // press 'l' to set yourself as loser
        else if (event.keyCode == 76) {
            if (selectOptionFromText('#id_loser', username)) {
                $('#id_winner').focus();
            }
        }
    });

    var selectOptionFromText = function(select, text) {
        var optionFound = false;

        $(select + ' option').each(function(){
            if ($(this).text() == text) {
                $(this).attr('selected', 'selected');
                optionFound = true;

                return false;
            }
        });

        return optionFound;
    };
});
