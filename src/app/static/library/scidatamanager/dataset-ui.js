(function ($) {
  $.fn.datasetlist = function (options) {
    var self = this;
    self.settings = $.extend(
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
        onSelectionChanged: $.noop,
        currentLoadedData: $.noop,
        selectedDataItem: null,
        apiUrl: null,
        secretKey: null,
        userName: null,
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
    self.evBind = (jqObj, data) => {
      jqObj.on("click", function (event) {
        if (
          event.target.className === "glyphicon glyphicon-triangle-bottom" ||
          event.target.className === "glyphicon glyphicon-triangle-top" ||
          event.target.className === "btn" ||
          event.target.className === "btn collapsed"
        ) {
          // const t = $(".glyphicon");
          self.setItemExpandIcon(event, data);
          // self.settings.onItemClick.call(null, event, data);
          // self.bindItemBodyEvents(data);
        }
      });

      jqObj.on("drag", function (event) {
        self.settings.onItemDrag.call(null, event, data);
      });

      jqObj.on("mousedown", function (event) {
        if (event.which === 3) {
          self.settings.onItemRightClick.call(null, event, data);
        }
      });
    };

    self.renderList = function () {
      if (!self.settings.data.length) {
        console.log("No data supplied!");
        return false;
      }
      self.settings.data.forEach((ele) => {
        let dataItem = self.createItem(ele);

        self.evBind(dataItem, ele);

        //appending every dataset item
        self.append(dataItem);

        // self.bindItemBodyEvents(ele);
      });
    };

    //callback binding for dataset item body dom events
    self.bindItemBodyEvents = (ele) => {
      // callback on dataset exapnding
      $(`#data-list-item-body-${ele.id}`).on("show.bs.collapse", function (e) {
        self.setItemExpandIcon(ele.id);
        self.settings.onItemExpand.call(null, e, ele);
      });

      // callback on dataset exapnded
      $(`#data-list-item-body-${ele.id}`).on("shown.bs.collapse", function (e) {
        self.settings.onItemExpanded.call(null, e, ele);
      });

      // callback on dataset closing
      $(`#data-list-item-body-${ele.id}`).on("hide.bs.collapse", function (e) {
        setItemCollapseIcon(ele.id);
        self.settings.onItemClosing.call(null, e, ele);
      });

      // callback on dataset closed
      $(`#data-list-item-body-${ele.id}`).on(
        "hidden.bs.collapse",
        function (e) {
          self.settings.onItemClosed.call(null, e, ele);
        }
      );
    };

    self.addNewDataset = function (data) {
      if (!data) {
        return false;
      }

      const element = self.createItem(data);

      self.evBind(element, data);

      self.append(element);
      self.bindItemBodyEvents(data);
    };

    self.setItemExpandIcon = (event, data) => {
      const target = $(`#dataset-item-expand-${data.id}`).find("i");
      if (target && target[0] && target[0].classList) {
        if (target[0].classList[1] === "glyphicon-triangle-bottom") {
          target
            .removeClass("glyphicon-triangle-bottom")
            .addClass("glyphicon-triangle-top");

            self.settings.onItemExpand.call(null, event, data);
        } else {
          console.log("Cloasing");
          target
            .removeClass("glyphicon-triangle-top")
            .addClass("glyphicon-triangle-bottom");
          $(`#card-body-${data.id}`).jstree("destroy");
          // localStorage.removeItem(data.id);
          self.settings.onItemClosing.call(null, event, data);
        }
      } else {
        return;
      }
    };

    const setItemCollapseIcon = (itemId) => {
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

    self.createItem = (data) => {
      let dataItems;
      if (data.data && data.data.length > 0) {
        // dataItems =createDataItems(data.data);
        dataItems = data.data;
      }
      let datasetItem = $(
        `<div class="card mb-1 ${self.settings.itemClass}" id="dataset-list-item-${data.id}">
                    <div class="card-header ${self.settings.itemHeaderClass}">
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
                    <div id="data-list-item-body-${data.id}" class="expanded-js-tree collapse ${self.settings.itemBodyClass}" aria-labelledby="headingTwo" data-parent="#accordion" style="max-height:30vh; overflow:scroll;">
                    <div >
                    <div style="display:flex">
                   <!--- <input  style="display: inline"id="search-data-${data.id}; height: 45vh; overflow: scroll" type="text" class="mt-5 form-control" placeholder="search text" aria-describedby="dataset-list-search">
                      <button id="search-btn-${data.id}" class="search-btn"> Search </button>
                     </div>
                     -->
                   <div>
                      <div id="card-body-${data.id}">
                      </div>
                    </div>
                </div>`
      );

      return datasetItem;
    };

    // const createDataItems = (dataItems) => {
    //   const parent = $(`<ul class="list-group"></ul>`);
    //   dataItems.forEach((item) => {
    //     if (item.id != null) {
    //       const itemDom = $(
    //         `<li class="list-group-item ${self.settings.dataItemClass}" id="${item.id}"><i class="glyphicon glyphicon-file"></i>${item.name}</li>`
    //       );

    //       itemDom.click(function (event) {
    //         event.stopPropagation();
    //         $(document)
    //           .find(".list-group-item")
    //           .removeClass("list-group-item-clicked");
    //         $(this).addClass("list-group-item-clicked");
    //         setSelectedDataItem(item);
    //       });

    //       itemDom.dblclick(function (event) {
    //         event.stopPropagation();
    //         self.settings.onDataItemDoubleClick.call(null, event, item);
    //       });

    //       parent.append(itemDom);
    //     }
    //   });
    //   return parent;
    // };

    self.lazyLoadDatasetItems = function (dataset) {
      let selectedNode;
      let currentNode;
      const itemPerPage = 3;
      $(`#card-body-${dataset.id}`)
        .bind("dblclick.jstree", function (e) {
          var instance = $.jstree.reference(this);
          const pathArr = instance.get_path(e.target);
          let path = "";
          pathArr.forEach((p) => (path += `/${p}`));
          self.settings.onDataItemDoubleClick(e, {
            path,
            dataset,
            selectedNode,
          });
        })
        .bind("move_node.jstree", function (e, data) {
          console.log("Move Event");
        })
        .on("changed.jstree", function (e, data) {
          e.preventDefault();
          e.cancelBubble = true;
          e.stopPropagation();

          const parent = data.node.parent;
          selectedNode = data.selected;
          const selectedNodeLoadInfo = getSelctedNodesStatus(
            dataset.id,
            selectedNode[0]
          );
          
          path = selectedNode[0];
          if (path && !path.includes("load more")) {
            self.settings.onSelectionChanged.call(null, e, { path: `/${path}`, data });
          }

          if (
            selectedNode &&
            selectedNode[0] &&
            selectedNode[0].includes(">")
          ) {
            document.getElementById(
              `${selectedNode[0]}_anchor`
            ).childNodes[0].className = `fa fa-spinner fa-spin jstree-icon jstree-themeicon jstree-themeicon-custom`;

            // document.getElementsById(
            //   `${selectedNode[0]}_anchor`
            // )[0].className = `fa fa-spinner fa-spin jstree-icon jstree-themeicon ${selectedNode[0]} jstree-themeicon-custom`;

            const nodeId = selectedNode[0].split(">")[0];
            const datasetId = selectedNode[0].split(">")[1];

            const loadedNodes = getLoadMoreNodes(
              self.settings.apiUrl,
              nodeId,
              datasetId,
              selectedNodeLoadInfo.pageNum,
              self.settings,
              (loadedNodes) => {
                const { commonApiObj, loadedData } = loadedNodes;
                appendLoadedChild(
                  loadedData,
                  commonApiObj.loadNodeId,
                  datasetId
                );
                // setSelctedNodesStatus(datasetId, commonApiObj);
                store.dispatch(
                  setDatasetChildNodeStateAction(datasetId, commonApiObj)
                );

                document.getElementById(
                  `${selectedNode[0]}_anchor`
                ).childNodes[0].className = `jstree-icon jstree-themeicon jstree-themeicon-custom`;

                if (!commonApiObj.hasMore) {
                  deleteLoadeMoreNode(datasetId, commonApiObj.loadNodeId);
                }
              }
            );
          }
        })
        .jstree({
          plugins: getJsTreePlugins(),
          core: {
            dblclick_toggle: false,
            check_callback: true,
            data: {
              type: "GET",
              async: true,
              url: function () {
                return self.settings.apiUrl;
              },
              dataFilter: function (data) {
                const commonApiResObj = getCommonApiResObj(JSON.parse(data));
                return getLoadMoreNodeWithRootResponse(
                  dataset.id,
                  commonApiResObj,
                  JSON.parse(data)
                );
              },
              data: function (node) {
                currentNode = node.id === "#" ? -1 : node.id;
                return getJsTreeApiRequestQueryString(
                  node.id,
                  dataset.id,
                  self.settings
                );
              },
              success: function (data) {
                console.log("success");
                self.settings.currentLoadedData(dataset.id, currentNode, data);
              },
            },
          },
          // search: {
          //   show_only_matches: true,
          //   ajax: function (str, callback) {
          //     $.ajax({
          //       url: self.settings.apiUrl,
          //       dataType: "json",
          //       contentType: "application/json;",
          //       data: { str: str },
          //     }).done(function (data) {
          //       data = data;
          //       callback(data);
          //     });
          //   },
          // },

          types: {
            default: {
              icon: "jstree-folder",
            },
            file: {
              icon: "jstree-file",
            },
          },
        });

      $(document).on("dnd_start.vakata", function (e, data) {
        if (data.data.jstree) {
          console.log("User started dragging");
        }
      });

      $(document).on("dnd_stop.vakata", function (e, eData) {
        // console.log(eData.data.jstree, eData.event.type)
        if (eData.data.jstree && eData.event.type !== "drop") {
          if ($(`#card-body-${dataset.id}`).jstree(true)) {
            const path = $(`#card-body-${dataset.id}`)
              .jstree(false)
              .get_path(eData.element, "/");
            console.log("User stopped dragging");

            if (path && !path.includes("load more")) {
              self.settings.onItemDrag.call(null, eData.event, { path: `/${path}`, dataset });
              // $(`#card-body-${dataset.id}`).jstree(true).refresh(true);
            }
            // $(`#card-body-${dataset.id}`).jstree(true).refresh()
          }
        }
      });

      // var to = false;
      // $(`#search-btn-${dataset.id}`).click(function () {
      //   if (to) {
      //     clearTimeout(to);
      //   }
      //   to = setTimeout(function () {
      //     console.log(dataset.id);
      //     let key = document.getElementById(`search-data-${dataset.id}`).value;
      //     console.log(key);
      //     $(`#card-body-${dataset.id}`).jstree(true).search(key);
      //   }, 250);
      // });
    };

    self.searchDatasetList = (e) => {
      if (!e.target.value) {
        $(`[id^='dataset-list-item-']`).show();
        return;
      }
      const searchString = e.target.value.toLowerCase();
      self.settings.data.forEach((ele) => {
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

    self.appendSearchBar = () => {
      if (!self.settings.searchBar) {
        return;
      }
      const searchBar = $(
        `<input id="dataset-list-search" type="text" class="form-control ${self.settings.searchBarClass}" placeholder="${self.settings.searchBarPlaceholder}" aria-describedby="dataset-list-search">`
      );

      searchBar.on("keyup", function (e) {
        debounce(searchDatasetList, 300, this, e)();
      });

      self.append(searchBar);
    };

    self.appendSearchBar();

    self.setSelectedDataItem = (data) => {
      self.settings.selectedDataItem = data;
    };

    self.getSelectedDataItem = function () {
      return self.settings.selectedDataItem;
    };

    return this;
  };
  // const render = () => {
  //   console.log(store.getState(), "redux store");
  // };
  // render();
})(jQuery);
