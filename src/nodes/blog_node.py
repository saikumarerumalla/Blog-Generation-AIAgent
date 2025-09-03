from src.states.blogstate import BlogState



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
                   a blog title for the {topic}. This title should be creative and SEO friendly and Short.
                   """
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog":{"title":response.content}}
        
    def content_generation(self, state:BlogState):
        """Generates blog content based on the given title and topic."""
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog":{"title": state['blog']['title'], "content":response.content}}
          