$(document).ready(function () {
    // $('#browserTabCarousel').on('dblclick', '.owl-item', function (e, data) {
    //     var src = $(this).find('img').attr('src');

    //     if(src == browserViewModel.folderImgPath || src == browserViewModel.fileImgPath){
    //         return;
    //     }

    //     var itemName = $(this).find('figcaption').html();
    //     showBrowserItemModal(src, itemName);
    // });

    hideTabInit();
    setInitModeView();

    $("#browserTabCarousel").on('mouseover', '.owl-item', function (e) {  
       
        $(this).addClass('owl-item-focus');
        $(this).css('transform', 'scale(1.11)');
        $(this).siblings().addClass('owl-shrink');
        $(this).siblings().css('transform-origin', 'center left');
        //$(this).next().css('transform-origin', 'center right');
    
    });

    $("#browserTabCarousel").on('mouseleave', '.owl-item', function (e) {  
        $(this).removeClass('owl-item-focus');
        $(this).css('transform', 'scale(1)');
        $(this).siblings().removeClass('owl-shrink');
        $(this).siblings().css('transform-origin', 'initial');
        //$(this).next().css('transform-origin', 'initial');
    });

    $('#browserItemModal').on('show.bs.modal', function (e) {
        $("#browserItemPopup").contents().find('body').find('img').css('display', 'block').css('margin', '0 auto');
    });
    
    // $("#btnOpenNewWindow").click(function (e) {  
    //     var contentUrl = $(this).parents('div.modal-content').find('iframe').attr('src');
    //     window.open(contentUrl, '_blank');
    // });


    $("#btnBrowserModalFullscreen").click(function (e) { 
        if ($("#browserItemModal").hasClass('modal-fullscreen')) {
            
            $("#browserItemModal").removeClass('modal-fullscreen');
            $("#browserItemModal").find('.modal-dialog').removeClass('modal-dialog-fullscreen');
            $("#browserItemModal").find('.modal-content').removeClass('modal-content-fullscreen');
            $("#browserItemModal").find('.modal-header').removeClass('modal-header-fullscreen');
            $("#browserItemModal").find('.modal-body').removeClass('modal-body-fullscreen');
            $("#browserItemModal").find('.modal-footer').removeClass('modal-footer-fullscreen');
            $("#browserItemModal").find('iframe').height($('#browsertab').height()).width('100%');
            $("#btnBrowserModalFullscreen").find('i').removeClass('glyphicon-resize-small').addClass('glyphicon-resize-full');
            return;
        } 
        $("#browserItemModal").addClass('modal-fullscreen');
        $("#browserItemModal").find('.modal-dialog').addClass('modal-dialog-fullscreen');
        $("#browserItemModal").find('.modal-content').addClass('modal-content-fullscreen');
        $("#browserItemModal").find('.modal-header').addClass('modal-header-fullscreen');
        $("#browserItemModal").find('.modal-body').addClass('modal-body-fullscreen');
        $("#browserItemModal").find('.modal-footer').addClass('modal-footer-fullscreen');
        $("#btnBrowserModalFullscreen").find('i').removeClass('glyphicon-resize-full').addClass('glyphicon-resize-small');

        // $("#browserItemModal").find('.modal-dialog').height('auto').width('auto')
        // $("#browserItemModal").find('.modal-content').addClass('modal-content-fullscreen');
        $("#browserItemModal").find('iframe').css('height', '100%').css('width', '100%');
    });

    $("#dataSets-addNew-dialog").css("left", $(window).width() / 4);

    $("input[name=dataSourcesTab]").on("click", function (e) {

        switch (e.currentTarget.value) {
            case "0":
                $("#dataSourcesPanel").show();
                $("#dataSetsPanel").hide();
                $("#liBrowserTab").siblings('li').removeClass("active");
                $("#liBrowserTab").addClass("active");
                $("#browsertab").siblings("div").removeClass("active");
                $("#browsertab").addClass("active in");
                if ($("#browserView").parent('div#browsertab').length == 0) {
                    $('#browsertab').append($("#browserView"));
                    $("#browserView").show();
                }
                break;
            case "1":
                $("#dataSourcesPanel").hide();
                $("#dataSetsPanel").show();
                $("#liDataset").show();
                $("#liDataset").siblings('li').removeClass("active");
                $("#liDataset").addClass("active");
                $("#datasettab").siblings('div').removeClass("active");
                $("#datasettab").addClass("active in");
                if ($("#datasetView").parent('div#datasettab').length == 0) {
                    $('#datasettab').append($("#datasetView"));
                    $("#datasetView").show();
                }
                break;
            default:
                $("#dataSourcesPanel").show();
                $("#dataSetsPanel").hide();
                break;
        }
    });
    $("#browserView").addClass('browser-list-view');
    $("#browserView").css('max-height', $("#browsertab").height() - $(".browser-panel-heading").height()-50);
    
    $("#browserItemDetails").on('load', function () {  
        $(this).contents().find('body').find('img').css('display', 'block').css('margin', '0 auto');
        $("#browserItemDetails").css('height', $("#browserViewDetails").height() - $("#browserViewDetailsHeader").height());
    })

    $("input[name=browserTabView]").on('click', function (e) {
        var selectedNode = $('#tree').jstree().get_selected(true)[0];
        switch (e.currentTarget.value) {
            case "0":
                browserViewModel.isListView(true);
                browserViewModel.loadItems(selectedNode);
                $("#browserViewList").removeClass('div-browser-items');
                $("#browserView").css('max-height', $("#browsertab").height() - $(".browser-panel-heading").height()-20);
                $("#browserView").removeClass('browser-details-view');
                $("#browserView").addClass('browser-list-view');
                break;
            case "1":
                browserViewModel.isListView(false);
                browserViewModel.loadItems(selectedNode);
                $("#browserViewDetails").addClass('div-browser-items');
                $("#browserView").addClass('browser-details-view');
                $("#browserView").removeClass('browser-list-view');
                $("#browserView").css('max-height', '');
                $("#browserItemDetails").css('height', $("#browserViewDetails").height() - $("#browserViewDetailsHeader").height());
                break;
            default:
                browserViewModel.isListView(true);
                browserViewModel.loadItems(selectedNode);
                $("#browserViewList").removeClass('div-browser-items');
                $("#browserView").addClass('browser-list-view');
                $("#browserView").css('max-height', $("#browsertab").height() -10 - $(".browser-panel-heading").height()-20);
                break;
        }
    });


    $("#graphtab").css('height', $("#scripttab").css('height'));
    // $("#graph").css('max-height', $("#graphtab").height() - $(".graph-panel-heading").height()-45);

    $("#visualtab").css('height', $("#scripttab").css('height'));

    $("#provenancetab").css('height', $("#scripttab").css('height'));
    $("#provenance").css('max-height', $("#provenancetab").height() - $(".prov-panel-heading").height()-45);

    $('.menu_button').click(function () {
        $(this).addClass('selected').siblings().removeClass('selected')
    });
   
    var runBioWL = $("#runBioWL");
    $(runBioWL).on('click', function () {
        $(".extab2-tab-content").css("min-height", "168px");
    });

    var logTab = $(".log-tab");
    $(logTab).css('height', '150px');

    //Toggle fullscreen
    $("#panel-fullscreen").click(function (e) {
        e.preventDefault();

        var $this = $(this);

        if ($this.children('i').hasClass('glyphicon-resize-full')) {
            $this.children('i').removeClass('glyphicon-resize-full');
            $this.children('i').addClass('glyphicon-resize-small');
        }
        else if ($this.children('i').hasClass('glyphicon-resize-small')) {
            $this.children('i').removeClass('glyphicon-resize-small');
            $this.children('i').addClass('glyphicon-resize-full');
        }
        $(this).closest('.panel').toggleClass('panel-fullscreen');
        editor.resize();
    });

    $("#panel-about").click(function (e) {
        e.preventDefault();
        window.open("static/biodsl-help.html#syntax", '_blank');
    });

    $("#panel-fontsize a").on('click', function (e) {
        e.preventDefault();

        editor.setFontSize($(e.target).text() + 'pt');
    });

    // $("#tree").on("search.jstree", function (e, data) {
    // 	$('.jstree-open').on("dragstart", function (e) {
    // 		e.stopPropagation();
    // 		var nodeId = e.target.id.replace("_anchor", "");
    // 		var node = $("#tree").jstree(true).get_node(nodeId);
    // 		e.originalEvent.dataTransfer.setData("text/plain", node.original.path);
    // 	});
    // });
    $("#editortabs-dropdown li").click(function (e) {  
        var targetTab = $(this).children().attr('href');
        $(targetTab).show();
        $(targetTab).children('a').tab('show');
    });


	$("#exTabBiowl").on('shown.bs.tab', function (e) {
		var x = $(e.target).attr('href');
		if (x === "#graphtab") {
            // var checked = $('select[name="graphTabView"]').val();
            // toggleGraphView(checked);
            tasksViewModel.buildGoDetailGraph();
        }
        if (x === "#visualtab") {
            var visualdiv = visualtab.querySelector('canvas');
            if(visualdiv == null)
                gojsControlFlow.show();   			
            else 
                return;
        }
        else if (x === "#provenancetab") {
            var selectedProvView = $("select[name=provTabView]").val();
            toggleProvView(selectedProvView)
        }
        if(x === "#scripttab")
            tasksViewModel.shouldRunActivate(true)
        else
            tasksViewModel.shouldRunActivate(false)
    });

    //for execstatus printing
    $("#exTab2").on('shown.bs.tab', function (e) {
		var x = $(e.target).attr('href');
		if (x === "#1" || x === "#2") {
            $("#execstatus").css("float", "right");
        }
        else if (x === "#3") {
            $("#execstatus")
            .css({
                "float": "left",
                "margin-left": "57%"
            });
		}
    });

    //job history floating toolbar visibility based on active tab 
    $(document).on('mouseenter', '#runnablesHistory', function (e) {
        // var activeTab = $("#exTabBiowl ul li.active").attr('id');
		// if (activeTab === "liScriptTab") 
        //     $(this).find(".runnableToolbar").css("display", "block");
        // else
        //     $(this).find(".runnableToolbar").css("display", "none");
        $(this).find(".runnableToolbar").css("display", "block");

    }).on('mouseleave', '#runnablesHistory', function () {
        $(this).find(".runnableToolbar").css("display", "none");
    });
      
    //handling any service addition on click
    $("#visual").droppable({

		activeClass: "ui-state-default",
		hoverClass: "ui-state-hover",
		accept: ":not(.ui-sortable-helper)",

		drop: function (event, ui) {
			event.preventDefault();
			event.stopPropagation();
			var v = ko.dataFor(ui.draggable[0]);
            inputParam = '';
            defaultOutputParam = '';
            outputParam = [];
            serviceName = '';
			if (v) {
				if (v.params() !== undefined) {	 
                    inputParam = JSON.stringify(v.params());	                    
                }
                if (v.returnData() !== undefined) {
                    defaultOutputParam = JSON.stringify(v.returnData());
                }                
                if (v.returns() !== undefined) {	   
                    outputParam.push({type: v.returns()});	
                }
                if (v.name() !== undefined) {
                    serviceName = v.name();
                }
            }
            if(defaultOutputParam == '')
                outputParam = JSON.stringify(outputParam);
            else
                outputParam = defaultOutputParam;

			gojsControlFlow.addNewNode(serviceName, inputParam, outputParam);			
			return true;
		}
    });
    
    //service drop in editor
    $("#editor").droppable({
        activeClass: "ui-state-default",
		hoverClass: "ui-state-hover",
		accept: ":not(.ui-sortable-helper)",

		drop: function (event, ui) {
			event.preventDefault();
			event.stopPropagation();
			
            var v = ko.dataFor(ui.draggable[0]);
			if (v.serviceID !== undefined) {
                tasksViewModel.copyToEditor(v);
            }
            else if(v.pluginID !== undefined){
                provpluginsViewModel.copyToEditor(v);
            }
            else {
				samplesViewModel.dropNLoadIntoEditor(v);
			}
		}
    });
    
    // $("select[name=graphTabView]").on('click', function (k) {
    //     toggleGraphView(k.currentTarget.value);
    // }); 
   
    //service delete button on hovar
    $(document).on('mouseenter', '.deleteService', function () {
        $(this).find(":button").show();
    }).on('mouseleave', '.deleteService', function () {
        $(this).find(":button").hide();
    });


    $("select[name=logTabView]").on('click', function (e) {  
        switch (e.currentTarget.value) {
            
            case '0':
                tasksViewModel.isListLog(true);
                break;
            case '1':
                tasksViewModel.isListLog(false);
                break;

            default:
                tasksViewModel.isListLog(true);
                break;
        }
    });
    
    $("select[name=provTabView]").on('click', function (e) {  
        toggleProvView(e.currentTarget.value);
    });
    
    // $("#btnfilterClose").click(function () {  
    //     $("#btnfilterToggle").trigger('click');
    // });

    // $('.grid-stack').gridstack({
    //     animate: true
    // });

    // var grid = $('.grid-stack').data('gridstack');

    // grid.disable();

    // $('.closeComponent').click(function (e) {  
    //     var componentId = $(this).parents('.grid-stack-item').attr('id');
    //     $("#" + componentId).hide();
    // });

    // $('#viewComponents-dropdown li').click(function (e) {  
    //     var component = $(this).children().attr('href');
    //     $(component).show();
    // });

    // $('.grid-stack-item').on('dragstop', function(event, ui) {
    //     var grid = this;
    //     var element = event.target;
    //     var t = $(element).find('.content-area').css('height', '100%');
    //   });

      
    // $('.grid-stack-item').on('change', function (event, items) {
        
    //     //serializeWidgetMap(items);
    // });

    // $('.grid-stack-item').on('dragstop', function(event, ui) {
        
    //     var grid = this;
    //     var element = event.target;
    //   });

    //   $('.grid-stack-item').on('resizestart', function(event, ui) {
        
    //     var grid = this;
    //     var element = event.target;
    //   });

    //   $('.grid-stack-item').on('resizestop', function(event, elem) {
          
    //     //var newHeight = $(elem).attr('data-gs-height');
    //     var element = event.target;
    //     var t = $(element).find('.content-area').css('height', '100%');
    //   });

    //   $('.grid-stack-item').change(function (e) { 
    //       e.preventDefault();
          
    //   });
});

