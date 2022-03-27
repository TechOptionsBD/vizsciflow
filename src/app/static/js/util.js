jsonArray2Table = function(table, jsonArr) {
	$.each(jsonArr, function (index, value) {
        var row = $('<tr></tr>');
        
        var cell = $("<td>" + value['name'] + "</td>")
       		.css('overflow', 'hidden')
       		.css('word-wrap', 'break-word');
        row.append(cell);
        
    	cell = $('<td></td>');
		data = value['data'];
    	if (!Array.isArray(data)) {
			data = [data];
		}
		var added = false;
    	$.each(data, function (key, val) {		
            var link =  $('<a />', {
                'href': 'javascript:void(0)',
				'text': val['data']
			}).on('click', function() {
				if ((parseInt(value['datatype']) & 0x02) != 0 || (parseInt(value['datatype']) & 0x400) != 0) {
					$.redirect('/datasources', { 'download': val['data'] }, "POST", "_blank");
				}
				else {
					// var w = window.open();
					// $(w.document.body).text(val['data']);
					tasksViewModel.openInDetailsView(val)
				}
            });
            
			if (added)
				cell.append("<br/><br/>");
				
            cell.append(link);
			added = true;
		});
        row.append(cell);
        
        cell = $("<td>" + value['status'] + "</td>");
        cell.css('text-align', 'center');
        if (value['status'] === 'SUCCESS') {
        	cell.css('background-color', 'green')
        		.css('color', 'white');
        }
        else if (value['status'] === 'FAILURE') {
        	cell.css('background-color', 'red')
    			.css('color', 'white');
        }
        row.append(cell);
        table.append(row);
    });
}

function activateTab(tab){
    $('.nav-tabs a[href="#' + tab + '"]').tab('show');
  };
 
 function showXHRText(jqXHR) {
 	if (jqXHR.responseJSON !== undefined && jqXHR.responseJSON.err !== undefined) {
 		$("#error").val(jqXHR.responseJSON.err);
 	}
 	else {
 		$("#error").val(jqXHR.statusText);
 	}
 	activateTab(2);
 }

 
 function printExecStatus(status) {
 	
 	var statusCtrl = $('#execstatus');
 	if (status === 'FAILURE') {
 		statusCtrl.removeClass('badge-primary')
 				.removeClass('badge-secondary')
 				.addClass('badge-danger');
 	}
 	else if (status === 'SUCCESS') {
 		statusCtrl.removeClass('badge-primary')
 			.removeClass('badge-danger')
			    .addClass('badge-secondary');
		}
 	else {
 		statusCtrl.removeClass('badge-secondary')
			.removeClass('badge-danger')
		    .addClass('badge-primary');
 	}
 	statusCtrl.text(status);
 	
 	$('#reportid').text("Runnable Id: " + reportId.toString());
 }
 