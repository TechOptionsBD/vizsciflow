const getStaticDataset = () => {
  let data = {
    parent: {
      id: "1", 
      parent: "#", 
      text: "Sample Root" 
    },
    child: [
      { 
        id: "6",
        parent: "1",
        text: "Child 1"
      },
      {
        id: "7",
        parent: "1",
        text: "cat.mp4",
        type: "file"
      },
      {
        id: "8",
        parent: "1",
        text: "Child 2"
      },
      { 
        id: "3",
        parent: "2",
        text: "Child 1"
      },
      {
        id: "4",
        parent: "2",
        text: "video.mp4",
        type: "file"
      },
      {
        id: "5",
        parent: "2",
        text: "Child 2"
      }
    ]
  }
  
  const datasetType = ["My Dataset", "Group Dataset", "Public Dataset"];

  return data;
};
