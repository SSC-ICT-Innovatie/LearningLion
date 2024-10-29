import re

class Preprocessor:
  
  def run_preprocessing(self, text:str, functions: list) -> str:
      """
      Run all preprocessing functions on the text.
      """
      for function in functions:
          text = function(text)
      return text

  def merge_hyphenated_words(self, text: str) -> str:
      """
      Merge words in the text that have been split with a hyphen.
      """
      return re.sub(r"(\w)-\n(\w)", r"\1\2", text)

  def fix_newlines(self, text: str) -> str:
      """
      Replace single newline characters in the text with spaces.
      """
      return re.sub(r"(?<!\n)\n(?!\n)", " ", text)

  def remove_multiple_newlines(self, text: str) -> str:
      """
      Reduce multiple newline characters in the text to a single newline.
      """
      return re.sub(r"\n{2,}", "\n", text)
    
  def get_question_and_answer(self, text):
          footnotes = self.extract_footnotes(text)
          footer = self.get_footer(text)
          pages = self.get_amount_of_pages(text,footer)
          text = self.remove_footer_and_pagenumbers(text,footer,pages)
          docspecs = self.get_doc_specs(text)
          text = text.replace(docspecs, "")
          text = self.normalize_whitespace(text)
          question_pattern = r"(Vraag\s\d+.*?)(?=\s*Antwoord)"
          answer_pattern = r"(Antwoord\s\d+.*?)(?=Vraag|\Z)"

          questions = re.findall(question_pattern, text, re.DOTALL)
          answers = re.findall(answer_pattern, text, re.DOTALL)

          questions = [q.strip() for q in questions]
          answers = [a.strip() for a in answers]

          # Remove footnotes from returns
          questions = [self.remove_footnotes(q, footnotes) for q in questions]
          answers = [self.remove_footnotes(a, footnotes) for a in answers]

          questions = [self.normalize_whitespace(q) for q in questions]
          answers = [self.normalize_whitespace(a) for a in answers]

          return [questions, answers]
        
  def get_context(self,text):
      # Pattern to find the first multi-digit number (1 or more digits) and everything up to the first question
      pattern = re.compile(r'(\d+)\s*(.*?)(Vraag \d+)', re.DOTALL)
      
      match = pattern.search(text)
      
      if match:
          # Return the text between the number and the first question
          return match.group(2).strip()
      else:
          return None
        
  def remove_footnotes(self, text, footnotes):
      for footnote in footnotes:
          text = text.replace(footnote, "")
      return text.strip()

  def get_amount_of_pages(self, text, footer):
      return text.find(footer)

  def remove_footer(self, text, footer):
      if footer is not None:
          text = text.replace(footer, "")
          return text.strip()
      return text.strip()

  def remove_footer_and_pagenumbers(self, text,footer, amountpages):
      textLength = len(text)
      for number in range(amountpages):
          text = self.remove_footer(text, f"{footer} {str(number + 1)}")
      if(textLength == len(text)):
          for number in range(amountpages):
              text = self.remove_footer(text, footer)
      return text.strip()

  def get_doc_specs(self, text):
      pattern = r"(ah-tk-\d{8}-\d{3} ISSN\s*\d{4}\s*-\s*\d{4}\s*’s-Gravenhage\s*\d{4})"

      match = re.search(pattern, text)

      if match:
          return match.group(1)
      else:
          return "Desired identifiers not found."

  def normalize_whitespace(self, text):
      # Replace multiple spaces with a single space
      return re.sub(r'\s+', ' ', text).strip()

