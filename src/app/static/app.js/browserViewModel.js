function BrowserViewModel() {
    var self = this;
    self.dataSourcesURI = '/datasources';
    self.browserItems = ko.observableArray();
    self.folderImgPath = '/static/folder_Icon_blue.png'; // "{{ url_for('static', filename='folder_Icon_blue.png') }}";
    self.fileImgPath = '/static/file_icon_blue.png'; //"{{ url_for('static', filename='file_icon_blue.png') }}";
    self.imageTypes = ["png", "jpg", "jpeg", "bmp", "gif", "ico", "ief", "jpe", "pbm", "pgm", "jng", "nef",
        "orf", "psd", "art", "pnm", "ppm", "rab", "rgb", "svg", "tif", "tiff", "xbm", "xpm", "xwd", "jp2",
        "jpm", "jpx", "jpf", "pcx", "svgz", "djvu", "djv", "pat", "cr2", "crw", "cdr", "cdt", "erf", "wbmp"];

    self.videoTypes = ["3gp", "axv", "dl", "dif", "dv", "fli", "gl", "ts", "ogv", "mxu", "flv", "lsf", "lsx", "mng", "asf",
        "asx", "wm", "wmv", "wmx", "wvx", "mpv", "mkv", "avi", "m1v", "mov", "movie", "mp4", "mpa", "mpe", "mpeg", "mpg", "webm"];

    // self.isNewSlider = false;
    self.itemName = ko.observable();
    self.itemSrc = ko.observable();
    self.currentItemPath = ko.observable();
    self.isListView = ko.observable(true);
    self.sliderItems = ko.observableArray();

    self.destroySlider = function () {
        $('#browserTabCarousel').trigger('destroy.owl.carousel');
    };


    self.initiateSlider = function () {

        $("#browserTabCarousel").owlCarousel({
            loop: false,
            margin: 10,
            nav: true,
            center: false,
            mouseDrag: true,
            dots: false,
            pagination: false,
            navText : ['<i class="fa fa-caret-left" aria-hidden="true"></i>','<i class="fa fa-caret-right" aria-hidden="true"></i>'],
            responsive: {
                0: {
                    items: 1
                },
                700: {
                    items: 3
                },
                1000: {
                    items: 3
                },
                1200: {
                    items: 3
                }
            }
        });
    };

    self.sliderController = function (data, element) { 
        self.destroySlider();
        self.initiateSlider();
        
    }

    self.getFileExtension = function (filename) {
        return filename.substring(filename.lastIndexOf('.') + 1, filename.length) || filename;
    };


    // self.addNewSliderContent = function (imgPath, itemName) {
    //     var figure = '<div style ="display: block"><figure style="display: inline-block">' + '<img class="center" height="50rem" width="45rem" src="' + imgPath + '" alt= "' + itemName + '" >';
    //     var figureCaption = '<figcaption>' + itemName + '</figcaption> </figure></div>';
    //     var slider = figure + figureCaption;

    //     if (self.isNewSlider) {
    //         $("#browserTabCarousel").append(slider);
    //         return;
    //     }
    //     return slider;
    // };

 
    self.openInNewTab = function (data, e) {

        if (ko.utils.unwrapObservable(data.dataType) == 'folder') {

            var treeNodes = $("#tree").jstree(true).get_json('#', { 'flat': true });

            for (var index = 0; index < treeNodes.length; index++) {
                var node = treeNodes[index];
                var targetNode = $("#tree").jstree(true).get_node(node.id);

                if (targetNode.original.path == data.originalPath()) {
                    $("#tree").jstree("deselect_all");
                    $("#tree").jstree(true).select_node(targetNode);
                    break;
                }
            }
            return;
        }
        // else if (ko.utils.unwrapObservable(data.dataType) == 'file') {
        //     var fileType = self.getFileExtension(data.itemName());
        //     if (fileType == 'html' || fileType == 'htm') {
        //         var oReq = new XMLHttpRequest();
        //         oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.originalPath(), true);
        //         oReq.responseType = "arraybuffer";

        //         oReq.send();

        //         oReq.onload = function (oEvent) {
        //             if (this.status == 200) {
        //                 var arrayBuffer = oReq.response;
        //                 var byteArray = new Uint8Array(arrayBuffer);

        //                 var blob = new Blob([arrayBuffer], { type: fileType });
        //                 var fileSrc = URL.createObjectURL(blob);

        //                 showBrowserItemModal(fileSrc, data.itemName());

        //             }
        //         };
        //         return;
        //     }
        // }

        $.redirect(self.dataSourcesURI, { 'download': ko.utils.unwrapObservable(data.originalPath) }, "POST", "_blank");

    };


    self.pushImage = function (data, imgUrl, isStatic = false ,isFolder = false) {  
        if (self.isListView() || isFolder) {
            self.browserItems.push(
                {
                    imgPath: ko.observable(imgUrl),
                    itemName: ko.observable(data.text),
                    originalPath: ko.observable(data.original.path),
                    dataType: ko.observable(data.type)
                }
            );
            return;
        }
        
        self.sliderItems.push(
            {
                imgPath: ko.observable(imgUrl),
                itemName: ko.observable(data.text),
                originalPath: ko.observable(data.original.path),
                dataType: ko.observable(data.type),
                isStatic : ko.observable(isStatic)
            }
        );
    };

    self.getImage = function (data, fileType) { 

        var oReq = new XMLHttpRequest();
        oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.original.path, true);
        oReq.responseType = "arraybuffer";
        var imgType = "image/" + fileType;

        oReq.send();

        oReq.onload = function (oEvent) {
            if (this.status == 200) {
                var arrayBuffer = oReq.response;
                // var byteArray = new Uint8Array(arrayBuffer);
                var blob = new Blob([arrayBuffer], { type: imgType });
                imgUrl = URL.createObjectURL(blob);
                self.pushImage(data, imgUrl);
            }
        };
    };

    self.emptyBrowser = function () {
        self.browserItems([]);
        self.destroySlider();
        self.sliderItems([]);
        self.itemName('Item Details');
        self.itemSrc('');
        self.currentItemPath('');
        $("#browserTabCarousel").empty();
    };

    self.browserItemCaptionCss = function () {
        var isFilterClosed = $(".box-zero").is(":hidden");
        if (!isFilterClosed) {
            $("#browserViewList").find('figcaption').addClass('figcaption-clipped');
        }
    };

    self.loadItems = function (data) {
        
        self.emptyBrowser();

        if (data.children.length == 0) {
            var imgUrl = '';
            if(data.type == 'folder'){
                
                imgUrl =  self.folderImgPath;
                self.pushImage(data, imgUrl, false ,true);
            }

            if (data.type == "file") {
                var fileType = self.getFileExtension(data.text);

                if (self.imageTypes.includes(fileType)) {
                    self.getImage(data, fileType);
                }
                else {
                    imgUrl = self.fileImgPath;
                    self.pushImage(data, imgUrl, true ,false);
                }
            }
        }
        else {
            data.children.forEach(function (child) {
                var childNode = $("#tree").jstree(true).get_node(child);
                var imgUrl = '';
                if(!childNode.state.hidden && childNode.type == 'folder'){
                    imgUrl = self.folderImgPath;
                    self.pushImage(childNode, imgUrl, false ,true);
                }
                else if (!childNode.state.hidden && childNode.type == "file") {
                    var fileType = self.getFileExtension(childNode.text);

                    if (self.imageTypes.includes(fileType)) {

                        self.getImage(childNode, fileType);
                    }
                    else {
                        imgUrl = self.fileImgPath;
                        self.pushImage(childNode, imgUrl, true)
                    }
                }
            });
        }
    };

    self.openIntoNewWindow = function () {  
        $.redirect(self.dataSourcesURI, { 'download': ko.utils.unwrapObservable(self.currentItemPath) }, "POST", "_blank");
    }

    self.openInDetailsView = function (data, ele) {
        var fileType = self.getFileExtension(data.itemName());

        self.currentItemPath(data.originalPath());

        if (self.imageTypes.includes(fileType)) {
            // self.showModal(data);
            self.itemSrc(data.imgPath());
            self.itemName(data.itemName());
        }

        else if (self.videoTypes.includes(fileType)) {
            var oReq = new XMLHttpRequest();
            oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.originalPath(), true);
            oReq.responseType = "arraybuffer";
            var videoType = "video/" + fileType;
            self.itemName(data.itemName());
            oReq.send();

            oReq.onload = function (oEvent) {
                if (this.status == 200) {
                    var arrayBuffer = oReq.response;
                    var blob = new Blob([arrayBuffer], { type: videoType });
                    itemSrc = URL.createObjectURL(blob);

                    self.itemSrc(itemSrc);
                    // self.showModal(data, itemSrc);
                }
            };
        }
        else if (fileType == 'htm' || fileType == 'html') {
            var oReq = new XMLHttpRequest();
            oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.originalPath(), true);
            oReq.responseType = "arraybuffer";

            oReq.send();
            self.itemName(data.itemName());
            oReq.onload = function (oEvent) {
                if (this.status == 200) {
                    var arrayBuffer = oReq.response;
                    var blob = new Blob([arrayBuffer], { type: "text/html" });
                    var reader = new FileReader();
                    reader.readAsDataURL(blob);
                    reader.onload = function () {
                        var base64UrlString = reader.result;
                        self.itemSrc(base64UrlString);
                    }
                }
            };
        }
        else if (fileType == 'pdf') {
            var oReq = new XMLHttpRequest();
            oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.data, true);
            oReq.responseType = "arraybuffer";

            oReq.send();
            self.itemName(data.data);
            oReq.onload = function (oEvent) {
                if (this.status == 200) {
                    var arrayBuffer = oReq.response;
                    var blob = new Blob([arrayBuffer], { type: "application/pdf" });
                    itemSrc = URL.createObjectURL(blob);
                    self.itemSrc(itemSrc);
                }
            };
        }
        else if (fileType == 'xml') {
            var oReq = new XMLHttpRequest();
            oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.originalPath(), true);
            oReq.responseType = "xml";
            
            oReq.send();
            self.itemName(data.itemName());
            oReq.onload = function (oEvent) {
                if (this.status == 200) {
                    var arrayBuffer = oReq.response;
                    var blob = new Blob([arrayBuffer], { type: "text/plain" });
                    itemSrc = URL.createObjectURL(blob);
                    self.itemSrc(itemSrc);
                }
            };
        }
        else {
            return;
        }
    };

    self.openInModal = function (data, ele) {

        var fileType = self.getFileExtension(data.itemName());

        if (self.imageTypes.includes(fileType)) {
            self.showModal(data);
        }

        else if (self.videoTypes.includes(fileType)) {
            var oReq = new XMLHttpRequest();
            oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.originalPath(), true);
            oReq.responseType = "arraybuffer";
            var videoType = "video/" + fileType;

            oReq.send();

            oReq.onload = function (oEvent) {
                if (this.status == 200) {
                    var arrayBuffer = oReq.response;
                    var blob = new Blob([arrayBuffer], { type: videoType });
                    itemSrc = URL.createObjectURL(blob);
                    
                    self.showModal(data, itemSrc);
                }
            };
        }
        else if(fileType == 'htm' || fileType == 'html'){
            var oReq = new XMLHttpRequest();
            oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.originalPath(), true);
            oReq.responseType = "arraybuffer";

            oReq.send();

            oReq.onload = function (oEvent) {
                if (this.status == 200) {
                    var arrayBuffer = oReq.response;
                    var blob = new Blob([arrayBuffer], { type: fileType });
                    itemSrc = URL.createObjectURL(blob);

                    self.showModal(data, itemSrc);
                }
            };
        }
        else if(fileType == 'xml'){
            var oReq = new XMLHttpRequest();
            oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.originalPath(), true);
            oReq.responseType = "arraybuffer";

            oReq.send();

            oReq.onload = function (oEvent) {
                if (this.status == 200) {
                    var arrayBuffer = oReq.response;
                    var blob = new Blob([arrayBuffer], { type: 'text/plain' });
                    itemSrc = URL.createObjectURL(blob);

                    self.showModal(data, itemSrc);
                }
            };
        }
        else{
            return;
        }
    };

    self.showModal = function (data, itemSrc = null) {

        browserItemModalViewModel.dataType(data.dataType());
        browserItemModalViewModel.itemSrc(data.imgPath());
        browserItemModalViewModel.itemName(data.itemName());
        browserItemModalViewModel.originalPath(data.originalPath());
        if(itemSrc != null){
            browserItemModalViewModel.itemSrc(itemSrc);
        }

        var iframe = $("#browserItemModal").find('iframe');

        $(iframe).height($('#browsertab').height()).width('100%');
        setTimeout(function () {
            $('#browserItemModal').modal('show');
        }, 200);
    };

};

ko.bindingHandlers.browserItemHover = {
    init: function (element, valueAccessor, allBindings, viewModel, bindingContext) {

        $(element).mouseover(function () {
            $(element).siblings().removeClass('browseritem-hover');
            $(element).addClass('browseritem-hover');
        });
        $(element).mouseleave(function () {
            $(element).removeClass('browseritem-hover');
        });
    }
};


function BrowserItemModalViewModel() {
    var self = this;
    self.iframeSource = ko.observable();
    self.dataType = ko.observable();
    self.itemSrc = ko.observable();
    self.itemName = ko.observable();
    self.originalPath = ko.observable();

    self.openInNewTab = function (data, ele) {  
        browserViewModel.openInNewTab(data, ele);
    }

}