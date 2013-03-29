$(document).ready(function() {
  var querytxtbox = $('#query');
  var defaultQueryVal = 'eg: "CMPT 300 or "Operating Systems"';
  if(!('placeholder' in querytxtbox[0])) {
    querytxtbox.on('blur', function() {
      var val = $.trim(querytxtbox.val());
      if( val === "" ) {
        querytxtbox.val(defaultQueryVal);
      }
    });

    querytxtbox.on('focus', function() {
      var val = querytxtbox.val();
      if(val === defaultQueryVal) {
        querytxtbox.val('');
      }
    });
  }
});