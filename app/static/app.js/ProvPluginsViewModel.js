function ProvPluginsViewModel() {
    
    var self = this;
    self.provpluginsURI = '/provenance';
    self.graphsURI = '/graphs';
    self.dataSourcesURI = '/datasources';
    self.username = "";
    self.password = "";
    self.provplugins = ko.observableArray();
    self.provpluginFilter = ko.observable("");
    self.access = ko.observable("0");
    self.isListLog = ko.observable(true);
    self.fileImgPath = '/static/file_icon_blue.png';
    self.folderImgPath = '/static/folder_Icon_blue.png';
    this.filteredProvPlugins = ko.computed(function () {
        return this.provplugins().filter(function (task) {
            if (!self.provpluginFilter() || 
                (task.name() !== undefined && task.name().toLowerCase().indexOf(self.provpluginFilter().toLowerCase()) !== -1) ||
                (task.package() !== undefined && task.package().toLowerCase().indexOf(self.provpluginFilter().toLowerCase()) !== -1) ||
                (task.desc() !== undefined && task.desc().toLowerCase().indexOf(self.provpluginFilter().toLowerCase()) !== -1)
            )
                return task;
        });
    }, this);

    self.userList = ko.observableArray();

    self.logData = ko.observableArray();

    self.imageTypes = ["png", "jpg", "jpeg", "bmp", "gif", "ico", "ief", "jpe", "pbm", "pgm", "jng", "nef",
        "orf", "psd", "art", "pnm", "ppm", "rab", "rgb", "svg", "tif", "tiff", "xbm", "xpm", "xwd", "jp2",
        "jpm", "jpx", "jpf", "pcx", "svgz", "djvu", "djv", "pat", "cr2", "crw", "cdr", "cdt", "erf", "wbmp"];

    self.videoTypes = ["3gp", "axv", "dl", "dif", "dv", "fli", "gl", "ts", "ogv", "mxu", "flv", "lsf", "lsx", "mng", "asf",
        "asx", "wm", "wmv", "wmx", "wvx", "mpv", "mkv", "avi", "m1v", "mov", "movie", "mp4", "mpa", "mpe", "mpeg", "mpg", "webm"];

        self.itemName = ko.observable();
        self.itemSrc = ko.observable();
        self.currentItemPath = ko.observable();
        self.isListView = ko.observable(true);
        self.sliderItems = ko.observableArray();

    self.serviceaccesstypes = ko.observableArray([
        {
            Id: 0,
            Name: "Public"
        },
        {
            Id: 1,
            Name: "Shared"
        },
        {
            Id: 2,
            Name: "Private"
        }]);

    self.selectedServiceAccessType = ko.observable({
        Id: 0,
        Name: "Public"
    });

    // self.categories = ko.observableArray([
    //     {
    //         Id: 0,
    //         Name: "Basic"
    //     }, {
    //         Id: 1,
    //         Name: "Advanced"
    //     }
    // ]);

    self.selectedCategory = ko.observable({
        Id: 0,
        Name: "Basic"
    });

    self.selectCategory = function (category) {
        self.selectedCategory(category);
    }

    // self.selectServiceAccessType = function (serviceAccessType) {
    //     self.selectedServiceAccessType(serviceAccessType);
    //     self.load();
    // }

    self.click = function (model) {
        self.load();
        return true;
    }
	self.beginAdd = function()
	{}
    self.clearResults = function () {
        $("#output").val("");
        $("#error").val("");
        $("#log tbody").empty();
        $("#duration").text("0s");
        printExecStatus("");
    }

    self.updateTask = function (task, newTask) {
        var i = self.provplugins.indexOf(task);
        self.provplugins()[i].package(newTask.package);
        self.provplugins()[i].name(newTask.name);
        self.provplugins()[i].example(newTask.example);
        self.provplugins()[i].desc(newTask.desc);
    }

	// /provenance?demoserviceadd
	self.beginAddProvPlugin = function () {
        $("#add-library-info").text("");
        $.getJSON('/functions?demoserviceadd', function (demoservice) {
            addLibraryViewModel.getCodeEditor().setValue(demoservice.demoservice.script, 1);
            addLibraryViewModel.getMapperEditor().setValue(demoservice.demoservice.mapper, 1);
            addLibraryViewModel.getUsers();
            centerDialog($('#add'));
            $('#add').modal('show');
        })
    }

    self.about = function () {
        window.open("static/biodsl-help.html#services", '_blank');
    }


    self.beginEditLibrary = function (task) {
        // editTaskViewModel.setTask(task);
        $('#edit').modal('show');
    }
    self.edit = function (task, data) {
        ajaxcalls.simple(task.uri(), 'PUT', data).done(function (res) {
            self.updateTask(task, res.task);
        });
    }
    self.remove = function (task) {
        ajaxcalls.simple(task.uri(), 'DELETE').done(function () {
            self.provplugins.remove(task);
        });
    }
    self.markInProgress = function (task) {
        ajaxcalls.simple(task.uri(), 'PUT', { internal: "" }).done(function (res) {
            self.updateTask(task, res.task);
        });
    }
    self.markDone = function (task) {
        ajaxcalls.simple(task.uri(), 'PUT', { internal: "" }).done(function (res) {
            self.updateTask(task, res.task);
        });
    }

    self.load = $.debounce(500, function () {
        ajaxcalls.simple(self.provpluginsURI, 'GET', { 'level': 1, 'access': self.access() }).done(function (data) {

            if (!data || !data.provplugins)
                return;

            self.provplugins([]);
            $.each(data.provplugins, function (i, f) {
                self.provplugins.push({
                    package: ko.observable(f.package),
                    name: ko.observable(f.name),
                    example: ko.observable(f.example),
                    desc: ko.observable(f.desc),
                    expanded: ko.observable(false),
                    access: ko.observable(f.access),
                    isowner: ko.observable(f.isowner),
                    pluginID: ko.observable(f.pluginID),
                    sharedWith: ko.observableArray(f.sharedWith? JSON.parse(f.sharedWith): [])                    
                });
            });
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    });

    self.reload = $.debounce(500, function () {
        ajaxcalls.simple(self.provpluginsURI, 'GET', { 'reload': 1 }).done(function (data) {
            self.load(); // now load the data
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    });
    self.paramToArg = function(param) {
		paramarg = param.name
		if (param.default !== undefined) {
			var paramvalue = param.default;
			if (paramvalue.constructor == String) {
				paramvalue = "'" + paramvalue + "'";
			}
			paramarg = paramarg + "=" + paramvalue;
		}
		return paramarg;
    }
    self.copyToEditor = function (item) {

		exmpl = "plugin = Plugin.get('" + item.name() + "')\r\nplugin.apply(params)";
        var pos = editor.selection.getCursor();             
        editor.session.insert(pos, exmpl + "\r\n");
        editor.focus();
    }

    self.clicks = 0;
    self.timer = null;
    
    
    
    //service delete button
    self.serviceToolbar = function (item, event) {
	    event.stopPropagation();

        function areYouSure(confirmation){
            if(confirmation == true){
                ajaxcalls.simple('/provenance', 'GET', { 'service_id': item.serviceID(), 'confirm':'true' }).done(function (data){
                    if (data === undefined)
                            return;
                    
                    if (data.return == 'deleted'){
                        serviceDeleted();
                    }
                    else if (data.return == 'error')
                        alert("ERROR");
                    
                }).fail(function (jqXHR) {
                    alert("status="+jqXHR.status);
                });  
            }
            else
                return;
        }
 
	    function serviceDeleted(){
            alert("SERVICE DELETED!");          

            index = self.provplugins.indexOf(item);
            if (self.provplugins()[index].serviceID()== item.serviceID()){
                self.provplugins.splice( index, 1 );            //delete this service from obsarevalbe array                                                                
            }  
        }
	
	    var x = $(event.target).attr('id');
	    if (x === "delete") {
	    	ajaxcalls.simple('/provenance', 'GET', { 'service_id': item.serviceID() }).done(function (data) {
        		if (data === undefined)
                        return;    

                data = data.return;

                if(data == 'shared'){
                    confirmation = confirm("This is a shared service. You still want to delete "+item.name()+"()?");
                    areYouSure(confirmation);
                }
                else if (data == 'not_shared'){
                    confirmation = confirm("Do you want to delete "+item.name()+"()?");
                	areYouSure(confirmation);
                }        			
        		else if (data == 'error')
        			alert("ERROR");
        		                                
            }).fail(function (jqXHR) {
                    alert("status="+jqXHR.status);
            }); 
        }
        
        else if (x === "copyProv") {
			
			var package = "";
			if (item.package())
			{
				package = ", package = '" + item.package() +"'";
			}
	    	var content =  "module = Module.Get(name = '"+ item.name() +"'" + package + ")"
                            +"\r\nprint(View.Graph(module))"; 
            
            var pos = editor.selection.getCursor();
            editor.session.insert(pos, content + "\r\n");
            editor.focus();
        }
    }

    self.copyToEditorDblClick = function (itme, event) {
        event.preventDefault();
    }
    
    self.toggleExpand = function (item, event) {
        event.stopPropagation();

        self.clicks++;
        if (self.clicks !== 1) {
            clearTimeout(self.timer);
            self.copyToEditor(item);
            self.clicks = 0;
            return;
        }

        self.timer = setTimeout(function () {
            self.clicks = 0;
            event.preventDefault();
            var domItem = $(event.target);
            if (item.expanded()) {
                item.expanded(false);
                $(".expandedtask").remove();
            } else {
                $(".expandedtask").remove();
                self.provplugins().forEach(function (candidateSample) {
                    candidateSample.expanded(item === candidateSample);
                    if (item === candidateSample) {

                        var url = "/provenance?tooltip&name=" + item.name() + "&package=" + item.package();
                        initExmplDom(url);

                        $.ajax({
                            url: url
                        })
                        .then(function (content) {
                            // Set the tooltip content upon successful retrieval
                            if (content) {
                                content = JSON.parse(content);

                                tooltip = "<div class=\'expandedtask\'> <p>Name: " + content.name + (content.package && content.package.length ? "<br>Package: " + content.package : "") + "<br>Access: " + content.access + "</p>"
                                if (content.package && content.name && content.params && content.returns) {
                                    exmplDOM = '', retrnNo = 0, paramNo = 0;
                                    
                                    if(Array.isArray(content.returns)){
                                        content.returns.forEach(function (retrn){
                                            retrnNo++;
                                            exmplDOM += "<input onkeyup = \"editParam(this);\" onkeydown = \"return editBoxSize(this);\" class = 'form-control inputBox' type=\'text\' id=\'return " + retrnNo + "\' name=\"Return\" value=\'" + retrn.name + "\'> , ";                                            
                                        });
                                    }
                                    else{
                                        retrnNo++;
										var retname = content.returns.constructor == Object ? content.returns.name : content.returns;
                                        exmplDOM += "<input onkeyup = \"editParam(this);\" onkeydown = \"return editBoxSize(this);\" class = 'form-control inputBox' type=\'text\' id=\'return " + retrnNo + "\' name=\"Return\" value=\'" + retname + "\'> , ";
                                    }
                                    exmplDOM = exmplDOM.substring(0, exmplDOM.length - 2);
                                    exmplDOM += " = " + content.package + '.' + content.name + '( ';

                                    if(Array.isArray(content.params)){
                                        content.params.forEach(function (param){
                                            paramNo++;
                                            exmplDOM += "<input onkeyup = \"editParam(this);\" onkeydown = \"return editBoxSize(this);\" class = 'form-control inputBox' type=\'text\' id=\'param " + paramNo + "\' name=\"Param\" value=\'" + self.paramToArg(param) + "\'> , ";                                            
                                            // if(param.name == "outdir"){
                                            //     exmplDOM = exmplDOM.substring(0, exmplDOM.length - 3);
                                            //     exmplDOM += "=";
                                            //     paramNo++;
                                            //     if(param.default == "''")
                                            //         exmplDOM += "<input onkeyup = \"editParam(this);\" onkeydown = \"return editBoxSize(this);\" class = 'form-control inputBox' type=\'text\' id=\'param " + paramNo + " outdir\' name=\"Param\" value=\''" + param.default + "'\' placeholder='' > , ";
                                            //     else
                                            //         exmplDOM += "<input onkeyup = \"editParam(this);\" onkeydown = \"return editBoxSize(this);\" class = 'form-control inputBox' style = \" border-color : 'red';\" type=\'text\' id=\'param " + paramNo + "\' name=\"Param\" value=\'" + param.default + "\'> , ";                                            
                                            // }
                                        });
                                    }
                                    else{
                                        paramNo++;
                                        exmplDOM += "<input onkeyup = \"editParam(this);\" onkeydown = \"return editBoxSize(this);\" class = 'form-control inputBox' type=\'text\' id=\'param " + paramNo + "\' name=\"Param\" value=\'" + content.params + "\'> , ";
                                    }
                                    exmplDOM = exmplDOM.substring(0, exmplDOM.length - 2);
                                    exmplDOM += ")";
                                    
                                    tooltip += '<p><a href="javascript:void(0);" onclick="copy2Editor(\'' + url + '\')">Add: </a>' + exmplDOM;
                                }
                                tooltip += "</p>";

                                var descHref = (content.desc && content.desc.length ? "Desc: " + content.desc : "") + (content.href && content.href.length ? "<br>" + serviceHelpRef(content.href) : "");
                                if (descHref !== undefined && descHref.length) {
                                    tooltip += "<p>" + descHref + "</p>";
                                }
                                tooltip += "<p>Double click item to insert into code editor.</p></div>";

                                domItem.parent().append(tooltip);
                            }
                        }, function (xhr, status, error) {
                            // Upon failure... set the tooltip content to error
                        });
                    };
                });
            }
        }, 300);
    };

    self.destroySlider = function () {
        $('#logTabCarousel').trigger('destroy.owl.carousel');
    };

    self.emptyCarousel = function () {
        self.logData([]);
        self.destroySlider();
        $("#logTabCarousel").empty();
    };

    self.initiateSlider = function () {

        $("#logTabCarousel").owlCarousel({
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
                },
                1600: {
                    items: 5
                }
            }
        });
    };

    self.getImage = function (data, fileType) { 

        var oReq = new XMLHttpRequest();
        oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.path, true);
        oReq.responseType = "arraybuffer";
        var imgType = "image/" + fileType;

        oReq.send();

        oReq.onload = function (oEvent) {
            if (this.status == 200) {
                var arrayBuffer = oReq.response;
                // var byteArray = new Uint8Array(arrayBuffer);
                var blob = new Blob([arrayBuffer], { type: imgType });
                imgUrl = URL.createObjectURL(blob);
                // self.pushLogData(data, imgUrl);
                return imgUrl;
            }
        };
    };

    self.getFileExtension = function (filename) {
        return filename.substring(filename.lastIndexOf('.') + 1, filename.length) || filename;
    };

    self.getFileName = function (absolutePath) {
        return absolutePath.substring(absolutePath.lastIndexOf('/') + 1, absolutePath.length) || absolutePath;
    };

    self.pushLogData = function (element, datatype ) {  
        
        // if (self.imageTypes.includes(fileType)) {

        // }
        // else {
        //     self.logData.push(
        //         {
        //             name: element,
        //             data: element,
        //             imgUrl: self.fileImgPath
        //         }
        //     );
        // }
        var fileName = self.getFileName(element);
        var fileType = self.getFileExtension(fileName);

        switch (datatype) {
            case 0: //unknown
                break;
            case 1: //folder
                self.logData.push(
                    {
                        name: fileName,
                        data: element,
                        imgUrl: self.folderImgPath
                    }
                );
                break;
            case 2: //file
                self.logData.push(
                    {
                        name: fileName,
                        data: element,
                        imgUrl: self.fileImgPath
                    }
                );
                break;
            case 4: // image
                if (self.imageTypes.includes(fileType)) {
                    var imgUrl = self.getImage(element, fileType);
                
                    self.logData.push(
                        {
                            name: fileName,
                            data: element,
                            imgUrl: imgUrl
                        }
                    );
                }
                break;
            case 8: // video
                self.logData.push(
                    {
                        name: fileName,
                        data: element,
                        imgUrl: self.fileImgPath
                    }
                );
                break;
            case 16: //binary
                break;
            case 32: // text
                break;
            case 64: //csv
                self.logData.push(
                    {
                        name: fileName,
                        data: element,
                        imgUrl: self.fileImgPath
                    }
                );
                break;
            case 128: //sql
                self.logData.push(
                    {
                        name: fileName,
                        data: element,
                        imgUrl: self.fileImgPath
                    }
                );
                break;
            case 256: //custom
                break;
            case 512: //root
                break;
            case 1024: //fileList
                self.logData.push(
                    {
                        name: fileName,
                        data: element,
                        imgUrl: self.fileImgPath
                    }
                );
                break;
            case 2048: //folderlist
                self.logData.push(
                    {
                        name: fileName,
                        data: element,
                        imgUrl: self.folderImgPath
                    }
                );
                break;
            case 4096: //value type
                break;
            default:
                break;
        }
    };

    self.loadLogData = function (logDataArray) {  
        self.emptyCarousel();
        logDataArray.forEach(dataInfo => {
            dataInfo.data.forEach(element => {
                let datatype = parseInt(element.datatype)

                switch (datatype) {
                    case 0: //unknown
                        break;
                    case 1: //folder
                        self.pushLogData(element.data, 1);
                        break;
                    case 2: //file
                        self.pushLogData(element.data, 2);
                        break;
                    case 4: // image
                        self.pushLogData(element.data, 4);
                        break;
                    case 8: // video
                        self.pushLogData(element.data, 8);
                        break;
                    case 16: //binary
                        break;
                    case 32: // text
                        break;
                    case 64: //csv
                        self.pushLogData(element.data, 64);
                        break;
                    case 128: //sql
                        self.pushLogData(element.data, 128);
                        break;
                    case 256: //custom
                        break;
                    case 512: //root
                        break;
                    case 1024: //fileList
                        element.data.forEach(ele => {
                            self.pushLogData(ele, 1024);
                        });
                        break;
                    case 2048: //folderlist
                        element.data.forEach(ele => {
                            self.pushLogData(ele, 2048);
                        });
                        break;
                    case 4096: //value type
                        break;
                    default:
                        break;
                }
            });
        });
    };

    //TODO: need to modify for output tab list view
    self.openInDetailsView = function (data, ele) {
        var fileType = self.getFileExtension(data.data);
        
        self.currentItemPath('');

        self.currentItemPath(data.data);

        if (self.imageTypes.includes(fileType)) {
            // self.showModal(data);
            self.itemSrc(data.data);
            self.itemName(data.name);
            $('.nav-tabs a[href="#outputtab"]').tab('show');
        }

        else if (self.videoTypes.includes(fileType)) {
            var oReq = new XMLHttpRequest();
            oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.data, true);
            oReq.responseType = "arraybuffer";
            var videoType = "video/" + fileType;
            self.itemName(data.name);
            oReq.send();

            oReq.onload = function (oEvent) {
                if (this.status == 200) {
                    var arrayBuffer = oReq.response;
                    var blob = new Blob([arrayBuffer], { type: videoType });
                    itemSrc = URL.createObjectURL(blob);
                    self.itemSrc(itemSrc);
                    // self.showModal(data, itemSrc);
                    $('.nav-tabs a[href="#outputtab"]').tab('show');
                }
            };
        }
        else if (fileType == 'htm' || fileType == 'html') {
            var oReq = new XMLHttpRequest();
            oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.data, true);
            oReq.responseType = "arraybuffer";

            oReq.send();
            self.itemName(data.data);
            oReq.onload = function (oEvent) {
                if (this.status == 200) {
                    var arrayBuffer = oReq.response;
                    var blob = new Blob([arrayBuffer], { type: "text/html" });
                    var reader = new FileReader();
                    reader.readAsDataURL(blob);
                    reader.onload = function () {
                        var base64UrlString = reader.result;
                        self.itemSrc(base64UrlString);
                        $('#liOutput').show();
                        $('.nav-tabs a[href="#outputtab"]').tab('show');
                    }
                }
            };
        }
        
        else {
            self.itemSrc('');
            return;
        }
    };

    self.sliderController = function (data, element) { 
        self.destroySlider();
        self.initiateSlider();
    }

    self.shareWithUsers = function (data, e) {  
        e.stopPropagation();
        taskSharingViewModel.shareWithUsers(data);
    }
    
};

