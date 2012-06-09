(function() {
    "use strict";
    $(document).ready(function(){
        var details = $('#item-details').fadeOut(1400);

        $('#item-type-box').click(function(){
            details.fadeOut();
        });

        $('#item-type-project').click(function(){
            details.fadeIn();
        });
    });
})();
