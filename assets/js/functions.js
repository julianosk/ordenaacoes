$(document).ready(function() {
	// call the tablesorter plugin
	
	$("button").button();
	$(".checkfilter").button();
	$(".returncheck").button();
	$(".spinnerfilter").spinner();
	$(".spinnerfilter").each(function() {
		$(this).spinner(($("#c"+this.id).is(':checked')) ? "enable" : "disable");
		// $(this).spinner(!($("#c"+this.id).checked) ? "disable" : "enable");
	});
	$("span.oscillation").each(function() {
		text = $(this).text();
		value = parseFloat(text.substring(1,text.length-2));
		if (value > 0) {
			$(this).addClass("blue");
		} else if (value < 0) {
			$(this).addClass("red");
		}
	});
	$( document ).tooltip({ position: { my: "left", at: "right center" } });
	$( "#recaptcha_widget_div" ).tooltip({ position: { my: "left+25 center", at: "right center" } });

	// var stocksTable = $("#tablecontent:first-child");
	/*$("#stockstable").fixheadertable({
		sortable    : true,
	});*/
	$(".tablesorter").tablesorter({
		sortList: [[1,0],[0,0]],
		widgets: ["stickyHeaders"], 
		textExtraction : function(node) {
			//console.log(node.firstElementChild.innerHTML);
			value = node.innerHTML;
			if (node.children.length > 0){
				var value = node.firstElementChild.innerHTML;
			}
            if (value.indexOf('(')>0){
                return parseFloat(value.substring(0,value.indexOf('(')-1));
            }
            if (isNaN(parseFloat(value))){
                return value;
            }
            return parseFloat(value);
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
				console.log($(this).val()*2+1);
				inds.push(parseInt($(this).val()) + 1);
				console.log(inds[inds.length-1]);
			}
		});
		var sum;
		$(".tablesorter tbody tr").each(function() {
			sum = 0;
			for (ind in inds) {
				// console.log(parseInt($('td:eq('+ inds[ind]
				// +')',this).html()));
				//console.log($('td:eq(' + inds[ind] + ') nobr', this).html());
				sum += parseInt($('td:eq(' + inds[ind] + ') nobr', this).html());
			}

			$('td:eq(' + 1 + ')', this).html(sum);
			// console.log($('td:eq('+ 2 +')',this).html());
		});
		// stocksTable.trigger("update");
		// set sorting column and direction, this will sort on the first and
		// third column
//		var sorting = [ [ 2, 0 ], [ 1, 0 ] ];
//		stocksTable.trigger("update").trigger("sorton", [ sorting ]);
		$(".tablesorter").tablesorter({
			sortList: [[1,0],[0,0]],
			widgets: ["stickyHeaders"], 
			textExtraction : function(node) {
				//console.log(node.firstElementChild.innerHTML);
				value = node.innerHTML;
				if (node.children.length > 0){
					var value = node.firstElementChild.innerHTML;
				}
	            if (value.indexOf('(')>0){
	                return parseFloat(value.substring(0,value.indexOf('(')-1));
	            }
	            if (isNaN(parseFloat(value))){
	                return value;
	            }
	            return parseFloat(value);
			},
		});
		$(".tablesorter").trigger("update");
		//var resort = "";
		//stockstable.trigger("updateCell",[this, resort]);
		return false;
	});
	
	$("#loadingprogress").progressbar({
		value:false,
	});
	var loadingdialog = $( "#loadingdialog" ).dialog({
		dialogClass: "no-close",
		autoOpen: false,
		show: {
			effect: "blind",
			duration: 1000
		},
		hide: {
			effect: "explode",
			duration: 1000
	    }
    });

	$( "#thankdialog" ).dialog({
		autoOpen: false,
		dialogClass: "no-close",
		open: function(event, ui){
	     	setTimeout("$('#thankdialog').dialog('close')",2000);
	    }	
	});    

    $( "#aboutdialog" ).dialog({
      autoOpen: false,
      show: {
        effect: "blind",
        duration: 1000
      },
      hide: {
        effect: "blind",
        duration: 1000
      },
      width: 500,

    });
    $("#aboutlink").click(function() {
		$( "#aboutdialog" ).dialog( "open" );
	});
    var allFields = $( [] ).add( name ).add( email ).add( message );
	$( "#contactdialog" ).dialog({
      autoOpen: false,
      height: 500,
      width: 500,
      modal: true,
      buttons: {
        "Enviar": function() {
          	$.ajax({  
	            type: "POST",  
	            url: "/mail",  
	            data: $("#mailForm").serialize(), 
	            success: function( data ) {
	            	if (data.indexOf("true") >= 0){
	            		$( "#contactdialog" ).dialog( "close" );
	            		$( "#thankdialog" ).dialog("open");
	            		$("#contactError").text("")
	            		allFields.val( "" );
	            		Recaptcha.reload();
	            	} else {
	            		$("#contactError").text("Código informado inválido.");
	            	}
	            }
	        });
	    },
        "Cancelar": function() {
          $( this ).dialog( "close" );
          $("#contactError").text("");
          allFields.val( "" );
        }
      },
      close: function() {
        allFields.val( "" );
      }
      
    });
    $("#contactlink").click(function() {
		$( "#contactdialog" ).dialog( "open" );
	});

    $(".checkfilter").each(function() {
    	$(this).click(function() {
    		$("#"+this.id.substring(1)).spinner((!this.checked) ? "disable" : "enable");
    	});
    });
	
	$("#filterall").click(function() {
		$(".spinnerfilter").spinner("enable");
		$(".checkfilter").prop('checked', true).button("refresh");
	});
	$("#filternone").click(function() {
		$(".spinnerfilter").spinner("disable");
		$(".checkfilter").prop('checked', false).button("refresh");
	});

	$("#aall").click(function() {
		$("input:checkbox[name='inds']").prop('checked', true);
	});

	$("#anone").click(function() {
		$("input:checkbox[name='inds']").prop('checked', false);
	});

	$("#returnall").click(function() {
		$(".returncheck").prop('checked', true).button("refresh");
	});

	$("#returnnone").click(function() {
		$(".returncheck").prop('checked', false).button("refresh");
		// $("#orderchecks").children().first().hide("blind",{}, 1000 );
	});

	$("#brefilter").on("click",function() {
		console.log("refilter!");
		// $( "#loadingdialog" ).dialog( "open" );
		loadingdialog.dialog( "open" );
		$(".tablesorter-stickyHeader").css('visibility','hidden');
		
		$("#tablecontent:first-child").on().hide("slide",{},1500, function callback() {
	        $.ajax({  
	            type: "POST",  
	            url: "/refilter",  
	            data: $("#refilterForm").serialize(), 
	            success: function( data )  
	            {  
	            	loadingdialog.dialog( "close" );
	            	// checkeds = new Array();
	            	reorderchecks = "<div>"
	            	i = 1
	            	$( ".returncheck:checked" ).each(function() {
	            		// console.log($(this).parent().parent().children().first().text());
	            		reorderchecks += "<input id=\"check"+i+"\" TYPE=\"checkbox\" class=\"checkreorder\" NAME=\"inds\" Value=\""+i+"\" checked/> <label for=\"check"+i+"\">"+$(this).parent().parent().children().first().text()+"</label><BR>";
	            		i++;
	            	});
	            	reorderchecks += "</div>"
	            	// console.log(reorderchecks);
	            	
	            	// alert(checkeds);
	            	$("#tablecontent:first-child").html(data).show("slide",{},1500, function callback() {
	            		$("span.oscillation").each(function() {
							text = $(this).text();
							value = parseFloat(text.substring(1,text.length-2));
							if (value > 0) {
								$(this).addClass("blue");
							} else if (value < 0) {
								$(this).addClass("red");
							}
						});
	            		
	            		$("#tablecontent:first-child").trigger("update");
	            		
	            		$(".tablesorter").tablesorter({
							sortList: [[1,0],[0,0]],
							widgets: ["stickyHeaders"], 
							textExtraction : function(node) {
								//console.log(node.firstElementChild.innerHTML);
								value = node.innerHTML;
								if (node.children.length > 0){
									var value = node.firstElementChild.innerHTML;
								}
					            if (value.indexOf('(')>0){
					                return parseFloat(value.substring(0,value.indexOf('(')-1));
					            }
					            if (isNaN(parseFloat(value))){
					                return value;
					            }
					            return parseFloat(value);
							},
						});
	            	});
	            	$("#orderchecks").children().first().hide("blind",{}, 1000, function callback() {
						$("#orderchecks").html(reorderchecks).show("blind",{},1000);
					});
            	}
            });
        });  
	});

});
