function TasksViewModel(sampleViewModel) {
    
    var self = this;
    self.tasksURI = '/functions';
    self.graphsURI = '/graphs';
    self.dataSourcesURI = '/datasources';
    self.username = "";
    self.password = "";
    self.tasks = ko.observableArray();
    self.taskFilter = ko.observable("");
    self.access = ko.observable("0");
    self.isListLog = ko.observable(true);
    self.fileImgPath = '/static/file_icon_blue.png';
    self.folderImgPath = '/static/folder_Icon_blue.png';
    self.sampleViewModel = sampleViewModel;
    this.filteredTasks = ko.computed(function () {
        return this.tasks().filter(function (task) {
            if (!self.taskFilter() || 
                (task.name() !== undefined && task.name().toLowerCase().indexOf(self.taskFilter().toLowerCase()) !== -1) ||
                (task.package() !== undefined && task.package().toLowerCase().indexOf(self.taskFilter().toLowerCase()) !== -1) ||
                (task.group() !== undefined && task.group().toLowerCase().indexOf(self.taskFilter().toLowerCase()) !== -1) ||
                (task.desc() !== undefined && task.desc().toLowerCase().indexOf(self.taskFilter().toLowerCase()) !== -1)
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
    self.pluginHtmlSrc = ko.observable();
    self.currentItemPath = ko.observable();
    self.isListView = ko.observable(true);
    self.shouldRunActivate = ko.observable(true);
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

    self.setItemSrc = function(src) {
        self.itemSrc(src);
        // self.showModal(data, itemSrc);
        $('.nav-tabs a[href="#outputtab"]').tab('show');
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
        clearResults();
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
        addLibraryViewModel.beginAddLibrary();
    }

    //ehtesum------------------------------------------------

    self.beginAddPackage = function()
    {
        addLibraryViewModel.beginAddPackage();
    }

    //ehtesum------------------------------------------------

    self.about = function () {
        window.open("static/biodsl-help.html#services", '_blank');
    }

    self.updateWorkflow = function (save) {
        var script = $.trim(editor.getSession().getValue());
        if (!script && !self.sampleViewModel.workflowId()) // || editor.session.getUndoManager().isClean())
            return; // if script empty and workflowId not set, it means (empty) workflow is not set yet.

        // workflow not saved yet
        if (!self.sampleViewModel.workflowId() && save) {
            // Show save dialog if user explicitely clicked save/saveas button
            return self.sampleViewModel.beginAdd({saveas: true});
            // save with default name and private access.
        }

        var formdata = new FormData();

        formdata.append('workflowId', self.sampleViewModel.workflowId());
        formdata.append('script', script);

        ajaxcalls.form(self.tasksURI, 'POST', formdata, false).done(function (data) {
            if (!$.isEmptyObject(data)) {
                if (data.err !== undefined) {
                    throw Error(data.err);
                }
                else {
                    self.sampleViewModel.workflowId(parseInt(data['workflowId']));
                    self.sampleViewModel.name(data['name']);
                    editor.session.getUndoManager().markClean();
                }
            }
        });
    }

    self.runBioWLInternal = function (task) {
        if (!sampleViewModel.workflowId()) {
            $("#error").val("Workflow is not updated or it is not saved. Change the code and run again.");
            return;
        }

        var script = $.trim(editor.getSession().getValue());
        if (!script)
            return;

        $('#refresh').show();
        var formdata = new FormData();

        formdata.append('workflowId', parseInt(sampleViewModel.workflowId()));
        formdata.append('args', ko.toJSON(self.sampleViewModel.wfArgs));
        formdata.append('immediate', $('#immediate').prop('checked'));
        self.clearResults();

        ajaxcalls.form(self.tasksURI, 'POST', formdata).done(function (data) {
            $('#refresh').hide();

            if (data === undefined)
                return;

            if (data.err) {
                showXHRText(data.err);    
            }
            else {
                reportId = parseInt(data.runnableId);
                runnablesViewModel.load();
                runnablesViewModel.loadHistory(reportId, true);
            }

        }).fail(function (jqXHR, textStatus) {
            $('#refresh').hide();
            showXHRText(jqXHR);
        });
    }

    self.runBioWL = function (task) {
        let currentMode = handleModeViewModel.getMode();

        try {
            self.updateWorkflow();
            switch(currentMode){
                case 'wfMode':
                    self.runBioWLInternal(task);
                    break;
                case 'provMode':
                    self.runProvenanceInternal(task);
                    break;
            }
        }
        catch(e) {
            console.log(e);
            $("#error").val(e);
        }
    }

    self.runGraph = function (task) {
        self.buildGoDetailGraph();
    }

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

    let subGraphNo = 1;
    function mergeJson(json, otherJson){
        otherJson["nodeDataArray"].forEach(otherJsonItem => {
            let isKeyExsit = false;
            if(json["nodeDataArray"].length > 0){
                json["nodeDataArray"].forEach( j => {
                    if(j['key'] == otherJsonItem['key'])
                        isKeyExsit = true;
                })
                if(!isKeyExsit){
                    otherJsonItem["group"] = "Subgraph " + subGraphNo;
                    json["nodeDataArray"].push(otherJsonItem)
                }
            }
            else{
                otherJsonItem["group"] = "Subgraph " + subGraphNo;
                json["nodeDataArray"].push(otherJsonItem)
            }
        });

        otherJson["linkDataArray"].forEach(otherJsonItem => {
            let isKeyExsit = false;
            if(json["linkDataArray"].length > 0){
                json["linkDataArray"].forEach( j => {
                    if(j['from'] == otherJsonItem['from'] && j['to'] == otherJsonItem['to'])
                        isKeyExsit= true;
                })
                if(!isKeyExsit)
                    json["linkDataArray"].push(otherJsonItem)
            }
            else
                json["linkDataArray"].push(otherJsonItem)
        });
        return json
    }

    self.runProvenanceInternal = function (task) {
        if (!self.sampleViewModel.workflowId()) {
            $("#error").val("Workflow is not updated or it is not saved. Change the code and run again.");
            return;
        }

        var script = $.trim(editor.getSession().getValue());
        if (!script)
            return;

        $('#refresh').show();
        var formdata = new FormData();

        formdata.append('workflowId', self.sampleViewModel.workflowId());
        formdata.append('args', ko.toJSON(self.sampleViewModel.wfArgs));
        formdata.append('immediate', 'true');
        formdata.append('provenance', 'true');
        self.clearResults();
        $('.nav-tabs a[href="#provenancetab"]').tab('show');

        ajaxcalls.form(self.tasksURI, 'POST', formdata).done(function (data) {
            if (data === undefined) {
				$('#refresh').hide();
                return;
			}

            reportId = parseInt(data.runnableId);

			ajaxcalls.simple('/runnables', 'GET', { 'id': reportId }).done(function (data) {
                self.createCompView(JSON.parse(data['view']));
			});
			
			$('#refresh').hide();

        }).fail(function (jqXHR, textStatus) {
            $('#refresh').hide();
            showXHRText(jqXHR);
        });
    }

    function createProvGraph (provGraphData) {
        let json = { "nodeDataArray" : [], "linkDataArray":[] }

        if (provGraphData === undefined)
            return;

        //json marger
        subGraphNo = 1;

        if(provGraphData.length == 1){
            json = provGraphData[0]
        }

        else{
            provGraphData.forEach((aGraphData) => {
                groupNode = {key: "Subgraph " + subGraphNo, isGroup: true}
                json["nodeDataArray"].push(groupNode)
                
                json = mergeJson(json, aGraphData)
                subGraphNo++;
            });
        }

        json = JSON.stringify(json)
        if(runnablesViewModel.monitorTimer()){
            runnablesViewModel.clearMonitorTimer()
        }
        provgraphviewmodel.show(JSON.parse(json));         //calling provenance graph
    }

    function provCompTable(data, tableNo = null){
        if(tableNo !== null){
            let comparisonTblId = 'compare:'+tableNo;
            $('#tblCompareDiv').append('<div id="'+comparisonTblId+'" style="height:39em; overflow-y: auto;"></div>');
            var comparisonTblDiv = document.getElementById(comparisonTblId);
            var tbl = document.createElement('table');
            tbl.id = "comparisonTbl"+tableNo;
            tbl.className = 'comparisonTbl';
            comparisonTblDiv.appendChild(tbl);
        }
        else{
            $('#tblCompareDiv').append('<div id="compare" style="height:39em; overflow-y: auto;"></div>');
            $("#compare").append('<table id="comparisonTbl" class="comparisonTbl"></table>');
            var tbl = document.getElementById("comparisonTbl");
        }
        
        data.forEach(row => {
            Object.entries(row).forEach(
                ([key, value]) => {
                    if(key == "Heading"){
                        var tr = tbl.insertRow();
                        
                        var td = tr.insertCell();
                        td.appendChild(document.createTextNode(value['Title']));
                        td.style.fontWeight = 'bold';
                        td.style.textAlign = 'center';
                        td.style.borderTopStyle = 'hidden';
                        td.style.borderLeftStyle = 'hidden';
                        td.style.borderBottomStyle = 'hidden';
                        td.style.width = 'fit-content';
                        td.style.backgroundColor = 'lightGray'
                    

                        var td = tr.insertCell();
                        td.appendChild(document.createTextNode(value['First']));
                        td.style.fontWeight = 'bold';
                        td.style.textAlign = 'center';
                        td.style.backgroundColor = 'lightGray'

                        var td = tr.insertCell();
                        td.appendChild(document.createTextNode(value['Second']));
                        td.style.fontWeight = 'bold';
                        td.style.textAlign = 'center';
                        td.style.backgroundColor = 'lightGray'
                    }
                    else if(key == "Properties"){
                        value.forEach(tableData => {
                            var tr = tbl.insertRow();
                            
                            var td = tr.insertCell();
                            td.appendChild(document.createTextNode(tableData['Name']));
                            td.style.textAlign = 'right';
                            td.style.borderTopStyle = 'hidden';
                            td.style.borderLeftStyle = 'hidden';
                            td.style.borderBottomStyle = 'hidden';
                            td.style.width = 'fit-content';
                            td.style.padding = '0px 5px';
                            
                            var td = tr.insertCell();
                            td.appendChild(document.createTextNode(tableData['First']));
                            td.style.textAlign = 'center';
                            
                            var td = tr.insertCell();
                            td.appendChild(document.createTextNode(tableData['Second']));
                            td.style.textAlign = 'center';
                        })
                    }
            })
        })
    }

    function provCompTxt(data, itemNo = null){
        if(itemNo !== null){
            let textCompareDivId = 'textcompare:'+itemNo;
            $('#textCompareMainDiv').append('<div id="'+textCompareDivId+'" style="height:39em; overflow-y: auto; background: #add8e62e;"></div>');
            var textCompareDiv = document.getElementById(textCompareDivId);
            var paragraph = document.createElement('p');
            paragraph.id = "textComparisonDiv"+itemNo;
            paragraph.textContent = data
            textCompareDiv.appendChild(paragraph);
        }
        else{
            $('#textCompareMainDiv').append('<div id="textcompare" style="height:39em; overflow-y: auto; background: #add8e62e;"></div>');
            $("#textcompare").append('<p id="textComparisonDiv"></p>');
            $('#textComparisonDiv').text(data)
        }
    }
	
    function pluginHtmlViewer(data) {
        var oReq = new XMLHttpRequest();
        oReq.open('GET', self.dataSourcesURI + "?" + 'file_data=' + data.url, true);
        oReq.responseType = "arraybuffer";

        oReq.send();
        // self.itemName(data.url);
        oReq.onload = function (oEvent) {
            if (this.status == 200) {
                var arrayBuffer = oReq.response;
                var blob = new Blob([arrayBuffer], { type: "text/html" });
                var reader = new FileReader();
                reader.readAsDataURL(blob);
                reader.onload = function () {
                    var base64UrlString = reader.result;
                    self.pluginHtmlSrc(base64UrlString);

					if (data.data !== undefined && data.data){
                        var frame = $("#pluginHtmlView")[0]; /*the iframe DOM object*/
                        frame.contentWindow.postMessage({call:'sendValue', value: data.data}, "*"); /*frame domain url or '*'*/
                    }
                }
            }
        };
    }

    function createLineChart() {
        var ctx = document.getElementById('canvasLineChart').getContext('2d');
        var lineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ["Jan", "Feb", "March", "April", "May", "June"],
                datasets: [{
                    label: '# of Data',
                    data: [12, 19, 3, 5, 2, 3],
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        stacked: false
                    }]
                }
            }
        });
    }

    function createPieChart() {
        var ctx = document.getElementById('canvasPieChart').getContext('2d');
        var pieChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                datasets: [{
                    label: '# of Data',
                    data: [12, 19, 3, 5, 2, 3],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            }
        });
    }


	function dynamicColors() {
        var r = Math.floor(Math.random() * 255);
        var g = Math.floor(Math.random() * 255);
        var b = Math.floor(Math.random() * 255);
        return "rgba(" + r + "," + g + "," + b + ", 0.5)";
    }

    function createBarChart(d) {
        var ctx = document.getElementById('canvasBarChart').getContext('2d');
        var barChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: d.labels,
                datasets: [{
                    label: d.datasets.label,
                    data: d.datasets.data,
					backgroundColor: dynamicColors,
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }
    
    function createHeatMapChart() {
        // create data
        var data = [
            { x: "2010", y: "A", heat: 15 },
            { x: "2011", y: "A", heat: 17 },
            { x: "2012", y: "A", heat: 21 },
            { x: "2010", y: "B", heat: 34 },
            { x: "2011", y: "B", heat: 33 },
            { x: "2012", y: "B", heat: 32 },
            { x: "2010", y: "C", heat: 51 },
            { x: "2011", y: "C", heat: 50 },
            { x: "2012", y: "C", heat: 47 }
        ];

        // create a chart and set the data
        chart = anychart.heatMap(data);

        // set the container id
        chart.container("proveHeatMap");

        // initiate drawing the chart
        chart.draw();
    }

    self.createCompView = function (view) {
        if(view == undefined)
            return;

        let provTabDdl = document.getElementsByClassName("provTabCombo");
        $(".provTabCombo").empty();
        
        diagramReload("provenance");				//removing the graph
        diagramReload("provDiagramOverview");		//removing the overview

        for (const val in view) {
            if(val === 'graph' || view[val].length === 1){
                let option = document.createElement("option");
                option.value = val;
                option.autocomplete = "off";
                option.text = val.charAt(0).toUpperCase() + val.slice(1);
                provTabDdl[0].appendChild(option);
            }
            else{
                view[val].forEach((item, index) => {
                    let option = document.createElement("option");
                    option.value = val + ":" + (index+1);
                    option.autocomplete = "off";
                    option.text = val.charAt(0).toUpperCase() + val.slice(1) + ":" + (index+1);
                    provTabDdl[0].appendChild(option);
                })
            }
        }
        provTabDdl[0].options[0].selected = true;

        if(view.graph !== undefined){
            $("#compareDiv").hide();
            $("#compareTxtDiv").hide();
            $("#pluginViewDiv").hide();
            $("#proveBarCharts").hide();
            $("#provePieCharts").hide();
            $("#proveHeatMap").hide();
            $("#proveLineCharts").hide();
            $("#provenance").show();
            $("#provDiagramOverview").show();
            
            createProvGraph(view.graph);
        }

        if(view.compare !== undefined){
            $("#tblCompareDiv").empty();
            
            if(view.compare.length === 1){
                provCompTable(view.compare[0]);
            }
            else{
                view.compare.forEach((item, index) => {
                    provCompTable(item, index+1);
                })
            }
        }

        if(view.textcompare !== undefined){
            $("#textCompareDiv").empty();
            
            if(view.textcompare.length === 1){
                provCompTxt(view.textcompare[0]);
            }
            else{
                view.textcompare.forEach((item, index) => {
                    provCompTxt(item, index+1);
                })
            }
        }

        if (view.plugin !== undefined) {
            if (view.graph === undefined) {
                $("#provenance").hide();
                $("#provDiagramOverview").hide();
                $("#compareDiv").hide();
                $("#compareTxtDiv").hide();
                $("#proveBarCharts").hide();
                $("#provePieCharts").hide();
                $("#proveHeatMap").hide();
                $("#proveLineCharts").hide();
                $("#pluginViewDiv").show();
            }

            pluginHtmlViewer(view.plugin[0].plugin);
        }

        if(view.lineChart !== undefined){
            if (view.graph === undefined) {
                $("#provenance").hide();
                $("#provDiagramOverview").hide();
                $("#compareDiv").hide();
                $("#compareTxtDiv").hide();
                $("#pluginViewDiv").hide();
                $("#proveBarCharts").hide();
                $("#provePieCharts").hide();
                $("#proveHeatMap").hide();
                $("#proveLineCharts").show();
            }

            createLineChart();
        }

        if (view.pieChart !== undefined) {
            if (view.graph === undefined) {
                $("#provenance").hide();
                $("#provDiagramOverview").hide();
                $("#compareDiv").hide();
                $("#compareTxtDiv").hide();
                $("#pluginViewDiv").hide();
                $("#proveBarCharts").hide();
                $("#proveHeatMap").hide();
                $("#proveLineCharts").hide();
                $("#provePieCharts").show();
            }

            createPieChart();
        }

        if (view.cpu !== undefined) {
            if (view.graph === undefined) {
                $("#provenance").hide();
                $("#provDiagramOverview").hide();
                $("#compareDiv").hide();
                $("#compareTxtDiv").hide();
                $("#pluginViewDiv").hide();
                $("#proveHeatMap").hide();
                $("#proveLineCharts").hide();
                $("#provePieCharts").hide();
                $("#proveBarCharts").show();
            }

            createBarChart(view.cpu[0]);
        }

        if (view.heatMap !== undefined) {
            if (view.graph === undefined) {
                $("#provenance").hide();
                $("#provDiagramOverview").hide();
                $("#compareDiv").hide();
                $("#compareTxtDiv").hide();
                $("#pluginViewDiv").hide();
                $("#proveBarCharts").hide();
                $("#proveLineCharts").hide();
                $("#provePieCharts").hide();
                $("#proveHeatMap").show();
            }

            createHeatMapChart();
        }
        toggleProvView(provTabDdl[0].options[0].value)
    }
    
    self.buildGoDetailGraph = function (task) {
        var updateDlg = self.updateWorkflow();
        if (updateDlg) {
            updateDlg.on('hidden.bs.modal', function () { self.buildGraphInternal(task); });
        }
        else
            self.buildDetailGraphInternal(task);
    }
    
    self.buildDetailGraphInternal = function (task) {
        if (!$.trim(editor.getSession().getValue()))
            return;

        var formdata = new FormData();

        formdata.append('workflowId', self.sampleViewModel.workflowId());

        $('.nav-tabs a[href="#provenancetab"]').tab('show').on('shown.bs.tab', function () {
            $('#liProvenanceTab').show();
            ajaxcalls.form(self.graphsURI, 'POST', formdata).done(function (data) {
                data = JSON.parse(data);
                if (data === undefined)
                    return;
                
                // detailgojsGraph.show(data);
                provgraphviewmodel.show(data);

            }).fail(function (jqXHR, textStatus) {
                $('#refresh').hide();
                showXHRText(jqXHR);
            });

            $(this).off('shown.bs.tab')
        });
    }

    // self.provenance = function () {
    //     $.redirect(self.tasksURI, { 'provenance': true }, "POST", "_blank");
    // }

    self.generatePythonCode = function (task) {
        $('#refresh').show();
        var formdata = new FormData();
        formdata.append('code', editor.getSession().getValue());
        formdata.append('args', ko.toJSON(self.sampleViewModel.wfArgs));
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
            $("#duration").text(parseInt(data.duration)/1000 + ' ms');
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
                    sharedWith: ko.observableArray(f.sharedWith? JSON.parse(f.sharedWith): [])                    
                });
            });
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    });

    self.reload = $.debounce(500, function () {
        ajaxcalls.simple(self.tasksURI, 'GET', { 'reload': 1 }).done(function (data) {
            self.load(); // now load the data
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    });
    self.paramToArg = function(param) {
		paramarg = param.name
		if (param.default !== undefined && param.default !== "") {
			var paramvalue = param.default;
            if (paramvalue == null) {
                paramvalue = "None"; 
            }
			paramarg = paramarg + "=" + paramvalue;
		}
		return paramarg;
    }
    self.copyToEditor = function (item) {

        exmpl = '';
        retrns=[],params=[];

            retrnNo = 0, paramNo = 0;

        if(Array.isArray(item.returns())){
            item.returns().forEach(function (retrn){
                retrns.push({
                    id: 'return ' + ++retrnNo,
                    value: retrn.name
                });
            });
        }
        else{
            retrns.push({
                id: 'return ' + ++retrnNo,
                value: item.returns().constructor == Object ? item.returns().name : item.returns()
            });
        }

        if(Array.isArray(item.params())){
            item.params().forEach(function (param){
                params.push({
                    id: 'param ' + ++paramNo,
                    value: self.paramToArg(param)
                });
            });
        }
        else{
            params.push({
                id: 'param ' + ++paramNo,
                value: self.paramToArg(item.params())
            });
        }
        
        retrns.forEach(function (retrn){
            exmpl += retrn.value + ','
        });

        if(retrns.length > 0){
            exmpl = exmpl.substring(0, exmpl.length - 1);
            exmpl += " = " 
        }
        
        if (item.package())
            exmpl += item.package() + '.'
        exmpl += item.name() + '(';
        params.forEach(function (param){
            exmpl += param.value + ','
        });
        if (exmpl.endsWith(','))
            exmpl = exmpl.substring(0, exmpl.length - 1);
        exmpl += ")";

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
                ajaxcalls.simple('/functions', 'GET', { 'service_id': item.serviceID(), 'confirm':'true' }).done(function (data){
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

            index = self.tasks.indexOf(item);
            if (self.tasks()[index].serviceID()== item.serviceID()){
                self.tasks.splice( index, 1 );            //delete this service from obsarevalbe array                                                                
            }  
        }
	
	    var x = $(event.target).attr('id');
	    if (x === "delete") {
	    	ajaxcalls.simple('/functions', 'GET', { 'service_id': item.serviceID() }).done(function (data) {
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
                            +"\r\nView.Graph(module)"; 
            
            handleModeViewModel.setMode('provMode');
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
                self.tasks().forEach(function (candidateSample) {
                    candidateSample.expanded(item === candidateSample);
                    if (item === candidateSample) {

                        var url = "/functions?tooltip&name=" + item.name() + "&package=" + item.package();
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
                                        if(content.returns.length > 0){
                                            exmplDOM = exmplDOM.substring(0, exmplDOM.length - 2);
                                            exmplDOM += " = "
                                        }
                                    }
                                    else{
                                        retrnNo++;
										var retname = content.returns.constructor == Object ? content.returns.name : content.returns;
                                        exmplDOM += "<input onkeyup = \"editParam(this);\" onkeydown = \"return editBoxSize(this);\" class = 'form-control inputBox' type=\'text\' id=\'return " + retrnNo + "\' name=\"Return\" value=\'" + retname + "\'> , ";
                                    }
                                    exmplDOM += content.package + '.' + content.name + '( ';

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
                            self.pushLogData(ele, 2);
                        });
                        break;
                    case 2048: //folderlist
                        element.data.forEach(ele => {
                            self.pushLogData(ele, 1);
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

    self.mimeTypeFromImageType = function(fileType) {
        if (self.imageTypes.includes(fileType)){
            if (fileType == 'svg'){
                return 'svg+xml';
            }
        }
        return fileType
    };

    //TODO: need to modify for output tab list view
    self.openInDetailsView = function (data, ele) {
        var fileType = self.getFileExtension(data.data);
        
        self.currentItemPath('');

        self.currentItemPath(data.data);

        if (data.datatype == 0x01 || data.datatype == 0x800) {
            dataSourceViewModel.selectByPath(data.data);
            $('.nav-tabs a[href="#browsertab"]').tab('show');
        }
        else if (self.imageTypes.includes(fileType)) {
            // self.showModal(data);
            var oReq = new XMLHttpRequest();
            oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.data, true);
            oReq.responseType = "arraybuffer";
            self.itemName(data.name);
            oReq.send();

            oReq.onload = function (oEvent) {
                if (this.status == 200) {
                    var arrayBuffer = oReq.response;
                    var blob = new Blob([arrayBuffer], { type: 'image/' + self.mimeTypeFromImageType(fileType) });
                    itemSrc = URL.createObjectURL(blob);
                    self.itemSrc(itemSrc);
                    // self.showModal(data, itemSrc);
                    $('.nav-tabs a[href="#outputtab"]').tab('show');
                }
            };
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
                    // self.showModal(data, itemSrc);
                    $('.nav-tabs a[href="#outputtab"]').tab('show');
                }
            };
        }
        else if (fileType == 'xml') {
            var oReq = new XMLHttpRequest();
            oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.data, true);
            oReq.responseType = "arraybuffer";

            oReq.send();
            self.itemName(data.data);
            oReq.onload = function (oEvent) {
                if (this.status == 200) {
                    var arrayBuffer = oReq.response;
                    var blob = new Blob([arrayBuffer], { type: "text/plain" });
                    itemSrc = URL.createObjectURL(blob);
                    self.itemSrc(itemSrc);
                    // self.showModal(data, itemSrc);
                    $('.nav-tabs a[href="#outputtab"]').tab('show');
                }
            }
        }
        else {

            $.ajax({
                url: "/datasources?mimetype=" + data.data //api.elements.target.attr('href') // Use href attribute as URL
            })
            .then(function(content) {
                // Set the tooltip content upon successful retrieval
                content = JSON.parse(content);
                if (content.mimetype == 'text/plain'){
                    
                    var oReq = new XMLHttpRequest();
                    oReq.open('GET', self.dataSourcesURI + "?" + 'filecontent=' + data.data, true);
                    oReq.responseType = "arraybuffer";

                    oReq.send();
                    self.itemName(data.data);
                    oReq.onload = function (oEvent) {
                        if (this.status == 200) {
                            var arrayBuffer = oReq.response;
                            var blob = new Blob([arrayBuffer], { type: "text/plain" });
                            itemSrc = URL.createObjectURL(blob);
                            self.itemSrc(itemSrc);
                            // self.showModal(data, itemSrc);
                            $('.nav-tabs a[href="#outputtab"]').tab('show');
                        }
                    }
                }
                else{
                    fetch(self.dataSourcesURI + "?" + 'filecontent=' + data.data)
                    .then(resp => resp.blob())
                    .then(blob => {
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.style.display = 'none';
                        a.href = url;
                        // the filename you want

                        //const getFileName = (fileName) => new URL(fileName).pathname.split("/").pop();
                        const getFileName = (fileName) => fileName.split('/').pop();
                        a.download = decodeURIComponent(getFileName(data.data));
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                    })

                    self.itemSrc('');
                }
                
            }, function(xhr, status, error) {
                // Upon failure... set the tooltip content to error
                //api.set('content.text', status + ': ' + error);
            });

            
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
    self.tasksURI = '/functions';
    self.selectedSharedUsers = ko.observableArray();
    self.selectedTask = ko.observable();
    self.access = ko.observable();
    self.userList = ko.observableArray();
    self.access.subscribe(function(newVal){
        $("#ddlShareService").multiselect(newVal ? 'disable' : 'enable');
    });

    self.saveServiceSharing = function () {  
        self.selectedTask().access= self.access();
        self.selectedTask().sharedWith = ko.toJS(self.selectedSharedUsers);
        ajaxcalls.simple(self.tasksURI, 'GET', {'share_service': ko.toJSON(self.selectedTask)}).done(function (res) {
            

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
        
        ajaxcalls.simple(self.tasksURI, 'GET', { 'users': 1 }).done(function (data) {
            
            data = Array.isArray(data) ? data : JSON.parse(data);
            data.forEach(element => {
                self.userList.push({id: parseInt(element[0]), name:  element[1]});
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
