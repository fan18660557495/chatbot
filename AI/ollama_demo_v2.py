
# 从 pydantic 模块导入 BaseModel 和 Field 类，用于定义数据模型和字段
from pydantic import BaseModel, Field
# 从 langchain.tools 模块导入 Tool 类，用于定义和创建工具
from langchain.tools import Tool
# 从 langchain_ollama 模块导入 OllamaLLM 类，用于与 Ollama 大语言模型进行交互
from langchain_ollama import OllamaLLM
# 从 langchain.schema 模块导入 HumanMessage 类，用于表示用户输入的消息
from langchain.schema import HumanMessage
# 导入 Agent 相关的类
from langchain.agents import initialize_agent, AgentType

# 导入 Python 的 warnings 模块，该模块用于控制警告消息的显示
import warnings
# 过滤掉 LangChainDeprecationWarning 警告
warnings.filterwarnings("ignore", category=DeprecationWarning)

# 定义一个名为 GetWeather 的类，继承自 BaseModel，用于获取指定城市的天气信息
class GetWeather(BaseModel):
    '''用于获取指定城市的天气信息'''

    # 定义一个字符串类型的字段 location，用于表示城市或地区名称
    # ... 表示该字段是必需的
    # description 为该字段提供描述信息，方便理解和使用
    location: str = Field(..., description="城市或地区名称, 如 北京、上海、深圳、朝阳区")

# 定义一个名为 GetPopulation 的类，继承自 BaseModel，用于获取指定城市的人口信息
class GetPopulation(BaseModel):
    '''用于获取指定城市的人口信息'''

    # 定义一个字符串类型的字段 location，用于表示城市或地区名称
    # ... 表示该字段是必需的
    # description 为该字段提供描述信息，方便理解和使用
    location: str = Field(..., description="城市或地区名称, 如 北京、上海、深圳、朝阳区")

# 定义一个名为 GetIncome 的类，继承自 BaseModel，用于获取指定企业的年收入
class GetIncome(BaseModel):
    '''获取指定企业的年收入'''

    # 定义一个字符串类型的字段 company，用于表示企业名称
    # ... 表示该字段是必需的
    # description 为该字段提供描述信息，方便理解和使用
    company: str = Field(..., description="企业名称, 如 华为、腾讯、阿里巴巴、幸福无限有限公司")

# 定义工具函数，用于获取指定城市的天气信息
def get_weather(location: str) -> str:
    # 这里只是简单模拟返回天气信息，实际应用中可替换为真实的天气查询逻辑
    print("get_weather 方法被调用")
    print("参数location:", location)
    if location == "北京":
        return f"{location} 的天气是多云."
    elif location == "上海":
        return f"{location} 的天气是阴."
    else:
        # 默认返回晴天
        return f"{location} 的天气是晴天."

# 定义工具函数，用于获取指定城市的人口信息
def get_population(location: str) -> str:
    # 这里只是简单模拟返回人口信息，实际应用中可替换为真实的人口查询逻辑
    print("get_population 方法被调用")
    print("参数location:", location)
    if location == "北京":
        return f"{location} 的人口为 20000000."
    elif location == "上海":
        return f"{location} 的人口为 15000000."
    else:
        return f"{location} 的人口为 1000000."

# 定义工具函数，用于获取指定企业的年收入
def get_income(company: str) -> str:
    # 这里只是简单模拟返回年收入，实际应用中可替换为真实的年收入查询逻辑
    print("get_income 方法被调用")
    print("参数company:", company)
    if company == "幸福无限有限公司":
        return f"{company} 的年收入是 20000亿人民币."
    else:
        return f"{company} 的年收入是 20万人民币."

