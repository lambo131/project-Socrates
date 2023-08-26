from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document

class ContentGenerator:

    def __init__(self):
        openai_api_key = "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"
        self.llm = OpenAI(temperature = 0.7, model_name="gpt-3.5-turbo",openai_api_key=openai_api_key)
        self.main_ideas_chain = self.get_main_ideas_chain()
        self.summary_chain = self.get_short_summary_chain()
        self.explore_chain = self.get_explore_chain()
        self.critical_chain = self.get_critical_chain()

    # interface methods

    def get_main_ideas(self, docs) -> List[str]:
        # input: docs
        # output: List[str] (main_ideas)
        main_ideas = self.main_ideas_chain.predict_and_parse(text=docs)
        main_ideas_list = []
        for i in main_ideas.content:
            main_ideas_list.append(i)
        return main_ideas_list
    
    def get_short_summary(self, main_ideas):
        # input: list of strs (main_ideas)
        # output: str (short summary)
        main_ideas_docs = []
        for i in main_ideas:
            main_ideas_docs.append(Document(page_content=i, metadata={"source": "user given document"}))
        short_summary = self.summary_chain.predict(main_ideas=main_ideas_docs)
        return short_summary
    
    def get_explore_questions(self, short_summary, statement):
        # input: short_summary, statement
        # output: List[str] (explore questions)
        explore_questions = self.explore_chain.predict_and_parse(
            summary=short_summary,
            statement=statement)
        explore_questions_list = []
        for i in explore_questions.content:
            explore_questions_list.append(i)
        return explore_questions_list

    def get_critical_questions(self, short_summary):
        # input: short_summary
        # output: List[str] (critical questions)

        challenge_question = self.critical_chain.predict_and_parse(summary=short_summary)
        challenge_question_list = []
        for i in challenge_question.content:
            challenge_question_list.append(i)
        return challenge_question_list

#--------------------------------------------------------------
    # __init__ functions

    def get_main_ideas_chain(self):
        # usage: main_ideas = main_ideas_chain.predict_and_parse(text=docs)
        parser = PydanticOutputParser(pydantic_object=ListOfStrings)
        prompt_template = PromptTemplate(
            input_variables=["text"], 
            template=template_1_2,
            partial_variables={"format_instructions": parser.get_format_instructions()},
            output_parser=parser
        )
        chain = LLMChain(llm=self.llm, prompt=prompt_template, output_key="main_ideas")
        return chain
    
    def get_short_summary_chain(self):
        # usage: short_summary = summary_chain.predict(main_ideas=main_ideas_docs)
        prompt_template = PromptTemplate(
            input_variables=["main_ideas"], 
            template=template_2,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt_template, output_key="short_summary")
        return chain
    
    def get_explore_chain(self):
        '''
        usage:
            explore_questions = explore_chain.predict_and_parse(
                summary=short_summary,
                main_idea=main_ideas_docs[0])
        '''
        parser = PydanticOutputParser(pydantic_object=ListOfStrings)
        prompt_template = PromptTemplate(
        input_variables=["summary", "statement"], 
        template=template_3b,
        partial_variables={"format_instructions": parser.get_format_instructions()},
        output_parser=parser
        )
        chain = LLMChain(llm=self.llm, prompt=prompt_template, output_key="explore questions")
        return chain
    
    def get_critical_chain(self):
        '''
        usage:
            challenge_question = challenge_question_chain.predict_and_parse(summary=short_summary)
        '''
        parser = PydanticOutputParser(pydantic_object=ListOfStrings)
        prompt_template = PromptTemplate(
            input_variables=["summary"], 
            template=template_4b,
            partial_variables={"format_instructions": parser.get_format_instructions()},
            output_parser=parser
        )
        chain = LLMChain(
            llm=self.llm, prompt=prompt_template, output_key="challenge questions"
        )
        return chain
    

# prompt template
template_1="""
You a professional reader. You understand reading material clearly and help people understand a reading material by providing great summaries. You are given this article:
article: {article}
{format_instructions}
task: Generate a list of single sentence summary of the main ideas based on the article. Include all important points.
"""
template_1_2="""
Write a very clear and detailed summary for the article below in point form.
article: {text}
{format_instructions}
"""
template_2="""
Summarize the following information in one paragraph. Include all information
{main_ideas}
your summary:
"""
template_3="""
base on the following text, generate five meaningful question to further explore the topic.
text: {main_ideas}
{format_instructions}
"""
template_3b="""
Based on the background information provided, generate 5 meaningful questions
for the following statement.
background information: {summary}
statement: {statement}
Again, your task is to based on the background information provided, generate 5 meaningful questions
for the following statement.
{format_instructions}
"""
template_4_1="""
Pretend you are Socrates, discussing a topic with your student. You are asked to think about a statement or point
regarding the topic.
topic: {summary}
Statement: {statement}
{format_instructions}
task: Generate a list of questions that challenges the legitimacy of the statement or point.
"""
template_4b="""
Pretend you are Socrates and ask as many questions that challenges the legitimacy of the following text
summary: "{summary}"
{format_instructions}
"""


# Pydantic class for output parsing
class ListOfStrings(BaseModel):
    content: List[str] = Field(description="a list of strings")