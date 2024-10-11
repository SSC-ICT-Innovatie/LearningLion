# This file is inspired by Langchains documents, and contains content from the files:
# langchain/chains/base.py and langchain/chains/conversational_retrieval/base.py.
# On langchain version==0.1.0. This custom file was necessary, to make it possible to
# intercept the retrieved documents, by manipulating the output. In this case, it
# makes it possible to give your own documents as input to the language model.
# You will be able to see the edited code at the functions: `invoke`` and `_call`.
#
# All credits to the original authors of the Langchain library.

"""Base interface that all chains should implement."""
from __future__ import annotations

import inspect
import json
import logging
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union, cast

import yaml
from langchain_core._api import deprecated
from langchain_core.documents import Document
from langchain_core.language_models import BaseLanguageModel
from langchain_core.load.dump import dumpd
from langchain_core.memory import BaseMemory
from langchain_core.messages import BaseMessage
from langchain_core.outputs import RunInfo
from langchain_core.prompts import BasePromptTemplate
from langchain_core.pydantic_v1 import (
    BaseModel,
    Extra,
    Field,
    create_model,
    root_validator,
    validator,
)
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import (
    RunnableConfig,
    RunnableSerializable,
    ensure_config,
    run_in_executor,
)
from langchain_core.vectorstores import VectorStore

from langchain.callbacks.base import BaseCallbackManager
from langchain.callbacks.manager import (
    AsyncCallbackManager,
    AsyncCallbackManagerForChainRun,
    CallbackManager,
    CallbackManagerForChainRun,
    Callbacks,
)
from langchain.schema import RUN_KEY
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain


logger = logging.getLogger(__name__)


def _get_verbosity() -> bool:
    from langchain.globals import get_verbose

    return get_verbose()


