import streamlit as st
import openai
import pandas as pd
import json

# Get API user keys from sidebar called OpenAI API Keys
user_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

client = openai.OpenAI(api_key=user_api_key)
prompt = """ You are an expert German-English translator. You will be given a German passage.
        Select some interesting german vocabulary in A2 level or upper that appear in the text.
        Definite article in the text will not be choosen as vocabulary.
        List the vocabulary in a JSON array, one vocabulary per line.
        If it's a noun, indicate its definite article, which are "der", "die", or "das" in front of the word.
        Each line should contains 3 fields of information:
            - "Words" -- the vocabulary
             -- If it is a verb or adjective, write in its infinitive form. 
            - "Part of Speech" -- noun, verb, adjective, adverb, or conjunction. write in lower case.
            - "Meaning" -- meaning in english
            (Sort the vocabulary in order of difficulty.)
        """
prompt_sum = """ Act as an expert German-English translator. You will be given a German text. 
            Summerize that text or each paragraph in English no more than 5 sentences.
            Use simple words and short sentences. 
            """

st.title('🇩🇪 _German Text Guru_')
st.markdown(':grey[To improve your German vocabulary, we will provide you the meaning of each word and its part of speech from your text.]')
st.subheader(':rainbow[_Deutsch_ macht Spaß!]🍻😎', divider='rainbow')

# Get user input in a text box
user_input = st.text_area("Enter German text.", height=150, value='German text here...')
if not user_input:
    st.warning('You have not enter any German text...🥺')

# check box if the user wants the summerized text in english
summerize = st.checkbox('Summerize the text in English', value=False)
if summerize:
    st.write(':grey[*We will do our best to help you better understand the text!*]')


#submit button 
if st.button('Submit', type='primary'):
    messages_so_far = [
        {'role': 'system', 'content': prompt},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_so_far
    )
    if summerize:
        messages_sum = [
            {'role': 'system', 'content': prompt_sum},
            {'role': 'user', 'content': user_input},
        ]
        response_sum = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_sum
        )
        st.markdown('Summerized text in English:')
        container = st.container(border=True)
        container.write(response_sum.choices[0].message.content)

    # create a table with 3 columns: words, part of speech, meaning
    st.markdown('German Vocabulary:')
    vocab_results = response.choices[0].message.content
    vocab = json.loads(vocab_results)
    vocab_table = pd.DataFrame.from_dict(vocab)
    st.table(vocab_table)