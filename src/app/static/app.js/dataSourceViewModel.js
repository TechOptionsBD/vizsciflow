function DataSourceViewModel() {
    var self = this;
    self.init = false;
    self.dataSourcesURI = '/datasources';
    self.dataSources = ko.observableArray();
    self.expandedNodes = [];
    self.searchDataSource = ko.observable();
    self.waittime = 5000; // for throttle
    self.tree = $('#tree');

    self.visualizers = ko.observableArray();
    self.mimetypes = ko.observableArray(["xx-pp", "yy-qq"]);

    self.findExpandibleNodes = function (text) {
        var options = {
            ignoreCase: true,
            exactMatch: false,
            revealResults: true,
        };
        return $('#tree').treeview('search', [text, options]);
    };

    self.searchDataSource.subscribe(function () {
        self.tree.jstree('search', self.searchDataSource());
    });

    self.beginFileUpload = function () {
        centerDialog($('#file-upload-dialog'));
        self.loadMetadataProperties();
        ko.cleanNode($("#file-upload-dialog")[0]);
        ko.applyBindings(dataSourceViewModel, $("#file-upload-dialog")[0]);
        $('#file-upload-dialog').modal('show');
    }

    self.beginUpdateMetadata = function () {
        //centerDialog($('#update-metadata-dialog'));
        var node = dataSourceViewModel.selectedNode().original;
        // var node = dataSourceViewModel.selectedNode();
        if (node === undefined)
            return;

        metadataViewModel.load(node.path);
        $('#update-metadata-dialog').modal('show');
    }

    self.loadMetadataProperties = function () {

        ajaxcalls.simple(metadataViewModel.metadataURI, 'GET', { 'properties': true }).done(function (data) {

            self.visualizers = ko.observableArray();
            $.each(data['visualizers'], function (key, value) {
                self.visualizers.push(ko.observable(key + ": " + value))
            });

            self.mimetypes = ko.observableArray();
            $.each(data['mimetypes'], function (key, value) {
                self.mimetypes.push(ko.observable(key + ": " + value))
            });

        }).fail(function (jqXHR, a, b) {
            showXHRText(jqXHR);
        });
    }

    self.loadFromJSON = function (datasources) {
        self.dataSources(datasources);

        ko.cleanNode($("#dataSourcesPanel")[0]);
        ko.applyBindings(self, $("#dataSourcesPanel")[0]);
    }

    self.load = function (recursive) {
        /*if (self.init) {
            node = self.selectedNode();
            if (node !== undefined) {
                self.loadItem(node, recursive)
                return;
            }
        }*/

        ajaxcalls.simple(self.dataSourcesURI, 'GET', { 'recursive': recursive }).done(function (data) {

            self.loadFromJSON(data.datasources);

            /*  self.tree.jstree(true).settings.core.data = self.dataSources();
             self.tree.jstree(true).refresh(); */

            //ko.mapping.fromJS($("#dataSourcesPanel")[0], self);

            /*$('#tree').find('li.list-group-item').each(function() {
                // cache jquery object
                var current = $(this);
                current.draggable({
                    revert : 'invalid',
                    stack : '.draggable-data',
                    helper : 'clone',
                    zIndex:10000
                });
            });*/

            //               for (node in self.expandedNodes) {
            //               	$('#tree').treeview('expandNode', [ parseInt(self.expandedNodes[node]), { levels: 0, silent: true } ]);
            //               }

        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.getItemByPath = function (source, path) {
        if (source.path === path)
            return source;

        if (source.children !== undefined || source.children != null) {
            for (var i = 0; i < source.children.length; ++i) {

                var subNode = self.getItemByPath(source.children[i], path);
                if (subNode)
                    return subNode;
            }
        }

        return null;
    }

    self.loadItem = function (node, recursive = true) {
        ajaxcalls.simple(self.dataSourcesURI, 'GET', { 'load': node.original.path, 'recursive': recursive }).done(function (data) {

            var dataSources = self.dataSources();

            for (var i = 0; i < dataSources.length; ++i) {

                var item = self.getItemByPath(dataSources[i], data.path);
                if (item != null) {
                    item.text = data.text;
                    item.nodes = data.nodes;

                    ko.cleanNode($("#dataSourcesPanel")[0]);
                    ko.applyBindings(self, $("#dataSourcesPanel")[0]);

                    //                     for (node in self.expandedNodes)
                    //                         $('#tree').jstree(true). ('expandNode', [ parseInt(self.expandedNodes[node]), { levels: 0, silent: true } ]);

                    break;
                }
            }
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.loadNewItem = function (node, newItemName, recursive = true) {
        ajaxcalls.simple(self.dataSourcesURI, 'GET', { 'load': node.original.path, 'recursive': recursive }).done(function (data) {
            var dataSources = self.dataSources();
            var newAddedItemPath = data.path + "\/" + newItemName;
            for (var i = 0; i < dataSources.length; ++i) {

                var item = self.getItemByPath(dataSources[i], data.path);
                if (item != null) {
                    item.text = data.text;
                    item.nodes = data.children;
                    for (var j = 0; j < item.nodes.length; ++j) {
                        var newAddedItem = self.getItemByPath(item.nodes[j], newAddedItemPath);
                        if (newAddedItem != null) {
                            var newItemPositon = 'inside';
                            var newItemId = $("#tree").jstree().create_node(node, newAddedItem, newItemPositon);
                            $("#tree").jstree("deselect_all");
                            $("#tree").jstree(true).select_node(newItemId);
                            break;
                        }
                    }
                    break;
                }
            }
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.selectByPath = function(path) {
        var node = self.getItemByPath(self.dataSources()[0], path);
        $('#tree').jstree("deselect_all");
        $("#tree").jstree(true).select_node(node);
    }

    self.selectedNode = function () {
        node = $('#tree').jstree("get_selected")
        return $('#tree').jstree().get_selected(true)[0];
    }

    self.parentNode = function (node) {
        var parentNodeId = $("#" + node.id).parent().parent().attr('id');
        var parentNode = $("#tree").jstree(true).get_node(parentNodeId);
        return parentNode;
        //return node.parentNode;
    }

    self.upload = function () {

        $('#file-upload-dialog').modal('hide');

        var files = $("#upload").get(0).files;
        var formdata = new FormData();
        formdata.append('upload', files[0]); //use get('files')[0]
        node = self.selectedNode();
        if (node === undefined)
            return;
        formdata.append('path', node.original.path);//you can append it to formdata with a proper parameter name
        formdata.append('filename', $("#inputFilename").val());
        var visualizer = $("#inputVisualizer").val();
        if (visualizer) {
            visualizer = visualizer.split(": ");
            visualizer = {
                [visualizer[0]]: visualizer[1]
            };
            formdata.append('visualizer', JSON.stringify(visualizer));
        }
        formdata.append('annotations', $("#inputAnnotations")[0].value);
        mimetype = $("#inputMimeType").val();
        if (mimetype) {
            mimetype = mimetype.split(": ");
            formdata.append('mimetype', JSON.stringify({ [mimetype[0].trim()]: mimetype[1].trim() }));
        }

        ajaxcalls.form(self.dataSourcesURI, 'POST', formdata).done(function (data) {
            var inputFileName = $("#inputFilename").val();
            self.loadNewItem(node, inputFileName);
        });
    }

    self.about = function () {

        window.open("static/biodsl-help.html#datasources", '_blank');
    }

    self.download = $.debounce(500, function () {

        node = self.selectedNode();
        if (node === undefined) {
            return;
        }

        $.redirect(self.dataSourcesURI, { 'download': node.original.path }, "POST", "_blank");
    });

    self.addFolder = $.debounce(500, function () {
        node = self.selectedNode();

        if (node === undefined)
            return;
        ajaxcalls.simple(self.dataSourcesURI, 'GET', { 'addfolder': node.original.path }).done(function (data) {
            var newNodePosition = 'inside';
            var parentNode = node;
            var newNode = $('#tree').jstree().create_node(parentNode, data, newNodePosition, function () {
                $("#btnAddFolder").removeClass('active');
            });
            $('#tree').jstree("deselect_all");
            $("#tree").jstree(true).select_node(newNode);
        });
    });

    self.remove = $.debounce(500, function () {
        node = self.selectedNode();
        if (node === undefined)
            return;
        ajaxcalls.simple(self.dataSourcesURI, 'GET', { 'delete': node.original.path }).done(function (data) {
            var parentNode = self.parentNode(node);
            if (parentNode === undefined)
                return;

            var siblings = parentNode.children;
            if (siblings !== undefined && siblings.length > 0)
                sibling = siblings[0].path;
            //self.loadItem(parentNode);
            $('#tree').jstree().delete_node(node.id);
            $('#tree').jstree(true).select_node(parentNode.id);

            if (sibling === undefined)
                $('#tree').jstree(true).select_node(node.nodeId);
            else {
                siblingNode = self.getItemByPath(parentNode, sibling);
                $('#tree').treeview('selectNode', siblingNode.nodeId);
            }
        });
    });

    self.openFilterArea = function () {  
        var isClosed = $("#filter-area").is(":hidden");
        if (isClosed) {
            $(".box-zero").show();
            $(".box-two").removeClass('col-md-6').addClass('col-md-4');
        }
    };

    self.openFilterDialog = function (isSave) {
        var okText = isSave ? "Save" : "Search";
        filterViewModel.okText(okText);
        self.openFilterArea();
        // $("#btnfilterToggle").trigger('click');
        // $('#filter-dialog').modal('show');
        // $('#filter-dialog .modal-body').css('max-height', $('#dataSourcesPanel').css('height'));
        // $('#filter-dialog .modal-body').css('width', $('#dataSourcesPanel').css('width')+ '5');
    }
    self.load(true);
    self.init = true;
}
