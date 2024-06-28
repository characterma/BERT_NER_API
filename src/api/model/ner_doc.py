from src.base.schema import CustomField, Schema

# Define query related Schema
InputSchema = Schema("InputMessages")
InputSchema.append(
    CustomField(name="docid", type=str, required=True),
    CustomField(name="content", type=str, required=True),
    CustomField(name="add_keywords", type=bool, required=False)
    )
InputSchema.docid.set_description("docid")
InputSchema.content.set_description("Text Content for Prediction")
InputSchema.content.set_description("whether or not to add keywords into input")

ResultSchema = Schema("ReturnResult").append(
    CustomField(name="docid", type=str),
    CustomField(name="text", type=list)
)
ResultSchema.docid.set_description("docid")
ResultSchema.text.set_description("list of details for each entity")


doc_example_1 = InputSchema.new_example(
    docid="202401081522",  # Field example
    content="星巴克的抹茶星冰乐好好喝啊，但是芝士拿铁好苦。",  # Field example
    add_keywords=False
)

doc_example_2 = InputSchema.new_example(
    docid="202401081524", 
    content="星爸爸推出了一款新品维也纳醇香鲜奶咖啡，快去试试吧！", 
    add_keywords=False
)

examples = {"sample 1": doc_example_1, "sample 2": doc_example_2}
