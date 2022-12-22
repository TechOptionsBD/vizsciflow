function EditTaskViewModel() {
    var self = this;
    self.package = ko.observable();
    self.name = ko.observable();
    self.internal = ko.observable();
    self.example = ko.observable();
    self.example2 = ko.observable();

    self.setTask = function(task) {
        self.task = task;
        self.package(task.package());
        self.name(task.name());
        self.internal(task.internal());
        self.example(task.example());
        self.example2(task.example2());
        $('edit').modal('show');
    }

    self.editTask = function() {
        $('#edit').modal('hide');
        tasksViewModel.edit(self.task, {
            package: self.package(),
            name: self.name(),
            internal: self.internal(),
            example: self.example(),
            example2: self.example2()
        });
    }
}
