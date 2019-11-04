$(document).ready(function () {
    $('#browserTabCarousel').on('dblclick', '.owl-item', function (e, data) {
        var src = $(this).find('img').attr('src');

        if(src == browserViewModel.folderImgPath || src == browserViewModel.fileImgPath){
            return;
        }

        var itemName = $(this).find('figcaption').html();
        showBrowserItemModal(src, itemName);
    });

    $("#browserTabCarousel").on('mouseover', '.owl-item', function (e) {  
       
        $(this).addClass('owl-item-focus');
    
    });

    $("#browserTabCarousel").on('mouseleave', '.owl-item', function (e) {  
        $(this).removeClass('owl-item-focus');
    });

    $('#browserItemModal').on('show.bs.modal', function (e) {
        $("#browserItemPopup").contents().find('body').find('img').css('display', 'block').css('margin', '0 auto');
    });
    
    $("#btnOpenNewWindow").click(function (e) {  
        var contentUrl = $(this).parents('div.modal-content').find('iframe').attr('src');
        window.open(contentUrl, '_blank');
    });


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
                $("#browserViewList").addClass('div-browser-items');
                $("#browserView").addClass('browser-details-view');
                $("#browserView").removeClass('browser-list-view');
                $("#browserView").css('max-height', '');
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

});