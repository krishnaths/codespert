
    $(document).ready(function($) {
//	var datas = Handlebars.compile("<div><p><strong>{{value}}</strong></p></div>");
        // Workaround for bug in mouse item selection
        $.fn.typeahead.Constructor.prototype.blur = function() {
            var that = this;
            setTimeout(function () { that.hide() }, 250);
        };
 	console.log(window.location.origin+"/codespert/default/getqs")
        $('#product_search').typeahead({
	     source: function(query,process){ 
		return $.getJSON(
                  "getqs",
                  {q:query},
                  function(data){
			// only search if stop typing for 300ms aka fast typers
			console.log(data);
                      return process(data);
                  }
              );
		 }, 
            items: 5,
	    updater: function (item) {
		    console.log(124);
		    return item;
		},
	    template: ['<div><p><strong>{{value}}</strong></p></div>'],
	    engine: Hogan
	});
    });


