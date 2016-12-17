$(document).ready(function($) {
    $('.modal').on('shown.bs.modal', function() {
      $(this).find('[autofocus]').focus();
    });

    $( "#id_euros" ).focus(function(event) {
        $( window ).scrollTop(0);
        $( "#id_euros" ).val('');
    });
    $( "#id_euros" ).focusout(function(event) {
        $( window ).scrollTop(0);
        var cents = $( "#id_cents" );
        if(!cents.val()) {
            cents.val('00');
        }
        var euros = $( "#id_euros" );
        if(!euros.val()) {
            euros.val('00');
        }
    });
    $( "#id_cents" ).focus(function(event) {
        $( window ).scrollTop(0);
        $( "#id_cents" ).val('');
    });
    $( "#id_cents" ).focusout(function(event) {
        $( window ).scrollTop(0);
        var cents = $( "#id_cents" );
        if (cents.val().length == 1){
            cents.val('0'+cents.val());
        } else if(!cents.val()) {
            cents.val('00');
        }
    });

    $( "#search" ).focus(function(event) {
        $( window ).scrollTop($("#search").offset().top - 100);
        //$( window ).scrollTop(0);
    });
    $( "#search" ).focusout(function(event) {
        //$( window ).scrollTop($("#search").offset().top);
        $( window ).scrollTop($("#page-top").offset().top);
    });
    $( "#search" ).keypress(function(event) {
        $( window ).scrollTop($("#search").offset().top - 100);
        //$( window ).scrollTop(0);
    });

    $('#search').hideseek();
    $(".product").fitText();
});
