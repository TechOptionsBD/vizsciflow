function SamplesViewModel(sampleViewModel) {
    var self = this;
    self.samplesURI = '/samples';
    self.tasksURI = '/functions';
    self.graphsURI = '/graphs';
    self.clicks = 0;
    self.timer = null;
    self.items = ko.observableArray();
    self.sampleViewModel = sampleViewModel; // the editor workflow
    self.sampleViewModelToAdd = new SampleViewModel(); // the workflow for save/saveas dialog
    self.access = ko.observable("0");
    self.workflowFilter = ko.observable("");
    self.wfList = ko.observableArray();
    self.selectedWfId1 = ko.observableArray();
    self.selectedWfId2 = ko.observableArray();
    self.wfVersionList = ko.observableArray();
    self.selectedWfVersionId1 = ko.observableArray();
    self.selectedWfVersionId2 = ko.observableArray();
    self.filteredWorkflows = ko.computed(function(){
    return this.items().filter(function(item){
        let filterValue = self.workflowFilter().toLowerCase();
        if(!self.workflowFilter() || item.name().toLowerCase().indexOf(filterValue) !== -1 || item.id().toString().indexOf(filterValue) !== -1 || item.desc().toLowerCase().indexOf(filterValue) !== -1)
            return item;
        }
        );
    },this);
     
   self.about = function() {
       
       window.open("static/biodsl-help.html#workflows", '_blank');
   }

    self.remove = function() {
        
        var item = self.firstSelectedItem();
        if (item == null)
            return;
        
        ajaxcalls.simple(self.samplesURI, 'POST', { 'delete': item.name }).done(function(data) {
            self.load();
        });
    }
    
    self.newwf = function() {
        self.saveCurrentLoadintoEditor({id: 0});
    }
    
    self.beginAdd = function(saveas) {
        var script = $.trim(self.sampleViewModel.sampleEditor.getSession().getValue());
        if (script.length == 0 && self.sampleViewModel.workflowId() == 0) { // script empty and not saved yet
            return false;
        }

        if (saveas === undefined)
            saveas = false;
        saveas = saveas.saveas || self.sampleViewModel.workflowId() <= 0;
        
        self.sampleViewModelToAdd.copy(self.sampleViewModel);
        self.sampleViewModelToAdd.getCodeEditor().setValue(script, 1);
        self.sampleViewModelToAdd.loaddatatypes();

        if (self.sampleViewModelToAdd.workflowId() == 0) {
            self.sampleViewModelToAdd.wfParams.removeAll();
            self.sampleViewModelToAdd.wfReturns.removeAll();
            if (!self.sampleViewModelToAdd.name())
                self.sampleViewModelToAdd.name("No Name");
            if (!self.sampleViewModelToAdd.desc())
                self.sampleViewModelToAdd.desc("No description");
        }
        else {

            ajaxcalls.simple(self.samplesURI, 'GET', {'sample_id': self.sampleViewModelToAdd.workflowId()}).done(function(data) {
            
                if ($.isEmptyObject(data))
                    return;
                
                self.sampleViewModelToAdd.copyFromJson(data);
                if (saveas) {
                    self.sampleViewModelToAdd.workflowId(0);
                }
            });
        }
        self.sampleViewModelToAdd.getUsers();

        $('#addSample').modal('show')
            .on('show.bs.modal', function () {
                // $("#addSampleButton").data("saveas", saveas);
                self.sampleViewModelToAdd.wfParams.valueHasMutated();
                self.sampleViewModelToAdd.wfReturns.valueHasMutated();
            })
            .on('hidden.bs.modal', function () {

            });
    }
    
    self.firstSelectedItem = function() {
        var items = self.items();
        for (var i = 0; i < items.length; i++) {
            if (items[i].selected()){
                return items[i];
            }
        }
        return null;
    }
    
    self.saveNeeded = function() {
        var script = $.trim(self.sampleViewModel.sampleEditor.getSession().getValue());
       if (!script && !self.sampleViewModel.workflowId()) // || self.sampleViewModel.sampleEditor.session.getUndoManager().isClean())
              return false; // if script empty and workflowId not set, it means (empty) workflow is not set yet.
          
       return isDirty;
    }

    self.toggleExpand = function (item, event) {
        event.stopPropagation();
        self.clicks++;
        if (self.clicks !== 1) {
            $(".expandedWorkflow").remove();
            self.loadIntoEditor(item.id);
            self.clicks = 0
            return;
        }
        else {
            self.clicks= 0;
            var domItem = $(event.target);
            if (domItem.next().next('div .expandedWorkflow').length !== 0) {
                $(".expandedWorkflow").remove();
                return;
            } else {
                $(".expandedWorkflow").remove();

                tooltip = "<div class=\"expandedWorkflow\" style=\"margin-top: 40px \"> <p>ID: " + item.id() + "<br>Name: " + item.name() + "<br>Owner: " + item.user() + "<br>Selected: " + item.selected() + "</p>";

                if(item.params().length > 0){
                    tooltip += "<table class=\"table\" style=\"border-bottom: 1px solid; border-right: 1px solid; border-left: 1px solid\">";
                    tooltip += "<thead class=\"thead-dark\" style=\"color: #fff; background-color: #337ab7;\">";
                    tooltip += "<tr>";
                    tooltip += "<th colspan=\"2\" style=\"text-align: center; \" class=\"header\" scope=\"col\">Params</th>";
                    tooltip += "</tr>";
                    tooltip += "<tr>";
                    tooltip += "<th style=\"text-align: center;\" class=\"header\" scope=\"col\">Name</th>";
                    tooltip += "<th style=\"text-align: center;\" class=\"header\" scope=\"col\">Type</th>";
                    tooltip += "</tr>";
                    tooltip += "</thead>";
                    tooltip += "<tbody>";
                    item.params().forEach(function (param){
                        tooltip += "<tr>";
                        tooltip += "<td style=\"text-align: center; border-right: 1px solid\" >" + param.name + "</td>";
                        tooltip += "<td style=\"text-align: center;\" >" + param.type + "</td>";
                        tooltip += "</tr>";
                    });
                    tooltip += "</tbody>";
                    tooltip += "</table>";
                }
                tooltip += "<br />";
                if(item.returns().length > 0){
                    tooltip += "<table class=\"table\" style=\"border-bottom: 1px solid; border-right: 1px solid; border-left: 1px solid\">";
                    tooltip += "<thead class=\"thead-dark\" style=\"color: #fff; background-color: #337ab7;\">";
                    tooltip += "<tr>";
                    tooltip += "<th colspan=\"2\" style=\"text-align: center; \" class=\"header\" scope=\"col\">Returns</th>";
                    tooltip += "</tr>";
                    tooltip += "<tr>";
                    tooltip += "<th style=\"text-align: center;\" class=\"header\" scope=\"col\">Name</th>";
                    tooltip += "<th style=\"text-align: center;\" class=\"header\" scope=\"col\">Type</th>";
                    tooltip += "</tr>";
                    tooltip += "</thead>";
                    tooltip += "<tbody>";
                    item.returns().forEach(function (param){
                        tooltip += "<tr>";
                        tooltip += "<td style=\"text-align: center; border-right: 1px solid\" >" + param.name + "</td>";
                        tooltip += "<td style=\"text-align: center;\" >" + param.type + "</td>";
                        tooltip += "</tr>";
                    });
                    tooltip += "</tbody>";
                    tooltip += "</table>";
                }
                

                tooltip += "<p>Double click item to insert into code editor.</p></div>";

                domItem.parents('.draggable-workflow').append(tooltip);
            }
        }
         
    };
    
    self.loadIntoEditor = function(item) {
        
        if (!item) {
            self.sampleViewModel.clear();
            self.sampleViewModel.sampleEditor.session.setValue("", 1);
            return;
        }
        
         ajaxcalls.simple(self.samplesURI, 'GET', {'sample_id': item}).done(function(data) {
            
            if ($.isEmptyObject(data))
                return;
            
            self.sampleViewModel.copyFromJson(data);
            self.sampleViewModel.sampleEditor.session.setValue(data['script'], 1);
            self.sampleViewModel.sampleEditor.focus();
        }).fail(function(jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.dropNLoadIntoEditor = function(item) {
         ajaxcalls.simple(self.samplesURI, 'GET', {'sample_id': item.id}).done(function(data) {
            if ($.isEmptyObject(data))
                return;
            
            var pos = self.sampleViewModel.sampleEditor.selection.getCursor();
            self.sampleViewModel.sampleEditor.session.insert(pos, data['script'] + "\r\n");
            self.sampleViewModel.sampleEditor.focus();

            self.sampleViewModel.workflowId(item.id());
        }).fail(function(jqXHR) {
            showXHRText(jqXHR);
        });
    }
    
    self.saveCurrentLoadintoEditor = function (item) {
        if (self.saveNeeded()) {
            centerDialog($('#save-needed'));
            $('#save-needed').modal('show')
                .on('click', '#save-needed-yes', function (e) {
                    var updateDlg = tasksViewModel.updateWorkflow(true);
                    if (updateDlg) {
                        updateDlg.on('hidden.bs.modal', function () {
                            self.loadIntoEditor(item.id);
                        }.bind(this));
                    }
                    else
                        self.loadIntoEditor(item.id);

                }).on('click', '#save-needed-no', function (e) {
                    self.loadIntoEditor(item.id);
                });
        }
        else {
            self.loadIntoEditor(item.id);
        }
    }
    
    self.click = function(model){
           self.load();
           return true;
    }
    
    self.load = function() {
        ajaxcalls.simple(self.samplesURI, 'GET', {'access': self.access()}).done(function(data) {
            self.items([]);
            $.each(data.samples, function(i, s){
                self.items.push({
                    id: ko.observable(s.id),
                    user:ko.observable(s.user),
                    name: ko.observable(s.name),
                    selected: ko.observable(false),
                    access: ko.observable(s.access),
                    isOwner: ko.observable(s.is_owner),
                    desc: ko.observable(s.desc),
                    params: ko.observable(s.params),
                    returns: ko.observable(s.returns),
                });
            });
            
        }).fail(function(jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.compareWf = function() {
        self.getAllSavedWf();
        $('#versionCompare').hide();
        
        // self.selectedWfId1([])
        // self.selectedWfId2([])

        $('#wfCompareSelection').modal('show');
    }
    
    self.getAllSavedWf = function () {
        self.wfList([]);
        ajaxcalls.simple(self.samplesURI, 'GET', {'access': 3}).done(function (data) {
            data.samples.forEach(wf => {
                self.wfList.push({
                    id: wf.id,
                    name: wf.name
                }); 
            });
            self.initiateWfSelectionDdl();

        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    };
    
    self.initiateWfSelectionDdl = function () {
        $("#compareWf1").multiselect({
            includeSelectAllOption: true,
            inheritClass: true,
            buttonWidth: '100%',
            enableFiltering: true,
            maxHeight: 200
        });

        $("#compareWf2").multiselect({
            includeSelectAllOption: true,
            inheritClass: true,
            buttonWidth: '100%',
            enableFiltering: true,
            maxHeight: 200
        });
    };

    self.wfSelectionChange = function (obj, event) {
        if (self.selectedWfId1() !== undefined && self.selectedWfId1()[0] == self.selectedWfId2()[0]) {
            //display versions selection ddl
            self.getAllVersion(self.selectedWfId1()[0]);

            // self.selectedWfVersionId1([])
            // self.selectedWfVersionId2([])
            
            $('#versionCompare').show();
        }
        else{
            $('#versionCompare').hide();
        }
    }

    self.wfVersionSelectionChange = function () {
        if (self.selectedWfVersionId1()[0] == self.selectedWfVersionId2()[0]) {
            $('#wfVersionSelectionAlert').show();
            $('#wfVersionSelectionAlert').text('Please select two different versions!');
        }
        else {
            $('#wfVersionSelectionAlert').hide();
            $('#wfVersionSelectionAlert').text('');
        }
    }

    self.compareSelectedWf = function () {
        let selectedWfId1 = ko.toJS(self.selectedWfId1()[0]);
        let selectedWfId2 = ko.toJS(self.selectedWfId2()[0]);
        
        if(selectedWfId1 !== selectedWfId2){
            //compare two workflow
            ajaxcalls.simple(self.samplesURI, 'GET', {'compare': selectedWfId1, 'with': selectedWfId2}).done(function (res) {
                $('#wfCompareSelection').modal('hide');
                $('.nav-tabs a[href="#provenancetab"]').tab('show').on('shown.bs.tab', function () {
                    $('#liProvenanceTab').show();
                });
                tasksViewModel.createCompView(res.view) 
            }).fail(function (jqXHR) {
                showXHRText(jqXHR);
            });
        }
        else{
            //compare two versions of selected workflow
            let selectedWfVersionId1 = ko.toJS(self.selectedWfVersionId1()[0]);
            let selectedWfVersionId2 = ko.toJS(self.selectedWfVersionId2()[0]);
            
            if(selectedWfVersionId1 !== selectedWfVersionId2){
                ajaxcalls.simple(self.samplesURI, 'GET', {'revcompare': true,'revision1': selectedWfVersionId1, 'revision2': selectedWfVersionId2}).done(function (res) {
                    $('#wfCompareSelection').modal('hide');
                    $('.nav-tabs a[href="#provenancetab"]').tab('show').on('shown.bs.tab', function () {
                        $('#liProvenanceTab').show();
                    });
                    tasksViewModel.createCompView(res) 
                }).fail(function (jqXHR) {
                    showXHRText(jqXHR);
                });
            }
        }
    }

    self.getAllVersion = function (workflowId) {
        self.wfVersionList([]);
        ajaxcalls.simple(self.samplesURI, 'GET', {'revisions': workflowId}, false).done(function (data) {
            //get the version list here & make dropdown from it
            data.forEach(wfVersion => {
                self.wfVersionList.push({
                    hex: wfVersion.hex,
                    name: wfVersion.summary,
					committer: wfVersion.committer,
					time: wfVersion.time
                }); 
            });
            
            self.initiateWfVersionSelectionDdl();
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    };

    self.initiateWfVersionSelectionDdl = function () {
        $("#compareWfVersion1").multiselect({
            includeSelectAllOption: true,
            inheritClass: true,
            buttonWidth: '100%',
            enableFiltering: true,
            maxHeight: 200
        });

        $("#compareWfVersion2").multiselect({
            includeSelectAllOption: true,
            inheritClass: true,
            buttonWidth: '100%',
            enableFiltering: true,
            maxHeight: 200
        });
    };

    function diagramReload(diagramName){
        var diagramDiv = document.getElementById(diagramName);
        if (diagramDiv !== null) {
            var olddiag = go.Diagram.fromDiv(diagramDiv);
            if (olddiag !== null){
                olddiag.div = null;
                diagramDiv = null;
            }
        }
    }

    function getGraphData(formdata){
        ajaxcalls.form(self.graphsURI, 'POST' , formdata).done(function (graphData) {
            if (graphData === undefined || graphData === null)
                return;
                
            provgraphviewmodel.show(JSON.parse(graphData))
        }).fail(function (jqXHR, textStatus) {
            showXHRText(jqXHR);
        });
    }
        
    function areYouSure(confirmation, item){
        if(confirmation == true){
            ajaxcalls.simple(self.samplesURI, 'GET', { 'workflow_id': item.id(), 'confirm':'true' }).done(function (data){               	          
                if (data === undefined)
                        return;
                
                if (data.return == 'deleted'){
                    workflowDeleted(item);
                }
                else if (data.return == 'error')
                    alert("ERROR");
                
            }).fail(function (jqXHR) {
                alert("Status: "+jqXHR.status);
            });  
        }
        else
            return;
    }

    function workflowDeleted(item){
        alert("WORKFLOW DELETED!");
        
        //delete this service from obsarevalbe array                                                                
        index = self.items.indexOf(item);
        if (self.items()[index].id()== item.id()){
            self.items.splice( index, 1 );
        } 
    }

    //workflow delete button
    self.workflowToolbar = function (item, event) {
	    event.stopPropagation();
	    
	    var x = $(event.target).attr('id');
	    if (x === "delete") {
	    	ajaxcalls.simple(self.samplesURI, 'GET', { 'workflow_id': item.id() }).done(function (data) {            
                // console.log(data);    
        		if (data === undefined)
                        return;        

                data = data.return;
                
                if(data == 'shared'){
                    confirmation = confirm("This is a shared workflow. You still want to delete "+item.name()+" workflow?");
                    areYouSure(confirmation, item);
                }
                else if (data == 'not_shared'){
                    confirmation = confirm("Do you want to delete "+item.name()+" workflow?");
                	areYouSure(confirmation, item);
                }       			
        		else if (data == 'error')
        			alert("ERROR");
                }).fail(function (jqXHR) {
                        alert("Status: "+jqXHR.status);
                }); 
        }
        
        else if (x === "copyProv") {
            handleModeViewModel.setMode('provMode');
            var content = "workflow = Workflow.Get(id="+ item.id() +")"
                            +"\r\nprint(View.Graph(workflow))"; 
            
            var pos = self.sampleViewModel.sampleEditor.selection.getCursor();
            self.sampleViewModel.sampleEditor.session.insert(pos, content + "\r\n");
            self.sampleViewModel.sampleEditor.focus();
        }

        else if( x === 'showGraph'){
            var formdata = new FormData();
            formdata.append('workflow', parseInt(item.id()));

            diagramReload("provenance");				    //reload the graph
            diagramReload("provDiagramOverview");	        //reload the overview

            //hide all div except graph
            $(".provTabCombo").empty();
            $("#tblCompareDiv").hide();
            $("#textCompareMainDiv").hide();
            $("#pluginViewDiv").hide();
            $("#proveBarCharts").hide();
            $("#provePieCharts").hide();
            $("#proveHeatMap").hide();
            $("#proveLineCharts").hide();
            $("#provenance").show();
            $("#provDiagramOverview").show();
            
            if ($('.nav-tabs a[href="#provenancetab"]').is(':visible')){
                getGraphData(formdata)
            }

            else{
                $('.nav-tabs a[href="#provenancetab"]').tab('show').on('shown.bs.tab', function () {
                    $('#liProvenanceTab').show();
                    getGraphData(formdata)                    
                    $(this).off('shown.bs.tab')
                });
            }
        }
    }
}
