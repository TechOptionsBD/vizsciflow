function ActivitiesViewModel() {
    var self = this;
    self.activitiesURI = '/activities';
    self.items = ko.observableArray();
    self.clicks = 0;
    self.timer = null;

    self.copyToEditorDblClick = function (itme, event) {
        event.preventDefault();
    }

    self.loadLog = function (item) {

        ajaxcalls.simple(self.activitiesURI, 'GET', { 'id': item.id() }).done(function (data) {

            if (data === undefined)
                return;

            var text = "Activity:" + "\n" + "Type: " + data.type + "\n" + "Status: " + data.status + "\n" + "Time: " + data.modified_on + "\n" + "Logs:" + "\n";
            $.each(data.logs, function(index, log) {
                text += "time: " + log.time + "   " + " type: " + log.type + "    log: " + log.log + "\n";
            });
            $("#output").val(text);
            activateTab(1);
        }).fail(function (jqXHR, textStatus) {
            $('#refresh').hide();
            showXHRText(jqXHR);
        });
    }

    self.about = function () {
        window.open("static/biodsl-help.html#activities", '_blank');
    }

    self.copyToEditor = function (item) {
        reportId = item.id();
        self.loadHistory(reportId, true);
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
        ajaxcalls.simple(self.activitiesURI, 'GET').done(function (data) {
            if (data == undefined)
                return;

            self.items([]);
            $.each(data, function (i, s) {
                self.items.push({
                    id: ko.observable(s.id),
                    type: ko.observable(s.type),
                    status: ko.observable(s.status),
                    modified: ko.observable(s.modified_on),
                    statusImg: ko.observable(self.statusIcon(s.status)),
                });
            });
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }
}
