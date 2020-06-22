function provgraphViewModel()
        {
        	var self = this;

    		self.show = function(rels) {
				
				//diagram reload function
    			function diagramReload(diagramName){
    				var diagramDiv = document.getElementById(diagramName);
        			if (diagramDiv !== null) {
        			    var olddiag = go.Diagram.fromDiv(diagramDiv);
        			    if (olddiag !== null)
        			    	olddiag.div = null;
        			}
    			}				

    			diagramReload("provenance");				//reload the graph
    			diagramReload("provDiagramOverview");		//reload the overview
      			
    			//gojs graph
    			var $$ = go.GraphObject.make;
    			provDiagram =
    		        $$(go.Diagram, "provenance",
    		          {
    		            initialContentAlignment: go.Spot.Center,		//display the graph at center initially
    		            initialAutoScale: go.Diagram.UniformToFill,
    		            layout: $$(go.LayeredDigraphLayout,				//graph layout is Layered
    		              { direction: 0,								//graph will extend towards Right direction
							layeringOption: go.LayeredDigraphLayout.LayerLongestPathSource,
							setsPortSpots: false
    		              }),
    		            "undoManager.isEnabled": true,
    		            "animationManager.isEnabled": true
    		          }
					);
					provDiagram.grid.visible = true;

				// create the Overview and initialize it to show the main Diagram
				var provOverview =
				$$(go.Overview, "provDiagramOverview",
					{ observed: provDiagram });
				provOverview.grid.visible = true;


				provDiagram.nodeTemplate = $$(go.Node, "Spot",
					{ selectionAdorned: false },  
					$$(go.Panel, "Auto",
						{ width: 120, height: 90,								//size of nodes
						  name: 'node', minSize: new go.Size(100, 70), maxSize: new go.Size(150,10)},							
						$$(go.Shape, "RoundedRectangle",						//shape of nodes
							{
								fill: "white", stroke: null, strokeWidth: 0,  
								spot1: go.Spot.TopLeft, spot2: go.Spot.BottomRight,
								portId: ""
							},
							new go.Binding("fill", "color"),
							new go.Binding("figure", "shape")),
						$$(go.Panel, "Table",
							$$(go.TextBlock, 
								{
									name: 'nodeName',
									row: 0,
									margin: 3,
									maxSize: new go.Size(80, NaN),
									stroke: "white",								//node name color
									font: "bold 9pt sans-serif",					//node name font	
								},
							new go.Binding("text", "name").makeTwoWay(),
								{
									toolTip:
									$$("ToolTip",
										$$(go.TextBlock, { margin: 4 },
										new go.Binding("text", "name"))
									)
								}
							),
							$$(go.TextBlock,
							{
								row: 2,
								margin: 3,
								maxSize: new go.Size(80, 40),
								stroke: "white",							//node type color
								font: "bold 6pt sans-serif"					//node type font
							},
							new go.Binding("text", "type").makeTwoWay()),
							),
							
							//newly added for contaxt menu
							$$(go.TextBlock),
							{
								contextMenu:     // define a context menu for each node
								  $$("ContextMenu",   
									$$(go.Panel, "Table",
										{background: 'white'},
										$$(go.TextBlock,
											{
												row: 0,
												alignment: go.Spot.Left,
												margin: 3
											},
											new go.Binding("text", "key").makeTwoWay()
										),
										$$(go.TextBlock,
											{
												row: 1,
												alignment: go.Spot.Left,
												margin: 3
											},
											new go.Binding("text", "type").makeTwoWay()
										),
										$$(go.TextBlock,
											{
												row: 2,
												alignment: go.Spot.Left,
												margin: 3
											},
											new go.Binding("text", "name").makeTwoWay()
										)
									)
								)  // end Adornment
							}
						)
					);
					
				provDiagram.linkTemplate =
				$$(go.Link,
					{
						routing: go.Link.AvoidsNodes,						//link routing style 
						corner: 5,
						relinkableFrom: true, 
						relinkableTo: true,
						fromSpot: go.Spot.RightSide, toSpot: go.Spot.LeftSide,
					},
					$$(go.Shape, { stroke: "gray", strokeWidth: 2 }),
					$$(go.TextBlock,                        
					new go.Binding("text", "value"), 						//link label data binding
					{font: "bold 6pt sans-serif"}),							//link label font
					
					$$(go.Shape, { fromArrow: "Block", fill: "gray" }),
					$$(go.TextBlock,
					{
						segmentIndex: 0, alignmentFocus: new go.Spot(1, 0.5, 2, 0),
						stroke: "white", 									//outport text color
    		         	font: "bold 6pt arial" 								//outport text font
					},
					new go.Binding("text", "frompid")),

					$$(go.Shape, { toArrow: "RoundedTriangle", fill: "orange" }),
					$$(go.TextBlock,
					{
						segmentIndex: -1, alignmentFocus: new go.Spot(0, 0.5, -2, 0),
						stroke: "white", 									//inport text color
    		         	font: "bold 6pt arial" 								//inport text font
					},
					new go.Binding("text", "topid"))
				); 	

				let typeArr = [];
				let colorArr = ['DarkSlateGray', 'SteelBlue', 'Teal', 'Indigo', 'MidnightBlue', 'IndianRed', 'DeepSkyBlue', 'DarkSalmon', 'DarkGreen', 'DarkOrange'];

				//set color for each type
				rels['nodeDataArray'].forEach(function(node) {
					if(!typeArr.includes(node.type)){
						typeArr.push(node.type);
					}
					
					let typeIndex = typeArr.indexOf(node.type);

					if(colorArr[typeIndex] !== undefined)
						node.color = colorArr[typeIndex];
					else
						node.color = 'Black';

					node.name += '\n';								//add a new line after node name
				});

				//creating graph using model data 
				var provModelData = ({class: 'go.GraphLinksModel', nodeDataArray: rels['nodeDataArray'], linkDataArray: rels['linkDataArray']});
				provDiagram.model = go.Model.fromJson(JSON.stringify(provModelData));  //load()
				
				provDiagram.model.isReadOnly = true;
			}		
		}
        
      //=======================================
      //=============gojs graph end============
      //=======================================
       