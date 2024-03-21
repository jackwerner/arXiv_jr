import arxiv
from openai import OpenAI
import streamlit as st

endpoint = "https://api.openai.com/v1/chat/completions" 
api_key = st.secrets['OPENAI_KEY']  
model = "gpt-4-1106-preview"
openai = OpenAI(api_key=api_key)

st.title('arXiv, Jr.')
st.write('by Jack Werner')

def translate(summary):
    system_message = "You are a patient and effective professor who explains difficult topics with one clear and concise paragraph." 
    prompt = f"Please read the following academic paper and translate it to a one-paragraph summary that an intelligent eighth-grader could understand it. Here is the original:\n\n{summary}" #include input text here... reference any tools by name if used
    messages = [{"role": "system","content": system_message}, {"role": "user", "content": prompt}]
    response = openai.chat.completions.create(model=model, temperature = .2, messages=messages)
    response_message = response.choices[0].message.content 
    return response_message

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
    query = st.text_input(label="",placeholder='Search for a subject'),
    max_results = 5,
    sort_by = arxiv.SortCriterion.SubmittedDate
    )
    
results = client.results(search)
for r in client.results(search):
    st.subheader(f'{r.title}')
    st.write(f"{translate(r.summary)}")
