function TasksViewModel() {
    
    var self = this;
    self.tasksURI = '/functions';
    self.graphsURI = '/graphs';
    self.username = "";
    self.password = "";
    self.tasks = ko.observableArray();
    self.taskFilter = ko.observable("");
    self.access = ko.observable("0");
    self.isListLog = ko.observable(true);
    self.fileImgPath = '/static/file_icon_blue.png';
    self.folderImgPath = '/static/folder_Icon_blue.png';
    this.filteredTasks = ko.computed(function () {
        return this.tasks().filter(function (task) {
            if (!self.taskFilter() || task.name().toLowerCase().indexOf(self.taskFilter().toLowerCase()) !== -1
                || task.package().toLowerCase().indexOf(self.taskFilter().toLowerCase()) !== -1)
//                || task.group().toLowerCase().indexOf(self.taskFilter().toLowerCase()) !== -1)
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

    self.clearResults = function () {
        $("#output").val("");
        $("#error").val("");
        $("#log tbody").empty();
        $("#duration").text("0s");
        printExecStatus("");
    }

    self.updateTask = function (task, newTask) {
        var i = self.tasks.indexOf(task);
        self.tasks()[i].package(newTask.package);
        self.tasks()[i].name(newTask.name);
        self.tasks()[i].internal(newTask.internal);
        self.tasks()[i].example(newTask.example);
        self.tasks()[i].example2(newTask.example2);
        self.tasks()[i].desc(newTask.desc);
        self.tasks()[i].runmode(newTask.runmode);
        self.tasks()[i].group(newTask.group);
        self.tasks()[i].href(newTask.href);
    }

    self.beginAddLibrary = function () {
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

    self.updateWorkflow = function (save) {
        var script = $.trim(editor.getSession().getValue());
        if (!script && !workflowId) // || editor.session.getUndoManager().isClean())
            return; // if script empty and workflowId not set, it means (empty) workflow is not set yet.

        // workflow not saved yet
        if (!workflowId) {

            // Show save dialog if user explicitely clicked save/saveas button
            if (save) {
                return samplesViewModel.beginAdd();
            }

            // save with default name and private access.
        }

        var formdata = new FormData();

        formdata.append('workflowId', parseInt(workflowId));
        formdata.append('script', script);

        ajaxcalls.form(self.tasksURI, 'POST', formdata, false).done(function (data) {
            if (!$.isEmptyObject(data)) {
                workflowId = parseInt(data['workflowId']);
                $('#script-name').text(data['name']);
                editor.session.getUndoManager().markClean();
            }
        });
    }

    self.runBioWLInternal = function (task) {
        if (!workflowId) {
            $("#error").val("Workflow is not updated. Change the code and run again.");
            return;
        }

        var script = $.trim(editor.getSession().getValue());
        if (!script)
            return;

        $('#refresh').show();
        var formdata = new FormData();

        formdata.append('workflowId', parseInt(workflowId));
        formdata.append('args', $('#args').val());
        formdata.append('immediate', $('#immediate').prop('checked'));
        self.clearResults();
        ajaxcalls.form(self.tasksURI, 'POST', formdata).done(function (data) {
            $('#refresh').hide();

            if (data === undefined)
                return;

            reportId = parseInt(data.runnableId);

            runnablesViewModel.load();
            runnablesViewModel.loadHistory(reportId, true);

        }).fail(function (jqXHR, textStatus) {
            $('#refresh').hide();
            showXHRText(jqXHR);
        });
    }

    self.runBioWL = function (task) {
        var updateDlg = self.updateWorkflow();
        if (updateDlg) {
            updateDlg.on('hidden.bs.modal', function () { self.runBioWLInternal(task); });
        }
        else
            self.runBioWLInternal(task);
    }

    self.buildGoSimpleGraph = function (task) {
        var updateDlg = self.updateWorkflow();
        if (updateDlg) {
            updateDlg.on('hidden.bs.modal', function () { self.buildGraphInternal(task); });
        }
        else
            self.buildSimpleGraphInternal(task);
    }
    
    self.buildGoDetailGraph = function (task) {
        var updateDlg = self.updateWorkflow();
        if (updateDlg) {
            updateDlg.on('hidden.bs.modal', function () { self.buildGraphInternal(task); });
        }
        else
            self.buildDetailGraphInternal(task);
    }
    
    self.buildSimpleGraphInternal = function (task) {
        if (!$.trim(editor.getSession().getValue()))
            return;

        var formdata = new FormData();

        formdata.append('workflowId', parseInt(workflowId));
        ajaxcalls.form(self.graphsURI, 'POST', formdata).done(function (data) {

        	data = JSON.parse(data);
            
        	 //if JSON is empty, clear both canvas
            if ($.isEmptyObject(data)){
            	var graphdiv = document.getElementById("graph");
            	var overviewdiv = document.getElementById("DiagramOverview");                
                if(graphdiv == null)
    				return;    			
                else {
    				graph = document.querySelector('canvas');
    				context = graph.getContext('2d');
    				context.clearRect(0, 0, graph.width, graph.height);
    			}
    			
    			if(overviewdiv == null)
    				return;    			
                else {
    				overview = overviewdiv.querySelector('canvas');
    				context = overview.getContext('2d');
    				context.clearRect(0, 0, overview.width, overview.height);
    			}
            }
        	
        	else if (data === undefined)
                return;

            simplegojsGraph.show(data);
            //d3graph.show(data);

        }).fail(function (jqXHR, textStatus) {
            $('#refresh').hide();
            showXHRText(jqXHR);
        });
    }
    
    self.buildDetailGraphInternal = function (task) {
        if (!$.trim(editor.getSession().getValue()))
            return;

        var formdata = new FormData();

        formdata.append('workflowId', parseInt(workflowId));
        ajaxcalls.form(self.graphsURI, 'POST', formdata).done(function (data) {
                    	
            data = JSON.parse(data);
            
            //if JSON is empty, clear both canvas
            if ($.isEmptyObject(data)){
            	var graphdiv = document.getElementById("graph");
            	var overviewdiv = document.getElementById("DiagramOverview");                
                if(graphdiv == null)
    				return;    			
                else {
    				graph = document.querySelector('canvas');
    				context = graph.getContext('2d');
    				context.clearRect(0, 0, graph.width, graph.height);
    			}
    			
    			if(overviewdiv == null)
    				return;    			
                else {
    				overview = overviewdiv.querySelector('canvas');
    				context = overview.getContext('2d');
    				context.clearRect(0, 0, overview.width, overview.height);
    			}
            }
        	
        	else if (data === undefined)
                return;
            
            detailgojsGraph.show(data);
            //d3graph.show(data);

        }).fail(function (jqXHR, textStatus) {
            $('#refresh').hide();
            showXHRText(jqXHR);
        });
    }

    self.provenance = function () {
        $.redirect(self.tasksURI, { 'provenance': true }, "POST", "_blank");
    }

    self.generatePythonCode = function (task) {
        $('#refresh').show();
        var formdata = new FormData();
        formdata.append('code', editor.getSession().getValue());
        formdata.append('args', $('#args').val());
        formdata.append('immediate', $('#immediate').prop('checked'));
        ajaxcalls.form(self.tasksURI, 'POST', formdata).done(function (data) {
            $('#refresh').hide();
            if (data === undefined)
                return;

            data = JSON.parse(data);

            $("#output").val(data.out);
            $("#error").val(data.err);
            $("#log tbody").empty();
            jsonArray2Table($("#log"), data['log']);
            printExecStatus(data['status']);
            $("#duration").text(data.duration + 's');
        });
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
            self.tasks.remove(task);
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
        ajaxcalls.simple(self.tasksURI, 'GET', { 'level': 1, 'access': self.access() }).done(function (data) {

            if (!data || !data.functions)
                return;

            self.tasks([]);
            $.each(data.functions, function (i, f) {
                self.tasks.push({
                    package: ko.observable(f.package),
                    name: ko.observable(f.name),
                    //internal: ko.observable(f.internal),
                    example: ko.observable(f.example),
                    example2: ko.observable(f.example2),
                    desc: ko.observable(f.desc),
                    //runmode: ko.observable(f.runmode),
                    group: ko.observable(f.group),
                    href: ko.observable(f.href),
                    expanded: ko.observable(false),
                    access: ko.observable(f.access),
                    isOwner: ko.observable(f.is_owner),
                    serviceID: ko.observable(f.service_id),

                    // internal: ko.observable(f.internal),
                    returns: ko.observable(f.returns),
                    params: ko.observable(f.params),                    
                    returnData: ko.observable(f.returnData),                    
                });
            });
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });

        self.getUsers();
    });

    self.reload = $.debounce(500, function () {
        ajaxcalls.simple(self.tasksURI, 'GET', { 'reload': 1 }).done(function (data) {
            self.load(); // now load the data
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    });

    self.copyToEditor = function (item) {
        var pos = editor.selection.getCursor();
        editor.session.insert(pos, self.selectedCategory().Id == 0 ? item.example() + "\r\n" : item.example2() + "\r\n");
        editor.focus();
    }

    self.clicks = 0;
    self.timer = null;
    
    
    
    //service delete button
    self.serviceToolbar = function (item, event) {
	    event.stopPropagation();
	    
	    function serviceDeleted(){
            alert("SERVICE DELETED!");            
            index = self.tasks.indexOf(item);
            if (self.tasks()[index].serviceID()== item.serviceID()){
                self.tasks.splice( index, 1 );            //delete this service from obsarevalbe array                                                                
            }  
	    }
	
	    var x = $(event.target).attr('id');
	    if (x === "delete") {
	    	ajaxcalls.simple('/functions', 'GET', { 'service_id': item.serviceID() }).done(function (data) {            
                console.log(data);    
        		if (data === undefined)
                        return;                
                data = data.return;
                
                if(data == 'shared'){
                	confirmation = confirm("This is a shared service. You still want to delete "+item.name()+"()?");
                	if(confirmation == true){
                		ajaxcalls.simple('/functions', 'GET', { 'service_id': item.serviceID(), 'confirm':'true' }).done(function (data){                	          
                    		if (data === undefined)
                                    return;
                    		
                            if (data.return == 'true'){
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
                else if (data == 'true'){
                	serviceDeleted();
                }        			
        		else if (data == 'error')
        			alert("ERROR");
        		                                
                }).fail(function (jqXHR) {
                        alert("status="+jqXHR.status);
                }); 
            }

            else if (x === "shareDropdown") {
                alert('service share button hit');
                serviceID = item.serviceID();
                ajaxcalls.simple('/functions', 'GET', { 'share_service': item.serviceID() }).done(function (data) {
                    if (data === undefined)
                        return; 
    
                    console.log(data);
                    data = data.return;
                    
                    if(data !== undefined){
                        
                        //for selecting shared user                    
                    }
                    
                }).fail(function (jqXHR) {
                    alert("status="+jqXHR.status);
                });                 
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
                self.tasks().forEach(function (candidateSample) {
                    candidateSample.expanded(item === candidateSample);
                    if (item === candidateSample) {

                        var url = "/functions?tooltip&name=" + item.name() + "&package=" + item.package();
                        $.ajax({
                            url: url
                        })
                            .then(function (content) {
                                // Set the tooltip content upon successful retrieval
                                if (content) {
                                    content = JSON.parse(content);

                                    tooltip = "<div class=\'expandedtask\'> <p>Name: " + content.name + (content.package && content.package.length ? "<br>Package: " + content.package : "") + "<br>Access: " + content.access + "</p>"
                                    if (content.example) {
                                        tooltip += '<p><a href="javascript:void(0);" onclick="copy2Editor(\'' + url + '\', 0); return false;">Add: </a>' + content.example;
                                    }
                                    if (content.example2 && content.example !== content.example2) {
                                        tooltip += '<br><a href="javascript:void(0);" onclick="copy2Editor(\'' + url + '\', 1); return false;">Add: </a>' + content.example2;
                                    }
                                    if (content.returns) {
                                        tooltip += "<br>Returns: " + content.returns;
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

    self.getFileExtension = function (filename) {
        return filename.substring(filename.lastIndexOf('.') + 1, filename.length) || filename;
    };

    self.pushLogData = function (element, datatype ) {  
        // let fileType = self.getFileExtension(element);
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

        switch (datatype) {
            case 0: //unknown
                break;
            case 1: //folder
                self.logData.push(
                    {
                        name: element,
                        data: element,
                        imgUrl: self.folderImgPath
                    }
                );
                break;
            case 2: //file
                self.logData.push(
                    {
                        name: element,
                        data: element,
                        imgUrl: self.fileImgPath
                    }
                );
                break;
            case 4: // image

                break;
            case 8: // video
                self.logData.push(
                    {
                        name: element,
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
                        name: element,
                        data: element,
                        imgUrl: self.fileImgPath
                    }
                );
                break;
            case 128: //sql
                self.logData.push(
                    {
                        name: element,
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
                        name: element,
                        data: element,
                        imgUrl: self.fileImgPath
                    }
                );
                break;
            case 2048: //folderlist
                self.logData.push(
                    {
                        name: element,
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

    self.loadLogData = function (data) {  
        self.emptyCarousel();
        data.forEach(element => {
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
    };

    self.sliderController = function (data, element) { 
        self.destroySlider();
        self.initiateSlider();
    }

    self.getUsers = function () { 
        self.userList([]);
        // self.selectedSharingUsers([]); 
        ajaxcalls.simple(self.tasksURI, 'GET', { 'users': 1 }).done(function (data) {
            
            JSON.parse(data).forEach(element => {
                self.userList.push({id: element[0], name:  element[1]});
            });

            // self.initiateMultiselectUser()
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }
};
