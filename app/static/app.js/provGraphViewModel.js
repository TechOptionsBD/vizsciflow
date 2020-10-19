function provgraphViewModel()
        {
        	var self = this;

    		self.show = function(rels) {
				if(rels == null)
					return;

				//diagram reload function
    			function diagramReload(diagramName){
    				var diagramDiv = document.getElementById(diagramName);
        			if (diagramDiv !== null) {
        			    var olddiag = go.Diagram.fromDiv(diagramDiv);
        			    if (olddiag !== null){
							olddiag.div = null;
							diagramDiv = null;
						}
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
					provDiagram.animationManager.initialAnimationStyle = go.AnimationManager.None;

				// create the Overview and initialize it to show the main Diagram
				var provOverview =
				$$(go.Overview, "provDiagramOverview",
					{ observed: provDiagram });
				provOverview.grid.visible = true;

				function geoFunc(geoname = "file") {
					var geo = icons[geoname];
					if (typeof geo === "string") {
						geo = icons[geoname] = go.Geometry.parse(geo, true);  // fill each geometry
					}
					return geo;
				}

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
							$$(go.Shape, "Circle",
								{ 
									row: 1,
									margin: 3,
									maxSize: new go.Size(25, 25),
									fill: "lightcoral", 
									strokeWidth: 0
								},
								{ 
									click: function(e, obj) { 
										self.showMessageModal(obj.part.data);
										e.handled = true; 
									} 
								}),
							$$(go.Shape,
								{ 
									row: 1,
									margin: 3,
									maxSize: new go.Size(15, 15),
									margin: 3, 
									fill: "white", 
									strokeWidth: 0 
								},
								{ 
									click: function(e, obj) {
										self.showMessageModal(obj.part.data);
										e.handled = true; 
									} 
								},
								new go.Binding("geometry", "geo", geoFunc)),
							$$(go.TextBlock,
							{
								row: 2,
								margin: 3,
								maxSize: new go.Size(80, 40),
								stroke: "white",							//node type color
								font: "bold 6pt sans-serif"					//node type font
							},
							new go.Binding("text", "type").makeTwoWay())
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

				provDiagram.groupTemplate =
				$$(go.Group, "Auto",
					{ selectionAdorned: false }, 
					{ layout: $$(go.LayeredDigraphLayout,
						{ direction: 0,								//graph will extend towards Right direction
						  layeringOption: go.LayeredDigraphLayout.LayerLongestPathSource,
						  setsPortSpots: false
						})
					},
					$$(go.Shape, "RoundedRectangle", 
						{ parameter1: 10, fill: "rgba(128,128,128,0.33)" , stroke: "darkorange" }),
					$$(go.Panel, "Table",
						{ margin: 0.5 },  											  	// avoid overlapping border with table contents
						$$(go.RowColumnDefinition, { row: 0, background: "DimGray" }),  	// header color
						$$("SubGraphExpanderButton", { row: 0, column: 0, margin: 3 }),
						$$(go.TextBlock,  												// title is centered in header
							{ row: 0, column: 1, font: "bold 14px Sans-Serif", stroke: "FloralWhite",		// title color
								textAlign: "center", stretch: go.GraphObject.Horizontal },
							new go.Binding("text", "key")),
						$$(go.Placeholder,  											// becomes zero-sized when Group.isSubGraphExpanded is false
							{ row: 1, columnSpan: 2, padding: 10, alignment: go.Spot.TopLeft },
							new go.Binding("padding", "isSubGraphExpanded",
											function(exp) { return exp ? 10 : 0; } ).ofObject())
						)
					);
			
				provDiagram.layout = $$(go.LayeredDigraphLayout,
									{ direction: 0,								//graph will extend towards Right direction
									  layeringOption: go.LayeredDigraphLayout.LayerLongestPathSource,
									  setsPortSpots: false
									});

				// provDiagram.addDiagramListener("ObjectSingleClicked",
				// 	function(e) {
				// 		var part = e.subject.part;
				// 		if (!(part instanceof go.Link)) 
				// 			self.showMessageModal(part.data);
				// 	});
					
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

					// node.name += '\n';								//add a new line after node name
					node.geo = "file";
				});

				//creating graph using model data 
				var provModelData = ({class: 'go.GraphLinksModel', nodeDataArray: rels['nodeDataArray'], linkDataArray: rels['linkDataArray']});
				provDiagram.model = go.Model.fromJson(JSON.stringify(provModelData));  //load()
				
				provDiagram.model.isReadOnly = true;
			}
			
			self.showMessageModal = function(node){
				var formdata = new FormData();
				formdata.append('nodeinfo', node.key);
				
				ajaxcalls.form('/graphs', 'POST', formdata).done( function (data){
					if(data == undefined)
						return;
						
					$("#showMessageModal").find('.modal-body ul li').remove();
					
					data = JSON.parse(data)
					Object.entries(data).forEach(
						([key, value]) => {
							if(value){
								if(key === 'name'){
									$("#showMessageModal").find('h4#NodeName').text(value)
								}
								else{
									$("#showMessageModal").find('.modal-body #NodeInfo').append("<li>"+key+" : "+value+"</li>")
								}
							}
						}
					)

					if (!($('.modal.in').length)) {
						$('.modal-dialog').css({
							top: 0,
							left: 0
						});
					}
					
					$('#showMessageModal .modal-dialog').draggable({
						handle: ".modal-header"
					});

					$('#showMessageModal').modal('show');
						
				}).fail(function(jqXHR){
					alert("Status:"+jqXHR.status)
				});
				
			}
		}
        
      //=======================================
      //=============gojs graph end============
      //=======================================
       
