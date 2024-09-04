from fastapi import APIRouter, HTTPException
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import List
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import ChatPromptTemplate


def create_slide_prompt() -> ChatPromptTemplate:
    # Join the list of strings into a single formatted string with bullet points
    
    
    prompt_text = (
        "You are a helpful assistant specializing in creating engaging slides given a topic.\n"
        "\n"
        "Create a presentation slide based on the following content:\n"
        "\n"
        "Title: {{topic}}\n"
        "\n"
        "Content:\n"
        "{{formatted_content}}\n"
        "\n"
        "Design specifications:\n"
        "- Professional and clean font style.\n"
        "- Simple layout with clear headings and bullet points.\n"
        "\n"
        "Please stick strictly to the provided topic and content. If you cannot generate the slide with the given information, respond with: 'Cannot create slide, need more data.'\n"
        "\n"
        "Format the output in a JSON template structure compatible with Reveal.js, using placeholders for the content:\n"
        "\n"
        "{{\n"
        '    "title": "<Replace with slide title>",\n'
        '    "content": [\n'
        '        {{\n'
        '            "heading": "<Replace with section heading>",\n'
        '            "bullet_points": [\n'
        '                "<Replace with first bullet point>",\n'
        '                "<Replace with second bullet point>",\n'
        '                "<Replace with third bullet point>"\n'
        '            ]\n'
        '        }},\n'
        '        {{\n'
        '            "heading": "<Replace with next section heading>",\n'
        '            "bullet_points": [\n'
        '                "<Replace with first bullet point in this section>",\n'
        '                "<Replace with second bullet point in this section>"\n'
        '            ]\n'
        '        }}\n'
        "    ]\n"
        "}}\n"
    )
    return prompt_text



# Initialize the router
router = APIRouter(
    prefix="/get-slide",
    tags=["content"],
    responses={404: {"description": "Not found"}},
)
llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # api_key="...",  # if you prefer to pass api key in directly instaed of using env vars
    # base_url="...",
    # organization="...",
    # other params...
)
# Pydantic model for request body
class ContentRequest(BaseModel):
    subtopic: str
    text_content: List[str]

# POST endpoint to process the content
@router.post("/")
async def get_llm_response(request: ContentRequest):
    try:
        # Call the dummy method with provided subtopic and text_content
        formatted_content = "\n".join(f"- {line}" for line in request.text_content)
        prompt_text=create_slide_prompt()
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_text)
                ,
                ("human", "content :{formatted_content} \n topic :{topic}"),
            ]
        )
        
        # This is just a placeholder for your actual logic
        chain = prompt | llm | StrOutputParser()
        json_result= chain.invoke({
            "formatted_content":formatted_content , "topic":request.subtopic
        })
        print(json_result)
        # Return some dummy response
        return json_result
         
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




 
  
