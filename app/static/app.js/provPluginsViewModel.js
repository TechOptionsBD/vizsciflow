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
        $("#add-library-info").val("");
        $.getJSON('/provenance?demoprovenanceadd', function (demoprovenance) {
            addProvPluginViewModel.getCodeEditor().setValue(demoprovenance.demoprovenance.script, 1);
            addProvPluginViewModel.getHtmlEditor().setValue(demoprovenance.demoprovenance.html, 1);
            // AddProvPluginViewModel.getUsers();
            centerDialog($('#addProv'));
            $('#addProv').modal('show');
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
                ajaxcalls.simple('/provenance', 'GET', { 'delete': item.pluginID(), 'confirm':'true' }).done(function (data){
                    if (data === undefined)
                            return;
                    
                    if (data.success){
                        serviceDeleted(data.success);
                    }
                    else if (data.error){
                        alert(data.error);
					}
                    
                }).fail(function (jqXHR) {
                    alert("status="+jqXHR.status);
                });  
            }
            else
                return;
        }
 
	    function serviceDeleted(msg){
            alert(msg);          

            index = self.provplugins.indexOf(item);
            if (self.provplugins()[index].pluginID()== item.pluginID()){
                self.provplugins.splice( index, 1 );            //delete this service from obsarevalbe array                                                                
            }  
        }
	
	    var x = $(event.target).attr('id');
	    if (x === "delete") {
	    	ajaxcalls.simple('/provenance', 'GET', { 'delete': item.pluginID() }).done(function (data) {
        		if (data === undefined)
                        return;    

                if (data.success){
                    serviceDeleted(data.success);
                }
                else if (data.error) {
					alert(data.error);
				}
                else if(data.shared){
                    confirmation = confirm("This is a shared service. You still want to delete "+item.name()+"()?");
                    areYouSure(confirmation);
                }
                else if (data.notshared){
                    confirmation = confirm("Do you want to delete "+item.name()+"()?");
                	areYouSure(confirmation);
                }
        		                                
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
                            +"\r\nView.Graph(module)"; 
            
            var pos = editor.selection.getCursor();
            editor.session.insert(pos, content + "\r\n");
            editor.focus();
        }
    }

    self.copyToEditorDblClick = function (item, event) {
        event.preventDefault();
        self.copyToEditor(item);
    }
    
    self.toggleExpand = function (item, event) {
        event.stopPropagation();
        self.clicks++;
        if (self.clicks !== 1) {
            $(".expandedProvenance").remove();
            self.copyToEditor(item);
            self.clicks = 0;
            return;
        }
        else {
            self.clicks= 0;
            var domItem = $(event.target);
            if (item.expanded()) {
                item.expanded(false);
                $(".expandedProvenance").remove();
                return
            } 
            else {
                $(".expandedProvenance").remove();
                item.expanded(true)

                tooltip = "<div class=\"expandedProvenance\"> <p>Name: " + item.name() + "<br>Package: " + item.package();
                tooltip += "</p>";
                tooltip += "<p>Double click item to insert into code editor.</p></div>";

                domItem.parents('.draggable-provenance').append(tooltip);
            }
        }
    };

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