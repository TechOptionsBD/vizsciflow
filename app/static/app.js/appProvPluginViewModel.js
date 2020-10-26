function AddProvPluginViewModel(userName) {
    var self = this;
    self.tasksURI = '/provenance';
    self.name = ko.observable(userName);
    self.org = ko.observable();
    self.access = ko.observable();
    self.pippkgs = ko.observable();
    self.userList = ko.observableArray();
    self.selectedSharingUsers = ko.observableArray();
     
    self.htmlEditor = CreateAceEditor("#provenancehtml", "ace/mode/html", 430, true);
    self.provCodeEditor = CreateAceEditor("#provenancescript", "ace/mode/python", 350);

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

    self.provenance = ko.observableDictionary(
        {   
            package: '',
            name: 'MyService',
            internal: '',   
            org: '',
            group: '',
            desc: '',
            href: '',
            example: 'data = MyService(data)'
        }
    );

    // self.serviceParams = ko.observableArray();

    // self.serviceReturns = ko.observableArray();

    // self.addParam = function () {  
    //     self.serviceParams.push(
    //         ko.observableDictionary(
    //             {
    //                 name: '',
    //                 type: '',
    //                 desc: ''
    //             }
    //         )
    //     );
    //     self.liveJsonView();
    // };

    // self.addServiceReturns = function () {
    //     self.serviceReturns.push(
    //         ko.observableDictionary(
    //             {
    //                 name: '',
    //                 type: ''
    //             }
    //         )
    //     );
    //     self.liveJsonView();
    // }

    // self.removeParam = function (data, e) {  
    //     self.serviceParams.remove(data);
    //     self.liveJsonView();
    // };

    // self.removeServiceReturns = function(data, e){
    //     self.serviceReturns.remove(data);
    //     self.liveJsonView();
    // }

    // self.liveJsonView = function () {  
    //     var jsonPreview = Object.entries(JSON.parse(JSON.stringify(self.provenance))).reduce(( obj ,[key,value])=>{
    //         if(value.length) 
    //             obj[key] = value;
    //         return obj;
    //     }, {});
        
    //     if(self.serviceParams().length){
    //         jsonPreview.params = self.serviceParams;
    //     }

    //     if (self.serviceReturns().length) {
    //         jsonPreview.returns = self.serviceReturns;
    //     }

    //     var jsonPrettyText = ko.toJSON(jsonPreview, null, 4);
    //     self.htmlEditor.session.setValue(jsonPrettyText);
    // };
    
	self.addPlugin = function(task) {
        
        /*if (!self.checkFunction()) {            		
            return;
        }
        
        $("#add-library-info").text("");
        $('#add').modal('hide');*/

        var files = $("#module").get(0).files;
        var formdata = new FormData();
        formdata.append('library', files[0]); //use get('files')[0]
        formdata.append('html', self.htmlEditor.getSession().getValue());
        formdata.append('script', self.provCodeEditor.getSession().getValue());
        
/*        if (self.access() !== undefined)
            formdata.append('publicaccess', self.access());*/
        if (self.pippkgs() !== undefined)
            formdata.append('pippkgs', self.pippkgs());
/*        if (self.selectedSharingUsers().length > 0) {
            formdata.append('sharedusers', ko.toJSON(self.selectedSharingUsers));
        }
*/
        ajaxcalls.form(self.tasksURI, 'POST', formdata).done(function(data) {
            
			data = JSON.parse(data);                   
            $("#output").val(data.out !== undefined ? data.out : "");
            $("#error").val(data.err !== undefined ? data.err : "");
            $("#log tbody").empty();
            
			if (data.err !== undefined && data.err.length != 0) {
				msg = data.err.join(";");
				
                $("#add-prov-library-info").text(msg);
                activateTab(1);
				return;
			}
			else {
	            if (provpluginsViewModel !== undefined) {
	                provpluginsViewModel.load();
	            }
	
	 			$('#add').modal('hide');
			}
        });
    }

    self.checkFunction = function() {
        
        var serviceName = (self.service.get('name') ? self.service.get('name') : self.service.get('internal'));
        if (!serviceName) {
            $("#add-prov-library-info").text("No valid service name is given.");
            return false;
        }
        
        var package = (self.service.get('package') ? self.service.get('package') : "");
        var serviceFormatted = JSON.parse(JSON.stringify(self.service)) ;
        serviceFormatted.params = self.serviceParams;
        serviceFormatted.returns = self.serviceReturns;

        var success = false;
        ajaxcalls.simple(self.tasksURI, 'GET', { 'check_function': '', 'package':  package, 'name': serviceName, 'script': self.provCodeEditor.getSession().getValue(), 'mapper': ko.toJSON(serviceFormatted)}, false).done(function(data) {
            
            if (data === undefined) {
                $("#add-prov-library-info").text("Can't retrieve service information. Check your internet connection.");
                return;
            }
            
            success = data['error'] === undefined;
            if (!success) {
                $("#add-prov-library-info").text(data['error']);
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

    // self.getUsers = function () { 
    //     self.userList([]);
    //     self.selectedSharingUsers([]); 
    //     ajaxcalls.simple(self.tasksURI, 'GET', { 'users': 1 }).done(function (data) {
            
    //         JSON.parse(data).forEach(element => {
    //             self.userList.push({id: element[0], name:  element[1]});
    //         });

    //         self.initiateMultiselectUser()
    //     }).fail(function (jqXHR) {
    //         showXHRText(jqXHR);
    //     });
    // }

    self.getHtmlEditor = function() { return self.htmlEditor; }
    self.getCodeEditor = function() { return self.provCodeEditor; }
}








// self.checkFunction = function() {
//     var formdata = new FormData();
    
//     var json = self.mapperEditor.getSession().getValue();
//     if (!isJson(json)) {
//         $("#add-library-info").text("Not a valid JSON mapper.");
//         return false;
//     }
    
//     var mapper = JSON.parse(json);
//     if (!mapper) {
//         $("#add-library-info").text("No valid service is defined for mapping in JSON.");
//         return false;
//     }
     
//     if (mapper.functions) {
        
//         if (mapper.functions.length)
//             mapper = mapper.functions[0];
//         else {
//             $("#add-library-info").text("No valid service is defined for mapping in JSON.");
//             return false;
//         }
//     }
    
//     var func = (mapper.name && mapper.name.length ? mapper.name : mapper.internal);
//     if (!func || !func.length) {
//         $("#add-library-info").text("No valid service name is given.");
//         return false;
//     }
    
//     var package = (self.name() && self.name().length ? self.name() : "");
    
//     var success = false;
//     ajaxcalls.simple(self.tasksURI, 'GET', { 'check_function': '', 'package':  package, 'name': func, 'script': self.codeEditor.getSession().getValue(), 'mapper': self.mapperEditor.getSession().getValue()}, false).done(function(data) {
        
//         if (data === undefined) {
//             $("#add-library-info").text("Can't retrieve service information. Check your internet connection.");
//             return;
//         }
        
//         success = data['error'] === undefined;
//         if (!success) {
//             $("#add-library-info").text(data['error']);
//         }
//     });
    
//     return success;
// }