function TaskSharingViewModel() {
    var self = this;
    self.provpluginsURI = '/provenance';
    self.selectedSharedUsers = ko.observableArray();
    self.selectedTask = ko.observable();
    self.access = ko.observable();
    self.userList = ko.observableArray();
    self.access.subscribe(function(newVal){
        if (newVal) {
            $("#ddlShareService").multiselect('disable');
        } else {
            $("#ddlShareService").multiselect('enable');
        }
    });

    self.saveServiceSharing = function () {  
        self.selectedTask().access= self.access();
        self.selectedTask().sharedWith = ko.toJS(self.selectedSharedUsers);
        ajaxcalls.simple(self.provpluginsURI, 'GET', {'share_service': ko.toJSON(self.selectedTask)}).done(function (res) {
            

        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });;
    }

    self.initiateMultiselect = function () {  
        $("#ddlShareService").multiselect(
                {
                    includeSelectAllOption: true,
                    inheritClass: true,
                    buttonWidth: '100%',
                    enableFiltering: true,
                    dropUp: false,
                    maxHeight: 200
                }
            );
    }

    self.getUsers = function () { 
        self.userList([]);
        
        ajaxcalls.simple(self.provpluginsURI, 'GET', { 'users': 1 }).done(function (data) {
            
            JSON.parse(data).forEach(element => {
                self.userList.push({id: element[0], name:  element[1]});
            });
            self.initiateMultiselect();
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.shareWithUsers = function (selectedTask) {  
        self.getUsers();
        self.selectedTask(selectedTask);
        $("#ddlShareService").multiselect('deselectAll', false);
        $("#ddlShareService").multiselect('updateButtonText');
        self.selectedSharedUsers([]);
        self.selectedSharedUsers(selectedTask.sharedWith());
        if (selectedTask.access() == 0) {
            self.access(true);
        } else {
            self.access(false);
        }
        
        $('#modalShareService').modal('show'); 
    }
}