// function toggleGraphView(selectedTab) {
//     switch (selectedTab) {   
//         case "0":
//             tasksViewModel.buildGoSimpleGraph();
//             break;
//         case "1":
//             tasksViewModel.buildGoDetailGraph();
//             break;
//         default:
//             tasksViewModel.buildGoSimpleGraph();
//             break;
//     }
// }

function toggleProvView(selectedTab) {
    switch (selectedTab) {   
        case "graph":
            $("#compareDiv").hide();
            $("#compareTxtDiv").hide();
            $("#pluginViewDiv").hide();
            $("#provenance").show();
            $("#provDiagramOverview").show();
            $("#proveBarCharts").hide();
            $("#provePieCharts").hide();
            $("#proveHeatMap").hide();
            $("#proveLineCharts").hide();
            break;

        case "compare":
            $("#provenance").hide();
            $("#provDiagramOverview").hide();
            $("#compareTxtDiv").hide();
            $("#pluginViewDiv").hide();
            $("#proveBarCharts").hide();
            $("#provePieCharts").hide();
            $("#proveHeatMap").hide();
            $("#proveLineCharts").hide();
            $("#compareDiv").show();
            break;

        case "textcompare":
            $("#provenance").hide();
            $("#provDiagramOverview").hide();
            $("#compareDiv").hide();
            $("#pluginViewDiv").hide();
            $("#proveBarCharts").hide();
            $("#provePieCharts").hide();
            $("#proveHeatMap").hide();
            $("#proveLineCharts").hide();
            $("#compareTxtDiv").show();
            break;

        case "plugin":
            $("#provenance").hide();
            $("#provDiagramOverview").hide();
            $("#compareDiv").hide();
            $("#compareTxtDiv").hide();
            $("#proveBarCharts").hide();
            $("#provePieCharts").hide();
            $("#proveHeatMap").hide();
            $("#proveLineCharts").hide();
            $("#pluginViewDiv").show();
            break;
        
        case "lineChart":
            $("#provenance").hide();
            $("#provDiagramOverview").hide();
            $("#compareDiv").hide();
            $("#compareTxtDiv").hide();
            $("#pluginViewDiv").hide();
            $("#proveBarCharts").hide();
            $("#provePieCharts").hide();
            $("#proveHeatMap").hide();
            $("#proveLineCharts").show();
            break;

        case "pieChart":
            $("#provenance").hide();
            $("#provDiagramOverview").hide();
            $("#compareDiv").hide();
            $("#compareTxtDiv").hide();
            $("#pluginViewDiv").hide();
            $("#proveBarCharts").hide();
            $("#proveHeatMap").hide();
            $("#proveLineCharts").hide();
            $("#provePieCharts").show();
            break;

        case "barChart":
            $("#provenance").hide();
            $("#provDiagramOverview").hide();
            $("#compareDiv").hide();
            $("#compareTxtDiv").hide();
            $("#pluginViewDiv").hide();
            $("#proveBarCharts").show();
            $("#proveHeatMap").hide();
            $("#proveLineCharts").hide();
            $("#provePieCharts").hide();
            break;

        case "heatMap":
            $("#provenance").hide();
            $("#provDiagramOverview").hide();
            $("#compareDiv").hide();
            $("#compareTxtDiv").hide();
            $("#pluginViewDiv").hide();
            $("#proveBarCharts").hide();
            $("#proveHeatMap").show();
            $("#proveLineCharts").hide();
            $("#provePieCharts").hide();
            break;

        default:
            $("#provenance").show();
            $("#provDiagramOverview").show();
            $("#compareDiv").hide();
            $("#compareTxtDiv").hide();
            $("#pluginViewDiv").hide();
            $("#proveBarCharts").hide();
            $("#proveHeatMap").hide();
            $("#proveLineCharts").hide();
            $("#provePieCharts").hide();
            break;            
    }
}

function hideTabInit() {
    $('#liVisualTab').hide();
    $('#liMetadataTab').hide();
    $('#liFilterHistoryTab').hide();
    $('#liDataset').hide();
}

function setInitModeView() {
    let currentMode = handleModeViewModel.getMode();
    handleModeViewModel.setMode(currentMode);
}