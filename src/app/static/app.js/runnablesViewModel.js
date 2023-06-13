function RunnablesViewModel() {
    var self = this;
    self.runnablesURI = '/runnables';
    self.graphsURI = '/graphs';
    self.items = ko.observableArray();
    self.monitorTimer = ko.observable();
    self.shouldTaskCompareActive = ko.observable(false);
    self.historyLoading = false;
    self.clicks = 0;
    self.timer = null;
    self.PageSize = ko.observable(2);
    self.AllData = ko.observableArray();
    self.PagaData = ko.observableArray();

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
                                content = "<div class=\'expanded-history\'> <p>Name: " + content.name + "</p><p>Created: " + content.created_on + "<br>Modified: " + content.modified_on + "<br>Duration: " + parseFloat(content.duration).toFixed(3) +
                                    " s</p><p>Status: " + content.status + (content.err && content.err.length > 0 ? "<br>Error: " + content.err : "") + "</p><p>Double click to show in report.<br>Check to pin job to report.</p></div>";

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
            $("#duration").html(parseFloat(data['duration']).toFixed(3) + ' s');
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

    self.compareTask = function() {
        selectedIds = self.selectedIds()
        if(self.shouldTaskCompareActive()){
            ajaxcalls.simple(self.runnablesURI, 'GET', {'compare': selectedIds[0], 'with': selectedIds[1]}).done(function (res) {
                $('.nav-tabs a[href="#provenancetab"]').tab('show').on('shown.bs.tab', function () {
                    $('#liProvenanceTab').show();
                });
                tasksViewModel.createCompView(res.view)
            }).fail(function (jqXHR) {
                showXHRText(jqXHR);
            });
        }
    }

    self.toggleTaskCompareBtn = function(){
        selectedIds = self.selectedIds()
        if(selectedIds.length === 2){
            self.shouldTaskCompareActive(true)
        }
        else{
            self.shouldTaskCompareActive(false)
        }
        return true
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
            self.AllData = self.items;
            
            // self.Paging() // Update({ PageSize: newPageSize, TotalCount: self.AllData().length, CurrentPage: self.Paging().CurrentPage() });
            self.Paging().TotalCount(self.AllData().length);
            self.RenderAgain();

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
            $("#tblCompareDiv").hide();
            $("#textCompareMainDiv").hide();
            $("#pluginViewDiv").hide();
            $("#proveBarCharts").hide();
            $("#provePieCharts").hide();
            $("#proveHeatMap").hide();
            $("#proveLineCharts").hide();
            $("#provenance").show();
            $("#provDiagramOverview").show();
            
            if(handleModeViewModel.getMode() !== 'provMode')
                handleModeViewModel.setMode('provMode');
            
            $('.nav-tabs a[href="#provenancetab"]').tab('show').on('shown.bs.tab', function () {
                $('#liProvenanceTab').show();
            });
            
            if(self.monitorTimer()){
                self.clearMonitorTimer()
            }

            self.monitorTimer(setInterval(() => {
                item.status() !== 'SUCCESS'
                ?   getGraphData()
                :   stopRefreshGraph()
            }, 1000))

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
                clearInterval(self.monitorTimer())
                self.monitorTimer(false);
            }
            
        }
    }

    self.clearMonitorTimer = function() {
        clearInterval(self.monitorTimer()); 
        self.monitorTimer(false);
    }

    self.Paging = ko.observable(new PagingVM({
        pageSize: self.PageSize(),
        totalCount: self.AllData().length,
    }));

    self.pageSizeSubscription = self.PageSize.subscribe(function (newPageSize) {
        self.Paging().Update({ PageSize: newPageSize, TotalCount: self.AllData().length, CurrentPage: self.Paging().CurrentPage() });
        self.RenderAgain();
    });

    self.currentPageSubscription = self.Paging().CurrentPage.subscribe(function (newCurrentPage) {
        self.RenderAgain();
    })

    self.RenderAgain = function () {
        var result = [];
        var startIndex = (self.Paging().CurrentPage() - 1) * self.Paging().PageSize();
        var endIndex = self.Paging().CurrentPage() * self.Paging().PageSize();

        for (var i = startIndex; i < endIndex; i++) {
            if (i < self.AllData().length)
                result.push(self.AllData()[i])
        }
        self.PagaData(result);
    }

    self.dispose = function () {
        self.currentPageSubscription.dispose();
        self.pageSizeSubscription.dispose();
    }
    self.RenderAgain();
}


