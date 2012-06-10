
(function() {
    "use strict";
    $(document).ready(function(){
        var details = $('#item-details');
        details.fadeOut(0)
        if ($('#item-type-project:checked').val()){
            details.fadeIn();
        }
        $('#item-type-box').click(function(){
            details.fadeOut();
        });

        $('#item-type-project').click(function(){
            details.fadeIn();
        });
    });
})();

