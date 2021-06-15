const getStaticDataset = () => {
  let data = [];
  const datasetType = ["My Dataset", "Group Dataset", "Public Dataset"];

  for (let i = 69; i < 75; i++) {
    const randChoice = Math.floor(Math.random() * 10);
    const dataset = {
      title: `Dataset ${i}`,
      url: `fakepath/${i}`,
      group: `Group ${i}`,
      type: datasetType[randChoice % 3],
      id: i,
      // data: [
      //   {
      //     plugins: ["dnd", "themes", "types"],
      //     core: {
      //       check_callback: true,
      //       dblclick_toggle: false,
      //       data: [
      //         { id: "ajson1", parent: "#", text: "Simple root node" },
      //         { id: "ajson2", parent: "#", text: "Root node 2" },

      //         { id: "ajson6", parent: "ajson1", text: "Child 1" },
      //         {
      //           id: "ajson7",
      //           parent: "ajson1",
      //           text: "cat.mp4",
      //           type: "file",
      //         },
      //         {
      //           id: "ajson8",
      //           parent: "ajson1",
      //           text: "Child 2",
      //         },

      //         { id: "ajson3", parent: "ajson2", text: "Child 1" },
      //         {
      //           id: "ajson4",
      //           parent: "ajson2",
      //           text: "video.mp4",
      //           type: "file",
      //         },
      //         {
      //           id: "ajson5",
      //           parent: "ajson2",
      //           text: "Child 2",
      //         },
      //       ],
      //     },

      //     types: {
      //       default: {
      //         icon: "jstree-folder",
      //       },
      //       file: {
      //         icon: "jstree-file",
      //       },
      //     },
      //   },
      // ],
    };
    // const dataset = {
    //   title: `Dataset ${i}`,
    //   url: `fakepath/${i}`,
    //   group: `Group ${i}`,
    //   type: datasetType[randChoice % 3],
    //   id: i,
    //   data: [
    //     { id: i, name: `abc ${i}` },
    //     { id: i + 1, name: `abc ${i + 1}` },
    //     { id: i + 2, name: `abc ${i + 2}` },
    //     { id: i + 3, name: `abc ${i + 3}` },
    //     { id: i + 4, name: `abc ${i + 4}` },
    //     { id: i + 5, name: `abc ${i + 5}` },
    //   ],
    // };
    data.push(dataset);
  }
  return data;
};

// $("#tree").jstree({
//   core: {
//     data: {
//       url: function (node) {
//         return "/url/getTree";
//       },
//       type: "GET",
//       data: function (node) {
//         return {
//           parentId: node.id === "#" ? 0 : node.id,
//           searchdepth: 1,
//         };
//       },
//       success: function (data) {
//         return data.list;
//       },
//     },
//     check_callback: true,
//   },
//   plugins: ["json_data"],
// });
