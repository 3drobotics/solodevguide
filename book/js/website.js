function redoMarkdown () {
  $('aside').each(function () {
    var $el = $(this);
    $el.html(kramed($el.text()));
  });
}

// Intercept pushstate
(function(history){
    var pushState = history.pushState;
    history.pushState = function(state) {
      setTimeout(redoMarkdown, 0);
      return pushState.apply(history, arguments);
    }
})(window.history);

$(redoMarkdown);
$(window).on('popstate', redoMarkdown);
