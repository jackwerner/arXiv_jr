import arxiv
from openai import OpenAI
import streamlit as st

endpoint = "https://api.openai.com/v1/chat/completions" 
api_key = st.secrets['OPENAI_KEY']
model = "gpt-4-0125-preview"
openai = OpenAI(api_key=api_key)

st.markdown("""
    <div style="float: left">
        <h1>arXiv, Jr.</h1>
        <span>by Jack Werner</span>
    </div>       
    <br>
    <form action="https://www.paypal.com/donate" method="post" target="_top" style="float: right;">
    <input type="hidden" name="hosted_button_id" value="67TS3QGYAWLLA" />
    <input type="image" src="https://cdn-icons-png.flaticon.com/64/8728/8728158.png" border="0" name="submit" title="We are completely user funded!"/>
    </form>""", unsafe_allow_html=True)

st.divider()
st.write("\:speech_balloon: Click or search for a topic to view 5 recent arXiv publications in an easy-to-read language. Toggle URL Mode  to translate directly from an arXiv link. Please consider donating if you enjoy arXiv Jr! \:heart:")
search_value = ""
st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

with col1:
    if st.button('Physics'):
        search_value = "Physics"

with col2:
    if st.button('Mathematics'):
        search_value = "Mathematics"

with col3:
    if st.button('Computer Science'):
        search_value = "Computer Science"

with col4:
    if st.button('Biology'):
        search_value = "Biology"

with col5:
    if st.button('Finance'):
        search_value = "Finance"

with col6:
    if st.button('Statistics'):
        search_value = "Statistics"

with col7:
    if st.button('Engineering'):
        search_value = "Engineering"

with col8:
    if st.button('Economics'):
        search_value = "Economics"


def translate(summary):
    system_message = "You are a patient and effective professor who explains difficult topics with one clear and concise paragraph." 
    prompt = f"Please read the following academic paper and translate it to a one-paragraph summary that an intelligent eighth-grader could understand it. Here is the original:\n\n{summary}" #include input text here... reference any tools by name if used
    messages = [{"role": "system","content": system_message}, {"role": "user", "content": prompt}]
    stream = openai.chat.completions.create(model=model, temperature = .2, messages=messages, stream = True)
    st.write_stream(stream)

client = arxiv.Client()

activate = st.toggle("URL Mode")

if activate:
    print(activate)
    url = st.text_input(label="",placeholder='Paste an arXiv URL')
    input = url.split('/')[-1]
    input = input+"v1"
    search = arxiv.Search(id_list=[input])
else:
    search = arxiv.Search(
    query = st.text_input(label="",value=search_value,placeholder='Search for a subject'),
    max_results = 5,
    sort_by = arxiv.SortCriterion.SubmittedDate
    )

#enable multithreading    
results = client.results(search)
for r in client.results(search):
    st.subheader(f'{r.title}')
    translate(r.summary)