function PagingVM(options) {
    var self = this;

    self.PageSize = ko.observable(5);
    self.CurrentPage = ko.observable(1);
    self.TotalCount = ko.observable(options.totalCount);
    self.FirstPage = 1;
    // this should be odd number always
    var maxPageCount = 3;

    self.PageCount = ko.pureComputed(function () {
        return Math.ceil(self.TotalCount() / self.PageSize());
    });

    self.SetCurrentPage = function (page) {
        if (page < self.FirstPage)
            page = self.FirstPage;

        if (page > self.LastPage())
            page = self.LastPage();

        self.CurrentPage(page);
    };

    self.LastPage = ko.pureComputed(function () {
        return self.PageCount();
    });

    self.NextPage = ko.pureComputed(function () {
        var next = self.CurrentPage() + 1;
        if (next > self.LastPage())
            return null;
        return next;
    });

    self.PreviousPage = ko.pureComputed(function () {
        var previous = self.CurrentPage() - 1;
        if (previous < self.FirstPage)
            return null;
        return previous;
    });

    self.NeedPaging = ko.pureComputed(function () {
        return self.PageCount() > 1;
    });

    self.NextPageActive = ko.pureComputed(function () {
        return self.NextPage() != null;
    });

    self.PreviousPageActive = ko.pureComputed(function () {
        return self.PreviousPage() != null;
    });

    self.LastPageActive = ko.pureComputed(function () {
        return (self.LastPage() != self.CurrentPage());
    });

    self.FirstPageActive = ko.pureComputed(function () {
        return (self.FirstPage != self.CurrentPage());
    });

    self.generateAllPages = function () {
        var pages = [];
        for (var i = self.FirstPage; i <= self.LastPage(); i++)
            pages.push(i);

        return pages;
    };

    self.generateMaxPage = function () {
        var current = self.CurrentPage();
        var pageCount = self.PageCount();
        var first = self.FirstPage;

        var upperLimit = current + parseInt((maxPageCount - 1) / 2);
        var downLimit = current - parseInt((maxPageCount - 1) / 2);

        while (upperLimit > pageCount) {
            upperLimit--;
            if (downLimit > first)
                downLimit--;
        }

        while (downLimit < first) {
            downLimit++;
            if (upperLimit < pageCount)
                upperLimit++;
        }

        var pages = [];
        for (var i = downLimit; i <= upperLimit; i++) {
            pages.push(i);
        }
        return pages;
    };

    self.GetPages = ko.pureComputed(function () {

        return ko.observableArray(self.PageCount() <= maxPageCount ? self.generateAllPages() : self.generateMaxPage());
    });

    self.Update = function (e) {
        self.TotalCount(e.TotalCount);
        self.PageSize(e.PageSize);
        self.SetCurrentPage(e.CurrentPage);
    };

    self.GoToPage = function (page) {
        if (page >= self.FirstPage && page <= self.LastPage())
            self.SetCurrentPage(page);
    }

    self.GoToFirst = function () {
        self.SetCurrentPage(self.FirstPage);
    };

    self.GoToPrevious = function () {
        var previous = self.PreviousPage();
        if (previous != null)
            self.SetCurrentPage(previous);
    };

    self.GoToNext = function () {
        var next = self.NextPage();
        if (next != null)
            self.SetCurrentPage(next);
    };

    self.GoToLast = function () {
        self.SetCurrentPage(self.LastPage());
    };
}