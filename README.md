# ChatGPT_Text_Feeder

Feed a text file to ChatGPT. Before discussing with ChatGPT, let it read a background document first.

## Run local

```
streamlit run streamlit_run.py
```

## Run online

Should be: https://goldengrape-chatgpt-text-feeder-streamlit-run-rksucb.streamlit.app/

However, uc.Chrome doesn't look like it will work on the web. I don't know what's going on.

## Known Issues

1. very slow
2. There is a possibility of http 429 error, which is more likely to occur if the text is longer.
3. ChatGPT has limited memory. It is known that there is a 24KB long patent, and after feeding ChatGPT completely and asking who the inventor is, it has forgotten it.

## Acknowledgements

From acheong08's [Reverse engineering ChatGPT API](https://github.com/acheong08/ChatGPT)
