(function($){
    $.fn.datasetlist = function(options){
        const self = this;
        const settings = $.extend({
            data: [],
            searchBar: false,
            searchBarClass: '',
            searchBarPlaceholder: "Search list",
            itemClass: '',
            itemHeaderClass: '',
            itemBodyClass: '',
            dataItemClass: '',
            onItemClick: $.noop,
            onItemDrag: $.noop,
            onItemRightClick: $.noop,
            onItemExpand: $.noop,
            onItemExpanded: $.noop,
            onItemClosing: $.noop,
            onItemClosed: $.noop,
            onDataItemDoubleClick: $.noop,
            selectedDataItem: null
        }, options);

        const debounce = function(funcTion, delay, scope, arg) {
            var timeout;
            return function () {
                var context = scope || this, args = arg;
                var later = function () {
                    timeout = null;
                    funcTion.call(context, args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, delay);
            };
        };

        // bind events on datasetItem
        const evBind = (jqObj, data) => {
            
            jqObj.on('click',function (event) {
                settings.onItemClick.call(null,event, data);
            });

            jqObj.on('drag', function(event){
                settings.onItemDrag.call(null, event, data);
            });

            jqObj.on('mousedown', function(event){
                if (event.which === 3) {
                    settings.onItemRightClick.call(null, event, data);
                }
            });
        }

        self.renderList = function () {
            if (!settings.data.length) {
                console.log("No data supplied!");
                return false;
            }
            settings.data.forEach(ele => {
                let dataItem = createItem(ele);
                
                evBind(dataItem, ele)

                //appending every dataset item
                self.append(dataItem);

                bindItemBodyEvents(ele);
            });
        }

        //callback binding for dataset item body dom events
        const bindItemBodyEvents = (ele) => {
            // callback on dataset exapnding
            $(`#data-list-item-body-${ele.id}`).on('show.bs.collapse', function(e){
                setItemExpandIcon(ele.id);
                settings.onItemExpand.call(null, e, ele);
            });

            // callback on dataset exapnded
            $(`#data-list-item-body-${ele.id}`).on('shown.bs.collapse', function(e){
                settings.onItemExpanded.call(null, e, ele);
            });

            // callback on dataset closing
            $(`#data-list-item-body-${ele.id}`).on('hide.bs.collapse', function(e){
                setItemCollapseIcon(ele.id);
                settings.onItemClosing.call(null, e, ele);
            });

            // callback on dataset closed
            $(`#data-list-item-body-${ele.id}`).on('hidden.bs.collapse', function(e){
                settings.onItemClosed.call(null, e, ele);
            });
        }

        self.addNewDataset = function (data) {
            if (!data || !data.id) {
                return false;
            }

            const element = createItem(data);
            
            evBind(element, data);

            self.append(element);
            bindItemBodyEvents(data);
        }

        const setItemExpandIcon = (itemId) => {
            const target = $(`#dataset-item-expand-${itemId}`).find('i');
            if (!target) {
                return
            }
            target.removeClass('glyphicon-triangle-bottom').addClass('glyphicon-triangle-top');
        }

        const setItemCollapseIcon = (itemId) => {
            const target = $(`#dataset-item-expand-${itemId}`).find('i');
            if (!target) {
                return
            }
            target.removeClass('glyphicon-triangle-top').addClass('glyphicon-triangle-bottom');
        }

        self.removeDatasetList = function () {  
            this.empty('div');
        }

        const createItem = (data) => {
            let dataItems;
            if (data.data && data.data.length > 0) {
                dataItems =createDataItems(data.data);
            }
            const datasetItem = $(
                `<div class="card mb-1 ${settings.itemClass}" id="dataset-list-item-${data.id}">
                    <div class="card-header ${settings.itemHeaderClass}">
                        <div class='container-fluid'>
                            <div class='row'>
                                <div class='col-xs-9 col-sm-9 col-md-10 col-lg-10'>
                                    <h4 style="margin-bottom: 1vh">
                                        <strong>${data.title}</strong>
                                    </h4>
                                </div>
                                <div class="col-xs-3 col-sm-3 col-md-2 col-lg-2">
                                    <button class="btn collapsed" id='dataset-item-expand-${data.id}' style="margin-top:1vh" data-toggle="collapse" data-target="#data-list-item-body-${data.id}" aria-expanded="false" aria-controls="data-list-item-${data.id}">
                                        <i class="glyphicon glyphicon-triangle-bottom"></i>
                                    </button>
                                </div>
                                <div class='col-xs-12 px-4'>
                                    <a href='${data.url}'>${data.url}</a>
                                </div>
                            </div>
                            <div class='row px-4'>
                                <div class='col-xs-9 col-sm-8 col-md-10 col-lg-9'>
                                    <p>${data.group}</p>
                                </div>
                                <div class='col-xs-3 col-sm-4 col-md-2 col-lg-3'>
                                    <p>${data.type}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="data-list-item-body-${data.id}" class="collapse ${settings.itemBodyClass}" aria-labelledby="headingTwo" data-parent="#accordion">
                        <div class="card-body">
                        </div>
                    </div>
                </div>`
            )
            
            datasetItem.find(`#data-list-item-body-${data.id}`).find('.card-body').append(dataItems);

            return datasetItem;
        }

        const createDataItems = (dataItems) => {
            const parent = $(`<ul class="list-group"></ul>`)
            dataItems.forEach(item => {
                if (item.id!= null) {
                    const itemDom = $(`<li class="list-group-item ${settings.dataItemClass}" id="${item.id}"><i class="glyphicon glyphicon-file"></i>${item.name}</li>`);

                    itemDom.click(function(event){
                        event.stopPropagation();
                        $(document).find(".list-group-item").removeClass('list-group-item-clicked');
                        $(this).addClass('list-group-item-clicked');
                        setSelectedDataItem(item);
                    });

                    itemDom.dblclick(function (event) {
                        event.stopPropagation();
                        settings.onDataItemDoubleClick.call(null, event, item);
                    });

                    parent.append(itemDom);
                }
            });
            return parent;
        }

        self.lazyLoadDatasetItems = function (datasetId, dataItems) {
            if (datasetId== null || datasetId == undefined) {
                return false
            }
            if(!Array.isArray(dataItems) && !dataItems.length){
                return false;
            }
            $(`#data-list-item-body-${datasetId}`).find('.card-body').empty();
            const domElements = createDataItems(dataItems);
            $(`#data-list-item-body-${datasetId}`).find('.card-body').append(domElements);
        }

        const searchDatasetList = (e) => {
            if (!e.target.value) {
                $(`[id^='dataset-list-item-']`).show();
                return;
            }
            const searchString = e.target.value.toLowerCase();
            settings.data.forEach((ele) => {
                if (ele.title.toLowerCase().indexOf(searchString) == -1  && ele.group.toLowerCase().indexOf(searchString) == -1  && ele.url.toLowerCase().indexOf(searchString) == -1 
                    && ele.type.toLowerCase().indexOf(searchString) == -1  ) {
                    $(`#dataset-list-item-${ele.id}`).hide();
                }
                else{
                    $(`#dataset-list-item-${ele.id}`).show();
                }
            })
        }

        const appendSearchBar = () => {
            if (!settings.searchBar) {
                return;
            }
            const searchBar = $(`<input id="dataset-list-search" type="text" class="form-control ${settings.searchBarClass}" placeholder="${settings.searchBarPlaceholder}" aria-describedby="dataset-list-search">`);
            
            searchBar.on('keyup',function(e){
                debounce(searchDatasetList, 300, this, e)();
            });

            self.append(searchBar);
        }

        appendSearchBar();

        const setSelectedDataItem = (data) => {
            settings.selectedDataItem = data;
        }

        self.getSelectedDataItem = function(){
            return settings.selectedDataItem;
        }
        
        return this;
    }
})(jQuery)