# 创建工具实例
# 创建一个名为 "GetWeather" 的工具实例，用于获取指定城市或地区的天气信息
weather_tool = Tool(
    # 工具的名称，用于在 Agent 中标识该工具，这个名称在智能体的决策过程中会被使用，
    # 智能体根据用户的输入和工具的描述来决定是否调用某个工具。在日志和调试信息中，也会使用这个名称来标识工具
    name="GetWeather",
    # 该工具实际调用的函数，这里是之前定义的 get_weather 函数
    # 当智能体决定调用某个工具时，会调用这个函数，并传入相应的参数。
    # 在此代码中， func=get_weather 表示当智能体需要获取天气信息时，会调用 get_weather 函数
    func=get_weather,
    # 工具的描述信息，帮助 Agent 理解该工具的用途
    # 这个描述帮助智能体理解工具的用途和适用场景。智能体根据用户的输入和工具的描述来判断是否需要调用某个工具。
    # 例如，在此代码中，描述信息为 "使用本工具获取指定城市或地区的天气信息." ，智能体可以根据这个描述来判断是否需要调用 GetWeather 工具
    description="使用本工具获取指定城市或地区的天气信息.",
    # 一个 pydantic 模型，用于定义工具的参数，这里使用了之前定义的 GetWeather 类
    # 这个模型定义了工具函数所需的参数及其类型和描述。智能体在调用工具时，会根据这个模型来验证和解析传入的参数。
    # 在此代码中， args_schema=GetWeather 表示 get_weather 函数需要一个 location 参数，该参数是一个字符串，代表城市或地区名称
    args_schema=GetWeather
)

# 创建一个名为 "GetPopulation" 的工具实例，用于获取指定城市或地区的人口信息
population_tool = Tool(
    # 工具的名称，用于在 Agent 中标识该工具，这个名称在智能体的决策过程中会被使用，
    # 智能体根据用户的输入和工具的描述来决定是否调用某个工具。在日志和调试信息中，也会使用这个名称来标识工具
    name="GetPopulation",
    # 该工具实际调用的函数，这里是之前定义的 get_population 函数
    # 当智能体决定调用某个工具时，会调用这个函数，并传入相应的参数。
    # 在此代码中， func=get_population 表示当智能体需要获取人口信息时，会调用 get_population 函数
    func=get_population,
    # 工具的描述信息，帮助 Agent 理解该工具的用途
    # 这个描述帮助智能体理解工具的用途和适用场景。智能体根据用户的输入和工具的描述来判断是否需要调用某个工具。
    # 例如，在此代码中，描述信息为 "使用本工具获取指定城市或地区的人口信息." ，智能体可以根据这个描述来判断是否需要调用 GetPopulation 工具
    description="使用本工具获取指定城市或地区的人口信息.",
    # 一个 pydantic 模型，用于定义工具的参数，这里使用了之前定义的 GetPopulation 类
    # 这个模型定义了工具函数所需的参数及其类型和描述。智能体在调用工具时，会根据这个模型来验证和解析传入的参数。
    # 在此代码中， args_schema=GetPopulation 表示 get_population 函数需要一个 location 参数，该参数是一个字符串，代表城市或地区名称
    args_schema=GetPopulation
)

# 创建一个名为 "GetIncome" 的工具实例，用于获取指定企业的年收入信息
income_tool = Tool(
    # 工具的名称，用于在 Agent 中标识该工具，这个名称在智能体的决策过程中会被使用，
    # 智能体根据用户的输入和工具的描述来决定是否调用某个工具。在日志和调试信息中，也会使用这个名称来标识工具
    name="GetIncome",
    # 该工具实际调用的函数，这里是之前定义的 get_income 函数
    # 当智能体决定调用某个工具时，会调用这个函数，并传入相应的参数。
    # 在此代码中， func=get_income 表示当智能体需要获取企业年收入信息时，会调用 get_income 函数
    func=get_income,
    # 工具的描述信息，帮助 Agent 理解该工具的用途
    # 这个描述帮助智能体理解工具的用途和适用场景。智能体根据用户的输入和工具的描述来判断是否需要调用某个工具。
    # 例如，在此代码中，描述信息为 "使用本工具获取指定企业的年收入." ，智能体可以根据这个描述来判断是否需要调用 GetIncome 工具
    description="使用本工具获取指定企业的年收入.",
    # 一个 pydantic 模型，用于定义工具的参数，这里使用了之前定义的 GetIncome 类
    # 这个模型定义了工具函数所需的参数及其类型和描述。智能体在调用工具时，会根据这个模型来验证和解析传入的参数。
    # 在此代码中， args_schema=GetIncome 表示 get_income 函数需要一个 company 参数，该参数是一个字符串，代表企业名称
    args_schema=GetIncome
)

# 定义一个工具列表，包含用于获取天气、人口和企业年收入的工具
tools = [
    # 天气工具，用于获取指定城市或地区的天气信息
    weather_tool,
    # 人口工具，用于获取指定城市或地区的人口信息
    population_tool,
    # 收入工具，用于获取指定企业的年收入信息
    income_tool
]



