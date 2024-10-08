import chatollama


PROMPT_SUMMARIZE = """Summarize the provided text directly and succinctly without any introductions, acknowledgments, or references to the task or AI's role. Deliver the summary as a plain statement that captures the essence of the content, strictly adhering to the guidelines: 1 sentence for short texts, 2 sentences for medium texts, and up to 5 sentences for longer texts. Ensure that the response contains only the summarized text itself, without any surrounding comments, formatting, or contextual information about the summarization process. The summarization must always be equal to or shorter in length than the input text, focusing solely on the key points without elaboration or unnecessary detail. Do not respond to the text in anyway contextual way. Only simplify the text. Respond as if you are an expert in language and can compress and simplify text to always make it smaller in length than the original text. 
Examples:
1. Provided text: The tree is blue
   Response: The tree blue

2. Provided text: Today marks a tremendous day for love and peace, we finally signed the long awaited peace treaty
   Response: Today is a historic day for love and peace as the long-awaited peace treaty has finally been signed.

3. Provided text: What a wonderful day for fun!
   Response: It's a great fun day

Make sure to always provide smaller text than what was provided

"""

PROMPT_REPLICATE = """Replicate the structure, tone, and formatting of the first text input using the context and meaning of the second input. Keep the new text aligned in style with the first input while modifying the content to reflect the second input's context. Maintain technical or descriptive details, replacing elements contextually. Do not acknowledge the task or explain the process, just provide the generated text.

Examples:
1. Template: def crop_video(input_path: str, output_path: str, crop_width: int, crop_height: int) -> None:
Context: resize function
Response: def resize_video(input_path: str, output_path: str, resize_width: int, resize_height: int) -> None:

2. Template: The sky is a bright blue, it's like a million waves of bright cobalt.
Context: red sky
Response: The sky is a bright red, it's like a million flames of bright crimson.

3. Template: Calculate the area of a circle by multiplying pi with the square of the radius.
Context: Calculate the perimeter of a circle
Response: Calculate the perimeter of a circle by multiplying pi with twice the radius.
"""

PROMPT_COMPLETE = """Complete the provided text naturally and coherently without any introductions, acknowledgments, or references to the task or AI's role. The response must only contain the completed text itself, without any additional comments, formatting, or contextual information. The completion should feel like a continuation of the given input, preserving the style, tone, and structure. Do not respond with any information outside of the direct completion task. Only provide the completed text, ensuring the input is replaced or extended seamlessly.

Examples:
1. Provided text: The quick brown fox jumps over
   Response:  the lazy dog.

2. Provided text: In recent years, artificial intelligence has evolved to
   Response:  revolutionize industries, automate tasks, and enhance human decision-making.

3. Provided text: As I walked into the room, I noticed
   Response:  the soft glow of the candles and the faint scent of jasmine filling the air.
"""


class ChatTools:
    def __init__(self, model: str = "llama3.1:8b") -> None:
        self.engine = chatollama.ChatEngine(model)
        self.engine.callback = self._chat_callback

    def _chat_callback(self, mode, delta, text):
        return

    @property
    def model(self):
        return self.engine.model

    @model.setter
    def model(self, model: str):
        self.engine.model = model

    def summarize(self, text: str, *, guide_lines: str = ""):
        system = PROMPT_SUMMARIZE

        if guide_lines.strip() != "":
            system += f"Please follow these guide lines for summarization aswell:\n{
                guide_lines}"

        self.engine.messages = chatollama.ChatMessages()
        self.engine.messages.system(system)
        self.engine.messages.user(text)
        self.engine.chat()
        self.engine.wait()
        return self.engine.response

    def replicate(self, template_text: str, context_text: str, *, guide_lines: str = ""):
        system = PROMPT_REPLICATE

        if guide_lines.strip() != "":
            system += f"Please follow these guide lines for replication aswell:\n{
                guide_lines}"

        self.engine.messages = chatollama.ChatMessages()
        self.engine.messages.system(system)
        self.engine.messages.user(
            f"Template: {template_text}\nContext: {context_text}")
        self.engine.chat()
        self.engine.wait()
        return self.engine.response

    def complete(self, text: str, *, guide_lines: str = ""):
        system = PROMPT_COMPLETE

        if guide_lines.strip() != "":
            system += f"Please follow these guide lines for completion aswell:\n{
                guide_lines}"

        self.engine.messages = chatollama.ChatMessages()
        self.engine.messages.system(system)
        self.engine.messages.user(text)
        self.engine.chat()
        self.engine.wait()
        # Replace the input text with an empty string to ensure it's not mistakenly included in the response.
        response = self.engine.response.replace(text, "")
        return response

    def task(self, text: str, *, guide_lines: str = ""):
        system = ""

        if guide_lines.strip() != "":
            system += f"Please follow these guide lines:\n{
                guide_lines}"

        self.engine.messages = chatollama.ChatMessages()
        self.engine.messages.system(system)
        self.engine.messages.user(text)
        self.engine.chat()
        self.engine.wait()
        return self.engine.response
