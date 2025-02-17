addLink = function(val){
	return $('<a />', {
		'href': 'javascript:void(0)',
		'text': val.data
	}).on('click', function() {
		if ((parseInt(val.datatype) & 0x02) != 0 || (parseInt(val.datatype) & 0x400) != 0  || (parseInt(val.datatype) & 0x01) != 0 || (parseInt(val.datatype) & 0x800) != 0 || (parseInt(val.datatype) & 0x1000) != 0 ) {
			// var w = window.open();
			// $(w.document.body).text(val['data']);
			tasksViewModel.openInDetailsView(val);
		}
		else {
			$.redirect('/datasources', { 'download': val.data }, "POST", "_blank");
		}
	});
}

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
			datavals = val.data;
            if (!Array.isArray(datavals)) {
				datavals = [datavals];
			}

			$.each(datavals, function (key, dataval) {
				let linkval = { 'data': dataval, 'datatype': val.datatype, 'id': val['id']};
				link = addLink(linkval);
				if (added)
					cell.append("<br/><br/>");
				
	            cell.append(link);
				added = true;
			});
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
        
		time = parseFloat(value['duration']) * 1000;
		cell = $("<td>" + time.toFixed(1) + " ms" + "</td>");
        row.append(cell);

		cell = $("<td>" + "</td>");
		var button = $('<input type="button" value="Log..." />');
		button.attr('id', value['id']);
		button.click(function() {
			taskId = parseInt(this.getAttribute('id'));
			var oReq = new XMLHttpRequest();
			oReq.open('GET', '/runnables' + "?" + 'tasklogs=' + taskId, true);
			oReq.responseType = "arraybuffer";

			oReq.send();
			//self.itemName(data.data);
			oReq.onload = function (oEvent) {
				if (this.status == 200) {
					var arrayBuffer = oReq.response;
					var blob = new Blob([arrayBuffer], { type: "text/plain" });
					itemSrc = URL.createObjectURL(blob);
					tasksViewModel.setItemSrc(itemSrc);
				}
			}
		});
		button.appendTo(cell);

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
 	else if (jqXHR.status == 0){
		$("#error").val("Error occured in AJAX call. Check your internet connection, VPN connectivity, Ad blocker blocking the call or access is denied due to cross-site scripting."); 
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
 
 function clearResults() {
	$("#output").val("");
	$("#error").val("");
	$("#log tbody").empty();
	$("#duration").text("0 ms");
	printExecStatus("");
}

 function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function isJson(item) {
	item = typeof item !== "string" ? JSON.stringify(item) : item;

	try {
		item = JSON.parse(item);
	} catch (e) {
		return false;
	}

	return (typeof item === "object" && item !== null);
}

function centerDialog(dlg) {
	var windowHeight = $(window).height();
	var windowWidth = $(window).width();
	var boxHeight = dlg.height();
	var boxWidth = dlg.width();
	dlg.css({'margin-left' : ((windowWidth - boxWidth )/2), 'margin-top' : ((windowHeight - boxHeight)/2)});
}