# 初始化 Ollama 大语言模型实例
llm = OllamaLLM(
    # 指定 Ollama 模型名称为 qwen2.5，可根据需求替换为其他模型，如 deepseek-r1:32b
    model="qwen2.5",
    # 指定 Ollama 服务器的地址，用于与模型进行通信
    base_url="http://www.esunrising.net:11434"
)


# 初始化一个智能体（Agent），用于根据用户输入和可用工具与大语言模型交互
agent = initialize_agent(
    # 传入工具列表，包含用于获取天气、人口和企业年收入的工具
    tools = tools,
    # 传入大语言模型实例，这里使用的是 Ollama 大语言模型
    llm = llm,
    # 指定智能体的类型为结构化聊天零样本反应描述类型
    # 这种类型的智能体可以根据工具的描述和用户输入，零样本地决定调用哪个工具来解决问题
    # 常见的智能体类型及使用场景如下：
    # - AgentType.ZERO_SHOT_REACT_DESCRIPTION: 适用于仅根据工具描述和用户输入，零样本地决定调用哪个工具解决问题，不依赖历史对话。
    # - AgentType.REACT_DOCSTORE: 适用于与文档存储交互的场景，例如在文档中查找信息。
    # - AgentType.SELF_ASK_WITH_SEARCH: 适用于需要逐步询问并搜索信息的场景，常用于信息检索。
    # - AgentType.CONVERSATIONAL_REACT_DESCRIPTION: 适用于对话场景，能结合历史对话上下文和工具描述来决定调用工具。
    agent = AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    # 设置为 True 以查看详细的执行过程，方便调试和监控智能体的决策过程
    verbose = True,
    # 可选参数，用于设置智能体的内存，如 ConversationBufferMemory 用于存储对话历史
    # 例如：memory=ConversationBufferMemory()
    # 当智能体类型为 CONVERSATIONAL_REACT_DESCRIPTION 时，此参数通常需要设置
    # memory=None,

    # 可选参数，用于设置智能体的前缀，可自定义智能体的提示信息
    # 例如：agent_kwargs={"prefix": "这是自定义的提示信息"}
    # agent_kwargs=None,

    # 可选参数，用于设置智能体的最大迭代次数，避免无限循环
    # 例如：max_iterations=5
    # max_iterations=None,

    # 可选参数，用于设置智能体在达到最大迭代次数时是否发出错误
    # 例如：handle_parsing_errors=True
    # handle_parsing_errors=None
)


# 定义一个 HumanMessage 对象，用于表示用户输入的消息
# content 参数为消息的具体内容，这里询问了幸福无限有限公司的年收入
# 常用参数：
# - content: 必选参数，用于设置消息的具体内容，类型为字符串
# - additional_kwargs: 可选参数，用于传递额外的关键字参数，可用于扩展消息的属性
#   例如可用于传递消息的元数据，如消息来源、优先级等，类型为字典
message = HumanMessage(content="3、幸福无限有限公司的年收入是多少？") # 1、北京的天气怎样？ 2、北京的人口有多少？ 3、幸福无限有限公司的年收入是多少？

# 使用 agent.run 方法处理用户输入，该方法返回一个字符串
# 注意：run 方法已被弃用，不建议使用
# 常用参数及其用法如下：
# - input: 必选参数，用于传递用户输入的消息内容，类型为字符串
# - return_only_outputs: 可选参数，布尔类型，默认为 False。如果设置为 True，只返回工具执行的输出结果，而不包含其他额外信息
# - tags: 可选参数，列表类型，用于为此次调用添加标签，方便后续的日志记录或跟踪
# - metadata: 可选参数，字典类型，用于传递额外的元数据，例如请求的来源、优先级等
# response = agent.run(message.content) # respoen即为返回值；注意：run 方法已被弃用

# 使用 agent.invoke 方法处理用户输入，该方法返回一个字典
# 常用参数及其用法如下：
# - input: 必选参数，用于传递用户输入的消息内容，类型为字符串
# - return_only_outputs: 可选参数，布尔类型，默认为 False。如果设置为 True，只返回工具执行的输出结果，而不包含其他额外信息
# - tags: 可选参数，列表类型，用于为此次调用添加标签，方便后续的日志记录或跟踪
# - metadata: 可选参数，字典类型，用于传递额外的元数据，例如请求的来源、优先级等
response = agent.invoke({
    "input": message.content
}) # invoke 方法返回值为字典， response.get('output')

# 打印模型的响应
print("用户问题:", message.content)
print("模型回复:", response.get('output'))
