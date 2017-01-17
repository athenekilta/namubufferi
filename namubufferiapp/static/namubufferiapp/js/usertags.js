function updateTagsModal() {
  $.get('/tag/').done(function(data) {
            $('#tags').html(data.taglist);
        });
  $('#tags').off('click', 'button');
  $('#tags').on('click', 'button', function(clickevent) {
      var uid = $(clickevent.currentTarget).data('uid');
      $.ajax({
              url:'/tag/'.concat(uid, '/'),
              type: 'DELETE',
              complete: updateTagsModal
            });
    });
}

$(document).ready(function() {
    'use strict';

// Tag auth form is filled by scannerDetector
    // which means there's no reason to directly show
    // it to user.
    $('#tag-auth-form').addClass('hidden');
    ajaxMyShit('#tag-auth-form', function (data) {
        if (typeof(data.redirect) !== 'undefined')
                  window.location.href = data.redirect;
      },
      function(errordata) {
        $('#tag-auth-form').removeClass('hidden');
        if (errordata.errors['tag_uid'][0].code == 'tagnotfound') {
          $('#tag-auth-error').removeClass('hidden');
          $('#tag-auth-error').text(errordata.errors['tag_uid'][0].message);
        }
    });

    // we want to attach scanner detection to whole document, but only
    // in login page. this is done by detecting tag authentication form
    $('#tag-auth-form').parentsUntil('html').scannerDetection(function(data){
        $('#id_tag_uid').val(data);
        $('#tag-auth-form').submit();
      });


    $('#tagModal').on('show.bs.modal', function(event) {
        updateTagsModal();

        $('html').scannerDetection(function(data){
           $.ajax({
                  url:'/tag/'.concat(data, '/'),
                  type: 'POST',
                  complete: updateTagsModal
                });
        });
    });
    $('#tagModal').on('hide.bs.modal', function(event) {
        $('html').scannerDetection(false);
    });

});
