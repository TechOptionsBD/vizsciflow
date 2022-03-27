$(function(){

    $("#btnfilterToggle").click(function () {  
        var isFilterClosed = $(".box-zero").is(":hidden");

        if (isFilterClosed) {
            $(".box-zero").show();
            resizeComponentBoxes();
            // $(".box-two").removeClass('col-md-6').addClass('col-md-4');
            $("#browserViewList").find('figcaption').addClass('figcaption-clipped');
        } else {
            $(".box-zero").hide();
            resizeComponentBoxes();
            // $(".box-two").removeClass('col-md-4').addClass('col-md-6');
            $("#browserViewList").find('figcaption').removeClass('figcaption-clipped');
        }
    });

    $('#viewComponents-dropdown li').click(function (e) {  
        var component = $(this).children().attr('href');
        $(component).parent().show();
        $(component).show();
        filterToolControl();
        boxVisiblityControl();
        resizeComponentBoxes();
    });

    $('.closeComponent').click(function (e) {
        var component= $(this).parent().parent();  
        $(component).hide();
        filterToolControl();
        boxVisiblityControl();
        resizeComponentBoxes();
    });

    function boxVisiblityControl() {
        var visibleBoxOne = $('.box-one').children(":visible").length == 0? false : true;
        var visibleBoxThree = $('.box-three').children(":visible").length == 0? false : true;

        switch (visibleBoxOne) {
            case true:
                $('.box-one').show();
                break;
            case false:
                $('.box-one').hide();
                break;
            default:
                $('.box-one').show();
                break;
        }

        switch (visibleBoxThree) {
            case true:
                $('.box-three').show();
                break;
            case false:
                $('.box-three').hide();
                break;
            default:
                $('.box-three').show();
                break;
        }
    }

    function filterToolControl() {

        var isDataSourcesHidden = $("#datasourceStack").is(":hidden");

        if (isDataSourcesHidden) {
            $("#btnfilterToggle").hide();
            $(".box-zero").hide();
        }
        else{
            $("#btnfilterToggle").show();
        }
    }

    function resizeComponentBoxes() {
        var visibleBoxOne = $('.box-one').children(":visible").length == 0? false : true;
        var visibleBoxThree = $('.box-three').children(":visible").length == 0? false : true;
        var visibleBoxZero = $('.box-zero').is(":visible");

        if (!visibleBoxOne && !visibleBoxThree) {
            $("#main").removeClass().addClass('col-md-12 box-two');
        }

        else if(!visibleBoxOne || !visibleBoxThree){
            $("#main").removeClass().addClass('col-md-9 box-two');
        }
        else if (visibleBoxOne || visibleBoxThree) {
            $("#main").removeClass().addClass('col-md-6 box-two');
        }
        
        if(visibleBoxZero && !visibleBoxThree){
            $("#main").removeClass().addClass('col-md-6 box-two');
        }

        if (visibleBoxZero && visibleBoxThree ) {
            $("#main").removeClass().addClass('col-md-4 box-two');
        }
    }

    $("#exTabService").on('shown.bs.tab', function (e) {  
        var targetTab = $(e.target).attr('href');

        if (targetTab == "#service2") {
            addLibraryViewModel.liveJsonView();
        }
    });
})