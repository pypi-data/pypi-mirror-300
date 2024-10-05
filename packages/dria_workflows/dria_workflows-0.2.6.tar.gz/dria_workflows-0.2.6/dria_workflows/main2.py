import logging

from dria_workflows import WorkflowBuilder, Operator, Write, Edge, Peek, Workflow


prompt = """
You are an AI assistant tasked with answering questions based on provided context while adopting a specific persona. Your goal is to generate an informative and engaging response that accurately addresses the question while maintaining the characteristics of the given persona.\n\nFirst, you will be presented with some context. Read it carefully as it contains the information needed to answer the question:\n\n\n{{context}}\n\n\nNext, here is the question you need to answer:\n\n\n{{question}}\n\n\nYou will adopt the following persona when crafting your response:\n\n\n{{persona}}\n\n\nWhen formulating your response, follow these guidelines:\n1. Thoroughly analyze the context to extract relevant information for answering the question.\n2. Generate rationales before answering question based on given context\n3. Context may not be sufficient to answer the question, if that's the case add this info to your rationale.\n4. Answer the question based on rationales and context.\n5. Adopt the speaking style, tone, and mannerisms described in the persona.\n6. Maintain the persona's perspective and attitude throughout your response.\n\nGenerate your rationales in tags.\n\nWrite your entire response inside tags. Do not include any explanations or meta-commentary outside of these tags. If context is insufficient, don't answer the question by answering empty string within tags. Reasoning: Think step-by-step.
"""

def generate_answer(
        input_data: dict,
        max_time: int = 300,
        max_steps: int = 30,
        max_tokens: int = 750
) -> Workflow:
    """Generate an answer to a question based on provided context while adopting a specific persona.

    Args:
        input_data (dict): The input data for the workflow.
        max_time (int, optional): The maximum time to run the workflow. Defaults to 300.
        max_steps (int, optional): The maximum number of steps to run the workflow. Defaults to 30.
        max_tokens (int, optional): The maximum number of tokens to run the workflow. Defaults to 750.

    Returns:
        dict: The output data from the workflow.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    builder = WorkflowBuilder(persona="")
    builder.set_max_time(max_time)
    builder.set_max_steps(max_steps)
    builder.set_max_tokens(max_tokens)

    # Step A: Answer Generation
    builder.generative_step(
        id="answer_generation",
        prompt=prompt,
        operator=Operator.GENERATION,
        outputs=[Write.new("answer")]
    )

    # Define the flow of the workflow
    flow = [
        Edge(source="answer_generation", target="_end")
    ]
    builder.flow(flow)

    # Set the return value of the workflow
    builder.set_return_value("answer")
    print(builder.get_required_inputs())
    # Build the workflow
    #workflow = builder.build()

    #return workflow

generate_answer(input_data={})