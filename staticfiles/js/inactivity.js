//var idleTime = 0;
//$(document).ready(function () {
//  //Increment the idle time counter every minute.
//  var idleInterval = setInterval(timerIncrement, 5000);
//
//  //Zero the idle timer on mouse movement.
//  $(this).mousemove(function (e) {
//    idleTime = 0;
//  });
//  $(this).keypress(function (e) {
//    idleTime = 0;
//  });
//  //Zero the idle timer on touch events.
//  $(this).bind('touchstart', function(){
//   idleTime = 0;
//  });
//  $(this).bind('touchmove', function(){
//   idleTime = 0;
//  });
//});
//
//function timerIncrement() {
//  idleTime = idleTime + 1;
//  console.log(idleTime)
//  if (idleTime > 0) {
//    alert("ok");
//  }
// }

(function() {

    const idleDurationSecs = 6;    // X number of seconds
    const redirectUrl = '/logout';  // Redirect idle users to this URL
    let idleTimeout; // variable to hold the timeout, do not modify

    const resetIdleTimeout = function() {

        // Clears the existing timeout
        if(idleTimeout) clearTimeout(idleTimeout);

        // Set a new idle timeout to load the redirectUrl after idleDurationSecs
        idleTimeout = setTimeout(() => location.href = redirectUrl, idleDurationSecs * 1000);
    };

    // Init on page load
    resetIdleTimeout();

    // Reset the idle timeout on any of the events listed below
    ['click', 'touchstart', 'mousemove'].forEach(evt =>
        document.addEventListener(evt, resetIdleTimeout, false)
    );

})();