class Chain(RunnableSerializable[Dict[str, Any], Dict[str, Any]], ABC):
    """Abstract base class for creating structured sequences of calls to components.

    Chains should be used to encode a sequence of calls to components like
    models, document retrievers, other chains, etc., and provide a simple interface
    to this sequence.

    The Chain interface makes it easy to create apps that are:
        - Stateful: add Memory to any Chain to give it state,
        - Observable: pass Callbacks to a Chain to execute additional functionality,
            like logging, outside the main sequence of component calls,
        - Composable: the Chain API is flexible enough that it is easy to combine
            Chains with other components, including other Chains.

    The main methods exposed by chains are:
        - `__call__`: Chains are callable. The `__call__` method is the primary way to
            execute a Chain. This takes inputs as a dictionary and returns a
            dictionary output.
        - `run`: A convenience method that takes inputs as args/kwargs and returns the
            output as a string or object. This method can only be used for a subset of
            chains and cannot return as rich of an output as `__call__`.
    """

    memory: Optional[BaseMemory] = None
    """Optional memory object. Defaults to None.
    Memory is a class that gets called at the start
    and at the end of every chain. At the start, memory loads variables and passes
    them along in the chain. At the end, it saves any returned variables.
    There are many different types of memory - please see memory docs
    for the full catalog."""
    callbacks: Callbacks = Field(default=None, exclude=True)
    """Optional list of callback handlers (or callback manager). Defaults to None.
    Callback handlers are called throughout the lifecycle of a call to a chain,
    starting with on_chain_start, ending with on_chain_end or on_chain_error.
    Each custom chain can optionally call additional callback methods, see Callback docs
    for full details."""
    verbose: bool = Field(default_factory=_get_verbosity)
    """Whether or not run in verbose mode. In verbose mode, some intermediate logs
    will be printed to the console. Defaults to the global `verbose` value,
    accessible via `langchain.globals.get_verbose()`."""
    tags: Optional[List[str]] = None
    """Optional list of tags associated with the chain. Defaults to None.
    These tags will be associated with each call to this chain,
    and passed as arguments to the handlers defined in `callbacks`.
    You can use these to eg identify a specific instance of a chain with its use case.
    """
    metadata: Optional[Dict[str, Any]] = None
    """Optional metadata associated with the chain. Defaults to None.
    This metadata will be associated with each call to this chain,
    and passed as arguments to the handlers defined in `callbacks`.
    You can use these to eg identify a specific instance of a chain with its use case.
    """
    callback_manager: Optional[BaseCallbackManager] = Field(default=None, exclude=True)
    """[DEPRECATED] Use `callbacks` instead."""

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def get_input_schema(
        self, config: Optional[RunnableConfig] = None
    ) -> Type[BaseModel]:
        # This is correct, but pydantic typings/mypy don't think so.
        return create_model(  # type: ignore[call-overload]
            "ChainInput", **{k: (Any, None) for k in self.input_keys}
        )

    def get_output_schema(
        self, config: Optional[RunnableConfig] = None
    ) -> Type[BaseModel]:
        # This is correct, but pydantic typings/mypy don't think so.
        return create_model(  # type: ignore[call-overload]
            "ChainOutput", **{k: (Any, None) for k in self.output_keys}
        )

    def invoke(
        self,
        input: Dict[str, Any],
        config: Optional[RunnableConfig] = None,
        custom_documents: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        config = ensure_config(config)
        callbacks = config.get("callbacks")
        tags = config.get("tags")
        metadata = config.get("metadata")
        run_name = config.get("run_name")
        include_run_info = kwargs.get("include_run_info", False)
        return_only_outputs = kwargs.get("return_only_outputs", False)

        if custom_documents is not None:
            custom_documents = [tup[0] for tup in custom_documents]
        inputs = self.prep_inputs(input)
        callback_manager = CallbackManager.configure(
            callbacks,
            self.callbacks,
            self.verbose,
            tags,
            self.tags,
            metadata,
            self.metadata,
        )
        new_arg_supported = inspect.signature(self._call).parameters.get("run_manager")
        run_manager = callback_manager.on_chain_start(
            dumpd(self),
            inputs,
            name=run_name,
        )
        try:
            outputs = (
                self._call(inputs, run_manager=run_manager, custom_documents=custom_documents)
                if new_arg_supported
                else self._call(inputs, custom_documents=custom_documents)
            )
        except BaseException as e:
            run_manager.on_chain_error(e)
            raise e
        run_manager.on_chain_end(outputs)
        final_outputs: Dict[str, Any] = self.prep_outputs(
            inputs, outputs, return_only_outputs
        )
        if include_run_info:
            final_outputs[RUN_KEY] = RunInfo(run_id=run_manager.run_id)
        return final_outputs

    async def ainvoke(
        self,
        input: Dict[str, Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        config = ensure_config(config)
        callbacks = config.get("callbacks")
        tags = config.get("tags")
        metadata = config.get("metadata")
        run_name = config.get("run_name")
        include_run_info = kwargs.get("include_run_info", False)
        return_only_outputs = kwargs.get("return_only_outputs", False)

        inputs = self.prep_inputs(input)
        callback_manager = AsyncCallbackManager.configure(
            callbacks,
            self.callbacks,
            self.verbose,
            tags,
            self.tags,
            metadata,
            self.metadata,
        )
        new_arg_supported = inspect.signature(self._acall).parameters.get("run_manager")
        run_manager = await callback_manager.on_chain_start(
            dumpd(self),
            inputs,
            name=run_name,
        )
        try:
            outputs = (
                await self._acall(inputs, run_manager=run_manager)
                if new_arg_supported
                else await self._acall(inputs)
            )
        except BaseException as e:
            await run_manager.on_chain_error(e)
            raise e
        await run_manager.on_chain_end(outputs)
        final_outputs: Dict[str, Any] = self.prep_outputs(
            inputs, outputs, return_only_outputs
        )
        if include_run_info:
            final_outputs[RUN_KEY] = RunInfo(run_id=run_manager.run_id)
        return final_outputs

    @property
    def _chain_type(self) -> str:
        raise NotImplementedError("Saving not supported for this chain type.")

    @root_validator()
    def raise_callback_manager_deprecation(cls, values: Dict) -> Dict:
        """Raise deprecation warning if callback_manager is used."""
        if values.get("callback_manager") is not None:
            if values.get("callbacks") is not None:
                raise ValueError(
                    "Cannot specify both callback_manager and callbacks. "
                    "callback_manager is deprecated, callbacks is the preferred "
                    "parameter to pass in."
                )
            warnings.warn(
                "callback_manager is deprecated. Please use callbacks instead.",
                DeprecationWarning,
            )
            values["callbacks"] = values.pop("callback_manager", None)
        return values

    @validator("verbose", pre=True, always=True)
    def set_verbose(cls, verbose: Optional[bool]) -> bool:
        """Set the chain verbosity.

        Defaults to the global setting if not specified by the user.
        """
        if verbose is None:
            return _get_verbosity()
        else:
            return verbose

    @property
    @abstractmethod
    def input_keys(self) -> List[str]:
        """Keys expected to be in the chain input."""

    @property
    @abstractmethod
    def output_keys(self) -> List[str]:
        """Keys expected to be in the chain output."""

    def _validate_inputs(self, inputs: Dict[str, Any]) -> None:
        """Check that all inputs are present."""
        missing_keys = set(self.input_keys).difference(inputs)
        if missing_keys:
            raise ValueError(f"Missing some input keys: {missing_keys}")

    def _validate_outputs(self, outputs: Dict[str, Any]) -> None:
        missing_keys = set(self.output_keys).difference(outputs)
        if missing_keys:
            raise ValueError(f"Missing some output keys: {missing_keys}")

    @abstractmethod
    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
        custom_documents: Optional[List[Document]] = None
    ) -> Dict[str, Any]:
        """Execute the chain.

        This is a private method that is not user-facing. It is only called within
            `Chain.__call__`, which is the user-facing wrapper method that handles
            callbacks configuration and some input/output processing.

        Args:
            inputs: A dict of named inputs to the chain. Assumed to contain all inputs
                specified in `Chain.input_keys`, including any inputs added by memory.
            run_manager: The callbacks manager that contains the callback handlers for
                this run of the chain.

        Returns:
            A dict of named outputs. Should contain all outputs specified in
                `Chain.output_keys`.
        """

    async def _acall(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        """Asynchronously execute the chain.

        This is a private method that is not user-facing. It is only called within
            `Chain.acall`, which is the user-facing wrapper method that handles
            callbacks configuration and some input/output processing.

        Args:
            inputs: A dict of named inputs to the chain. Assumed to contain all inputs
                specified in `Chain.input_keys`, including any inputs added by memory.
            run_manager: The callbacks manager that contains the callback handlers for
                this run of the chain.

        Returns:
            A dict of named outputs. Should contain all outputs specified in
                `Chain.output_keys`.
        """
        return await run_in_executor(
            None, self._call, inputs, run_manager.get_sync() if run_manager else None
        )

    @deprecated("0.1.0", alternative="invoke", removal="0.2.0")
    def __call__(
        self,
        inputs: Union[Dict[str, Any], Any],
        return_only_outputs: bool = False,
        callbacks: Callbacks = None,
        *,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        run_name: Optional[str] = None,
        include_run_info: bool = False,
    ) -> Dict[str, Any]:
        """Execute the chain.

        Args:
            inputs: Dictionary of inputs, or single input if chain expects
                only one param. Should contain all inputs specified in
                `Chain.input_keys` except for inputs that will be set by the chain's
                memory.
            return_only_outputs: Whether to return only outputs in the
                response. If True, only new keys generated by this chain will be
                returned. If False, both input keys and new keys generated by this
                chain will be returned. Defaults to False.
            callbacks: Callbacks to use for this chain run. These will be called in
                addition to callbacks passed to the chain during construction, but only
                these runtime callbacks will propagate to calls to other objects.
            tags: List of string tags to pass to all callbacks. These will be passed in
                addition to tags passed to the chain during construction, but only
                these runtime tags will propagate to calls to other objects.
            metadata: Optional metadata associated with the chain. Defaults to None
            include_run_info: Whether to include run info in the response. Defaults
                to False.

        Returns:
            A dict of named outputs. Should contain all outputs specified in
                `Chain.output_keys`.
        """
        config = {
            "callbacks": callbacks,
            "tags": tags,
            "metadata": metadata,
            "run_name": run_name,
        }

        return self.invoke(
            inputs,
            cast(RunnableConfig, {k: v for k, v in config.items() if v is not None}),
            return_only_outputs=return_only_outputs,
            include_run_info=include_run_info,
        )

    @deprecated("0.1.0", alternative="ainvoke", removal="0.2.0")
    async def acall(
        self,
        inputs: Union[Dict[str, Any], Any],
        return_only_outputs: bool = False,
        callbacks: Callbacks = None,
        *,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        run_name: Optional[str] = None,
        include_run_info: bool = False,
    ) -> Dict[str, Any]:
        """Asynchronously execute the chain.

        Args:
            inputs: Dictionary of inputs, or single input if chain expects
                only one param. Should contain all inputs specified in
                `Chain.input_keys` except for inputs that will be set by the chain's
                memory.
            return_only_outputs: Whether to return only outputs in the
                response. If True, only new keys generated by this chain will be
                returned. If False, both input keys and new keys generated by this
                chain will be returned. Defaults to False.
            callbacks: Callbacks to use for this chain run. These will be called in
                addition to callbacks passed to the chain during construction, but only
                these runtime callbacks will propagate to calls to other objects.
            tags: List of string tags to pass to all callbacks. These will be passed in
                addition to tags passed to the chain during construction, but only
                these runtime tags will propagate to calls to other objects.
            metadata: Optional metadata associated with the chain. Defaults to None
            include_run_info: Whether to include run info in the response. Defaults
                to False.

        Returns:
            A dict of named outputs. Should contain all outputs specified in
                `Chain.output_keys`.
        """
        config = {
            "callbacks": callbacks,
            "tags": tags,
            "metadata": metadata,
            "run_name": run_name,
        }
        return await self.ainvoke(
            inputs,
            cast(RunnableConfig, {k: v for k, v in config.items() if k is not None}),
            return_only_outputs=return_only_outputs,
            include_run_info=include_run_info,
        )

    def prep_outputs(
        self,
        inputs: Dict[str, str],
        outputs: Dict[str, str],
        return_only_outputs: bool = False,
    ) -> Dict[str, str]:
        """Validate and prepare chain outputs, and save info about this run to memory.

        Args:
            inputs: Dictionary of chain inputs, including any inputs added by chain
                memory.
            outputs: Dictionary of initial chain outputs.
            return_only_outputs: Whether to only return the chain outputs. If False,
                inputs are also added to the final outputs.

        Returns:
            A dict of the final chain outputs.
        """
        self._validate_outputs(outputs)
        if self.memory is not None:
            self.memory.save_context(inputs, outputs)
        if return_only_outputs:
            return outputs
        else:
            return {**inputs, **outputs}

    def prep_inputs(self, inputs: Union[Dict[str, Any], Any]) -> Dict[str, str]:
        """Validate and prepare chain inputs, including adding inputs from memory.

        Args:
            inputs: Dictionary of raw inputs, or single input if chain expects
                only one param. Should contain all inputs specified in
                `Chain.input_keys` except for inputs that will be set by the chain's
                memory.

        Returns:
            A dictionary of all inputs, including those added by the chain's memory.
        """
        if not isinstance(inputs, dict):
            _input_keys = set(self.input_keys)
            if self.memory is not None:
                # If there are multiple input keys, but some get set by memory so that
                # only one is not set, we can still figure out which key it is.
                _input_keys = _input_keys.difference(self.memory.memory_variables)
            if len(_input_keys) != 1:
                raise ValueError(
                    f"A single string input was passed in, but this chain expects "
                    f"multiple inputs ({_input_keys}). When a chain expects "
                    f"multiple inputs, please call it by passing in a dictionary, "
                    "eg `chain({'foo': 1, 'bar': 2})`"
                )
            inputs = {list(_input_keys)[0]: inputs}
        if self.memory is not None:
            external_context = self.memory.load_memory_variables(inputs)
            inputs = dict(inputs, **external_context)
        self._validate_inputs(inputs)
        return inputs

    @property
    def _run_output_key(self) -> str:
        if len(self.output_keys) != 1:
            raise ValueError(
                f"`run` not supported when there is not exactly "
                f"one output key. Got {self.output_keys}."
            )
        return self.output_keys[0]

    @deprecated("0.1.0", alternative="invoke", removal="0.2.0")
    def run(
        self,
        *args: Any,
        callbacks: Callbacks = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Convenience method for executing chain.

        The main difference between this method and `Chain.__call__` is that this
        method expects inputs to be passed directly in as positional arguments or
        keyword arguments, whereas `Chain.__call__` expects a single input dictionary
        with all the inputs

        Args:
            *args: If the chain expects a single input, it can be passed in as the
                sole positional argument.
            callbacks: Callbacks to use for this chain run. These will be called in
                addition to callbacks passed to the chain during construction, but only
                these runtime callbacks will propagate to calls to other objects.
            tags: List of string tags to pass to all callbacks. These will be passed in
                addition to tags passed to the chain during construction, but only
                these runtime tags will propagate to calls to other objects.
            **kwargs: If the chain expects multiple inputs, they can be passed in
                directly as keyword arguments.

        Returns:
            The chain output.

        Example:
            .. code-block:: python

                # Suppose we have a single-input chain that takes a 'question' string:
                chain.run("What's the temperature in Boise, Idaho?")
                # -> "The temperature in Boise is..."

                # Suppose we have a multi-input chain that takes a 'question' string
                # and 'context' string:
                question = "What's the temperature in Boise, Idaho?"
                context = "Weather report for Boise, Idaho on 07/03/23..."
                chain.run(question=question, context=context)
                # -> "The temperature in Boise is..."
        """
        # Run at start to make sure this is possible/defined
        _output_key = self._run_output_key

        if args and not kwargs:
            if len(args) != 1:
                raise ValueError("`run` supports only one positional argument.")
            return self(args[0], callbacks=callbacks, tags=tags, metadata=metadata)[
                _output_key
            ]

        if kwargs and not args:
            return self(kwargs, callbacks=callbacks, tags=tags, metadata=metadata)[
                _output_key
            ]

        if not kwargs and not args:
            raise ValueError(
                "`run` supported with either positional arguments or keyword arguments,"
                " but none were provided."
            )
        else:
            raise ValueError(
                f"`run` supported with either positional arguments or keyword arguments"
                f" but not both. Got args: {args} and kwargs: {kwargs}."
            )

    @deprecated("0.1.0", alternative="ainvoke", removal="0.2.0")
    async def arun(
        self,
        *args: Any,
        callbacks: Callbacks = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Convenience method for executing chain.

        The main difference between this method and `Chain.__call__` is that this
        method expects inputs to be passed directly in as positional arguments or
        keyword arguments, whereas `Chain.__call__` expects a single input dictionary
        with all the inputs


        Args:
            *args: If the chain expects a single input, it can be passed in as the
                sole positional argument.
            callbacks: Callbacks to use for this chain run. These will be called in
                addition to callbacks passed to the chain during construction, but only
                these runtime callbacks will propagate to calls to other objects.
            tags: List of string tags to pass to all callbacks. These will be passed in
                addition to tags passed to the chain during construction, but only
                these runtime tags will propagate to calls to other objects.
            **kwargs: If the chain expects multiple inputs, they can be passed in
                directly as keyword arguments.

        Returns:
            The chain output.

        Example:
            .. code-block:: python

                # Suppose we have a single-input chain that takes a 'question' string:
                await chain.arun("What's the temperature in Boise, Idaho?")
                # -> "The temperature in Boise is..."

                # Suppose we have a multi-input chain that takes a 'question' string
                # and 'context' string:
                question = "What's the temperature in Boise, Idaho?"
                context = "Weather report for Boise, Idaho on 07/03/23..."
                await chain.arun(question=question, context=context)
                # -> "The temperature in Boise is..."
        """
        if len(self.output_keys) != 1:
            raise ValueError(
                f"`run` not supported when there is not exactly "
                f"one output key. Got {self.output_keys}."
            )
        elif args and not kwargs:
            if len(args) != 1:
                raise ValueError("`run` supports only one positional argument.")
            return (
                await self.acall(
                    args[0], callbacks=callbacks, tags=tags, metadata=metadata
                )
            )[self.output_keys[0]]

        if kwargs and not args:
            return (
                await self.acall(
                    kwargs, callbacks=callbacks, tags=tags, metadata=metadata
                )
            )[self.output_keys[0]]

        raise ValueError(
            f"`run` supported with either positional arguments or keyword arguments"
            f" but not both. Got args: {args} and kwargs: {kwargs}."
        )

    def dict(self, **kwargs: Any) -> Dict:
        """Dictionary representation of chain.

        Expects `Chain._chain_type` property to be implemented and for memory to be
            null.

        Args:
            **kwargs: Keyword arguments passed to default `pydantic.BaseModel.dict`
                method.

        Returns:
            A dictionary representation of the chain.

        Example:
            .. code-block:: python

                chain.dict(exclude_unset=True)
                # -> {"_type": "foo", "verbose": False, ...}
        """
        _dict = super().dict(**kwargs)
        try:
            _dict["_type"] = self._chain_type
        except NotImplementedError:
            pass
        return _dict

    def save(self, file_path: Union[Path, str]) -> None:
        """Save the chain.

        Expects `Chain._chain_type` property to be implemented and for memory to be
            null.

        Args:
            file_path: Path to file to save the chain to.

        Example:
            .. code-block:: python

                chain.save(file_path="path/chain.yaml")
        """
        if self.memory is not None:
            raise ValueError("Saving of memory is not yet supported.")

        # Fetch dictionary to save
        chain_dict = self.dict()
        if "_type" not in chain_dict:
            raise NotImplementedError(f"Chain {self} does not support saving.")

        # Convert file to Path object.
        if isinstance(file_path, str):
            save_path = Path(file_path)
        else:
            save_path = file_path

        directory_path = save_path.parent
        directory_path.mkdir(parents=True, exist_ok=True)

        if save_path.suffix == ".json":
            with open(file_path, "w") as f:
                json.dump(chain_dict, f, indent=4)
        elif save_path.suffix == ".yaml":
            with open(file_path, "w") as f:
                yaml.dump(chain_dict, f, default_flow_style=False)
        else:
            raise ValueError(f"{save_path} must be json or yaml")

    @deprecated("0.1.0", alternative="batch", removal="0.2.0")
    def apply(
        self, input_list: List[Dict[str, Any]], callbacks: Callbacks = None
    ) -> List[Dict[str, str]]:
        """Call the chain on all inputs in the list."""
        return [self(inputs, callbacks=callbacks) for inputs in input_list]


"""Chain for chatting with a vector database."""
# Depending on the memory type and configuration, the chat history format may differ.
# This needs to be consolidated.
CHAT_TURN_TYPE = Union[Tuple[str, str], BaseMessage]


_ROLE_MAP = {"human": "Human: ", "ai": "Assistant: "}


def _get_chat_history(chat_history: List[CHAT_TURN_TYPE]) -> str:
    buffer = ""
    for dialogue_turn in chat_history:
        if isinstance(dialogue_turn, BaseMessage):
            role_prefix = _ROLE_MAP.get(dialogue_turn.type, f"{dialogue_turn.type}: ")
            buffer += f"\n{role_prefix}{dialogue_turn.content}"
        elif isinstance(dialogue_turn, tuple):
            human = "Human: " + dialogue_turn[0]
            ai = "Assistant: " + dialogue_turn[1]
            buffer += "\n" + "\n".join([human, ai])
        else:
            raise ValueError(
                f"Unsupported chat history format: {type(dialogue_turn)}."
                f" Full chat history: {chat_history} "
            )
    return buffer


class InputType(BaseModel):
    """Input type for ConversationalRetrievalChain."""

    question: str
    """The question to answer."""
    chat_history: List[CHAT_TURN_TYPE] = Field(default_factory=list)
    """The chat history to use for retrieval."""


class BaseConversationalRetrievalChain(Chain):
    """Chain for chatting with an index."""

    combine_docs_chain: BaseCombineDocumentsChain
    """The chain used to combine any retrieved documents."""
    question_generator: LLMChain
    """The chain used to generate a new question for the sake of retrieval.
    This chain will take in the current question (with variable `question`)
    and any chat history (with variable `chat_history`) and will produce
    a new standalone question to be used later on."""
    output_key: str = "answer"
    """The output key to return the final answer of this chain in."""
    rephrase_question: bool = True
    """Whether or not to pass the new generated question to the combine_docs_chain.
    If True, will pass the new generated question along.
    If False, will only use the new generated question for retrieval and pass the
    original question along to the combine_docs_chain."""
    return_source_documents: bool = False
    """Return the retrieved source documents as part of the final result."""
    return_generated_question: bool = False
    """Return the generated question as part of the final result."""
    get_chat_history: Optional[Callable[[List[CHAT_TURN_TYPE]], str]] = None
    """An optional function to get a string of the chat history.
    If None is provided, will use a default."""
    response_if_no_docs_found: Optional[str]
    """If specified, the chain will return a fixed response if no docs 
    are found for the question. """

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    @property
    def input_keys(self) -> List[str]:
        """Input keys."""
        return ["question", "chat_history"]

    def get_input_schema(
        self, config: Optional[RunnableConfig] = None
    ) -> Type[BaseModel]:
        return InputType

    @property
    def output_keys(self) -> List[str]:
        """Return the output keys.

        :meta private:
        """
        _output_keys = [self.output_key]
        if self.return_source_documents:
            _output_keys = _output_keys + ["source_documents"]
        if self.return_generated_question:
            _output_keys = _output_keys + ["generated_question"]
        return _output_keys

    @abstractmethod
    def _get_docs(
        self,
        question: str,
        inputs: Dict[str, Any],
        *,
        run_manager: CallbackManagerForChainRun,
    ) -> List[Document]:
        """Get docs."""

    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
        custom_documents: Optional[List[Document]] = None
    ) -> Dict[str, Any]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        question = inputs["question"]
        get_chat_history = self.get_chat_history or _get_chat_history
        chat_history_str = get_chat_history(inputs["chat_history"])

        if chat_history_str:
            callbacks = _run_manager.get_child()
            new_question = self.question_generator.run(
                question=question, chat_history=chat_history_str, callbacks=callbacks
            )
        else:
            new_question = question
        accepts_run_manager = (
            "run_manager" in inspect.signature(self._get_docs).parameters
        )
        if custom_documents is not None:
            docs = custom_documents
        elif accepts_run_manager:
            docs = self._get_docs(new_question, inputs, run_manager=_run_manager)
        else:
            docs = self._get_docs(new_question, inputs)  # type: ignore[call-arg]
        output: Dict[str, Any] = {}
        if self.response_if_no_docs_found is not None and len(docs) == 0:
            output[self.output_key] = self.response_if_no_docs_found
        else:
            new_inputs = inputs.copy()
            if self.rephrase_question:
                new_inputs["question"] = new_question
            new_inputs["chat_history"] = chat_history_str
            answer = self.combine_docs_chain.run(
                input_documents=docs, callbacks=_run_manager.get_child(), **new_inputs
            )
            output[self.output_key] = answer

        if self.return_source_documents:
            output["source_documents"] = docs
        if self.return_generated_question:
            output["generated_question"] = new_question
        return output

    @abstractmethod
    async def _aget_docs(
        self,
        question: str,
        inputs: Dict[str, Any],
        *,
        run_manager: AsyncCallbackManagerForChainRun,
    ) -> List[Document]:
        """Get docs."""

    async def _acall(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        _run_manager = run_manager or AsyncCallbackManagerForChainRun.get_noop_manager()
        question = inputs["question"]
        get_chat_history = self.get_chat_history or _get_chat_history
        chat_history_str = get_chat_history(inputs["chat_history"])
        if chat_history_str:
            callbacks = _run_manager.get_child()
            new_question = await self.question_generator.arun(
                question=question, chat_history=chat_history_str, callbacks=callbacks
            )
        else:
            new_question = question
        accepts_run_manager = (
            "run_manager" in inspect.signature(self._aget_docs).parameters
        )
        if accepts_run_manager:
            docs = await self._aget_docs(new_question, inputs, run_manager=_run_manager)
        else:
            docs = await self._aget_docs(new_question, inputs)  # type: ignore[call-arg]

        output: Dict[str, Any] = {}
        if self.response_if_no_docs_found is not None and len(docs) == 0:
            output[self.output_key] = self.response_if_no_docs_found
        else:
            new_inputs = inputs.copy()
            if self.rephrase_question:
                new_inputs["question"] = new_question
            new_inputs["chat_history"] = chat_history_str
            answer = await self.combine_docs_chain.arun(
                input_documents=docs, callbacks=_run_manager.get_child(), **new_inputs
            )
            output[self.output_key] = answer

        if self.return_source_documents:
            output["source_documents"] = docs
        if self.return_generated_question:
            output["generated_question"] = new_question
        return output

    def save(self, file_path: Union[Path, str]) -> None:
        if self.get_chat_history:
            raise ValueError("Chain not saveable when `get_chat_history` is not None.")
        super().save(file_path)


class CustomConversationalRetrievalChain(BaseConversationalRetrievalChain):
    """Chain for having a conversation based on retrieved documents.

    This chain takes in chat history (a list of messages) and new questions,
    and then returns an answer to that question.
    The algorithm for this chain consists of three parts:

    1. Use the chat history and the new question to create a "standalone question".
    This is done so that this question can be passed into the retrieval step to fetch
    relevant documents. If only the new question was passed in, then relevant context
    may be lacking. If the whole conversation was passed into retrieval, there may
    be unnecessary information there that would distract from retrieval.

    2. This new question is passed to the retriever and relevant documents are
    returned.

    3. The retrieved documents are passed to an LLM along with either the new question
    (default behavior) or the original question and chat history to generate a final
    response.

    Example:
        .. code-block:: python

            from langchain.chains import (
                StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
            )
            from langchain_core.prompts import PromptTemplate
            from langchain_community.llms import OpenAI

            combine_docs_chain = StuffDocumentsChain(...)
            vectorstore = ...
            retriever = vectorstore.as_retriever()

            # This controls how the standalone question is generated.
            # Should take `chat_history` and `question` as input variables.
            template = (
                "Combine the chat history and follow up question into "
                "a standalone question. Chat History: {chat_history}"
                "Follow up question: {question}"
            )
            prompt = PromptTemplate.from_template(template)
            llm = OpenAI()
            question_generator_chain = LLMChain(llm=llm, prompt=prompt)
            chain = ConversationalRetrievalChain(
                combine_docs_chain=combine_docs_chain,
                retriever=retriever,
                question_generator=question_generator_chain,
            )
    """

    retriever: BaseRetriever
    """Retriever to use to fetch documents."""
    max_tokens_limit: Optional[int] = None
    """If set, enforces that the documents returned are less than this limit.
    This is only enforced if `combine_docs_chain` is of type StuffDocumentsChain."""

    def _reduce_tokens_below_limit(self, docs: List[Document]) -> List[Document]:
        num_docs = len(docs)

        if self.max_tokens_limit and isinstance(
            self.combine_docs_chain, StuffDocumentsChain
        ):
            tokens = [
                self.combine_docs_chain.llm_chain._get_num_tokens(doc.page_content)
                for doc in docs
            ]
            token_count = sum(tokens[:num_docs])
            while token_count > self.max_tokens_limit:
                num_docs -= 1
                token_count -= tokens[num_docs]

        return docs[:num_docs]

    def _get_docs(
        self,
        question: str,
        inputs: Dict[str, Any],
        *,
        run_manager: CallbackManagerForChainRun,
    ) -> List[Document]:
        """Get docs."""
        docs = self.retriever.get_relevant_documents(
            question, callbacks=run_manager.get_child()
        )
        return self._reduce_tokens_below_limit(docs)

    async def _aget_docs(
        self,
        question: str,
        inputs: Dict[str, Any],
        *,
        run_manager: AsyncCallbackManagerForChainRun,
    ) -> List[Document]:
        """Get docs."""
        docs = await self.retriever.aget_relevant_documents(
            question, callbacks=run_manager.get_child()
        )
        return self._reduce_tokens_below_limit(docs)

    @classmethod
    def from_llm(
        cls,
        llm: BaseLanguageModel,
        retriever: BaseRetriever,
        condense_question_prompt: BasePromptTemplate = CONDENSE_QUESTION_PROMPT,
        chain_type: str = "stuff",
        verbose: bool = False,
        condense_question_llm: Optional[BaseLanguageModel] = None,
        combine_docs_chain_kwargs: Optional[Dict] = None,
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> BaseConversationalRetrievalChain:
        """Convenience method to load chain from LLM and retriever.

        This provides some logic to create the `question_generator` chain
        as well as the combine_docs_chain.

        Args:
            llm: The default language model to use at every part of this chain
                (eg in both the question generation and the answering)
            retriever: The retriever to use to fetch relevant documents from.
            condense_question_prompt: The prompt to use to condense the chat history
                and new question into a standalone question.
            chain_type: The chain type to use to create the combine_docs_chain, will
                be sent to `load_qa_chain`.
            verbose: Verbosity flag for logging to stdout.
            condense_question_llm: The language model to use for condensing the chat
                history and new question into a standalone question. If none is
                provided, will default to `llm`.
            combine_docs_chain_kwargs: Parameters to pass as kwargs to `load_qa_chain`
                when constructing the combine_docs_chain.
            callbacks: Callbacks to pass to all subchains.
            **kwargs: Additional parameters to pass when initializing
                ConversationalRetrievalChain
        """
        combine_docs_chain_kwargs = combine_docs_chain_kwargs or {}
        doc_chain = load_qa_chain(
            llm,
            chain_type=chain_type,
            verbose=verbose,
            callbacks=callbacks,
            **combine_docs_chain_kwargs,
        )

        _llm = condense_question_llm or llm
        condense_question_chain = LLMChain(
            llm=_llm,
            prompt=condense_question_prompt,
            verbose=verbose,
            callbacks=callbacks,
        )
        return cls(
            retriever=retriever,
            combine_docs_chain=doc_chain,
            question_generator=condense_question_chain,
            callbacks=callbacks,
            **kwargs,
        )


class ChatVectorDBChain(BaseConversationalRetrievalChain):
    """Chain for chatting with a vector database."""

    vectorstore: VectorStore = Field(alias="vectorstore")
    top_k_docs_for_context: int = 4
    search_kwargs: dict = Field(default_factory=dict)

    @property
    def _chain_type(self) -> str:
        return "chat-vector-db"

    @root_validator()
    def raise_deprecation(cls, values: Dict) -> Dict:
        warnings.warn(
            "`ChatVectorDBChain` is deprecated - "
            "please use `from langchain.chains import ConversationalRetrievalChain`"
        )
        return values

    def _get_docs(
        self,
        question: str,
        inputs: Dict[str, Any],
        *,
        run_manager: CallbackManagerForChainRun,
    ) -> List[Document]:
        """Get docs."""
        vectordbkwargs = inputs.get("vectordbkwargs", {})
        full_kwargs = {**self.search_kwargs, **vectordbkwargs}
        return self.vectorstore.similarity_search(
            question, k=self.top_k_docs_for_context, **full_kwargs
        )

    async def _aget_docs(
        self,
        question: str,
        inputs: Dict[str, Any],
        *,
        run_manager: AsyncCallbackManagerForChainRun,
    ) -> List[Document]:
        """Get docs."""
        raise NotImplementedError("ChatVectorDBChain does not support async")

    @classmethod
    def from_llm(
        cls,
        llm: BaseLanguageModel,
        vectorstore: VectorStore,
        condense_question_prompt: BasePromptTemplate = CONDENSE_QUESTION_PROMPT,
        chain_type: str = "stuff",
        combine_docs_chain_kwargs: Optional[Dict] = None,
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> BaseConversationalRetrievalChain:
        """Load chain from LLM."""
        combine_docs_chain_kwargs = combine_docs_chain_kwargs or {}
        doc_chain = load_qa_chain(
            llm,
            chain_type=chain_type,
            callbacks=callbacks,
            **combine_docs_chain_kwargs,
        )
        condense_question_chain = LLMChain(
            llm=llm, prompt=condense_question_prompt, callbacks=callbacks
        )
        return cls(
            vectorstore=vectorstore,
            combine_docs_chain=doc_chain,
            question_generator=condense_question_chain,
            callbacks=callbacks,
            **kwargs,
        )
