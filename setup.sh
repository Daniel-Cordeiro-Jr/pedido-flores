mdir -p ~/.streamlit/
mdir -p ~/.streamlit/config
mdir -p ~/.streamlit/data

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config/config.toml