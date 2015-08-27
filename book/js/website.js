$(function () {
  $('aside').each(function () {
    var $el = $(this);
    $el.html(kramed($el.text()));
  });
});
