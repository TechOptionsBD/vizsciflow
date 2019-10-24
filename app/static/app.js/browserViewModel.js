function BrowserViewModel() {
    var self = this;
    self.dataSourcesURI = '/datasources';
    self.browserItems = ko.observableArray();
    self.folderImgPath = '/static/folder_Icon_blue.png'; // "{{ url_for('static', filename='folder_Icon_blue.png') }}";
    self.fileImgPath = '/static/file_icon_blue.png'; //"{{ url_for('static', filename='file_icon_blue.png') }}";
    self.imageTypes = ["png", "jpg", "jpeg", "bmp", "gif", "ico", "ief", "jpe", "pbm", "pgm", "jng", "nef",
        "orf", "psd", "art", "pnm", "ppm", "rab", "rgb", "svg", "tif", "tiff", "xbm", "xpm", "xwd", "jp2",
        "jpm", "jpx", "jpf", "pcx", "svgz", "djvu", "djv", "pat", "cr2", "crw", "cdr", "cdt", "erf", "wbmp"];

    self.isNewSlider = false;
    self.isListView = ko.observable(true);
    self.destroySlider = function () {
        $('#browserTabCarousel').trigger('destroy.owl.carousel');
        $("#browserTabCarousel").empty();
    };


    self.initiateSlider = function () {
        

        $("#browserTabCarousel").owlCarousel({
            loop: true,
            margin: 10,
            nav: true,
            mouseDrag: true,
            dots: false,
            pagination: false,
            navText : ['<i class="fa fa-caret-left" aria-hidden="true"></i>','<i class="fa fa-caret-right" aria-hidden="true"></i>'],
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 2
                },
                1000: {
                    items: 5
                }
            }
        });
    };

    self.getFileExtension = function (filename) {
        return filename.substring(filename.lastIndexOf('.') + 1, filename.length) || filename;
    };

    self.pushImg = function (data, fileType) {  
        var oReq = new XMLHttpRequest();
        oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.original.path, true);
        oReq.responseType = "arraybuffer";
        var imgType = "image/" + fileType;

        oReq.send();

        oReq.onload = function (oEvent) {
            if (this.status == 200) {
                var arrayBuffer = oReq.response;
                var byteArray = new Uint8Array(arrayBuffer);

                var blob = new Blob([arrayBuffer], { type: imgType });
                imgUrl = URL.createObjectURL(blob);

                if (self.isListView()) {
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
                

                if (self.isNewSlider) {
                    self.addNewSliderContent(imgUrl, data.text);
                    self.initiateSlider();
                    self.isNewSlider = false;
                    return;
                }

                $("#browserTabCarousel").trigger('add.owl.carousel', [self.addNewSliderContent(imgUrl, data.text)]).trigger('refresh.owl.carousel');
            }
        };
    };

    self.addNewSliderContent = function (imgPath, itemName) {
        var figure = '<div style ="display: block"><figure style="display: inline-block">' + '<img class="center" height="50rem" width="45rem" src="' + imgPath + '" alt= "' + itemName + '" >';
        var figureCaption = '<figcaption>' + itemName + '</figcaption> </figure></div>';
        var slider = figure + figureCaption;

        if (self.isNewSlider) {
            $("#browserTabCarousel").append(slider);
            return;
        }
        return slider;
    };

    // self.pushImgIntoSlider = function (data, fileType) {
    //     var oReq = new XMLHttpRequest();
    //     oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.original.path, true);
    //     oReq.responseType = "arraybuffer";
    //     var imgType = "image/" + fileType;

    //     oReq.send();

    //     oReq.onload = function (oEvent) {
    //         if (this.status == 200) {
    //             var arrayBuffer = oReq.response;
    //             var byteArray = new Uint8Array(arrayBuffer);

    //             var blob = new Blob([arrayBuffer], { type: imgType });
    //             imgUrl = URL.createObjectURL(blob);

    //             // self.browserItems.push(
    //             // 	{
    //             // 		imgPath: ko.observable(imgUrl),
    //             // 		itemName: ko.observable(data.text),
    //             // 		originalPath: ko.observable(data.original.path),
    //             // 		dataType: ko.observable(data.type)
    //             // 	}
    //             // );

    //             if (self.isNewSlider) {
    //                 self.addNewSliderContent(imgUrl, data.text);
    //                 self.initiateSlider();
    //                 self.isNewSlider = false;
    //                 return;
    //             }

    //             $("#browserTabCarousel").trigger('add.owl.carousel', [self.addNewSliderContent(imgUrl, data.text)]).trigger('refresh.owl.carousel');
    //         }
    //     };
    // };

    self.openInNewTab = function (data, event) {

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
        else if (ko.utils.unwrapObservable(data.dataType) == 'file') {
            var fileType = self.getFileExtension(data.itemName());
            if (fileType == 'html' || fileType == 'htm') {
                var oReq = new XMLHttpRequest();
                oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.originalPath(), true);
                oReq.responseType = "arraybuffer";

                oReq.send();

                oReq.onload = function (oEvent) {
                    if (this.status == 200) {
                        var arrayBuffer = oReq.response;
                        var byteArray = new Uint8Array(arrayBuffer);

                        var blob = new Blob([arrayBuffer], { type: fileType });
                        var fileSrc = URL.createObjectURL(blob);

                        showBrowserItemModal(fileSrc, data.itemName());

                    }
                };
                return;
            }
        }

        $.redirect(self.dataSourcesURI, { 'download': ko.utils.unwrapObservable(data.originalPath) }, "POST", "_blank");

    };

    self.loadItems = function (data) {
        self.browserItems([]);
        self.destroySlider();
        self.isNewSlider = true;

        if(!self.isListView()){

            
        }

        if (data.children.length == 0) {

            var imgUrl = data.type == "folder" ? self.folderImgPath : self.fileImgPath;

            if (data.type == "file") {
                var fileType = self.getFileExtension(data.text);

                if (self.imageTypes.includes(fileType)) {
                    self.pushImg(data, fileType);
                }
                else {
                    self.browserItems.push(
                        {
                            imgPath: ko.observable(imgUrl),
                            itemName: ko.observable(data.text),
                            originalPath: ko.observable(data.original.path),
                            dataType: ko.observable(data.type)
                        }
                    );
                }
            }
            else {
                self.browserItems.push(
                    {
                        imgPath: ko.observable(imgUrl),
                        itemName: ko.observable(data.text),
                        originalPath: ko.observable(data.original.path),
                        dataType: ko.observable(data.type)
                    }
                );
            }
        }
        else {
            data.children.forEach(function (child) {
                var childNode = $("#tree").jstree(true).get_node(child);
                var imgUrl = childNode.type == "folder" ? self.folderImgPath : self.fileImgPath;

                if (childNode.type == "file") {
                    var fileType = self.getFileExtension(childNode.text);

                    if (self.imageTypes.includes(fileType)) {

                        self.pushImg(childNode, fileType);
                    }
                    else {
                        self.browserItems.push(
                            {
                                imgPath: ko.observable(imgUrl),
                                itemName: ko.observable(childNode.text),
                                originalPath: ko.observable(childNode.original.path),
                                dataType: ko.observable(childNode.type)
                            }
                        );
                    }
                }
                else {
                    self.browserItems.push(
                        {
                            imgPath: ko.observable(imgUrl),
                            itemName: ko.observable(childNode.text),
                            originalPath: ko.observable(childNode.original.path),
                            dataType: ko.observable(childNode.type)
                        }
                    );
                }
            });

        }
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
