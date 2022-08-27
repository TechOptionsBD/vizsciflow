function AddLibraryViewModel(userName) {
    var self = this;
    self.tasksURI = '/functions';
    self.name = ko.observable(userName);
    self.org = ko.observable();
    self.access = ko.observable();
    self.pippkgs = ko.observable();
    self.userList = ko.observableArray();
    self.selectedSharingUsers = ko.observableArray();
     
    self.mapperEditor = CreateAceEditor("#mapper", "ace/mode/json", 430, true);
    self.codeEditor = CreateAceEditor("#servicescript", "ace/mode/python", 350);

    self.isFuncExpanded = ko.observable(false);
    self.textToggleFuncArea = ko.observable('More..');

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
            // example: 'data = MyService(data)'
        }
    );

    self.editService = (refData) => {
        refData.internal && self.service.set('internal',refData.internal)
        refData.name && self.service.set('name',refData.name)
        refData.package && self.service.set('package',refData.package)
        refData.org && self.service.set('org',refData.org)
        refData.group && self.service.set('group',refData.group)

        refData.params.map(param => {
            self.addParam(param)
        })

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
                    type: returns.type !== undefined ? returns.type : ''
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
                self.userList.push({id: parseInt(element[0]), name:  element[1]});
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

        $("#add-library-info").text("");
        $('#add').modal('hide');

        var serviceFormatted = JSON.parse(JSON.stringify(self.service)) ;
        serviceFormatted.params = self.serviceParams;
        serviceFormatted.returns = self.serviceReturns; 
        
        var files = $("#module").get(0).files;
        var formdata = new FormData();
        formdata.append('library', files[0]); //use get('files')[0]
        formdata.append('mapper', ko.toJSON(serviceFormatted));//you can append it to formdata with a proper parameter name
        formdata.append('script', self.codeEditor.getSession().getValue());//you can append it to formdata with a proper parameter name
        
        if (self.access() !== undefined)
            formdata.append('publicaccess', self.access());
        if (self.pippkgs() !== undefined)
            formdata.append('pippkgs', self.pippkgs());
        if (self.selectedSharingUsers().length > 0) {
            formdata.append('sharedusers', ko.toJSON(self.selectedSharingUsers));
        }

        ajaxcalls.form(self.tasksURI, 'POST', formdata).done(function(data) {
                               
            $("#output").val(data.out !== undefined ? data.out : "");
            $("#error").val(data.err !== undefined ? data.err : "");
            $("#log tbody").empty();
            
            if (tasksViewModel !== undefined) {
                tasksViewModel.load();
            }
            
            if (data.err !== undefined && data.err.length != 0) {
                printExecStatus("Service cannot be added.");
                activateTab(2);
            }
            else {
                activateTab(1);
            }
        });
    }
    
    self.getMapperEditor = function() { return self.mapperEditor; }
    self.getCodeEditor = function() { return self.codeEditor; }
}