(function ($) {
  $.fn.datasetlist = function (options) {
    const self = this;
    const settings = $.extend(
      {
        data: [],
        searchBar: false,
        searchBarClass: "",
        searchBarPlaceholder: "Search list",
        itemClass: "",
        itemHeaderClass: "",
        itemBodyClass: "",
        dataItemClass: "",
        onItemClick: $.noop,
        onItemDrag: $.noop,
        onItemRightClick: $.noop,
        onItemExpand: $.noop,
        onItemExpanded: $.noop,
        onItemClosing: $.noop,
        onItemClosed: $.noop,
        onDataItemDoubleClick: $.noop,
        selectedDataItem: null,
      },
      options
    );

    const debounce = function (funcTion, delay, scope, arg) {
      var timeout;
      return function () {
        var context = scope || this,
          args = arg;
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
      jqObj.on("click", function (event) {
        if (
          event.target.className === "glyphicon glyphicon-triangle-bottom" ||
          event.target.className === "glyphicon glyphicon-triangle-top" ||
          event.target.className === "btn" ||
          event.target.className === "btn collapsed"
        ) {
          // const t = $(".glyphicon");
          setItemExpandIcon(event, data);
          // settings.onItemClick.call(null, event, data);
          //   bindItemBodyEvents(data);
        }
      });

      jqObj.on("drag", function (event) {
        settings.onItemDrag.call(null, event, data);
      });

      jqObj.on("mousedown", function (event) {
        if (event.which === 3) {
          settings.onItemRightClick.call(null, event, data);
        }
      });
    };

    self.renderList = function () {
      if (!settings.data.length) {
        console.log("No data supplied!");
        return false;
      }
      settings.data.forEach((ele) => {
        let dataItem = createItem(ele);

        evBind(dataItem, ele);

        //appending every dataset item
        self.append(dataItem);

        // bindItemBodyEvents(ele);
      });
    };

    //callback binding for dataset item body dom events
    const bindItemBodyEvents = (ele) => {
      // console.log("bindItembody", ele)
      // callback on dataset exapnding
      $(`#data-list-item-body-${ele.id}`).on("show.bs.collapse", function (e) {
        // console.log("expand");
        setItemExpandIcon(ele.id);
        settings.onItemExpand.call(null, e, ele);
      });

      // callback on dataset exapnded
      $(`#data-list-item-body-${ele.id}`).on("shown.bs.collapse", function (e) {
        settings.onItemExpanded.call(null, e, ele);
      });

      // callback on dataset closing
      $(`#data-list-item-body-${ele.id}`).on("hide.bs.collapse", function (e) {
        setItemCollapseIcon(ele.id);
        settings.onItemClosing.call(null, e, ele);
      });

      // callback on dataset closed
      $(`#data-list-item-body-${ele.id}`).on(
        "hidden.bs.collapse",
        function (e) {
          settings.onItemClosed.call(null, e, ele);
        }
      );
    };

    self.addNewDataset = function (data) {
      if (!data || !data.id) {
        return false;
      }

      const element = createItem(data);

      evBind(element, data);

      self.append(element);
      bindItemBodyEvents(data);
    };

    const setItemExpandIcon = (event, data) => {
      // console.log("setItemExpanIcon", itemId)
      const target = $(`#dataset-item-expand-${data.id}`).find("i");
      //   console.log(target[0].classList[1], "xxxx");
      if (target && target[0] && target[0].classList) {
        if (target[0].classList[1] === "glyphicon-triangle-bottom") {
          target
            .removeClass("glyphicon-triangle-bottom")
            .addClass("glyphicon-triangle-top");

          settings.onItemExpand.call(null, event, data);
        } else {
          target
            .removeClass("glyphicon-triangle-top")
            .addClass("glyphicon-triangle-bottom");
          $(`#card-body-${data.id}`).jstree("destroy");
          localStorage.clear();
          settings.onItemClosing.call(null, event, data);
        }
      } else {
        return;
      }
    };

    const setItemCollapseIcon = (itemId) => {
      // console.log("setItemCollapseIcon")
      const target = $(`#dataset-item-expand-${itemId}`).find("i");
      if (!target) {
        return;
      }
      target
        .removeClass("glyphicon-triangle-top")
        .addClass("glyphicon-triangle-bottom");
    };

    self.removeDatasetList = function () {
      this.empty("div");
    };

    const createItem = (data) => {
      let dataItems;
      if (data.data && data.data.length > 0) {
        // dataItems =createDataItems(data.data);
        dataItems = data.data;
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
                        <div id="card-body-${data.id}">
                        </div>
                    </div>
                </div>`
      );

      return datasetItem;
    };

    const createDataItems = (dataItems) => {
      const parent = $(`<ul class="list-group"></ul>`);
      dataItems.forEach((item) => {
        if (item.id != null) {
          const itemDom = $(
            `<li class="list-group-item ${settings.dataItemClass}" id="${item.id}"><i class="glyphicon glyphicon-file"></i>${item.name}</li>`
          );

          itemDom.click(function (event) {
            event.stopPropagation();
            $(document)
              .find(".list-group-item")
              .removeClass("list-group-item-clicked");
            $(this).addClass("list-group-item-clicked");
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
    };

    self.lazyLoadDatasetItems = function (dataset, dataItems) {
      let selectedNode;
      if (dataItems.parent === "#") {
        $(`#card-body-${dataset.id}`)
          .bind("dblclick.jstree", function (e) {
            const savedItem = localStorage.getItem(`${selectedNode}`);
            if (savedItem === null) {
              var instance = $.jstree.reference(this);
              const path = instance.get_path(e.target);
              localStorage.setItem(`${selectedNode}`, true);
              settings.onDataItemDoubleClick(e, {
                path,
                dataset,
                selectedNode,
              });
            }
          })
          .bind("move_node.jstree", function (e, data) {
            console.log("Move Event");
          })
          .on("changed.jstree", function (e, data) {
            selectedNode = data.selected;
          })
          .jstree({
            plugins: ["dnd", "themes", "types"],
            core: {
              dblclick_toggle: false,
              check_callback: true,
              data: dataItems,
            },
            types: {
              default: {
                icon: "jstree-folder",
              },
              file: {
                icon: "jstree-file",
              },
            },
          })
          .on("create_node.jstree", function (e, data) {
            console.log("saved");
          });

        $(document).on("dnd_start.vakata", function (e, data) {
          if (data.data.jstree) {
            // console.log(data.data.jstree);
            console.log("User started dragging");
          }
        });

        $(document).on("dnd_stop.vakata", function (e, eData) {
          // console.log(eData.event.target);
          if (eData.data.jstree) {
            // console.log(data.id);
            const path = $(`#card-body-${dataset.id}`)
              .jstree(true)
              .get_path(eData.element, "/");
            console.log("User stopped dragging");
            // console.log(dataset)
            settings.onItemDrag.call(null, e, { path, dataset });
          }
        });
      } else {
        dataItems.forEach(dataItem =>{
          $(`#card-body-${dataset.id}`)
          .jstree()
          .create_node(
            dataItem.parent,
            {
              id: dataItem.id,
              text: dataItem.text,
            },
            "last",
            function () {
              // alert("Parent created");
            }
          );
          
        })
       
      }
    };

    const searchDatasetList = (e) => {
      if (!e.target.value) {
        $(`[id^='dataset-list-item-']`).show();
        return;
      }
      const searchString = e.target.value.toLowerCase();
      settings.data.forEach((ele) => {
        if (
          ele.title.toLowerCase().indexOf(searchString) == -1 &&
          ele.group.toLowerCase().indexOf(searchString) == -1 &&
          ele.url.toLowerCase().indexOf(searchString) == -1 &&
          ele.type.toLowerCase().indexOf(searchString) == -1
        ) {
          $(`#dataset-list-item-${ele.id}`).hide();
        } else {
          $(`#dataset-list-item-${ele.id}`).show();
        }
      });
    };

    const appendSearchBar = () => {
      if (!settings.searchBar) {
        return;
      }
      const searchBar = $(
        `<input id="dataset-list-search" type="text" class="form-control ${settings.searchBarClass}" placeholder="${settings.searchBarPlaceholder}" aria-describedby="dataset-list-search">`
      );

      searchBar.on("keyup", function (e) {
        debounce(searchDatasetList, 300, this, e)();
      });

      self.append(searchBar);
    };

    appendSearchBar();

    const setSelectedDataItem = (data) => {
      settings.selectedDataItem = data;
    };

    self.getSelectedDataItem = function () {
      return settings.selectedDataItem;
    };

    return this;
  };
})(jQuery);
