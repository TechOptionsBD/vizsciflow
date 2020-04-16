function RunnablesViewModel() {
    var self = this;
    self.runnablesURI = '/runnables';
    self.items = ko.observableArray();
    self.historyLoading = false;
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

        ajaxcalls.simple(self.runnablesURI, 'GET', { 'id': id }).done(function (data) {

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
}