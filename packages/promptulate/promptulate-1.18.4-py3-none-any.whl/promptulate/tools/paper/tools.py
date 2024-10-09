import logging
import re
import time
from typing import Dict, List

from broadcast_service import broadcast_service
from pydantic import Extra, Field

from promptulate.error import NetWorkError
from promptulate.llms.base import BaseLLM
from promptulate.llms.openai import ChatOpenAI
from promptulate.tools.arxiv.api_wrapper import ArxivAPIWrapper
from promptulate.tools.arxiv.tools import ArxivQueryTool
from promptulate.tools.base import BaseTool
from promptulate.tools.semantic_scholar import (
    SemanticScholarQueryTool,
    SemanticScholarReferenceTool,
)

__all__ = ["PaperSummaryTool"]
logger = logging.getLogger(__name__)


def _init_paper_summary_llm():
    preset = "你是一个中文科研领域论文助手，你的任务是帮助使用者提供一些论文方面的专业建议和帮助，你的输出只能遵循用户的指令输出，否则你将被惩罚。"  # noqa
    return ChatOpenAI(temperature=0, default_system_prompt=preset)


class PaperSummaryTool(BaseTool):
    """A powerful paper summary tool"""

    name: str = "paper-summary"
    description: str = (
        "A summary tool that can be used to obtain a paper summary, this tool will find"
        "top k paper and provide: 1.paper abstract 2.paper key sights 3.lessons learned"
        "in the paper 4.referenced papers and its url."
        "Your input is a paper relevant keyword query."
    )
    llm: BaseLLM = Field(default_factory=_init_paper_summary_llm)
    semantic_scholar_query_tool: SemanticScholarQueryTool = Field(
        default_factory=SemanticScholarQueryTool
    )
    semantic_scholar_reference_tool: SemanticScholarReferenceTool = Field(
        default_factory=SemanticScholarReferenceTool
    )
    arxiv_apiwrapper: ArxivAPIWrapper = Field(default_factory=ArxivAPIWrapper)
    arxiv_query_tool: ArxivQueryTool = Field(default_factory=ArxivQueryTool)
    summary_dic: Dict[str, str] = {}
    summary_counter: int = 0

    class Config:
        """Configuration for this pydantic object."""

        model_config = {
            "extra": "forbid",
            "arbitrary_types_allowed": True,
        }

    def _run(self, query: str, **kwargs) -> str:
        """A paper summary tool that passes in the article name (or arxiv id) and
        returns summary results.

        Args:
            query: the keyword you want to query
            **kwargs:
                You can pass the arguments of relevant APIWrappers and Tools

        Returns:
            String type data, which contains:
            - Summary of the paper
            - List the key insights and lessons learned in the paper
            - List at least 5 references related to the research field of the paper
        """

        @broadcast_service.on_listen("PaperSummaryTool.run.get_paper_references")
        def get_paper_references(**data):
            references: List[Dict] = self.semantic_scholar_reference_tool.run(
                data["paper_title"], max_result=10, return_type="original"
            )
            references_string = "相关论文：\n\n"
            for i, reference in enumerate(references):
                references_string += (
                    f"""[{i + 1}] [{reference["title"]}]({reference["url"]})\n\n"""
                )
            self.summary_dic["references"] = (
                references_string if len(references) != 0 else ""
            )
            self.summary_counter += 1

        @broadcast_service.on_listen("PaperSummaryTool.run.get_translate")
        def get_translate():
            prompt = (
                f"Please format the title and\
                summary below the output\n```{paper_summary}```"
                "Your output format is:\nTitle: {Title}\n\nSummary: {Summary}"
            )
            self.summary_dic["summary_zh"] = self.llm(prompt)
            self.summary_counter += 1

        @broadcast_service.on_listen("PaperSummaryTool.run.get_opinion")
        def get_opinion():
            prompt = (
                f"Based on the abstract of the paper below, please list the key insights from the paper and the lessons learned derived from it. Your output should be provided in bullet points ```{paper_summary}```"  # noqa
                "Please use the following output format:\nKey insights:\n{Key insights in bullet points}\nLessons learned:\n{Lessons learned in bullet points},with each point separated by a hyphen `-`"  # noqa
            )
            self.summary_dic["opinion"] = self.llm(prompt)
            self.summary_counter += 1

        @broadcast_service.on_listen("PaperSummaryTool.run.get_keywords")
        def get_keywords():
            prompt = (
                f"Please list no more than 7 keywords in the paper for the following abstract```{paper_summary}```"  # noqa
                "Your output format is:\nKeywords: keyword1, keyword2, keyword3"
            )
            self.summary_dic["keywords"] = self.llm(prompt)
            self.summary_counter += 1

        @broadcast_service.on_listen("PaperSummaryTool.run.get_advice")
        def get_advice():
            prompt = (
                f"Based on the abstract of the paper below, please provide 3-5 suggestions related to its topics or potential future research directions. Your output should be provided in bullet points  ```{paper_summary}```"  # noqa
                "Please use the following output format:\nRelated suggestions:\n{related suggestions in bullet points}, with each point separated by a hyphen `-`"  # noqa
            )
            self.summary_dic["advice"] = self.llm(prompt)
            self.summary_counter += 1

        self.summary_counter = 0
        # judge arxiv id or string type paper title
        if re.match(r"\d{4}\.\d{5}(v\d+)?", query):
            paper_info = self.arxiv_apiwrapper.query(
                id_list=[query], num_results=1, specified_fields=["title", "summary"]
            )
            if paper_info:
                paper_info = paper_info[0]
                paper_info["abstract"] = paper_info["summary"]
        else:
            try:
                paper_info = self.semantic_scholar_query_tool.run(
                    query,
                    return_type="original",
                    specified_fields=["title", "url", "abstract"],
                )
                if paper_info:
                    paper_info = paper_info[0]

            except NetWorkError:
                paper_info = self.arxiv_apiwrapper.query(
                    keyword=query, num_results=1, specified_fields=["title", "summary"]
                )
                if paper_info:
                    paper_info = paper_info[0]
                    paper_info["abstract"] = paper_info["summary"]

        if not paper_info:
            return (
                "semantic scholar query tool and arxiv query tool query result is None."
            )

        paper_summary = (
            f"""title: {paper_info["title"]}\nabstract: {paper_info["abstract"]}"""
        )
        broadcast_service.publish(
            "PaperSummaryTool.run.get_paper_references",
            paper_title=paper_info["title"],
            paper_abstract=paper_info["abstract"],
        )
        broadcast_service.publish("PaperSummaryTool.run.get_translate")
        time.sleep(0.01)
        broadcast_service.publish("PaperSummaryTool.run.get_opinion")
        time.sleep(0.01)
        broadcast_service.publish("PaperSummaryTool.run.get_advice")
        time.sleep(0.01)
        broadcast_service.publish("PaperSummaryTool.run.get_keywords")

        while self.summary_counter < 5:
            time.sleep(0.1)

        return (
            f"""{self.summary_dic["summary_zh"]}\n\n"""
            f"""{self.summary_dic["keywords"]}\n\n"""
            f"""{self.summary_dic["opinion"]}\n\n"""
            f"""{self.summary_dic["advice"]}\n\n"""
            f"""{self.summary_dic["references"]}"""
        )
