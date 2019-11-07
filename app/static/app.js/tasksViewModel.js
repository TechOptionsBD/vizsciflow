function TasksViewModel() {
    
    var self = this;
    self.tasksURI = '/functions';
    self.graphsURI = '/graphs';
    self.username = "";
    self.password = "";
    self.tasks = ko.observableArray();
    self.taskFilter = ko.observable("");
    self.access = ko.observable("0");
    this.filteredTasks = ko.computed(function () {
        return this.tasks().filter(function (task) {
            if (!self.taskFilter() || task.name().toLowerCase().indexOf(self.taskFilter().toLowerCase()) !== -1
                || task.package_name().toLowerCase().indexOf(self.taskFilter().toLowerCase()) !== -1
                || task.group().toLowerCase().indexOf(self.taskFilter().toLowerCase()) !== -1)
                return task;
        });
    }, this);

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
        self.tasks()[i].package_name(newTask.package_name);
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

    self.buildGraph = function (task) {
        var updateDlg = self.updateWorkflow();
        if (updateDlg) {
            updateDlg.on('hidden.bs.modal', function () { self.buildGraphInternal(task); });
        }
        else
            self.buildGraphInternal(task);
    }
    self.buildGraphInternal = function (task) {
        if (!$.trim(editor.getSession().getValue()))
            return;

        var formdata = new FormData();

        formdata.append('workflowId', parseInt(workflowId));
        ajaxcalls.form(self.graphsURI, 'POST', formdata).done(function (data) {

            if (data === undefined)
                return;
            data = JSON.parse(data);
            if ($.isEmptyObject(data))
                return;

            d3graph.show(data);

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

            data = JSON.parse(data)

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
                    package_name: ko.observable(f.package_name),
                    name: ko.observable(f.name),
                    //internal: ko.observable(f.internal),
                    example: ko.observable(f.example),
                    example2: ko.observable(f.example2),
                    desc: ko.observable(f.desc),
                    //runmode: ko.observable(f.runmode),
                    group: ko.observable(f.group),
                    href: ko.observable(f.href),
                    expanded: ko.observable(false),
                    access: ko.observable(self.access())
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

    self.copyToEditor = function (item) {
        var pos = editor.selection.getCursor();
        editor.session.insert(pos, self.selectedCategory().Id == 0 ? item.example() + "\r\n" : item.example2() + "\r\n");
        editor.focus();
    }

    self.clicks = 0;
    self.timer = null;

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

                        var url = "/functions?tooltip&name=" + item.name() + "&package=" + item.package_name();
                        $.ajax({
                            url: url
                        })
                            .then(function (content) {
                                // Set the tooltip content upon successful retrieval
                                if (content) {
                                    content = JSON.parse(content);

                                    tooltip = "<div class=\'expandedtask\'> <p>Name: " + content.name + (content.package_name && content.package_name.length ? "<br>Package: " + content.package_name : "") + "<br>Access: " + content.access + "</p>"
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
    }
};
