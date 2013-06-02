$(document).ready(function() {
	// call the tablesorter plugin
	var stocksTable = $("#stockstable");
	stocksTable.tablesorter({
		widgets : [ 'zebra' ],
		textExtraction : function(node) {
//		console.log(node.innerHTML)
//		console.log(node.innerHTML.indexOf('('))
//            if(node.childNodes[0]){
//		        return node.childNodes[0].innerHTML;
//		    }
//http://motherrussia.polyester.se/pub/jquery/demos/extraction/
            var jQueryNode = $(node);
 
            if ($('a', jQueryNode)) {
                return $('a', jQueryNode).text();
            }
//            if ($('a', node)) {
//                console.log('aqui')
//                return $('a', node).text();
//            }
            var aa = parseFloat(node.innerHTML.substring(0,node.innerHTML.indexOf('(')-1));
		    return aa;
		},
	});

	$("#formreorder").submit(function() {
		return false;
	});

	$("#breorder").click(function() {
		// $('td:nth-child(3), th:nth-child(3)').hide(1500)
		var inds = new Array();
		$("input:checkbox[name='inds']").each(function() {
			// console.log($(this).val()+" "+$(this).is(":checked"));
			if ($(this).is(":checked")) {
				// console.log($(this).val()*2+1);
				inds.push(parseInt($(this).val()) * 2 + 1);
				// console.log(inds[inds.length-1]);
			}
		});
		var sum;
		$("#stockstable tbody tr").each(function() {
			sum = 0;
			for (ind in inds) {
				// console.log(parseInt($('td:eq('+ inds[ind]
				// +')',this).html()));
				sum += parseInt($('td:eq(' + inds[ind] + ')', this).html());
			}

			$('td:eq(' + 2 + ')', this).html(sum);
			// console.log($('td:eq('+ 2 +')',this).html());
		});
		// stocksTable.trigger("update");
		// set sorting column and direction, this will sort on the first and
		// third column
//		var sorting = [ [ 2, 0 ], [ 1, 0 ] ];
//		stocksTable.trigger("update").trigger("sorton", [ sorting ]);
		stocksTable.tablesorter({
			widgets : [ 'zebra' ], sortList: [[2,0],[1,0]] 
		});
		// stocksTable.trigger("update");
		return false;
	});

	$("#ball").click(function() {
		$("input:checkbox[name='inds']").attr('checked', true);
	});

	$("#bnone").click(function() {
		$("input:checkbox[name='inds']").attr('checked', false);
	});

	// $("#stockstable tbody tr").each(function(){
	// console.log($('td:eq('+ 1 +')',this).html());
	// });
});
