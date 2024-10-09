# jqgpt

jqgpt is a gpt powered tool that helps you write jq queries. It takes a human user query and a json file as input and outputs a jq query that answers the user query.

It accomplishes this by sending a very helpful jq prompt with tons of examples and a sample from the json file to the model.

You can install this using

```
pip install jqgpt
```

Examples:

```
$ jqgpt 'Get the total number of clams of type dolphin' seaCreatures.json

jq 'map(select(.type == "dolphin").clams) | add' seaCreatures.json
```

```
$ cat seaCreatures.json | jqgpt 'Get the names of sea creatures'

jq -r '.[] | .name' seaCreatures.json
```
