text = """
You are now an expert in the GIS field and an AI assistant. 
Answer the following questions as best you can. 
You have access to the following tools:
[
    {
        "name": "buffer",
        "description": "Get a buffer",
        "inputs": {
            "datafile": "Data file requiring a buffer",
            "radius": "Buffer radius"
        },
        "output": "Buffer result file"
    },
    {
        "name": "slope",
        "description": "Calculate slope based on terrain data",
        "inputs": {
            "tiffile": "Raster terrain TIFF file"
        },
        "output": "Raster TIFF file with slope calculation results"
    },
    {
        "name": "area",
        "description": "Calculate area",
        "inputs": {
            "datafile": "Data file requiring area calculation"
        },
        "output": "Area calculation result"
    },
    {
        "name": "overlay",
        "description": "Overlay analysis",
        "inputs": {
            "datafile1": "Data file 1",
            "datafile2": "Data file 2"
        },
        "output": "Overlay analysis result file"
    },
    {
        "name": "extractByValues",
        "description": "Extract raster data based on given minimum and maximum values",
        "inputs": {
            "tiffile": "Raster TIFF file to be extracted",
            "min": "Minimum value",
            "max": "Maximum value"
        },
        "output": "Extracted raster TIFF file"
    }
]

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of  upper tool names, using the following json format.
{
	name: used tool name,
	inputs:{
		used inputs file or value
	},
	output: output file or value
}
Observation: the result of the action, same as the output of the tool
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Please only provide the Thought, Action and Observation of the next step with selecting one tool, do not provide subsequent steps.
Question: To construct a railway with a width of 30 meters, calculate the area of farmland that has slopes of less than 15 degrees in the vicinity. The railway data is in 'railway.shp,' the farmland data is in 'farmland.shp,' and the terrain data is in 'terrain.tif. 

Thought: 
"""
# Based on the following task instruction, think comprehensively and reason, and output the tool invocation in JSON format, with the JSON content enclosed in [].

# INSTRUCTION: Construct a railway with a width of 30 meters and calculate the area of farmland with slopes less than 15 degrees in the vicinity. The railway data is 'railway.shp,' the farmland data is 'farmland.shp,' and the terrain data is 'terrain.tif.'

# import llm.gpt4 as gpt4
# gpt_key = 'sk-ohe7INluTagKkdGRXP2QGs14n0rhL7sKs5BMEJT41e0Ezwzm'
# myllm = gpt4.GPT4()
# myllm.set_api_key(gpt_key)

# import llm.gpt3_5 as gpt3_5
# gpt_key = 'sk-ohe7INluTagKkdGRXP2QGs14n0rhL7sKs5BMEJT41e0Ezwzm'
# myllm = gpt3_5.GPT3_5()
# myllm.set_api_key(gpt_key)

import llm.text2sql as text2sql
text2sql_key = "=="
myllm = text2sql.Text2SQL()
myllm.set_api_key(text2sql_key)


result = myllm.invoke(text)
print(result)