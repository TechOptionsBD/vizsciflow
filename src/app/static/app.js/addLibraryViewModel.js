function AddLibraryViewModel(userName) {
    var self = this;
    self.tasksURI = '/functions';
    self.name = ko.observable(userName);
    self.org = ko.observable();
    self.access = ko.observable(true);
    self.userList = ko.observableArray();
    self.selectedSharingUsers = ko.observableArray();
    self.newVenvName = ko.observable('');
    self.newDockerImageName = ko.observable('');
    self.newDockerContainerName = ko.observable('');
    self.isFuncExpanded = ko.observable(false);
    self.textToggleFuncArea = ko.observable('More..');
    self.TList = ko.observableArray();
    self.pippkgsList = ko.observableArray();
    self.containersList = ko.observableArray();
    self.imagesList = ko.observableArray();
    self.radioSelectedOptionValue = ko.observable('newvenv'); 
    self.modulepath = "";
    self.submittedData = ko.observableArray([]);
    self.submittedData = self.containersList;

   
    self.mapperEditor = CreateAceEditor("#mapper", "ace/mode/json", 430, true);
    self.codeEditor = CreateAceEditor("#servicescript", "ace/mode/python", 350);

    self.hasNewVenvName = ko.computed(function () { 
        return self.newVenvName() !== undefined && self.newVenvName().trim().length > 0; 
    });
    
    self.NotHasNewVenvName = ko.computed(function () { 
        return self.newVenvName() === undefined || self.newVenvName().trim().length == 0; 
    });

    self.hasDockerContainerName = ko.computed(function () { 
        return ((self.newDockerImageName() !== undefined && self.newDockerContainerName() !== undefined) && (self.newDockerImageName().trim().length > 0 && self.newDockerContainerName().trim().length > 0)); 
    });
    
    self.NotHasDockerContainerName = ko.computed(function () { 
        return self.newDockerImageName() === undefined || self.newDockerContainerName() === undefined || self.newDockerImageName().trim().length == 0 || self.newDockerContainerName().trim().length == 0; 
    });
    self.hasDockerContainerNameActive = ko.computed(function () { 
        return self.newDockerImageName() !== undefined && self.newDockerImageName().trim().length > 0;
    });
    
    self.NotHasDockerContainerNameActive = ko.computed(function () { 
        return self.newDockerImageName() === undefined || self.newDockerImageName().trim().length == 0; 
    });

    self.addNewVenv = function() {
        if (self.newVenvName().trim().length == 0)
            return;
        ajaxcalls.simple(self.tasksURI, 'GET', { 'newpyvenvs':  self.newVenvName(), 'pyversion' : self.radioSelectedOptionValue()}).done(function (data) {
            if (!data['err']){
                self.newVenvName('');
                self.loadpipvenvs();
            }
            else {
                $("#add-library-info").text("Error on creating virtual env: " + data['err']);
            }
            
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.addNewDockerContainer = function() {
        if (self.newDockerImageName().trim().length == 0 && self.newDockerContainerName().trim().length == 0)
            return;
        ajaxcalls.simple(self.tasksURI, 'GET', { 'newdockerimagename':  self.newDockerImageName(), 'newdockercontainername' : self.newDockerContainerName()}).done(function (data) {
            if (!data['err']){
                self.newDockerImageName('');
                self.newdockercontainername('');
            }
            else {
                $("#add-library-info").text("Error on creating docker: " + data['err']);
            }
            
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
        alert('done');
        console.log('done');
    }

    self.loadpipvenvs = function(){
        self.pippkgsList.removeAll();
        ajaxcalls.simple(self.tasksURI, 'GET', { 'pyenvs': '' }).done(function (data) {
            
            $(data["pyvenvs"]).each((index, element)=> {
                self.pippkgsList.push(element);
            });
            
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.loadcontainers = function(){
        self.containersList.removeAll();
        ajaxcalls.simple(self.tasksURI, 'GET', { 'dockercontainers': '' }).done(function (data) {
            
            $(data["dockercontainers"]).each((index, element)=> {
                self.containersList.push(element.name);
            });
            
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.loadimages = function(){
        self.imagesList.removeAll();
        ajaxcalls.simple(self.tasksURI, 'GET', { 'dockerimages': '' }).done(function (data) {
            
            $(data["dockerimages"]).each((index, element)=> {
                self.imagesList.push(element.nametag);
            });
            
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.loaddatatypes = function(){
        self.TList.removeAll();
        ajaxcalls.simple(self.tasksURI, 'GET', { 'datatypes': '' }).done(function (data) {
            $(data["datatypes"]).each((index, element)=> {
                self.TList.push(element);
            });
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }
    self.loaddatatypes();
    self.loadcontainers();
    self.loadimages();

    self.submitData = function() {
      var inputData = self.newDockerContainerName();
      if (inputData !== '') {
        if (!self.submittedData().includes(inputData)) {
        //   self.submittedData.push(inputData);
        } else {
          alert('Data is already added.');
        }
      }
  
      // Clear the input box
    //   self.newDockerContainerName('');
    };
  
    self.checkTypingData = function() {
      debounceLogData(self.newDockerContainerName());
    };
  
    var typingTimer;
    function debounceLogData(data) {
      clearTimeout(typingTimer);
      typingTimer = setTimeout(function() {
      }, 300); // Delay of 300 milliseconds (adjust as needed)
    }

    self.getLibrary = function(){
        $("#add-library-info").text("");
        ajaxcalls.simple(self.tasksURI, 'GET', { 'demoserviceadd':  $("#selected_tool_type").val()}).done(function (demoservice) {
            $("#module").val("");
            self.newVenvName("");

            self.getUsers();
            self.loadpipvenvs();
            self.loadcontainers();
            self.getCodeEditor().setValue(demoservice.demoservice.script, 1);
            self.editService(demoservice.demoservice.mapper)
            
            if (demoservice.demoservice.mapper && 'access' in demoservice.demoservice.mapper) {
                self.access = demoservice.demoservice.mapper['access'] == 'True'
            }
        });
    }

    self.beginAddLibrary = function () {
        self.getLibrary();
        centerDialog($('#add'));
        $('#add').modal('show')
            .on('show.bs.modal', function () {
                if(dropperModule.files.length > 0){
                    dropperModule.removeAllFiles();
                }
            });
    }

    //for uploading package

    self.beginAddPackage = function ()
    {
        centerDialog($('#addPackage'));
        $('#addPackage').modal('show')
            .on('show.bs.modal', function () {
                $("#add-package-info").text("");
                $("#packagemodule").val("");
                $( "#packagemodule" ).change();

                if(dropperPackage.files.length > 0){
                    dropperPackage.removeAllFiles();
                }

            });
        }


    self.toggleFuncArea = function () {
        if (!self.isFuncExpanded()) {
            self.isFuncExpanded(true);
            self.textToggleFuncArea('Less');
        }
        else{
            self.isFuncExpanded(false);
            self.textToggleFuncArea('More..');
        }
    };

    self.service = ko.observableDictionary(
        {   
            package: '',
            name: 'MyService',
            internal: '',   
            org: '',
            group: '',
            desc: '',
            href: '',
            pippkgs: '',
            pipvenv: '',
            reqfile: '',
        }
    );

    self.editService = (refData) => {
        refData.internal && self.service.set('internal',refData.internal)
        refData.name && self.service.set('name',refData.name)
        refData.package && self.service.set('package',refData.package)
        refData.org && self.service.set('org',refData.org)
        refData.group && self.service.set('group',refData.group)
        refData.pippkgs && self.service.set('pippkgs',refData.pippkgs)
        refData.reqfile && self.service.set('reqfile',refData.reqfile)
        refData.pipvenv && self.service.set('pipvenv',refData.pipvenv)
        
        self.serviceParams([]);
        refData.params.map(param => {
            self.addParam(param)
        })

        self.serviceReturns([]);
        if(Array.isArray(refData.returns)){
            refData.returns.map(item => {
                self.addServiceReturns(item)
            })
        }
        else if(refData.returns.constructor == Object){
            self.addServiceReturns(refData.returns)
        }
    }

    self.serviceParams = ko.observableArray();

    self.serviceReturns = ko.observableArray();

    self.addParam = function (param = null) {   
        self.serviceParams.push(
            ko.observableDictionary(
                {
                    name: param.name && typeof(param.name) !== 'function' ? param.name : '',
                    type: param.type ?? '',
                    desc: param.desc ?? '',
                    default: param.default ?? ''
                }
            )
        );
        self.liveJsonView();
    };

    self.addServiceReturns = function (returns = null) {
        self.serviceReturns.push(
            ko.observableDictionary(
                {
                    name: returns.name && typeof(returns.name) !== 'function' ? returns.name : '',
                    type: returns.type ?? '',
                    desc: returns.desc ?? ''
                }
            )
        );
        self.liveJsonView();
    }

    self.removeParam = function (data, e) {  
        self.serviceParams.remove(data);
        self.liveJsonView();
    };

    self.removeServiceReturns = function(data, e){
        self.serviceReturns.remove(data);
        self.liveJsonView();
    }

    self.liveJsonView = function () {                
        var jsonPreview = Object.entries(JSON.parse(JSON.stringify(self.service))).reduce(( obj ,[key,value])=>{
            if(value.length) 
                obj[key] = value;
            return obj;
        }, {});
        
        if(self.serviceParams().length){
            jsonPreview.params = self.serviceParams;
        }

        if (self.serviceReturns().length) {
            jsonPreview.returns = self.serviceReturns;
        }

        var jsonPrettyText = ko.toJSON(jsonPreview, null, 4);        
        self.mapperEditor.session.setValue(jsonPrettyText);
    };
    
    self.checkFunction = function() {
        
        var serviceName = (self.service.get('name') ? self.service.get('name') : self.service.get('internal'));
        if (!serviceName) {
            $("#add-library-info").text("No valid service name is given.");
            return false;
        }
        
        var package = (self.service.get('package') ? self.service.get('package') : "");
        var serviceFormatted = JSON.parse(JSON.stringify(self.service)) ;
        serviceFormatted.params = self.serviceParams;
        serviceFormatted.returns = self.serviceReturns;

        var success = false;
        ajaxcalls.simple(self.tasksURI, 'GET', { 'check_function': '', 'package':  package, 'name': serviceName, 'script': self.codeEditor.getSession().getValue(), 'mapper': ko.toJSON(serviceFormatted)}, false).done(function(data) {
            
            if (data === undefined) {
                $("#add-library-info").text("Can't retrieve service information. Check your internet connection.");
                return;
            }
            
            success = data['error'] === undefined;
            if (!success) {
                $("#add-library-info").text(data['error']);
            }
        });
        
        return success;
    }
    
    self.initiateMultiselectUser = function () {  
        $("#userSelection").multiselect({
            includeSelectAllOption: true,
            inheritClass: true,
            buttonWidth: '100%',
            enableFiltering: true,
            dropUp: true,
            maxHeight: 200
        });
    };

    self.access.subscribe(function(newVal){
        if (newVal) {
            // $("#userSelection").multiselect('deselectAll');
            // $("#userSelection").multiselect('updateButtonText');
            $("#userSelection").multiselect('disable');
        } else {
            $("#userSelection").multiselect('enable');
        }
    });

    self.getUsers = function () { 
        self.userList([]);
        self.selectedSharingUsers([]); 
        ajaxcalls.simple(self.tasksURI, 'GET', { 'users': 1 }).done(function (data) {
            
            data = Array.isArray(data) ? data : JSON.parse(data);
            data.forEach(element => {
                e = JSON.parse(element);
                self.userList.push({id: parseInt(e[0]), name:  e[1]});
            });

            self.initiateMultiselectUser()
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.addLibrary = function(task) {
        
        if (!self.checkFunction()) {            		
            return;
        }

        var serviceFormatted = JSON.parse(JSON.stringify(self.service)) ;
        serviceFormatted.params = self.serviceParams;
        serviceFormatted.returns = self.serviceReturns; 
        
        var formdata = new FormData();
        if(self.modulepath){
            formdata.append("library", self.modulepath);
        }
        formdata.append('mapper', ko.toJSON(serviceFormatted));//you can append it to formdata with a proper parameter name
        formdata.append('script', self.codeEditor.getSession().getValue());//you can append it to formdata with a proper parameter name
        
        var reqfiles = $("#reqfile").get(0).files;
        if (reqfiles.length > 0)
            formdata.append('reqfile', reqfiles[0]);

        if (self.access() !== undefined)
            formdata.append('publicaccess', self.access());
        
        if (self.selectedSharingUsers().length > 0) {
            formdata.append('sharedusers', ko.toJSON(self.selectedSharingUsers));
        }

        ajaxcalls.form(self.tasksURI, 'POST', formdata).done(function(data) {
                               
            $("#output").val(data.out !== undefined ? data.out : "");
            $("#error").val(data.err !== undefined ? data.err : "");
            $("#log tbody").empty();
            
            if (data.err !== undefined && data.err.length != 0) {
                $("#add-library-info").text(data.err);
                printExecStatus("Tool/Module/Service is not added.");
                activateTab(2);
            }
            else {
                $('#add').modal('hide');
                $("#add-library-info").text("");
                printExecStatus("Module/Service added.");
                activateTab(1);
                if (tasksViewModel !== undefined) {
                    tasksViewModel.load();
                }
            }
        });
    }

    self.getMapperEditor = function() { return self.mapperEditor; }
    self.getCodeEditor = function() { return self.codeEditor; }

    self.addPackage = function(task) {

        if(!self.modulepath){
            $("#add-package-info").text("A tool/module must be selected in zip/tar format.");
            return;
        }

        var formdata = new FormData();
        formdata.append("package", self.modulepath);
        formdata.append('update', $('#inlineCheckbox1').is(":checked") ? 1 : 0);
        
        ajaxcalls.form(self.tasksURI, 'POST', formdata).done(function(data) {
                               
            $("#output").val(data.out !== undefined ? data.out : "");
            $("#error").val(data.err !== undefined ? data.err : "");
            $("#log tbody").empty();
            
            if (data.err !== undefined && data.err.length != 0) {
                $("#add-package-info").text(data.err);
                printExecStatus("No service/module added.");
                activateTab(2);
            }
            else {
                printExecStatus("Service/module added.");
                $('#addPackage').modal('hide');
                $("#add-package-info").text("");
                activateTab(1);
                if (tasksViewModel !== undefined) {
                    tasksViewModel.load();
                }
            }
        });
    }
}
