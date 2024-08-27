

from models.langchain_memory_model import talk_to_me_with_langchain
from models.openai_with_file_backed_store import talk_to_me
from models.openai_with_pinecone_backed_store import talk_to_me_with_embeddings
from models.langchain_analyser import essential_analyser


# prompt = talk_to_me_with_embeddings("uploaded_files/fourth.m4a")


# talk_to_me_with_langchain()

# talk_to_me("uploaded_files/first.mp3")

essential_analyser("""
    { role: 'user', content: 'Hi, I want to transcribe this recording.' },
    {
        role: 'user',
        content: 'यह मुझे सेकंट प्रॉंट है। मुझे एक प्रॉंट के लिए कुछ कहा।'
    },
    {
        role: 'user',
        content: "Ok, my name is Tejas and I live in Bangalore. Tell me about today's weather."
    },
    {
        role: 'user',
        content: 'Do you remember my name and where I live?'
    },
    """)
