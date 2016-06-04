
function relocateMenu() {
    var window_top = $(window).scrollTop();
    var div_top = $('#sticky-anchor').offset().top;
    if (window_top > div_top) {
        $('#sticky').addClass('stick');
        $('.dropdown').removeClass('dropup');
        $('#sticky-anchor').height($('#sticky').outerHeight());
        $('.logo-menu-footer-left').addClass('display-visble');
    } else {
        $('#sticky').removeClass('stick');
        $('#sticky-anchor').height(0);
        $('.dropdown').addClass('dropup');
        $('.logo-menu-footer-left').removeClass('display-visble');
    }
}


$(document).ready(function() {
 $(window).scroll(relocateMenu);
    relocateMenu();
    $('#carousel-example-generic').carousel({
        interval: 1000 * 3
    });
 });

 $(function(){
  $.scrollIt({
      upKey: 38,             // key code to navigate to the next section
      downKey: 40,           // key code to navigate to the previous section
      easing: 'linear',      // the easing function for animation
      scrollTime: 600,       // how long (in ms) the animation takes
      activeClass: 'active', // class given to the active nav element
      onPageChange: null,    // function(pageIndex) that is called when page is changed
      topOffset: -60           // offste (in px) for fixed top navigation
    });
});