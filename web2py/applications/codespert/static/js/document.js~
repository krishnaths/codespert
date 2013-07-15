function displayResult(item, val, text) {
    console.log(item);
    //$('.alert').show().html('You selected <strong>' + val + '</strong>: <strong>' + text + '</strong>');
}

$(function () {

    $('#product_search').typeahead({
        source: [
		    { id: 1, name: 'Toronto' },
		    { id: 2, name: 'Montreal' },
		    { id: 3, name: 'New York' },
		    { id: 4, name: 'Buffalo' },
		    { id: 5, name: 'Boston' },
		    { id: 6, name: 'Columbus' },
		    { id: 7, name: 'Dallas' },
		    { id: 8, name: 'Vancouver' },
		    { id: 9, name: 'Seattle' },
		    { id: 10, name: 'Los Angeles' }
	    ],
        itemSelected: displayResult
    });

   

    // Mock an AJAX request
    $.mockjax({
        url: '/cities/list',
        responseText: [{ id: 1, name: 'Toronto' },
				    { id: 2, name: 'Montreal' },
				    { id: 3, name: 'New York' },
				    { id: 4, name: 'Buffalo' },
				    { id: 5, name: 'Boston' },
				    { id: 6, name: 'Columbus' },
				    { id: 7, name: 'Dallas' },
				    { id: 8, name: 'Vancouver' },
				    { id: 9, name: 'Seattle' },
				    { id: 10, name: 'Los Angeles' }]
    });

    
});
