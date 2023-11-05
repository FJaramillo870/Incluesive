from llm.together_llm import TogetherLLM
import llm.langchain_prompting as lp
from langchain import PromptTemplate, LLMChain

LLM = TogetherLLM(
    model="togethercomputer/llama-2-70b-chat",
    temperature=0.1,
    max_tokens=512
)

INSTRUCTIONS = ["a professional tone", "a personal tone", "an educational tone", "an instructional tone"]


class IncluesiveLLM:
    def __init__(self, user_text, instruction_choice=0):
        self.user_text = user_text
        self.instruction_choice = instruction_choice
        self.instruction = f"Rewrite the following text to be more inclusive while maintaining {INSTRUCTIONS[self.instruction_choice]}" + ":\n\n {text}"
        self.corrected_text = ""
        self.reasoning = ""
        self.template = lp.get_prompt(self.instruction)
        self.prompt = PromptTemplate(template=self.template, input_variables=["text"])
        self.llm_chain = LLMChain(llm=LLM, prompt=self.prompt)
        self.output = self.llm_chain.run(self.user_text).split("\n\n", 1)

    def get_corrections(self):
        return self.output[0]
    
    def get_reasoning(self):
        return self.output[1]
