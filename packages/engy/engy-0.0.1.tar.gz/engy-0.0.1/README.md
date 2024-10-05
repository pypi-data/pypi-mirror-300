# engy

## Basics

Install
```
pip install -e .
```

Generate new app.
```
mkdir xxx && cd xxx
edit input.txt
engy
```

Add featrue
```
edit feature.txt
engy feature
```

Only edit front-end (promprt from input in terminal)
```
engy frontend
```

Only edit back-end (promprt from input in terminal)
```
engy frontend
```

Clone new app based on existng one.
```
mkdir yyy && cd yyy
edit input.txt
engy clone /path/to/xxx
```

## Owner Tasks

1. (P1.5) merge everything into a config.yaml. different sections contain initial prompt, features, bugs. have a separate state.yaml which is the current generated state. diff between config.yaml and state.yaml to figure out what to change
2. (P1) doc add quick start, tutorials, examples, commandline usage
3. (P2) optionally generate dockerfile
4. (P2) optionally generate a doc page for the backend?
5. (P1.5) generate README.md along side for each app.
6. (P2) optionally tech explain: agentic workflow
7. (P2) switch LLM back-end, user API key. (i.e. .env)

