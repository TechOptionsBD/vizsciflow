function RunnablesViewModel() {
    var self = this;
    self.runnablesURI = '/runnables';
    self.graphsURI = '/graphs';
    self.items = ko.observableArray();
    self.historyLoading = false;
    self.clicks = 0;
    self.timer = null;
    let monitorTimer = false;

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
            $(".expanded-history").remove();
            if (item.expanded()) {
                item.expanded(false);
            } else {
                self.items().forEach(function (candidateSample) {
                    candidateSample.expanded(item === candidateSample);
                    if (item === candidateSample) {

                        $.ajax({
                            url: "/runnables?tooltip=" + item.id()
                        })
                            .then(function (content) {
                                // Set the tooltip content upon successful retrieval
                                content = JSON.parse(content);
                                content = "<div class=\'expanded-history\'> <p>Name: " + content.name + "</p><p>Created: " + content.created_on + "<br>Modified: " + content.modified_on + "<br>Duration: " + content.duration +
                                    "(s)</p><p>Status: " + content.status + (content.err && content.err.length > 0 ? "<br>Error: " + content.err : "") + "</p><p>Double click to show in report.<br>Check to pin job to report.</p></div>";

                                domItem.parents('.div-history-item').append(content);

                            }, function (xhr, status, error) {
                                // Upon failure... set the tooltip content to error
                            });
                    }
                });
            }
        }, 300);
    }

    self.loadHistory = function (id, switchTab = false) {

        ajaxcalls.simple(self.runnablesURI, 'GET', { 'status': id }).done(function (data) {

            if (data === undefined)
                return;

            if (switchTab) {
                if (data['err'] && data['status'] !== 'SUCCESS') {
                    activateTab(2);
                }
                else {

                    if (!$.isEmptyObject(data['log']))
                        activateTab(3);
                    else
                        activateTab(1);
                }
            }

            $("#output").val(data['out']);
            $("#error").val(data['err']);
            $("#log tbody").empty();
            jsonArray2Table($("#log"), data['log']);
            $("#duration").html(data['duration'] + 's');
            printExecStatus(data['status']);
            tasksViewModel.loadLogData(data.log);
        }).fail(function (jqXHR, textStatus) {
            $('#refresh').hide();
            showXHRText(jqXHR);
        });
    }

    self.about = function () {
        window.open("static/biodsl-help.html#jobs", '_blank');
    }

    self.copyToEditor = function (item) {
        reportId = item.id();
        self.loadHistory(reportId, true);
    }

    self.selectedIds = function () {
        var ids = [];
        var items = self.items();
        for (var i = 0; i < items.length; i++) {
            if (items[i].selected()) {
                ids.push(items[i].id());
            }
        }
        return ids;
    }

    self.stop = function () {

        ids = self.selectedIds();
        if (ids.length == 0)
            return;

        ajaxcalls.simple(self.runnablesURI, 'GET', { 'stop': ids.join() }).done(function (data) {

        });
    }

    self.restart = function () {

        ids = self.selectedIds();
        if (ids.length == 0)
            return;

        ajaxcalls.simple(self.runnablesURI, 'GET', { 'restart': ids.join() }).done(function (data) {

        });
    }

    self.changeSelection = function (state) {
        $.each(self.items(), function (index, item) {
            item.selected(state);
        });
    }

    self.selectAll = function () {
        self.changeSelection(true);
    }

    self.deselectAll = function () {
        self.changeSelection(false);
    }

    self.statusIcon = function (status) {
        if (status == "STARTED" || status == "PENDING" || status == "RECEIVED")
            return "/static/spinner.gif";
        else if (status == "FAILURE")
            return "/static/cancel.gif";
        else
            return "/static/completed.gif";
    }

    self.load = function () {
        if (self.historyLoading)
            return;

        self.historyLoading = true;
        ajaxcalls.simple(self.runnablesURI, 'GET').done(function (data) {
            if (data == undefined)
                return;

            var selectedIds = self.selectedIds();
            self.items([]);
            $.each(data['runnables'], function (i, s) {
                self.items.push({
                    id: ko.observable(s.id),
                    name: ko.observable(s.name),
                    modified: ko.observable(s.modified),
                    status: ko.observable(s.status),
                    recent: ko.observable(s.recent !== undefined),
                    statusImg: ko.observable(self.statusIcon(s.status)),
                    selected: ko.observable($.inArray(s.id, selectedIds) !== -1),
                    expanded: ko.observable(false)
                });
            });
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        }).always(function (x, textStatus, jqXHR) {
            self.historyLoading = false;
        });
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

    //job history floating toolbar
    self.runnableToolbar = function (item, event) {
	    event.stopPropagation();
        var x = $(event.target).attr('id');

        //runnableID insert button
	    if (x === "insert2Editor") {
            handleModeViewModel.setMode('provMode');

            var content = "run = Run.Get(id = "+ item.id() +")"
                          +"\r\nView.Graph(run)"; 
            
            var pos = editor.selection.getCursor();
            editor.session.insert(pos, content + "\r\n");
            editor.focus();            
        }

        //graph monitor
        else if (x === "monitorGraph") {
            event.stopPropagation();
            var formdata = new FormData();
            formdata.append('monitor', parseInt(item.id()));
            // $('#monitorModal').modal('show');
            // $(".modal-body #taskName").text( 'Name: ' + item.name() );
            // $(".modal-body #taskID").text( 'ID: ' + item.id() );
            // $(".modal-body #taskStatus").text( 'Status: ' + item.status() );
            
            // $('#monitorModal').on('show.bs.modal', function (e) {
            //     console.log(e);
            //     monitorGraphViewModel.show(JSON.parse(data))
            //     monitorGraphViewModel.requestUpdate();
            // })
            
            // $('#monitorModal').on('hidden.bs.modal', function (e) {
            //     diagramReload("monitorGraph");				    //reload the graph
            //     diagramReload("monitorDiagramOverview");	        //reload the overview
            // })

            diagramReload("provenance");				    //reload the graph
            diagramReload("provDiagramOverview");	        //reload the overview

            //hide all div except graph
            $(".provTabCombo").empty();
            $("#compareDiv").hide();
            $("#compareTxtDiv").hide();
            $("#pluginViewDiv").hide();
            $("#provenance").show();
            $("#provDiagramOverview").show();

            if(handleModeViewModel.getMode() !== 'provMode')
                handleModeViewModel.setMode('provMode');
            
            $('.nav-tabs a[href="#provenancetab"]').tab('show').on('shown.bs.tab', function () {
                $('#liProvenanceTab').show();
            });
            
            if(monitorTimer){
                clearInterval(monitorTimer); 
                monitorTimer = false;
            }

            monitorTimer = setInterval(() => {
                item.status() !== 'SUCCESS'
                ?   getGraphData()
                :   stopRefreshGraph()
            }, 1000);

            function getGraphData () {
                ajaxcalls.form(self.graphsURI, 'POST' , formdata).done(function (newData) {
                    if (newData === undefined){
                        diagramReload("provenance");				   
                        diagramReload("provDiagramOverview");	        
                        return;
                    }
                    provgraphviewmodel.show(JSON.parse(newData))

                }).fail(function (jqXHR, textStatus) {
                    showXHRText(jqXHR);
                });
            }

            function stopRefreshGraph(){
                getGraphData();
                clearInterval(monitorTimer)
                monitorTimer = false;
            }
            
        }
    }
}