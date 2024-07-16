mermaid = """
Rules for mermaid js flowcharts:
The graph must use the LR (Left to Right) direction.
Each mermaid js node must have the following structure:
id:type:shape and text
    id - it is a unique identifier. Integer from 1 to n. Each node has a unique identifier
    type - defines the type of the element regarding to BPMN 2.0 notation.
        possible types are: start event, end event, task, exclusive gateway and parallel gateway.
        Based on the type of the node following shapes and texts are to be used:
        startevent: ((startevent))     i.e., id:startevent:((startevent))
        endevent: ((endevent))	     i.e., id:endevent:((endevent))
        task: (task label)             i.e., id:task:(task label)
        exclusivegateway: {x}          i.e., id:exclusivegateway:{x}
        parallelgateway: {AND}         i.e., id:exclusivegateway:{AND}

All nodes that have occurred more than once should have following structure: id:type: (i.e., 2:task: ) by further occurrence.
It is strictly prohibited to use only id (i.e. 2) as a reference.

    all elements are connected with each other with the help of the direction.
        direction: -->
    if there are some conditions or annotations it is necessary to use text on links (i.e., edge labels)
        edge label: |condition or annotation|
    edge label is always located between 2 nodes: id:exclusivegateway:{x} --> |condition or annotation|id:task:(task label)
"""

graphviz = """
Graphviz rules:
Each graph must have LR (Left to Right) direction and consists of nodes and edges.
Each node has following structure: "name"[attributes]
There are 5 diferent types of nodes: start event, end event, task, exclusive gateway and parallel gateway.
Each node has its specific attributes based on the type of the node.
  start node:        "start_1"[shape=circle label=""];
  end node:          "end_1"[shape=doublecircle label=""];
In both start and end nodes labels are always empty.
  task:              "task label"[shape=rectangle];
Task labels are always unique.
  exclusive gateway: "seg_1"[shape=diamond label="X"];
  parallel gateway:  "spg_1"[shape=diamond label="AND"];

Gateways are not tasks, they just indicate that the control flow of the process is splitted or merged.
Following names "seg_1" and "meg_1" should be used for splitting and merging exclusive gateways.
Following names "spg_1" and "mpg_1" should be used for splitting and merging parallel gateways.

Each time when new start, end or gateways node is used, the counter should be incrimented at 1.

all elements are connected with each other with the help of the edges.
  edge: ->
examples:
"start" -> "task 1"
"task 1" -> "task 2"

if there are some conditions or annotations it is necessary to use text on links (i.e., edge labels)
    edge label:  "task 1" -> "task 2"[label="condition 1"]
"""

