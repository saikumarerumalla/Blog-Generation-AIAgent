from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """A class representing a blog node with a title and content.
    """
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state:BlogState):
        """Generates a blog title based on the given topic."""
        if "topic" in state and state["topic"]:
            prompt="""
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog title for the {topic}. This title should be creative and SEO friendly and Short to around 2 sentences.
                   """
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog":{"title":response.content}}
        
    def content_generation(self, state:BlogState):
        """Generates blog content based on the given title and topic."""
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed and explanatory blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog":{"title": state['blog']['title'], "content":response.content}}
        

    def translation(self, state:BlogState):
        """Translates the blog content to the specified Language."""

        translation_prompt = """
        You are an expert translator. Translate the following blog content to {current_language}.
        Maintain the original meaning and tone. Adapt cultural references and idioms to be appropriate for {current_language}.

        ORIGINAL CONTENT:
        {blog_content}
        """

        blog_content= state['blog']['content']
        messages = [
            HumanMessage(translation_prompt.format(current_language=state['current_language'], blog_content=blog_content))
        ]

        translated_content = self.llm.with_structured_output(Blog).invoke(messages)
        return {"blog":{"title": state['blog']['title'], "content":translated_content.content}}

    def route(self, state:BlogState):
        return {"current_language": state["current_language"]}
    
    def route_decision(self, state:BlogState):
        """Route the content to the respective language translation."""
        if state["current_language"]=="Hindi":
            return "hindi"
        elif state["current_language"]=="French":
            return "french"
        elif state["current_language"]=="Telugu":
            return "telugu"
        else:
            return state["current_language"]
