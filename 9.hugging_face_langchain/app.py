import validators
import streamlit as st
from langchain_classic.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader


st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader("Summarize URL")


## Get the HuggingFace API and url(YT or website) to be summarized
with st.sidebar:
    hf_api_key=st.text_input("HuggingFace API Key",value="",type="password")
generic_url=st.text_input("URL", label_visibility="collapsed")

repo_id="google/gemma-2-9b"
llm=HuggingFaceEndpoint(repo_id=repo_id,max_new_tokens=150,temperature=0.7,huggingfacehub_api_token=hf_api_key)

prompt_template="""
Provide a summary of the following content in 300 words:
content:{text}
"""
prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

if st.button("Summarize the Content from YT or Website"):
    if not hf_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid url. It can maybe a YT video url or website url")
    else:
        try:
            with st.spinner("Waiting..."):
                ## Loading website or YT video data
                if 'youtube.com' in generic_url:
                    loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=False)
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                docs=loader.load()
                ## Chain for summarization
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)
                st.success(output_summary)
        except Exception as e:
            st.exception(e)