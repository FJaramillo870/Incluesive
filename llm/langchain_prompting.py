import textwrap

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = """You are an advanced assistant that excels at rewriting text to be more inclusive while maintaining the intended tone of the text. If text contains any sexist, racist, ableist, homophobic, or otherwise non-inclusive language, you re-write it to be inclusive to all people. If you think the text is already inclusive, then just say there's nothing to change."""


def get_prompt(instruction, new_system_prompt=DEFAULT_SYSTEM_PROMPT):
    SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
    prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
    return prompt_template

def cut_off_text(text, prompt):
    cutoff_phrase = prompt
    index = text.find(cutoff_phrase)
    if index != -1:
        return text[:index]
    else:
        return text
    
def remove_substring(string, substring):
    return string.replace(substring, "")

def parse_text(text):
    wrapped_text = textwrap.fill(text, width=100)
    print(wrapped_text + "\n\n")
    # return assistant_text
